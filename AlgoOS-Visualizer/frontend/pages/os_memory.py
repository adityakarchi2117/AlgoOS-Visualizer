# File: frontend/pages/os_memory.py
"""OS Memory/Page Replacement Visualizer - Enhanced with Frame Animations"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.runner import run_os_page_replacement
import pandas as pd

st.set_page_config(page_title="Page Replacement", page_icon="🧠", layout="wide")

st.title("🧠 Page Replacement Algorithms")
st.markdown("Visualize FIFO, LRU, and Optimal page replacement with frame animations")

# Configuration
col1, col2 = st.columns([1, 2])

with col1:
    algorithm = st.selectbox(
        "Select Algorithm",
        ["FIFO", "LRU", "Optimal"],
        help="Choose a page replacement algorithm"
    )
    
    num_frames = st.slider("Number of Frames", 2, 6, 3)
    
    input_method = st.radio("Input Method", ["Manual", "Random"])

with col2:
    st.markdown("### Page Reference String")
    
    if input_method == "Manual":
        page_string = st.text_input(
            "Enter pages (space-separated)",
            value="7 0 1 2 0 3 0 4 2 3 0 3 2",
            help="Enter page numbers separated by spaces"
        )
        pages = [int(p) for p in page_string.split() if p.isdigit()]
    else:
        import random
        num_pages = st.slider("Number of Page References", 10, 30, 15)
        max_page = st.slider("Max Page Number", 5, 15, 9)
        
        if st.button("Generate Random"):
            pages = [random.randint(0, max_page) for _ in range(num_pages)]
            st.session_state['random_pages'] = pages
        
        pages = st.session_state.get('random_pages', [random.randint(0, max_page) for _ in range(num_pages)])
    
    st.write(f"**Pages:** {' '.join(map(str, pages))}")

# Run simulation
if st.button("🚀 Run Simulation", type="primary"):
    with st.spinner("Running simulation..."):
        result = run_os_page_replacement(algorithm.lower(), num_frames, pages)
        
        if result and "error" not in result:
            st.success(f"Algorithm: {result.get('algorithm', algorithm)}")
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            metrics = result.get("metrics", {})
            
            with col1:
                st.metric("Total Faults", metrics.get("faults", 0))
            with col2:
                st.metric("Total Hits", metrics.get("hits", 0))
            with col3:
                st.metric("Fault Rate", f"{metrics.get('fault_rate', 0):.1f}%")
            with col4:
                st.metric("Hit Rate", f"{metrics.get('hit_rate', 0):.1f}%")
            
            # Step visualization
            if "steps" in result:
                st.markdown("### 📊 Frame State Over Time")
                
                # Create frame state visualization
                steps = result["steps"]
                
                # Animated frame visualization
                fig = go.Figure()
                
                # Track frame states for each step
                frame_states = []
                hit_miss = []
                
                for step in steps:
                    frames_str = step.get("frames", "[-,-,-]")
                    # Parse frames
                    frames = frames_str.strip("[]").split(",")
                    frames = [f.strip() for f in frames]
                    frame_states.append(frames)
                    hit_miss.append("HIT" in step.get("result", ""))
                
                # Create heatmap-style visualization
                for i, (frames, is_hit) in enumerate(zip(frame_states, hit_miss)):
                    for j, frame_val in enumerate(frames):
                        color = 'lightgreen' if is_hit else ('indianred' if frame_val != '-' and i > 0 and frame_states[i-1][j] != frame_val else 'lightblue')
                        
                        fig.add_trace(go.Scatter(
                            x=[i + 1],
                            y=[j],
                            mode='markers+text',
                            marker=dict(size=30, color=color, symbol='square'),
                            text=frame_val,
                            textposition='middle center',
                            showlegend=False,
                            hovertemplate=f"Step {i+1}<br>Frame {j}: {frame_val}<br>{'Hit' if is_hit else 'Fault'}<extra></extra>"
                        ))
                
                fig.update_layout(
                    title="Frame States Over Time",
                    xaxis_title="Reference Step",
                    yaxis_title="Frame",
                    height=250,
                    yaxis=dict(tickmode='array', tickvals=list(range(num_frames)), ticktext=[f"Frame {i}" for i in range(num_frames)])
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Hit/Miss meter
                st.markdown("### 🎯 Hit/Miss Meter")
                
                fig2 = go.Figure()
                
                # Create cumulative hit/miss chart
                cum_hits = []
                cum_faults = []
                current_hits = 0
                current_faults = 0
                
                for is_hit in hit_miss:
                    if is_hit:
                        current_hits += 1
                    else:
                        current_faults += 1
                    cum_hits.append(current_hits)
                    cum_faults.append(current_faults)
                
                fig2.add_trace(go.Scatter(
                    x=list(range(1, len(pages) + 1)),
                    y=cum_hits,
                    mode='lines+markers',
                    name='Cumulative Hits',
                    line=dict(color='green')
                ))
                
                fig2.add_trace(go.Scatter(
                    x=list(range(1, len(pages) + 1)),
                    y=cum_faults,
                    mode='lines+markers',
                    name='Cumulative Faults',
                    line=dict(color='red')
                ))
                
                fig2.update_layout(title="Cumulative Hits vs Faults", height=300)
                st.plotly_chart(fig2, use_container_width=True)
                
                # Step-by-step details
                with st.expander("📋 Step-by-Step Execution", expanded=True):
                    for step in steps:
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
            st.error(f"Error running simulation: {result.get('error', 'Unknown error')}")

# Algorithm comparison
with st.expander("📊 Compare All Algorithms"):
    if st.button("Compare FIFO, LRU, and Optimal"):
        results = {}
        
        for algo in ["fifo", "lru", "optimal"]:
            result = run_os_page_replacement(algo, num_frames, pages)
            if result and "error" not in result:
                results[algo.upper()] = result.get("metrics", {})
        
        if results:
            comparison_data = {
                "Algorithm": list(results.keys()),
                "Faults": [r.get("faults", 0) for r in results.values()],
                "Hits": [r.get("hits", 0) for r in results.values()],
                "Fault Rate %": [r.get("fault_rate", 0) for r in results.values()]
            }
            
            st.dataframe(pd.DataFrame(comparison_data))
            
            fig = go.Figure(data=[
                go.Bar(name='Faults', x=comparison_data["Algorithm"], y=comparison_data["Faults"], marker_color='indianred'),
                go.Bar(name='Hits', x=comparison_data["Algorithm"], y=comparison_data["Hits"], marker_color='lightgreen')
            ])
            fig.update_layout(barmode='group', title="Algorithm Comparison")
            st.plotly_chart(fig, use_container_width=True)

# Info section
with st.expander("ℹ️ Algorithm Information"):
    st.markdown("""
    ### Page Replacement Algorithms
    
    - **FIFO (First In First Out):** Replaces the oldest page in memory
    - **LRU (Least Recently Used):** Replaces the page that hasn't been used for the longest time
    - **Optimal:** Replaces the page that won't be used for the longest time in the future (theoretical best)
    
    ### Metrics
    - **Page Fault:** Occurs when a requested page is not in memory
    - **Page Hit:** Occurs when a requested page is already in memory
    - **Fault Rate:** Percentage of references that result in faults
    """)
