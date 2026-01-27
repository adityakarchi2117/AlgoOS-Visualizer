# File: frontend/pages/os_disk.py
"""OS Disk Scheduling Visualizer - Enhanced with Head Movement Animation"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.runner import run_os_disk_scheduling
import pandas as pd

st.set_page_config(page_title="Disk Scheduling", page_icon="💾", layout="wide")

st.title("💾 Disk Scheduling Algorithms")
st.markdown("Visualize SCAN, C-SCAN, LOOK, and C-LOOK with head movement animations")

# Configuration
col1, col2 = st.columns([1, 2])

with col1:
    algorithm = st.selectbox(
        "Select Algorithm",
        ["SCAN", "C-SCAN", "LOOK", "C-LOOK"],
        help="Choose a disk scheduling algorithm"
    )
    
    head_position = st.number_input("Initial Head Position", min_value=0, max_value=199, value=50)
    max_cylinder = st.number_input("Max Cylinder", min_value=100, max_value=500, value=199)
    
    direction = st.selectbox("Initial Direction", ["UP", "DOWN"])

with col2:
    st.markdown("### Disk Request Queue")
    
    input_method = st.radio("Input Method", ["Manual", "Random"])
    
    if input_method == "Manual":
        request_string = st.text_input(
            "Enter requests (space-separated)",
            value="82 170 43 140 24 16 190",
            help="Enter cylinder numbers separated by spaces"
        )
        requests = [int(r) for r in request_string.split() if r.isdigit()]
    else:
        import random
        num_requests = st.slider("Number of Requests", 5, 15, 8)
        
        if st.button("Generate Random"):
            requests = sorted(random.sample(range(0, max_cylinder), num_requests))
            random.shuffle(requests)
            st.session_state['random_requests'] = requests
        
        requests = st.session_state.get('random_requests', random.sample(range(0, max_cylinder), num_requests))
    
    st.write(f"**Requests:** {' '.join(map(str, requests))}")

# Run simulation
if st.button("🚀 Run Simulation", type="primary"):
    with st.spinner("Running simulation..."):
        result = run_os_disk_scheduling(algorithm.lower().replace("-", ""), head_position, max_cylinder, direction, requests)
        
        if result and "error" not in result:
            st.success(f"Algorithm: {result.get('algorithm', algorithm)}")
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            metrics = result.get("metrics", {})
            
            with col1:
                st.metric("Total Seek Time", metrics.get("total_seek", 0))
            with col2:
                st.metric("Average Seek Time", f"{metrics.get('avg_seek', 0):.2f}")
            with col3:
                st.metric("Requests Served", len(requests))
            
            # Head movement visualization
            if "sequence" in result:
                st.markdown("### 📊 Head Movement Visualization")
                
                sequence = result["sequence"]
                
                # Create head movement chart
                fig = go.Figure()
                
                # Plot the sequence
                fig.add_trace(go.Scatter(
                    x=list(range(len(sequence))),
                    y=sequence,
                    mode='lines+markers',
                    name='Head Position',
                    line=dict(color='blue', width=2),
                    marker=dict(size=10, color='blue'),
                    hovertemplate='Step %{x}<br>Cylinder: %{y}<extra></extra>'
                ))
                
                # Highlight start position
                fig.add_trace(go.Scatter(
                    x=[0],
                    y=[sequence[0]],
                    mode='markers',
                    name='Start',
                    marker=dict(size=15, color='green', symbol='star'),
                ))
                
                # Highlight end position
                fig.add_trace(go.Scatter(
                    x=[len(sequence) - 1],
                    y=[sequence[-1]],
                    mode='markers',
                    name='End',
                    marker=dict(size=15, color='red', symbol='star'),
                ))
                
                # Add boundary lines
                fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Cylinder 0")
                fig.add_hline(y=max_cylinder, line_dash="dash", line_color="gray", annotation_text=f"Cylinder {max_cylinder}")
                
                fig.update_layout(
                    title="Head Movement Path",
                    xaxis_title="Step",
                    yaxis_title="Cylinder Position",
                    height=400,
                    yaxis=dict(range=[-10, max_cylinder + 10])
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Seek distance per step
                st.markdown("### 📈 Seek Distance Per Step")
                
                seek_distances = []
                for i in range(1, len(sequence)):
                    seek_distances.append(abs(sequence[i] - sequence[i-1]))
                
                fig2 = go.Figure(data=[
                    go.Bar(
                        x=[f"Step {i+1}" for i in range(len(seek_distances))],
                        y=seek_distances,
                        marker_color=px.colors.sequential.Blues[3:]
                    )
                ])
                
                fig2.update_layout(
                    title="Seek Distance at Each Step",
                    xaxis_title="Step",
                    yaxis_title="Seek Distance",
                    height=300
                )
                
                st.plotly_chart(fig2, use_container_width=True)
            
            # Step-by-step details
            if "steps" in result:
                with st.expander("📋 Step-by-Step Execution", expanded=True):
                    for step in result["steps"]:
                        step_num = step.get("step", "")
                        action = step.get("action", "")
                        seek = step.get("seek", "")
                        total = step.get("total", "")
                        
                        if "JUMP" in action:
                            st.info(f"**Step {step_num}:** {action} | {seek} | Total: {total}")
                        elif "boundary" in str(step.get("note", "")):
                            st.warning(f"**Step {step_num}:** {action} | {seek} | Total: {total} (boundary)")
                        else:
                            st.success(f"**Step {step_num}:** {action} | {seek} | Total: {total}")
        
        else:
            st.error(f"Error running simulation: {result.get('error', 'Unknown error')}")

# Algorithm comparison
with st.expander("📊 Compare All Algorithms"):
    if st.button("Compare All Disk Algorithms"):
        results = {}
        
        for algo in ["scan", "c-scan", "look", "c-look"]:
            result = run_os_disk_scheduling(algo.replace("-", ""), head_position, max_cylinder, direction, requests)
            if result and "error" not in result:
                results[algo.upper()] = result.get("metrics", {})
        
        if results:
            comparison_data = {
                "Algorithm": list(results.keys()),
                "Total Seek": [r.get("total_seek", 0) for r in results.values()],
                "Avg Seek": [r.get("avg_seek", 0) for r in results.values()]
            }
            
            st.dataframe(pd.DataFrame(comparison_data))
            
            fig = go.Figure(data=[
                go.Bar(name='Total Seek', x=comparison_data["Algorithm"], y=comparison_data["Total Seek"])
            ])
            fig.update_layout(title="Algorithm Comparison - Total Seek Time")
            st.plotly_chart(fig, use_container_width=True)

# Info section
with st.expander("ℹ️ Algorithm Information"):
    st.markdown("""
    ### Disk Scheduling Algorithms
    
    - **SCAN (Elevator):** Moves in one direction, servicing all requests, then reverses at the boundary
    - **C-SCAN (Circular SCAN):** Moves in one direction, then jumps back to the start without servicing
    - **LOOK:** Like SCAN but reverses at the last request instead of the boundary
    - **C-LOOK:** Like C-SCAN but jumps back to the first request instead of cylinder 0
    
    ### Metrics
    - **Seek Time:** Total head movement distance
    - **Average Seek:** Average movement per request
    """)
