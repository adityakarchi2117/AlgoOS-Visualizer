# File: frontend/utils/parser.py
"""
Parser utility to convert C++ output into structured data for visualization.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class StackState:
    elements: List[int] = field(default_factory=list)
    operation: str = ""
    value: Optional[int] = None


@dataclass
class QueueState:
    elements: List[int] = field(default_factory=list)
    operation: str = ""
    value: Optional[int] = None
    front: int = 0
    rear: int = -1


@dataclass
class LinkedListNode:
    data: int
    position: int


@dataclass
class LinkedListState:
    nodes: List[LinkedListNode] = field(default_factory=list)
    operation: str = ""
    size: int = 0


@dataclass
class TreeNode:
    value: int
    level: int
    left: Optional['TreeNode'] = None
    right: Optional['TreeNode'] = None


@dataclass
class GanttEntry:
    process_id: int  # -1 for idle
    start_time: int
    end_time: int


@dataclass
class ProcessResult:
    id: int
    arrival: int
    burst: int
    start: int
    finish: int
    waiting: int
    turnaround: int


@dataclass
class CPUSchedulingResult:
    gantt_chart: List[GanttEntry] = field(default_factory=list)
    processes: List[ProcessResult] = field(default_factory=list)
    avg_waiting: float = 0.0
    avg_turnaround: float = 0.0
    steps: List[str] = field(default_factory=list)


@dataclass
class PageReplacementStep:
    page: int
    frames: List[int]
    is_fault: bool
    replaced_page: Optional[int] = None


@dataclass
class PageReplacementResult:
    steps: List[PageReplacementStep] = field(default_factory=list)
    total_faults: int = 0
    total_hits: int = 0
    fault_rate: float = 0.0
    hit_rate: float = 0.0


@dataclass
class DiskSchedulingResult:
    sequence: List[int] = field(default_factory=list)
    total_seek: int = 0
    avg_seek: float = 0.0
    movements: List[Tuple[int, int, int]] = field(default_factory=list)  # from, to, seek


@dataclass
class BankersResult:
    is_safe: bool = False
    safe_sequence: List[int] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    need_matrix: List[List[int]] = field(default_factory=list)


def parse_stack_output(output: str) -> List[StackState]:
    """Parse stack visualizer output into a list of states.
    
    New format: STEP | OPERATION | LINE | STATE | META
    Example: 1 | PUSH 10 | 3 | STACK:[10] | TOP=10,SIZE=1
    """
    states = []
    
    for line in output.split('\n'):
        line = line.strip()
        if not line or ' | ' not in line:
            continue
        
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 4:
            continue
        
        operation = parts[1].strip()
        state_str = parts[3].strip()
        meta = parts[4].strip() if len(parts) > 4 else ""
        
        # Parse operation and value
        op_parts = operation.split()
        op_name = op_parts[0] if op_parts else ""
        op_value = None
        if len(op_parts) > 1 and op_parts[1].lstrip('-').isdigit():
            op_value = int(op_parts[1])
        
        # Parse state - STACK:[1,2,3]
        elements = []
        if state_str.startswith('STACK:'):
            array_str = state_str[6:]  # Remove "STACK:"
            if array_str.startswith('[') and array_str.endswith(']'):
                content = array_str[1:-1]
                if content:
                    for x in content.split(','):
                        x = x.strip()
                        if x.lstrip('-').isdigit():
                            elements.append(int(x))
        
        states.append(StackState(
            elements=elements,
            operation=op_name,
            value=op_value
        ))
    
    return states


def parse_queue_output(output: str) -> List[QueueState]:
    """Parse queue visualizer output into a list of states.
    
    New format: STEP | OPERATION | LINE | STATE | META
    Example: 1 | ENQUEUE 5 | 3 | QUEUE:[5] | REAR=5,SIZE=1
    """
    states = []
    
    for line in output.split('\n'):
        line = line.strip()
        if not line or ' | ' not in line:
            continue
        
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 4:
            continue
        
        operation = parts[1].strip()
        state_str = parts[3].strip()
        meta = parts[4].strip() if len(parts) > 4 else ""
        
        # Parse operation and value
        op_parts = operation.split()
        op_name = op_parts[0] if op_parts else ""
        op_value = None
        if len(op_parts) > 1 and op_parts[1].lstrip('-').isdigit():
            op_value = int(op_parts[1])
        
        # Parse state - QUEUE:[1,2,3]
        elements = []
        if state_str.startswith('QUEUE:'):
            array_str = state_str[6:]  # Remove "QUEUE:"
            if array_str.startswith('[') and array_str.endswith(']'):
                content = array_str[1:-1]
                if content:
                    for x in content.split(','):
                        x = x.strip()
                        if x.lstrip('-').isdigit():
                            elements.append(int(x))
        
        # Parse front/rear from meta
        front = 0
        rear = len(elements) - 1
        if meta:
            for kv in meta.split(','):
                if '=' in kv:
                    k, v = kv.split('=', 1)
                    if k.strip() == 'FRONT' and v.strip().isdigit():
                        front = int(v.strip())
                    elif k.strip() == 'REAR' and v.strip().isdigit():
                        rear = int(v.strip())
        
        states.append(QueueState(
            elements=elements,
            operation=op_name,
            value=op_value,
            front=front,
            rear=rear
        ))
    
    return states


def parse_linkedlist_output(output: str) -> List[LinkedListState]:
    """Parse linked list visualizer output into a list of states.
    
    New format: STEP | OPERATION | LINE | STATE | META
    Example: 2 | INSERT_TAIL 20 | 4 | LIST:10->20->NULL | CUR=20,SIZE=2
    """
    states = []
    
    for line in output.split('\n'):
        line = line.strip()
        if not line or ' | ' not in line:
            continue
        
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 4:
            continue
        
        operation = parts[1].strip()
        state_str = parts[3].strip()
        meta = parts[4].strip() if len(parts) > 4 else ""
        
        # Parse operation
        op_parts = operation.split()
        op_name = op_parts[0] if op_parts else ""
        
        # Parse state - LIST:10->20->30->NULL
        nodes = []
        if state_str.startswith('LIST:'):
            list_str = state_str[5:]  # Remove "LIST:"
            if list_str == "NULL":
                nodes = []
            else:
                # Parse "10->20->30->NULL"
                node_parts = list_str.replace("->NULL", "").split("->")
                for i, p in enumerate(node_parts):
                    p = p.strip()
                    if p and p != "NULL" and p.lstrip('-').isdigit():
                        nodes.append(LinkedListNode(data=int(p), position=i))
        
        # Parse size from meta
        size = len(nodes)
        if meta:
            for kv in meta.split(','):
                if '=' in kv:
                    k, v = kv.split('=', 1)
                    if k.strip() == 'SIZE' and v.strip().isdigit():
                        size = int(v.strip())
        
        states.append(LinkedListState(
            nodes=nodes,
            operation=op_name,
            size=size
        ))
    
    return states


def parse_cpu_scheduling_output(output: str) -> CPUSchedulingResult:
    """Parse CPU scheduling output into structured result."""
    result = CPUSchedulingResult()
    
    for line in output.split('\n'):
        line = line.strip()
        
        # Parse Gantt chart
        if line.startswith('GANTT_CHART:'):
            continue
        
        # Parse steps
        if line.startswith('STEP:'):
            result.steps.append(line)
        
        # Parse process results from table
        if line.startswith('  P') and '|' in line:
            parts = line.split('|')
            if len(parts) >= 7:
                try:
                    pid = int(re.search(r'P(\d+)', parts[0]).group(1))
                    arrival = int(parts[1].strip())
                    burst = int(parts[2].strip())
                    start = int(parts[3].strip())
                    finish = int(parts[4].strip())
                    waiting = int(parts[5].strip())
                    turnaround = int(parts[6].strip())
                    
                    result.processes.append(ProcessResult(
                        id=pid,
                        arrival=arrival,
                        burst=burst,
                        start=start,
                        finish=finish,
                        waiting=waiting,
                        turnaround=turnaround
                    ))
                except (ValueError, AttributeError):
                    pass
        
        # Parse averages
        if 'Average Waiting Time:' in line:
            match = re.search(r'[\d.]+', line.split(':')[1])
            if match:
                result.avg_waiting = float(match.group())
        
        if 'Average Turnaround Time:' in line:
            match = re.search(r'[\d.]+', line.split(':')[1])
            if match:
                result.avg_turnaround = float(match.group())
    
    # Build Gantt chart from process results
    for p in sorted(result.processes, key=lambda x: x.start):
        result.gantt_chart.append(GanttEntry(
            process_id=p.id,
            start_time=p.start,
            end_time=p.finish
        ))
    
    return result


def parse_page_replacement_output(output: str) -> PageReplacementResult:
    """Parse page replacement output into structured result."""
    result = PageReplacementResult()
    current_step = None
    
    for line in output.split('\n'):
        line = line.strip()
        
        if line.startswith('STEP'):
            match = re.search(r'STEP \d+: Access page (\d+)', line)
            if match:
                current_step = PageReplacementStep(
                    page=int(match.group(1)),
                    frames=[],
                    is_fault=False
                )
        
        if current_step and 'RESULT:' in line:
            current_step.is_fault = 'FAULT' in line
            if 'Replacing page' in line:
                match = re.search(r'Replacing page (\d+)', line)
                if match:
                    current_step.replaced_page = int(match.group(1))
        
        if current_step and line.startswith('  FRAMES:'):
            frames = []
            parts = re.findall(r'\[(\d+)\]=(\d+|_)', line)
            for idx, val in parts:
                if val != '_':
                    frames.append(int(val))
                else:
                    frames.append(-1)
            current_step.frames = frames
            result.steps.append(current_step)
            current_step = None
        
        # Parse statistics
        if 'Page Faults:' in line:
            match = re.search(r'(\d+)', line.split(':')[1])
            if match:
                result.total_faults = int(match.group(1))
        
        if 'Page Hits:' in line:
            match = re.search(r'(\d+)', line.split(':')[1])
            if match:
                result.total_hits = int(match.group(1))
        
        if 'Fault Rate:' in line:
            match = re.search(r'([\d.]+)', line.split(':')[1])
            if match:
                result.fault_rate = float(match.group(1))
        
        if 'Hit Rate:' in line:
            match = re.search(r'([\d.]+)', line.split(':')[1])
            if match:
                result.hit_rate = float(match.group(1))
    
    return result


def parse_disk_scheduling_output(output: str) -> DiskSchedulingResult:
    """Parse disk scheduling output into structured result."""
    result = DiskSchedulingResult()
    
    for line in output.split('\n'):
        line = line.strip()
        
        if line.startswith('  Move:'):
            match = re.search(r'Move: (\d+) -> (\d+) \(seek=(\d+)', line)
            if match:
                from_pos = int(match.group(1))
                to_pos = int(match.group(2))
                seek = int(match.group(3))
                result.movements.append((from_pos, to_pos, seek))
        
        if line.startswith('SEQUENCE:'):
            numbers = re.findall(r'\d+', line)
            result.sequence = [int(n) for n in numbers]
        
        if line.startswith('TOTAL_SEEK:'):
            match = re.search(r'(\d+)', line)
            if match:
                result.total_seek = int(match.group(1))
        
        if line.startswith('AVERAGE_SEEK:'):
            match = re.search(r'([\d.]+)', line)
            if match:
                result.avg_seek = float(match.group(1))
    
    return result


def parse_bankers_output(output: str) -> BankersResult:
    """Parse Banker's algorithm output into structured result."""
    result = BankersResult()
    
    for line in output.split('\n'):
        line = line.strip()
        
        if 'STEP' in line:
            result.steps.append(line)
        
        if 'SAFE state' in line:
            result.is_safe = True
        elif 'UNSAFE state' in line:
            result.is_safe = False
        
        if line.startswith('SAFE_SEQUENCE:') and 'None' not in line:
            # Extract process IDs
            processes = re.findall(r'P(\d+)', line)
            result.safe_sequence = [int(p) for p in processes]
    
    return result


def parse_dijkstra_output(output: str) -> Dict[str, Any]:
    """Parse Dijkstra's algorithm output.
    
    New format: STEP | OPERATION | LINE | STATE | META
    Example: 3 | RELAX 1->2 | 9 | DIST:[0,4,7,∞] | CUR=1,EDGE=1-2
    """
    result = {
        'steps': [],
        'distances': [],
        'paths': {},
        'visited_order': []
    }
    
    for line in output.split('\n'):
        line = line.strip()
        if not line or ' | ' not in line:
            continue
        
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 4:
            continue
        
        step_num = parts[0].strip()
        operation = parts[1].strip()
        state_str = parts[3].strip()
        meta = parts[4].strip() if len(parts) > 4 else ""
        
        step_info = {
            'step': step_num,
            'operation': operation,
            'state': state_str,
            'meta': meta
        }
        
        # Parse distances from DIST:[0,4,7,∞]
        if state_str.startswith('DIST:'):
            dist_str = state_str[5:]
            if dist_str.startswith('[') and dist_str.endswith(']'):
                content = dist_str[1:-1]
                distances = []
                for x in content.split(','):
                    x = x.strip()
                    if x == '∞' or x == 'INF' or x == 'inf':
                        distances.append(float('inf'))
                    elif x.lstrip('-').isdigit():
                        distances.append(int(x))
                step_info['distances'] = distances
                result['distances'] = distances
        
        # Parse visited node
        if 'VISIT' in operation:
            node_parts = operation.split()
            if len(node_parts) > 1 and node_parts[1].isdigit():
                result['visited_order'].append(int(node_parts[1]))
        
        # Parse path results
        if operation.startswith('PATH'):
            meta_dict = {}
            for kv in meta.split(','):
                if '=' in kv:
                    k, v = kv.split('=', 1)
                    meta_dict[k.strip()] = v.strip()
            if 'PATH' in meta_dict and 'COST' in meta_dict:
                step_info['path'] = meta_dict['PATH']
                step_info['cost'] = int(meta_dict['COST'])
                result['paths'][operation] = {
                    'path': meta_dict['PATH'],
                    'cost': int(meta_dict['COST'])
                }
        
        result['steps'].append(step_info)
    
    return result


def parse_huffman_output(output: str) -> Dict[str, Any]:
    """Parse Huffman coding output.
    
    New format: STEP | OPERATION | LINE | STATE | META
    Example: 3 | LEAF e | 101 | TREE:1:e:1(_,_) | CHAR=e,FREQ=1,ID=1
    """
    result = {
        'frequencies': {},
        'codes': {},
        'steps': [],
        'encoded': '',
        'compression_ratio': 0.0,
        'tree_states': []
    }
    
    for line in output.split('\n'):
        line = line.strip()
        if not line or ' | ' not in line:
            continue
        
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 4:
            continue
        
        step_num = parts[0].strip()
        operation = parts[1].strip()
        state_str = parts[3].strip()
        meta = parts[4].strip() if len(parts) > 4 else ""
        
        step_info = {
            'step': step_num,
            'operation': operation,
            'state': state_str,
            'meta': meta
        }
        
        # Parse frequencies from FREQ:{a:2,b:3,c:5}
        if state_str.startswith('FREQ:{'):
            freq_str = state_str[5:]
            if freq_str.startswith('{') and freq_str.endswith('}'):
                content = freq_str[1:-1]
                for kv in content.split(','):
                    if ':' in kv:
                        k, v = kv.split(':', 1)
                        k = k.strip().strip("'")
                        if k and v.strip().isdigit():
                            result['frequencies'][k] = int(v.strip())
        
        # Parse codes from CODES:{a:00,b:01,c:10}
        if state_str.startswith('CODES:{'):
            codes_str = state_str[6:]
            if codes_str.startswith('{') and codes_str.endswith('}'):
                content = codes_str[1:-1]
                for kv in content.split(','):
                    if ':' in kv:
                        k, v = kv.split(':', 1)
                        k = k.strip().strip("'")
                        if k:
                            result['codes'][k] = v.strip()
        
        # Parse tree state from TREE:...
        if state_str.startswith('TREE:') and state_str != 'TREE:EMPTY':
            tree_str = state_str[5:]
            result['tree_states'].append({
                'operation': operation,
                'tree': tree_str
            })
        
        # Parse encoded result
        if state_str.startswith('ENCODED:'):
            result['encoded'] = state_str[8:]
        
        # Parse compression ratio from meta
        if 'COMPRESSION' in meta:
            for kv in meta.split(','):
                if 'COMPRESSION' in kv and '=' in kv:
                    v = kv.split('=')[1].replace('%', '')
                    if v.isdigit():
                        result['compression_ratio'] = int(v)
        
        result['steps'].append(step_info)
    
    return result


# ============== NEW FORMAT GENERIC PARSER ==============

def parse_dsa_generic_output(output: str) -> Dict[str, Any]:
    """Generic parser for new DSA output format: STEP | OPERATION | LINE | STATE | META"""
    result = {
        'steps': [],
        'raw_output': output
    }
    
    for line in output.split('\n'):
        line = line.strip()
        if not line or ' | ' not in line:
            continue
        
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 4:
            step = {
                'step': int(parts[0]) if parts[0].isdigit() else parts[0],
                'operation': parts[1].strip(),
                'line': int(parts[2]) if parts[2].isdigit() else parts[2],
                'state': parts[3].strip(),
                'meta': parts[4].strip() if len(parts) > 4 else ''
            }
            
            # Parse meta into dict
            step['meta_dict'] = {}
            if step['meta']:
                for kv in step['meta'].split(','):
                    if '=' in kv:
                        k, v = kv.split('=', 1)
                        step['meta_dict'][k.strip()] = v.strip()
            
            result['steps'].append(step)
    
    return result


def parse_heap_output(output: str) -> List[Dict[str, Any]]:
    """Parse heap visualizer output.
    
    New format: STEP | OPERATION | LINE | STATE | META
    Example: 4 | SWAP 20<->5 | 8 | HEAP:[5,15,20] | IDX=0,PERCOLATE=UP
    """
    states = []
    
    for line in output.split('\n'):
        line = line.strip()
        if not line or ' | ' not in line:
            continue
        
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 4:
            continue
        
        operation = parts[1].strip()
        state_str = parts[3].strip()
        meta = parts[4].strip() if len(parts) > 4 else ""
        
        # Parse heap array from HEAP:[1,2,3]
        elements = []
        if state_str.startswith('HEAP:'):
            array_str = state_str[5:]
            if array_str.startswith('[') and array_str.endswith(']'):
                content = array_str[1:-1]
                if content:
                    for x in content.split(','):
                        x = x.strip()
                        if x.lstrip('-').isdigit():
                            elements.append(int(x))
        
        states.append({
            'operation': operation,
            'heap': elements,
            'meta': meta
        })
    
    return states


def parse_tree_output(output: str) -> List[Dict[str, Any]]:
    """Parse BST/AVL tree visualizer output.
    
    New format: STEP | OPERATION | LINE | STATE | META
    Example: 3 | INSERT 7 | 5 | TREE:10(5,15),5(3,7),15(_,_) | CUR=7
    """
    states = []
    
    for line in output.split('\n'):
        line = line.strip()
        if not line or ' | ' not in line:
            continue
        
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 4:
            continue
        
        operation = parts[1].strip()
        state_str = parts[3].strip()
        meta = parts[4].strip() if len(parts) > 4 else ""
        
        # Parse tree nodes from TREE:10(5,15),5(3,7),15(_,_)
        tree_nodes = []
        if state_str.startswith('TREE:'):
            tree_str = state_str[5:]
            if tree_str != 'EMPTY':
                # Find all node patterns: value(left,right) - support negative values
                node_matches = re.findall(r'(-?\d+)\(([^,]+),([^)]+)\)', tree_str)
                for val, left, right in node_matches:
                    left_val = None
                    right_val = None
                    if left != '_':
                        left_val = int(left) if left.lstrip('-').isdigit() else None
                    if right != '_':
                        right_val = int(right) if right.lstrip('-').isdigit() else None
                    node = {
                        'value': int(val),
                        'left': left_val,
                        'right': right_val
                    }
                    tree_nodes.append(node)
        
        # Parse balance factors for AVL from BF:{10:0,5:-1,15:0}
        balance_factors = {}
        if 'BF:' in meta:
            bf_match = re.search(r'BF:\{([^}]+)\}', meta)
            if bf_match:
                bf_str = bf_match.group(1)
                for kv in bf_str.split(','):
                    if ':' in kv:
                        k, v = kv.split(':')
                        if k.strip().lstrip('-').isdigit():
                            balance_factors[int(k.strip())] = int(v.strip())
        
        states.append({
            'operation': operation,
            'tree_nodes': tree_nodes,
            'balance_factors': balance_factors,
            'meta': meta
        })
    
    return states


def extract_tree_structure(output: str) -> List[Dict[str, Any]]:
    """Extract tree structure for visualization."""
    nodes = []
    
    for line in output.split('\n'):
        if '├──' in line or '└──' in line:
            # Count indent to determine level
            indent = len(line) - len(line.lstrip())
            level = indent // 4
            
            # Extract value
            match = re.search(r'[├└]──(\d+)', line)
            if match:
                nodes.append({
                    'value': int(match.group(1)),
                    'level': level,
                    'line': line
                })
    
    return nodes
