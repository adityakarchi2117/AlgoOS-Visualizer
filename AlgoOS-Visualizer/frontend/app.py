# File: frontend/app.py
"""
AlgoOS Visualizer - Main Application
A comprehensive visualization tool for Data Structures, Algorithms, and OS concepts.
"""

import streamlit as st
import sys
from pathlib import Path

# Configure the page
st.set_page_config(
    page_title="AlgoOS Visualizer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add the current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))


def load_css():
    """Load custom CSS."""
    css_path = Path(__file__).parent / "assets" / "styles.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    """Main application entry point."""
    load_css()
    
    # Sidebar navigation
    st.sidebar.title("🎯 AlgoOS Visualizer")
    st.sidebar.markdown("---")
    
    # Navigation categories
    category = st.sidebar.selectbox(
        "Select Category",
        ["🏠 Home", "📚 Data Structures", "⚙️ Operating Systems"]
    )
    
    if category == "🏠 Home":
        show_home()
    
    elif category == "📚 Data Structures":
        from pages import dsa_stack, dsa_linkedlist, dsa_tree
        
        dsa_page = st.sidebar.radio(
            "Select Topic",
            [
                "Stack & Queue",
                "Linked List",
                "Trees & Graphs"
            ]
        )
        
        if dsa_page == "Stack & Queue":
            dsa_stack.main()
        elif dsa_page == "Linked List":
            dsa_linkedlist.main()
        elif dsa_page == "Trees & Graphs":
            dsa_tree.main()
    
    elif category == "⚙️ Operating Systems":
        os_page = st.sidebar.radio(
            "Select Topic",
            [
                "CPU Scheduling",
                "Page Replacement",
                "Disk Scheduling",
                "Deadlock Avoidance"
            ]
        )
        
        if os_page == "CPU Scheduling":
            show_os_cpu()
        elif os_page == "Page Replacement":
            show_os_memory()
        elif os_page == "Disk Scheduling":
            show_os_disk()
        elif os_page == "Deadlock Avoidance":
            show_os_deadlock()
    
    # Sidebar footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📖 About")
    st.sidebar.markdown("""
    This application visualizes:
    - **DSA**: Stack, Queue, Linked List, Trees, Heap, Graphs, Huffman Coding
    - **OS**: CPU Scheduling (FCFS, SJF, Round Robin), Page Replacement (FIFO, LRU, Optimal), Disk Scheduling, Banker's Algorithm
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("Made with ❤️ using Streamlit + C++")


def show_home():
    """Display the home page."""
    st.title("🎯 AlgoOS Visualizer")
    st.markdown("### Interactive Visualization for Data Structures, Algorithms & Operating Systems")
    
    st.markdown("---")
    
    st.markdown("""
    Welcome to **AlgoOS Visualizer**, a comprehensive educational tool that helps you understand 
    fundamental concepts in Computer Science through interactive visualizations.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📚 Data Structures & Algorithms")
        st.markdown("""
        - **Stack**: LIFO operations with step-by-step visualization
        - **Queue**: FIFO operations including circular queues
        - **Linked List**: Dynamic node operations with visual representation
        - **Binary Search Tree**: Insert, delete, search with tree visualization
        - **AVL Tree**: Self-balancing tree with rotation animations
        - **Heap**: Min/Max heap operations and heap sort
        - **Dijkstra's Algorithm**: Shortest path visualization on graphs
        - **Huffman Coding**: Compression algorithm with tree building
        """)
    
    with col2:
        st.markdown("### ⚙️ Operating Systems")
        st.markdown("""
        - **CPU Scheduling**:
          - First Come First Serve (FCFS)
          - Shortest Job First (SJF/SRTF)
          - Round Robin with configurable quantum
          - Priority Scheduling
        - **Page Replacement**:
          - FIFO (First In First Out)
          - LRU (Least Recently Used)
          - Optimal Page Replacement
        - **Disk Scheduling**:
          - SCAN, C-SCAN, LOOK, C-LOOK
        - **Deadlock**:
          - Banker's Algorithm for deadlock avoidance
        """)
    
    st.markdown("---")
    
    st.markdown("### 🚀 Getting Started")
    st.markdown("""
    1. Select a **category** from the sidebar (Data Structures or Operating Systems)
    2. Choose a **topic** to explore
    3. Configure the **input parameters**
    4. Click **Run Simulation** to see the visualization
    """)


# ============== OS PAGE FUNCTIONS ==============

def show_os_cpu():
    """Show CPU Scheduling page."""
    import plotly.graph_objects as go
    import plotly.express as px
    from utils.runner import run_os_cpu_scheduling
    import pandas as pd
    
    st.title("⚙️ CPU Scheduling Algorithms")
    st.markdown("Visualize FCFS, SJF, SRTF, Round Robin, and Priority scheduling with Gantt charts")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        algorithm = st.selectbox(
            "Select Algorithm",
            ["FCFS", "SJF", "SRTF", "Round Robin", "Priority"]
        )
        
        if algorithm == "Round Robin":
            quantum = st.number_input("Time Quantum", min_value=1, max_value=10, value=2)
        
        num_processes = st.slider("Number of Processes", 2, 8, 4)
    
    with col2:
        st.markdown("### Process Configuration")
        processes = []
        cols = st.columns(min(num_processes, 4))
        
        for i in range(num_processes):
            with cols[i % len(cols)]:
                st.markdown(f"**P{i+1}**")
                arrival = st.number_input(f"Arrival", min_value=0, max_value=20, value=i, key=f"at_{i}")
                burst = st.number_input(f"Burst", min_value=1, max_value=20, value=(i % 5) + 2, key=f"bt_{i}")
                
                if algorithm == "Priority":
                    priority = st.number_input(f"Priority", min_value=1, max_value=10, value=(i % 5) + 1, key=f"pr_{i}")
                    processes.append((arrival, burst, priority))
                else:
                    processes.append((arrival, burst))
    
    if st.button("🚀 Run Simulation", type="primary"):
        with st.spinner("Running simulation..."):
            if algorithm == "Round Robin":
                result = run_os_cpu_scheduling("round_robin", processes, quantum=quantum)
            elif algorithm == "Priority":
                result = run_os_cpu_scheduling("priority", processes, preemptive=False)
            elif algorithm in ["SJF", "SRTF"]:
                result = run_os_cpu_scheduling("sjf", processes, preemptive=(algorithm == "SRTF"))
            else:
                result = run_os_cpu_scheduling("fcfs", processes)
            
            if result and "error" not in result:
                st.success(f"Algorithm: {result.get('algorithm', algorithm)}")
                
                # Create Gantt chart
                if "steps" in result:
                    gantt_data = []
                    colors = px.colors.qualitative.Set2
                    
                    for step in result["steps"]:
                        if "EXEC" in step.get("action", ""):
                            process = step["action"].split()[-1]
                            times = step.get("time", "0-0").split("-")
                            if len(times) == 2:
                                gantt_data.append({
                                    "Process": process,
                                    "Start": int(times[0]),
                                    "Finish": int(times[1]),
                                    "Duration": int(times[1]) - int(times[0])
                                })
                    
                    if gantt_data:
                        fig = go.Figure()
                        for item in gantt_data:
                            fig.add_trace(go.Bar(
                                name=item["Process"],
                                x=[item["Duration"]],
                                y=[item["Process"]],
                                orientation='h',
                                base=item["Start"],
                                marker_color=colors[hash(item["Process"]) % len(colors)],
                                text=f"{item['Start']}-{item['Finish']}",
                                textposition='inside'
                            ))
                        
                        fig.update_layout(title="Gantt Chart", xaxis_title="Time", height=300, showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                
                # Results
                if "results" in result:
                    df = pd.DataFrame(result["results"])
                    st.dataframe(df, use_container_width=True)
                
                metrics = result.get("metrics", {})
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Avg Waiting Time", f"{metrics.get('avg_wt', 0):.2f}")
                col2.metric("Avg Turnaround", f"{metrics.get('avg_tat', 0):.2f}")
                col3.metric("Context Switches", metrics.get("context_switches", 0))
                col4.metric("Total Time", metrics.get("total_time", 0))
            else:
                st.error(f"Error: {result.get('error', 'Unknown')}")


def show_os_memory():
    """Show Page Replacement page."""
    import plotly.graph_objects as go
    from utils.runner import run_os_page_replacement
    
    st.title("🧠 Page Replacement Algorithms")
    st.markdown("Visualize FIFO, LRU, and Optimal page replacement")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        algorithm = st.selectbox("Select Algorithm", ["FIFO", "LRU", "Optimal"])
        num_frames = st.slider("Number of Frames", 2, 6, 3)
    
    with col2:
        page_string = st.text_input("Page Reference String (space-separated)", value="7 0 1 2 0 3 0 4 2 3 0 3 2")
        pages = [int(p) for p in page_string.split() if p.isdigit()]
        st.write(f"**Pages:** {' '.join(map(str, pages))}")
    
    if st.button("🚀 Run Simulation", type="primary"):
        with st.spinner("Running simulation..."):
            result = run_os_page_replacement(algorithm.lower(), num_frames, pages)
            
            if result and "error" not in result:
                st.success(f"Algorithm: {result.get('algorithm', algorithm)}")
                
                metrics = result.get("metrics", {})
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Faults", metrics.get("faults", 0))
                col2.metric("Total Hits", metrics.get("hits", 0))
                col3.metric("Fault Rate", f"{metrics.get('fault_rate', 0):.1f}%")
                col4.metric("Hit Rate", f"{metrics.get('hit_rate', 0):.1f}%")
                
                if "steps" in result:
                    with st.expander("Step-by-Step Execution", expanded=True):
                        for step in result["steps"]:
                            step_num = step.get("step", "")
                            page = step.get("page", "")
                            result_type = step.get("result", "")
                            frames = step.get("frames", "")
                            replaced = step.get("replaced", "")
                            
                            if "HIT" in result_type:
                                st.success(f"**Step {step_num}:** Page {page} | ✅ HIT | Frames: {frames}")
                            else:
                                msg = f"**Step {step_num}:** Page {page} | ❌ FAULT | Frames: {frames}"
                                if replaced:
                                    msg += f" | Replaced: {replaced}"
                                st.error(msg)
            else:
                st.error(f"Error: {result.get('error', 'Unknown')}")


def show_os_disk():
    """Show Disk Scheduling page."""
    import plotly.graph_objects as go
    from utils.runner import run_os_disk_scheduling
    
    st.title("💾 Disk Scheduling Algorithms")
    st.markdown("Visualize SCAN, C-SCAN, LOOK, and C-LOOK disk scheduling")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        algorithm = st.selectbox("Select Algorithm", ["SCAN", "C-SCAN", "LOOK", "C-LOOK"])
        head_position = st.number_input("Initial Head Position", min_value=0, max_value=199, value=50)
        max_cylinder = st.number_input("Max Cylinder", min_value=100, max_value=500, value=199)
        direction = st.selectbox("Initial Direction", ["UP", "DOWN"])
    
    with col2:
        request_string = st.text_input("Disk Requests (space-separated)", value="82 170 43 140 24 16 190")
        requests = [int(r) for r in request_string.split() if r.isdigit()]
        st.write(f"**Requests:** {' '.join(map(str, requests))}")
    
    if st.button("🚀 Run Simulation", type="primary"):
        with st.spinner("Running simulation..."):
            algo_key = algorithm.lower().replace("-", "")
            result = run_os_disk_scheduling(algo_key, head_position, max_cylinder, direction, requests)
            
            if result and "error" not in result:
                st.success(f"Algorithm: {result.get('algorithm', algorithm)}")
                
                metrics = result.get("metrics", {})
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Seek Time", metrics.get("total_seek", 0))
                col2.metric("Average Seek Time", f"{metrics.get('avg_seek', 0):.2f}")
                col3.metric("Requests Served", len(requests))
                
                if "sequence" in result:
                    sequence = result["sequence"]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=list(range(len(sequence))),
                        y=sequence,
                        mode='lines+markers',
                        name='Head Position',
                        line=dict(color='blue', width=2),
                        marker=dict(size=10)
                    ))
                    
                    fig.update_layout(
                        title="Head Movement Path",
                        xaxis_title="Step",
                        yaxis_title="Cylinder Position",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"Error: {result.get('error', 'Unknown')}")


def show_os_deadlock():
    """Show Deadlock Avoidance page."""
    import plotly.graph_objects as go
    from utils.runner import run_os_bankers
    import pandas as pd
    
    st.title("🔒 Deadlock Avoidance - Banker's Algorithm")
    st.markdown("Visualize the Banker's Algorithm for deadlock avoidance")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        num_processes = st.slider("Number of Processes", 3, 6, 5)
        num_resources = st.slider("Number of Resource Types", 2, 5, 3)
    
    with col2:
        st.markdown("**Available Resources:**")
        available = []
        avail_cols = st.columns(num_resources)
        for j, col in enumerate(avail_cols):
            with col:
                available.append(st.number_input(f"R{j}", min_value=0, max_value=20, value=3, key=f"avail_{j}"))
    
    st.markdown("### Process Configuration")
    allocation = []
    maximum = []
    
    for i in range(num_processes):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**P{i} Allocation:**")
            alloc_row = []
            alloc_cols = st.columns(num_resources)
            for j, col in enumerate(alloc_cols):
                with col:
                    alloc_row.append(st.number_input(f"A", min_value=0, max_value=10, value=min(i % 3 + 1, 2), key=f"alloc_{i}_{j}"))
            allocation.append(alloc_row)
        
        with col2:
            st.markdown(f"**P{i} Maximum:**")
            max_row = []
            max_cols = st.columns(num_resources)
            for j, col in enumerate(max_cols):
                with col:
                    max_row.append(st.number_input(f"M", min_value=0, max_value=15, value=min(i % 3 + 3, 7), key=f"max_{i}_{j}"))
            maximum.append(max_row)
    
    if st.button("🚀 Run Safety Check", type="primary"):
        with st.spinner("Running Banker's Algorithm..."):
            result = run_os_bankers(num_processes, num_resources, allocation, maximum, available)
            
            if result and "error" not in result:
                is_safe = result.get("is_safe", False)
                
                if is_safe:
                    st.success("✅ System is in SAFE STATE!")
                    safe_sequence = result.get("safe_sequence", [])
                    st.markdown(f"**Safe Sequence:** {' → '.join(safe_sequence)}")
                else:
                    st.error("❌ System is in UNSAFE STATE - Potential Deadlock!")
                    blocked = result.get("blocked_processes", [])
                    st.markdown(f"**Blocked Processes:** {', '.join(blocked)}")
                
                # Display matrices
                st.markdown("### Resource Matrices")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Allocation:**")
                    alloc_df = pd.DataFrame(allocation, index=[f"P{i}" for i in range(num_processes)], columns=[f"R{j}" for j in range(num_resources)])
                    st.dataframe(alloc_df)
                
                with col2:
                    st.markdown("**Maximum:**")
                    max_df = pd.DataFrame(maximum, index=[f"P{i}" for i in range(num_processes)], columns=[f"R{j}" for j in range(num_resources)])
                    st.dataframe(max_df)
                
                with col3:
                    st.markdown("**Need:**")
                    need = [[maximum[i][j] - allocation[i][j] for j in range(num_resources)] for i in range(num_processes)]
                    need_df = pd.DataFrame(need, index=[f"P{i}" for i in range(num_processes)], columns=[f"R{j}" for j in range(num_resources)])
                    st.dataframe(need_df)
            else:
                st.error(f"Error: {result.get('error', 'Unknown')}")


if __name__ == "__main__":
    main()
