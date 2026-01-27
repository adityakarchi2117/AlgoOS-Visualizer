# File: frontend/pages/dsa_stack.py
"""
Stack and Queue Visualization Page
"""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.runner import run_dsa_stack, run_dsa_queue
from utils.parser import parse_stack_output, parse_queue_output


def draw_stack(elements: list, title: str = "Stack State"):
    """Draw stack visualization using Plotly."""
    if not elements:
        st.info("Stack is empty")
        return
    
    fig = go.Figure()
    
    n = len(elements)
    colors = [f'hsl({200 + i * 20}, 70%, 50%)' for i in range(n)]
    
    for i, val in enumerate(elements):
        fig.add_trace(go.Bar(
            x=[1],
            y=[1],
            base=[i],
            marker_color=colors[i],
            text=[str(val)],
            textposition='inside',
            textfont=dict(size=16, color='white'),
            hoverinfo='text',
            hovertext=f'Index: {i}, Value: {val}',
            showlegend=False
        ))
    
    # Add TOP indicator
    fig.add_annotation(
        x=1.7,
        y=n - 0.5,
        text="← TOP",
        showarrow=False,
        font=dict(size=14, color='red')
    )
    
    # Add BOTTOM indicator
    fig.add_annotation(
        x=1.7,
        y=0.5,
        text="← BOTTOM",
        showarrow=False,
        font=dict(size=14, color='blue')
    )
    
    fig.update_layout(
        title=title,
        xaxis=dict(visible=False, range=[0, 3]),
        yaxis=dict(visible=False, range=[-0.5, max(n + 1, 5)]),
        height=400,
        bargap=0.1,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def draw_queue(elements: list, title: str = "Queue State"):
    """Draw queue visualization using Plotly."""
    if not elements:
        st.info("Queue is empty")
        return
    
    fig = go.Figure()
    
    n = len(elements)
    colors = [f'hsl({120 + i * 15}, 70%, 50%)' for i in range(n)]
    
    for i, val in enumerate(elements):
        fig.add_trace(go.Bar(
            x=[1],
            y=[i],
            orientation='h',
            marker_color=colors[i],
            text=[str(val)],
            textposition='inside',
            textfont=dict(size=16, color='white'),
            hoverinfo='text',
            hovertext=f'Position: {i}, Value: {val}',
            showlegend=False,
            base=[i]
        ))
    
    # Create horizontal bars
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=['Queue'],
        x=[1] * n,
        orientation='h',
        marker_color=colors,
        text=[str(v) for v in elements],
        textposition='inside',
        textfont=dict(size=14, color='white'),
        showlegend=False
    ))
    
    # Simple horizontal representation
    fig = go.Figure()
    
    for i, val in enumerate(elements):
        fig.add_shape(
            type="rect",
            x0=i, y0=0, x1=i+0.9, y1=1,
            fillcolor=colors[i],
            line=dict(color='white', width=2)
        )
        fig.add_annotation(
            x=i + 0.45, y=0.5,
            text=str(val),
            showarrow=False,
            font=dict(size=16, color='white')
        )
    
    # Add FRONT and REAR labels
    fig.add_annotation(x=0.45, y=-0.3, text="FRONT", showarrow=False, font=dict(size=12, color='green'))
    fig.add_annotation(x=n-0.55, y=-0.3, text="REAR", showarrow=False, font=dict(size=12, color='red'))
    
    fig.update_layout(
        title=title,
        xaxis=dict(visible=False, range=[-0.5, max(n + 1, 6)]),
        yaxis=dict(visible=False, range=[-1, 2]),
        height=200,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def stack_page():
    """Stack visualization page."""
    st.header("🥞 Stack Visualization")
    st.markdown("A stack is a LIFO (Last In, First Out) data structure.")
    
    # Initialize session state
    if 'stack_commands' not in st.session_state:
        st.session_state.stack_commands = []
    if 'stack_history' not in st.session_state:
        st.session_state.stack_history = []
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Operations")
        
        # Push operation
        push_val = st.number_input("Value to push", value=0, step=1, key="push_val")
        if st.button("Push", key="push_btn", use_container_width=True):
            st.session_state.stack_commands.append(f"PUSH {push_val}")
        
        # Pop operation
        if st.button("Pop", key="pop_btn", use_container_width=True):
            st.session_state.stack_commands.append("POP")
        
        # Other operations
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Peek", key="peek_btn", use_container_width=True):
                st.session_state.stack_commands.append("TOP")
        with col_b:
            if st.button("Size", key="size_btn", use_container_width=True):
                st.session_state.stack_commands.append("SIZE")
        
        st.divider()
        
        # Batch input
        st.subheader("Batch Operations")
        batch_input = st.text_area(
            "Enter commands (one per line)",
            placeholder="PUSH 10\nPUSH 20\nPOP\nPUSH 30",
            height=100
        )
        
        if st.button("Execute Batch", use_container_width=True):
            commands = [cmd.strip() for cmd in batch_input.strip().split('\n') if cmd.strip()]
            st.session_state.stack_commands.extend(commands)
        
        if st.button("Clear All", use_container_width=True):
            st.session_state.stack_commands = []
            st.session_state.stack_history = []
            st.rerun()
    
    with col2:
        st.subheader("Visualization")
        
        if st.session_state.stack_commands:
            # Run the stack program
            success, stdout, stderr = run_dsa_stack(st.session_state.stack_commands)
            
            if success:
                states = parse_stack_output(stdout)
                
                if states:
                    # Show animation controls
                    step = st.slider("Step", 0, len(states) - 1, len(states) - 1, key="stack_step")
                    current_state = states[step]
                    
                    # Show current operation
                    if current_state.operation:
                        op_text = f"**{current_state.operation}**"
                        if current_state.value is not None:
                            op_text += f" value: {current_state.value}"
                        st.markdown(op_text)
                    
                    # Draw stack
                    draw_stack(current_state.elements, f"Stack (Step {step + 1}/{len(states)})")
                    
                    # Show raw output in expander
                    with st.expander("View Raw Output"):
                        st.code(stdout, language="text")
                else:
                    st.warning("No states parsed from output")
                    st.code(stdout)
            else:
                st.error(f"Execution failed: {stderr}")
                st.info("Make sure the C++ programs are compiled. Run the build commands in the README.")
        else:
            # Show empty stack
            draw_stack([], "Empty Stack")
            st.info("👆 Use the operations on the left to interact with the stack")


def queue_page():
    """Queue visualization page."""
    st.header("🚶 Queue Visualization")
    st.markdown("A queue is a FIFO (First In, First Out) data structure.")
    
    # Initialize session state
    if 'queue_commands' not in st.session_state:
        st.session_state.queue_commands = []
    if 'queue_type' not in st.session_state:
        st.session_state.queue_type = "LINEAR"
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Settings")
        queue_type = st.selectbox("Queue Type", ["LINEAR", "CIRCULAR"], key="queue_type_select")
        queue_size = st.number_input("Size (for circular)", value=5, min_value=1, max_value=20, key="queue_size")
        
        st.subheader("Operations")
        
        # Enqueue operation
        enqueue_val = st.number_input("Value to enqueue", value=0, step=1, key="enqueue_val")
        if st.button("Enqueue", key="enqueue_btn", use_container_width=True):
            st.session_state.queue_commands.append(f"ENQUEUE {enqueue_val}")
        
        # Dequeue operation
        if st.button("Dequeue", key="dequeue_btn", use_container_width=True):
            st.session_state.queue_commands.append("DEQUEUE")
        
        # Other operations
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Front", key="front_btn", use_container_width=True):
                st.session_state.queue_commands.append("FRONT")
        with col_b:
            if st.button("Size", key="qsize_btn", use_container_width=True):
                st.session_state.queue_commands.append("SIZE")
        
        st.divider()
        
        # Batch input
        st.subheader("Batch Operations")
        batch_input = st.text_area(
            "Enter commands (one per line)",
            placeholder="ENQUEUE 10\nENQUEUE 20\nDEQUEUE\nENQUEUE 30",
            height=100,
            key="queue_batch"
        )
        
        if st.button("Execute Batch", use_container_width=True, key="queue_batch_btn"):
            commands = [cmd.strip() for cmd in batch_input.strip().split('\n') if cmd.strip()]
            st.session_state.queue_commands.extend(commands)
        
        if st.button("Clear All", use_container_width=True, key="queue_clear_btn"):
            st.session_state.queue_commands = []
            st.rerun()
    
    with col2:
        st.subheader("Visualization")
        
        if st.session_state.queue_commands:
            success, stdout, stderr = run_dsa_queue(queue_type, queue_size, st.session_state.queue_commands)
            
            if success:
                states = parse_queue_output(stdout)
                
                if states:
                    step = st.slider("Step", 0, len(states) - 1, len(states) - 1, key="queue_step")
                    current_state = states[step]
                    
                    if current_state.operation:
                        op_text = f"**{current_state.operation}**"
                        if current_state.value is not None:
                            op_text += f" value: {current_state.value}"
                        st.markdown(op_text)
                    
                    draw_queue(current_state.elements, f"Queue (Step {step + 1}/{len(states)})")
                    
                    with st.expander("View Raw Output"):
                        st.code(stdout, language="text")
                else:
                    st.code(stdout)
            else:
                st.error(f"Execution failed: {stderr}")
        else:
            draw_queue([], "Empty Queue")
            st.info("👆 Use the operations on the left to interact with the queue")


def main():
    """Main function for the stack/queue page."""
    st.title("📚 Stack & Queue Visualizer")
    
    tab1, tab2 = st.tabs(["Stack", "Queue"])
    
    with tab1:
        stack_page()
    
    with tab2:
        queue_page()


if __name__ == "__main__":
    main()
