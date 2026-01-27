# File: frontend/utils/runner.py
"""
Runner utility to execute C++ binaries and capture output.
Enhanced with parsing for new OS visualizer output format.
"""

import subprocess
import os
import sys
import re
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path


def get_build_path() -> Path:
    """Get the path to the build directory."""
    current_dir = Path(__file__).parent.parent.parent
    return current_dir / "build"


def get_source_path(category: str, name: str) -> Path:
    """Get the path to a C++ source file."""
    current_dir = Path(__file__).parent.parent.parent
    backend = current_dir / "backend" / category / name
    return backend.with_suffix(".cpp") if backend.suffix != ".cpp" else backend


def compile_if_needed(name: str, source_path: Path) -> bool:
    """Compile C++ source if executable doesn't exist."""
    exe_path = get_executable_path(name)
    
    # Skip if already compiled
    if exe_path.exists():
        return True
    
    # Create build directory if needed
    build_path = get_build_path()
    build_path.mkdir(parents=True, exist_ok=True)
    
    # Compile the source
    try:
        compile_cmd = ["g++", "-std=gnu++17", "-o", str(exe_path), str(source_path)]
        result = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except Exception:
        return False


def get_executable_path(name: str) -> Path:
    """Get the full path to an executable."""
    build_path = get_build_path()
    if sys.platform == "win32":
        return build_path / f"{name}.exe"
    return build_path / name


def run_executable(
    executable_name: str,
    input_data: str,
    timeout: int = 30,
    source_path: Optional[Path] = None
) -> Tuple[bool, str, str]:
    """
    Run a C++ executable with the given input.
    
    Args:
        executable_name: Name of the executable (without extension)
        input_data: Input string to pass to stdin
        timeout: Maximum execution time in seconds
        source_path: Path to source file (for auto-compilation)
    
    Returns:
        Tuple of (success, stdout, stderr)
    """
    exe_path = get_executable_path(executable_name)
    
    # Auto-compile if needed
    if not exe_path.exists() and source_path:
        if not compile_if_needed(executable_name, source_path):
            return False, "", f"Failed to compile: {source_path}"
    
    if not exe_path.exists():
        return False, "", f"Executable not found: {exe_path}"
    
    try:
        process = subprocess.Popen(
            [str(exe_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(get_build_path())
        )
        
        stdout, stderr = process.communicate(input=input_data, timeout=timeout)
        success = process.returncode == 0
        
        return success, stdout, stderr
        
    except subprocess.TimeoutExpired:
        process.kill()
        return False, "", "Execution timed out"
    except FileNotFoundError:
        return False, "", f"Executable not found: {exe_path}"
    except Exception as e:
        return False, "", f"Error running executable: {str(e)}"


# ============== OS OUTPUT PARSERS ==============

def parse_cpu_output(output: str) -> Dict[str, Any]:
    """Parse CPU scheduling output into structured format."""
    result = {
        "algorithm": "",
        "steps": [],
        "results": [],
        "metrics": {}
    }
    
    lines = output.strip().split("\n")
    section = "header"
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("ALGORITHM:"):
            result["algorithm"] = line.split(":", 1)[1].strip()
        elif line.startswith("QUANTUM:"):
            result["metrics"]["quantum"] = int(line.split(":", 1)[1].strip())
        elif line == "---":
            section = "next"
        elif line == "RESULTS:":
            section = "results"
        elif " | " in line and section not in ["results"]:
            # Parse step: "1 | EXEC P1 | TIME=0-5 | GANTT:P1"
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                step = {
                    "step": parts[0].strip(),
                    "action": parts[1].strip(),
                    "metric": parts[2].strip() if len(parts) > 2 else "",
                    "state": parts[3].strip() if len(parts) > 3 else ""
                }
                # Extract time range
                for p in parts:
                    if "TIME=" in p:
                        step["time"] = p.split("=")[1]
                result["steps"].append(step)
        elif line.startswith("P") and " | " in line and section == "results":
            # Parse result: "P1 | AT=0 | BT=5 | ST=0 | FT=5 | WT=0 | TAT=5"
            parts = [p.strip() for p in line.split("|")]
            proc_result = {"process": parts[0].strip()}
            for p in parts[1:]:
                if "=" in p:
                    key, val = p.split("=")
                    key = key.strip().lower()
                    proc_result[key] = int(val.strip()) if val.strip().isdigit() else float(val.strip())
            
            # Map short keys to full names
            key_map = {"at": "arrival", "bt": "burst", "st": "start", "ft": "finish", "wt": "waiting", "tat": "turnaround"}
            mapped_result = {"process": proc_result["process"]}
            for k, v in proc_result.items():
                if k in key_map:
                    mapped_result[key_map[k]] = v
                else:
                    mapped_result[k] = v
            result["results"].append(mapped_result)
        elif line.startswith("AVG_WT:"):
            result["metrics"]["avg_wt"] = float(line.split(":")[1].strip())
        elif line.startswith("AVG_TAT:"):
            result["metrics"]["avg_tat"] = float(line.split(":")[1].strip())
        elif line.startswith("CONTEXT_SWITCHES:"):
            result["metrics"]["context_switches"] = int(line.split(":")[1].strip())
        elif line.startswith("TOTAL_TIME:"):
            result["metrics"]["total_time"] = int(line.split(":")[1].strip())
    
    return result


def parse_memory_output(output: str) -> Dict[str, Any]:
    """Parse page replacement output into structured format."""
    result = {
        "algorithm": "",
        "steps": [],
        "metrics": {}
    }
    
    lines = output.strip().split("\n")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("ALGORITHM:"):
            result["algorithm"] = line.split(":", 1)[1].strip()
        elif line.startswith("FRAMES:"):
            result["metrics"]["num_frames"] = int(line.split(":")[1].strip())
        elif " | PAGE " in line:
            # Parse: "1 | PAGE 7 | FAULT | FRAMES:[7,-,-] | REPLACED:3"
            parts = [p.strip() for p in line.split("|")]
            step = {
                "step": parts[0].strip(),
                "page": "",
                "result": "",
                "frames": "",
                "replaced": ""
            }
            for p in parts:
                p = p.strip()
                if p.startswith("PAGE"):
                    step["page"] = p.split()[1]
                elif p in ["HIT", "FAULT"]:
                    step["result"] = p
                elif p.startswith("FRAMES:"):
                    step["frames"] = p.split(":", 1)[1]
                elif p.startswith("REPLACED:"):
                    step["replaced"] = p.split(":")[1]
            result["steps"].append(step)
        elif line.startswith("TOTAL_FAULTS:"):
            result["metrics"]["faults"] = int(line.split(":")[1].strip())
        elif line.startswith("TOTAL_HITS:"):
            result["metrics"]["hits"] = int(line.split(":")[1].strip())
        elif line.startswith("FAULT_RATE:"):
            result["metrics"]["fault_rate"] = float(line.split(":")[1].strip())
        elif line.startswith("HIT_RATE:"):
            result["metrics"]["hit_rate"] = float(line.split(":")[1].strip())
    
    return result


def parse_disk_output(output: str) -> Dict[str, Any]:
    """Parse disk scheduling output into structured format."""
    result = {
        "algorithm": "",
        "steps": [],
        "sequence": [],
        "metrics": {}
    }
    
    lines = output.strip().split("\n")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("ALGORITHM:"):
            result["algorithm"] = line.split(":", 1)[1].strip()
        elif line.startswith("HEAD:"):
            result["metrics"]["initial_head"] = int(line.split(":")[1].strip())
        elif " | MOVE " in line or " | JUMP " in line:
            # Parse: "1 | MOVE 50->82 | SEEK=32 | TOTAL=32"
            parts = [p.strip() for p in line.split("|")]
            step = {
                "step": parts[0].strip(),
                "action": parts[1].strip() if len(parts) > 1 else "",
                "seek": "",
                "total": "",
                "note": ""
            }
            for p in parts:
                p = p.strip()
                if p.startswith("SEEK="):
                    step["seek"] = p
                elif p.startswith("TOTAL="):
                    step["total"] = p.split("=")[1].split()[0]
                elif "boundary" in p or "circular" in p:
                    step["note"] = p
            result["steps"].append(step)
        elif line.startswith("SEQUENCE:"):
            seq_str = line.split(":", 1)[1].strip()
            result["sequence"] = [int(x) for x in seq_str.split(",") if x.strip().isdigit()]
        elif line.startswith("TOTAL_SEEK:"):
            result["metrics"]["total_seek"] = int(line.split(":")[1].strip())
        elif line.startswith("AVG_SEEK:"):
            result["metrics"]["avg_seek"] = float(line.split(":")[1].strip())
    
    return result


def parse_bankers_output(output: str) -> Dict[str, Any]:
    """Parse Banker's algorithm output into structured format."""
    result = {
        "is_safe": False,
        "safe_sequence": [],
        "blocked_processes": [],
        "steps": [],
        "matrices": {}
    }
    
    lines = output.strip().split("\n")
    section = "header"
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line == "SAFETY CHECK:":
            section = "safety"
        elif line == "---":
            continue
        elif line.startswith("STATE:"):
            state = line.split(":")[1].strip()
            result["is_safe"] = state == "SAFE"
        elif line.startswith("SAFE_SEQUENCE:"):
            seq_str = line.split(":", 1)[1].strip()
            result["safe_sequence"] = [p.strip() for p in seq_str.replace("->", ",").split(",")]
        elif line.startswith("BLOCKED_PROCESSES:"):
            blocked_str = line.split(":", 1)[1].strip()
            result["blocked_processes"] = [p.strip() for p in blocked_str.split(",")]
        elif " | CHECK " in line or " | RELEASE " in line:
            parts = [p.strip() for p in line.split("|")]
            step = {
                "step": parts[0].strip(),
                "action": parts[1].strip() if len(parts) > 1 else "",
                "details": parts[2].strip() if len(parts) > 2 else "",
                "result": parts[3].strip() if len(parts) > 3 else ""
            }
            result["steps"].append(step)
    
    return result


def run_dsa_stack(commands: List[str]) -> Tuple[bool, str, str]:
    """Run stack operations."""
    input_data = "\n".join(commands) + "\nEND\n"
    src = get_source_path("dsa/stack", "stack.cpp")
    return run_executable("stack", input_data, source_path=src)


def run_dsa_queue(queue_type: str, size: int, commands: List[str]) -> Tuple[bool, str, str]:
    """Run queue operations."""
    input_data = f"{queue_type} {size}\n" + "\n".join(commands) + "\nEND\n"
    src = get_source_path("dsa/queue", "queue.cpp")
    return run_executable("queue", input_data, source_path=src)


def run_dsa_linkedlist(commands: List[str]) -> Tuple[bool, str, str]:
    """Run linked list operations."""
    input_data = "\n".join(commands) + "\nEND\n"
    src = get_source_path("dsa/linked-list", "ll.cpp")
    return run_executable("ll", input_data, source_path=src)


def run_dsa_bst(commands: List[str]) -> Tuple[bool, str, str]:
    """Run BST operations."""
    input_data = "\n".join(commands) + "\nEND\n"
    src = get_source_path("dsa/trees", "bst.cpp")
    return run_executable("binary_tree", input_data, source_path=src)


def run_dsa_avl(commands: List[str]) -> Tuple[bool, str, str]:
    """Run AVL tree operations."""
    input_data = "\n".join(commands) + "\nEND\n"
    src = get_source_path("dsa/trees", "avl.cpp")
    return run_executable("avl", input_data, source_path=src)


def run_dsa_heap(heap_type: str, commands: List[str]) -> Tuple[bool, str, str]:
    """Run heap operations."""
    input_data = f"{heap_type}\n" + "\n".join(commands) + "\nEND\n"
    src = get_source_path("dsa/heap", "heap.cpp")
    return run_executable("heap", input_data, source_path=src)


def run_dsa_dijkstra(
    num_vertices: int,
    edges: List[Tuple[int, int, int]],
    source: int
) -> Tuple[bool, str, str]:
    """Run Dijkstra's algorithm."""
    lines = [
        str(num_vertices),
        str(len(edges))
    ]
    for u, v, w in edges:
        lines.append(f"{u} {v} {w}")
    lines.append(str(source))
    
    input_data = "\n".join(lines) + "\n"
    src = get_source_path("dsa/graphs", "dijkstra.cpp")
    return run_executable("dijkstra", input_data, source_path=src)


def run_dsa_huffman(text: str) -> Tuple[bool, str, str]:
    """Run Huffman coding."""
    input_data = f"TEXT {text}\nENCODE\nEND\n"
    src = get_source_path("dsa/huffman", "huffman.cpp")
    return run_executable("huffman", input_data, source_path=src)


def run_os_fcfs(processes: List[Tuple[int, int]]) -> Tuple[bool, str, str]:
    """
    Run FCFS CPU scheduling.
    
    Args:
        processes: List of (arrival_time, burst_time) tuples
    """
    lines = [str(len(processes))]
    for arrival, burst in processes:
        lines.append(f"{arrival} {burst}")
    
    input_data = "\n".join(lines) + "\n"
    src = get_source_path("os/cpu", "fcfs.cpp")
    return run_executable("fcfs", input_data, source_path=src)


def run_os_sjf(
    processes: List[Tuple[int, int]],
    preemptive: bool = False
) -> Tuple[bool, str, str]:
    """
    Run SJF/SRTF CPU scheduling.
    
    Args:
        processes: List of (arrival_time, burst_time) tuples
        preemptive: If True, use SRTF (preemptive SJF)
    """
    mode = "PREEMPTIVE" if preemptive else "NON_PREEMPTIVE"
    lines = [mode, str(len(processes))]
    for arrival, burst in processes:
        lines.append(f"{arrival} {burst}")
    
    input_data = "\n".join(lines) + "\n"
    src = get_source_path("os/cpu", "sjf.cpp")
    return run_executable("sjf", input_data, source_path=src)


def run_os_round_robin(
    processes: List[Tuple[int, int]],
    quantum: int
) -> Tuple[bool, str, str]:
    """
    Run Round Robin CPU scheduling.
    
    Args:
        processes: List of (arrival_time, burst_time) tuples
        quantum: Time quantum
    """
    lines = [str(len(processes)), str(quantum)]
    for arrival, burst in processes:
        lines.append(f"{arrival} {burst}")
    
    input_data = "\n".join(lines) + "\n"
    src = get_source_path("os/cpu", "round_robin.cpp")
    return run_executable("round_robin", input_data, source_path=src)


def run_os_priority(
    processes: List[Tuple[int, int, int]],
    preemptive: bool = False
) -> Tuple[bool, str, str]:
    """
    Run Priority CPU scheduling.
    
    Args:
        processes: List of (arrival_time, burst_time, priority) tuples
        preemptive: If True, use preemptive priority scheduling
    """
    mode = "PREEMPTIVE" if preemptive else "NON_PREEMPTIVE"
    lines = [mode, str(len(processes))]
    for arrival, burst, priority in processes:
        lines.append(f"{arrival} {burst} {priority}")
    
    input_data = "\n".join(lines) + "\n"
    src = get_source_path("os/cpu", "priority.cpp")
    return run_executable("priority", input_data, source_path=src)


# ============== HIGH-LEVEL OS RUNNER FUNCTIONS ==============

def run_os_cpu_scheduling(algorithm: str, processes: List, **kwargs) -> Dict[str, Any]:
    """
    High-level function to run CPU scheduling and return parsed results.
    
    Args:
        algorithm: 'fcfs', 'sjf', 'round_robin', or 'priority'
        processes: List of process tuples
        **kwargs: Additional arguments (quantum, preemptive)
    
    Returns:
        Parsed result dictionary
    """
    if algorithm == "fcfs":
        success, stdout, stderr = run_os_fcfs(processes)
    elif algorithm == "sjf":
        preemptive = kwargs.get("preemptive", False)
        success, stdout, stderr = run_os_sjf(processes, preemptive)
    elif algorithm == "round_robin":
        quantum = kwargs.get("quantum", 2)
        success, stdout, stderr = run_os_round_robin(processes, quantum)
    elif algorithm == "priority":
        preemptive = kwargs.get("preemptive", False)
        success, stdout, stderr = run_os_priority(processes, preemptive)
    else:
        return {"error": f"Unknown algorithm: {algorithm}"}
    
    if not success:
        return {"error": stderr or "Execution failed"}
    
    return parse_cpu_output(stdout)


def run_os_page_replacement(algorithm: str, num_frames: int, pages: List[int]) -> Dict[str, Any]:
    """
    High-level function to run page replacement and return parsed results.
    
    Args:
        algorithm: 'fifo', 'lru', or 'optimal'
        num_frames: Number of frames
        pages: Page reference string
    
    Returns:
        Parsed result dictionary
    """
    lines = [str(num_frames)] + [str(p) for p in pages]
    input_data = "\n".join(lines) + "\n"
    
    src = get_source_path(f"os/memory", f"{algorithm}.cpp")
    success, stdout, stderr = run_executable(algorithm, input_data, source_path=src)
    
    if not success:
        return {"error": stderr or "Execution failed"}
    
    return parse_memory_output(stdout)


def run_os_disk_scheduling(algorithm: str, head: int, max_cylinder: int, direction: str, requests: List[int]) -> Dict[str, Any]:
    """
    High-level function to run disk scheduling and return parsed results.
    
    Args:
        algorithm: 'scan', 'cscan', 'look', or 'clook'
        head: Initial head position
        max_cylinder: Maximum cylinder number
        direction: 'UP' or 'DOWN'
        requests: List of cylinder requests
    
    Returns:
        Parsed result dictionary
    """
    # Map algorithm names
    algo_map = {
        "scan": "SCAN",
        "cscan": "C-SCAN",
        "look": "LOOK",
        "clook": "C-LOOK"
    }
    algo_name = algo_map.get(algorithm.lower(), algorithm.upper())
    
    lines = [algo_name, str(head), str(max_cylinder), direction.upper()]
    lines.extend([str(r) for r in requests])
    input_data = "\n".join(lines) + "\n"
    
    src = get_source_path("os/disk", "scan.cpp")
    success, stdout, stderr = run_executable("scan", input_data, source_path=src)
    
    if not success:
        return {"error": stderr or "Execution failed"}
    
    return parse_disk_output(stdout)


def run_os_bankers(num_processes: int, num_resources: int, allocation: List[List[int]], maximum: List[List[int]], available: List[int]) -> Dict[str, Any]:
    """
    High-level function to run Banker's algorithm and return parsed results.
    
    Args:
        num_processes: Number of processes
        num_resources: Number of resource types
        allocation: Allocation matrix
        maximum: Maximum matrix
        available: Available resources
    
    Returns:
        Parsed result dictionary
    """
    lines = [f"{num_processes} {num_resources}"]
    
    # Allocation matrix
    for row in allocation:
        lines.append(" ".join(map(str, row)))
    
    # Maximum matrix
    for row in maximum:
        lines.append(" ".join(map(str, row)))
    
    # Available resources
    lines.append(" ".join(map(str, available)))
    
    input_data = "\n".join(lines) + "\n"
    
    src = get_source_path("os/deadlock", "bankers.cpp")
    success, stdout, stderr = run_executable("bankers", input_data, source_path=src)
    
    if not success:
        return {"error": stderr or "Execution failed"}
    
    return parse_bankers_output(stdout)


if __name__ == "__main__":
    # Test the runner
    print("Testing runner utilities...")
    
    # Test stack
    success, stdout, stderr = run_dsa_stack(["PUSH 10", "PUSH 20", "PUSH 30", "POP"])
    print(f"Stack test: {'SUCCESS' if success else 'FAILED'}")
    if stdout:
        print(stdout[:500])
