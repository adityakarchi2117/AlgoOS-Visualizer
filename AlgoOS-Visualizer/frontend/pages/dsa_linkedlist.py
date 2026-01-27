# File: frontend/pages/dsa_linkedlist.py
"""
Linked List Visualization Page
"""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.runner import run_dsa_linkedlist
from utils.parser import parse_linkedlist_output


def draw_linked_list(nodes: list, title: str = "Linked List"):
    """Draw linked list visualization using Plotly."""
    fig = go.Figure()
    
    if not nodes:
        fig.add_annotation(
            x=0.5, y=0.5,
            text="Empty List (HEAD → NULL)",
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            title=title,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=150
        )
        st.plotly_chart(fig, use_container_width=True)
        return
    
    n = len(nodes)
    node_width = 0.8
    arrow_width = 0.4
    total_width = n * (node_width + arrow_width)
    
    colors = [f'hsl({280 + i * 20}, 70%, 50%)' for i in range(n)]
    
    # Draw HEAD label
    fig.add_annotation(
        x=-0.5, y=0.5,
        text="HEAD →",
        showarrow=False,
        font=dict(size=12, color='green')
    )
    
    for i, node in enumerate(nodes):
        x_pos = i * (node_width + arrow_width)
        
        # Draw node box
        fig.add_shape(
            type="rect",
            x0=x_pos, y0=0, x1=x_pos + node_width, y1=1,
            fillcolor=colors[i],
            line=dict(color='white', width=2)
        )
        
        # Add value text
        fig.add_annotation(
            x=x_pos + node_width/2, y=0.5,
            text=str(node.data),
            showarrow=False,
            font=dict(size=16, color='white')
        )
        
        # Add index label
        fig.add_annotation(
            x=x_pos + node_width/2, y=-0.3,
            text=f"[{i}]",
            showarrow=False,
            font=dict(size=10, color='gray')
        )
        
        # Draw arrow to next node
        if i < n - 1:
            fig.add_annotation(
                x=x_pos + node_width + arrow_width/2,
                y=0.5,
                text="→",
                showarrow=False,
                font=dict(size=20, color='black')
            )
    
    # Draw NULL at the end
    fig.add_annotation(
        x=total_width, y=0.5,
        text="→ NULL",
        showarrow=False,
        font=dict(size=12, color='red')
    )
    
    fig.update_layout(
        title=title,
        xaxis=dict(visible=False, range=[-1, total_width + 1]),
        yaxis=dict(visible=False, range=[-1, 2]),
        height=200,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def main():
    """Main function for the linked list page."""
    st.title("🔗 Linked List Visualizer")
    st.markdown("A linked list is a linear data structure where elements are stored in nodes connected by pointers.")
    
    # Initialize session state
    if 'll_commands' not in st.session_state:
        st.session_state.ll_commands = []
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Operations")
        
        # Insert operations
        st.markdown("**Insert Operations**")
        
        insert_val = st.number_input("Value", value=0, step=1, key="ll_insert_val")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Insert Front", use_container_width=True):
                st.session_state.ll_commands.append(f"INSERT_FRONT {insert_val}")
        with col_b:
            if st.button("Insert End", use_container_width=True):
                st.session_state.ll_commands.append(f"INSERT_END {insert_val}")
        
        insert_pos = st.number_input("Position", value=0, min_value=0, step=1, key="ll_insert_pos")
        if st.button("Insert at Position", use_container_width=True):
            st.session_state.ll_commands.append(f"INSERT_AT {insert_pos} {insert_val}")
        
        st.divider()
        
        # Delete operations
        st.markdown("**Delete Operations**")
        
        col_c, col_d = st.columns(2)
        with col_c:
            if st.button("Delete Front", use_container_width=True):
                st.session_state.ll_commands.append("DELETE_FRONT")
        with col_d:
            if st.button("Delete End", use_container_width=True):
                st.session_state.ll_commands.append("DELETE_END")
        
        delete_pos = st.number_input("Position to delete", value=0, min_value=0, step=1, key="ll_del_pos")
        if st.button("Delete at Position", use_container_width=True):
            st.session_state.ll_commands.append(f"DELETE_AT {delete_pos}")
        
        delete_val = st.number_input("Value to delete", value=0, step=1, key="ll_del_val")
        if st.button("Delete by Value", use_container_width=True):
            st.session_state.ll_commands.append(f"DELETE_VALUE {delete_val}")
        
        st.divider()
        
        # Other operations
        st.markdown("**Other Operations**")
        
        search_val = st.number_input("Value to search", value=0, step=1, key="ll_search_val")
        if st.button("Search", use_container_width=True):
            st.session_state.ll_commands.append(f"SEARCH {search_val}")
        
        if st.button("Reverse List", use_container_width=True):
            st.session_state.ll_commands.append("REVERSE")
        
        if st.button("Show Details", use_container_width=True):
            st.session_state.ll_commands.append("DETAILED")
        
        st.divider()
        
        # Batch input
        st.subheader("Batch Operations")
        batch_input = st.text_area(
            "Enter commands (one per line)",
            placeholder="INSERT_END 10\nINSERT_END 20\nINSERT_END 30\nREVERSE",
            height=100,
            key="ll_batch"
        )
        
        if st.button("Execute Batch", use_container_width=True, key="ll_batch_btn"):
            commands = [cmd.strip() for cmd in batch_input.strip().split('\n') if cmd.strip()]
            st.session_state.ll_commands.extend(commands)
        
        if st.button("Clear All", use_container_width=True, key="ll_clear_btn"):
            st.session_state.ll_commands = []
            st.rerun()
    
    with col2:
        st.subheader("Visualization")
        
        if st.session_state.ll_commands:
            success, stdout, stderr = run_dsa_linkedlist(st.session_state.ll_commands)
            
            if success:
                states = parse_linkedlist_output(stdout)
                
                if states:
                    if len(states) > 1:
                        step = st.slider("Step", 0, len(states) - 1, len(states) - 1, key="ll_step")
                    else:
                        step = 0
                    current_state = states[step]
                    
                    # Show operation info
                    if current_state.operation:
                        st.markdown(f"**Operation:** {current_state.operation}")
                    st.markdown(f"**Size:** {current_state.size}")
                    
                    # Draw linked list
                    draw_linked_list(current_state.nodes, f"Linked List (Step {step + 1}/{len(states)})")
                    
                    # Show node details
                    if current_state.nodes:
                        st.markdown("**Node Details:**")
                        node_data = []
                        for node in current_state.nodes:
                            node_data.append({
                                "Position": node.position,
                                "Data": node.data,
                                "Next": f"Node[{node.position + 1}]" if node.position < len(current_state.nodes) - 1 else "NULL"
                            })
                        st.dataframe(node_data, use_container_width=True)
                    
                    with st.expander("View Raw Output"):
                        st.code(stdout, language="text")
                else:
                    st.code(stdout)
            else:
                st.error(f"Execution failed: {stderr}")
        else:
            draw_linked_list([], "Empty Linked List")
            st.info("👆 Use the operations on the left to interact with the linked list")
    
    # Show command history
    if st.session_state.ll_commands:
        with st.expander("Command History"):
            for i, cmd in enumerate(st.session_state.ll_commands):
                st.text(f"{i + 1}. {cmd}")


if __name__ == "__main__":
    main()
