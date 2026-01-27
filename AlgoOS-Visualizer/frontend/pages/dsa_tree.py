# File: frontend/pages/dsa_tree.py
"""
Tree Visualization Page - BST, AVL, Heap, and Graph algorithms
"""

import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.runner import (
    run_dsa_bst, run_dsa_avl, run_dsa_heap, 
    run_dsa_dijkstra, run_dsa_huffman
)
from utils.parser import parse_dijkstra_output, parse_huffman_output, parse_tree_output, parse_heap_output


def parse_tree_state(state_str: str):
    """Parse tree state from format: TREE:10(5,15),5(3,7),15(_,_)"""
    if not state_str.startswith('TREE:'):
        return []
    
    tree_str = state_str[5:]
    if tree_str == 'EMPTY':
        return []
    
    nodes = []
    node_matches = re.findall(r'(\d+)\(([^,]+),([^)]+)\)', tree_str)
    for val, left, right in node_matches:
        node = {
            'value': int(val),
            'left': None if left == '_' else int(left),
            'right': None if right == '_' else int(right)
        }
        nodes.append(node)
    return nodes


def draw_bst_tree(nodes: list, title: str = "Binary Search Tree", highlight_node: int = None, balance_factors: dict = None):
    """Draw BST/AVL tree from node list."""
    if not nodes:
        st.info("Tree is empty")
        return
    
    fig = go.Figure()
    
    # Build adjacency for tree structure
    children = {}
    for node in nodes:
        children[node['value']] = (node['left'], node['right'])
    
    # Find root (node that is not a child of anyone)
    all_values = set(n['value'] for n in nodes)
    all_children = set()
    for node in nodes:
        if node['left'] is not None:
            all_children.add(node['left'])
        if node['right'] is not None:
            all_children.add(node['right'])
    root_candidates = all_values - all_children
    root = nodes[0]['value'] if not root_candidates else list(root_candidates)[0]
    
    # Calculate positions using BFS
    positions = {}
    
    def calc_positions(val, x, y, dx):
        if val is None or val not in children:
            return
        positions[val] = (x, y)
        left, right = children.get(val, (None, None))
        if left is not None:
            calc_positions(left, x - dx, y - 1, dx / 2)
        if right is not None:
            calc_positions(right, x + dx, y - 1, dx / 2)
    
    calc_positions(root, 0, 0, 2)
    
    # Draw edges
    edge_x = []
    edge_y = []
    for val, (left, right) in children.items():
        if val not in positions:
            continue
        if left is not None and left in positions:
            edge_x.extend([positions[val][0], positions[left][0], None])
            edge_y.extend([positions[val][1], positions[left][1], None])
        if right is not None and right in positions:
            edge_x.extend([positions[val][0], positions[right][0], None])
            edge_y.extend([positions[val][1], positions[right][1], None])
    
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(color='gray', width=2),
        hoverinfo='none'
    ))
    
    # Draw nodes
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    hover_text = []
    
    for val in positions:
        node_x.append(positions[val][0])
        node_y.append(positions[val][1])
        
        # Add balance factor if available
        if balance_factors and val in balance_factors:
            node_text.append(f"{val}\n({balance_factors[val]:+d})")
        else:
            node_text.append(str(val))
        
        # Highlight node color
        if val == root:
            node_colors.append('green')
        elif highlight_node is not None and val == highlight_node:
            node_colors.append('orange')
        else:
            node_colors.append('lightblue')
        
        hover_text.append(f'Value: {val}')
    
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(size=45, color=node_colors, line=dict(color='black', width=2)),
        text=node_text,
        textposition='middle center',
        textfont=dict(size=12, color='white'),
        hoverinfo='text',
        hovertext=hover_text
    ))
    
    fig.update_layout(
        title=title,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=450,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def draw_heap_tree(elements: list, is_max_heap: bool = True):
    """Draw heap as a tree structure."""
    if not elements:
        st.info("Heap is empty")
        return
    
    fig = go.Figure()
    
    n = len(elements)
    # Calculate positions for a binary tree
    positions = {}
    
    def calc_positions(idx, x, y, dx):
        if idx >= n:
            return
        positions[idx] = (x, y)
        calc_positions(2 * idx + 1, x - dx, y - 1, dx / 2)  # Left child
        calc_positions(2 * idx + 2, x + dx, y - 1, dx / 2)  # Right child
    
    calc_positions(0, 0, 0, 2)
    
    # Draw edges first
    edge_x = []
    edge_y = []
    for idx in range(n):
        if idx in positions:
            left = 2 * idx + 1
            right = 2 * idx + 2
            if left < n and left in positions:
                edge_x.extend([positions[idx][0], positions[left][0], None])
                edge_y.extend([positions[idx][1], positions[left][1], None])
            if right < n and right in positions:
                edge_x.extend([positions[idx][0], positions[right][0], None])
                edge_y.extend([positions[idx][1], positions[right][1], None])
    
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(color='gray', width=2),
        hoverinfo='none'
    ))
    
    # Draw nodes
    node_x = [positions[i][0] for i in range(n) if i in positions]
    node_y = [positions[i][1] for i in range(n) if i in positions]
    node_text = [str(elements[i]) for i in range(n) if i in positions]
    
    colors = ['red' if i == 0 else 'lightblue' for i in range(n)]
    
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(size=40, color=colors[:len(node_x)], line=dict(color='black', width=2)),
        text=node_text,
        textposition='middle center',
        textfont=dict(size=14, color='white'),
        hoverinfo='text',
        hovertext=[f'Index: {i}, Value: {elements[i]}' for i in range(n)]
    ))
    
    title = f"{'Max' if is_max_heap else 'Min'} Heap (Root highlighted in red)"
    fig.update_layout(
        title=title,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def draw_graph(num_vertices: int, edges: list, distances = None, source: int = 0):
    """Draw a graph using networkx and plotly."""
    G = nx.Graph()
    
    for i in range(num_vertices):
        G.add_node(i)
    
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    
    pos = nx.spring_layout(G, seed=42)
    
    fig = go.Figure()
    
    # Draw edges
    for u, v, w in edges:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode='lines',
            line=dict(color='gray', width=2),
            hoverinfo='none'
        ))
        # Edge weight label
        fig.add_annotation(
            x=(x0 + x1) / 2,
            y=(y0 + y1) / 2,
            text=str(w),
            showarrow=False,
            font=dict(size=10, color='red'),
            bgcolor='white'
        )
    
    # Draw nodes
    node_x = [pos[i][0] for i in range(num_vertices)]
    node_y = [pos[i][1] for i in range(num_vertices)]
    
    # Convert list distances to dict if needed
    dist_dict = {}
    if distances:
        if isinstance(distances, list):
            for i, d in enumerate(distances):
                dist_dict[i] = d
        else:
            dist_dict = distances
    
    # Color nodes based on distance
    if dist_dict:
        colors = []
        for i in range(num_vertices):
            if i == source:
                colors.append('green')
            elif i in dist_dict and dist_dict[i] != float('inf'):
                colors.append('lightblue')
            else:
                colors.append('lightgray')
    else:
        colors = ['lightblue'] * num_vertices
    
    labels = []
    for i in range(num_vertices):
        label = str(i)
        if dist_dict and i in dist_dict:
            dist = dist_dict[i]
            label += f"\n(d={dist if dist != float('inf') else '∞'})"
        labels.append(label)
    
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(size=40, color=colors, line=dict(color='black', width=2)),
        text=labels,
        textposition='middle center',
        textfont=dict(size=12),
        hoverinfo='text',
        hovertext=[f'Vertex {i}' for i in range(num_vertices)]
    ))
    
    fig.update_layout(
        title="Graph Visualization",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def draw_huffman_tree(tree_str: str, title: str = "Huffman Tree"):
    """Draw Huffman tree from tree string format: id:char:freq(left,right),..."""
    if not tree_str or tree_str == 'EMPTY':
        st.info("Tree is empty")
        return
    
    # Parse nodes from format: 14:*:11(12,13),12:*:4(9,10),...
    nodes = {}  # id -> {char, freq, left, right}
    node_pattern = re.compile(r'(\d+):([^:]+):(\d+)\(([^,]*),([^)]*)\)')
    
    for match in node_pattern.finditer(tree_str):
        node_id = int(match.group(1))
        char = match.group(2)
        freq = int(match.group(3))
        left = match.group(4)
        right = match.group(5)
        
        nodes[node_id] = {
            'char': char if char != '*' else '●',
            'freq': freq,
            'left': int(left) if left != '_' and left.isdigit() else None,
            'right': int(right) if right != '_' and right.isdigit() else None,
            'is_leaf': char != '*'
        }
    
    if not nodes:
        st.warning("Could not parse tree structure")
        return
    
    # Find root (node with highest freq or the one not referenced as child)
    all_children = set()
    for node in nodes.values():
        if node['left'] is not None:
            all_children.add(node['left'])
        if node['right'] is not None:
            all_children.add(node['right'])
    
    root_candidates = [nid for nid in nodes if nid not in all_children]
    root = root_candidates[0] if root_candidates else max(nodes.keys())
    
    # Calculate positions using BFS
    positions = {}
    
    def calc_positions(node_id, x, y, dx):
        if node_id is None or node_id not in nodes:
            return
        positions[node_id] = (x, y)
        node = nodes[node_id]
        if node['left'] is not None:
            calc_positions(node['left'], x - dx, y - 1, dx / 2)
        if node['right'] is not None:
            calc_positions(node['right'], x + dx, y - 1, dx / 2)
    
    calc_positions(root, 0, 0, 3)
    
    fig = go.Figure()
    
    # Draw edges with 0/1 labels
    for node_id, node in nodes.items():
        if node_id not in positions:
            continue
        px, py = positions[node_id]
        
        # Left child (0)
        if node['left'] is not None and node['left'] in positions:
            cx, cy = positions[node['left']]
            fig.add_trace(go.Scatter(
                x=[px, cx], y=[py, cy],
                mode='lines',
                line=dict(color='green', width=2),
                hoverinfo='none',
                showlegend=False
            ))
            # Add '0' label
            fig.add_annotation(
                x=(px + cx) / 2 - 0.1, y=(py + cy) / 2,
                text="0", showarrow=False,
                font=dict(size=12, color='green', weight='bold'),
                bgcolor='white'
            )
        
        # Right child (1)
        if node['right'] is not None and node['right'] in positions:
            cx, cy = positions[node['right']]
            fig.add_trace(go.Scatter(
                x=[px, cx], y=[py, cy],
                mode='lines',
                line=dict(color='blue', width=2),
                hoverinfo='none',
                showlegend=False
            ))
            # Add '1' label
            fig.add_annotation(
                x=(px + cx) / 2 + 0.1, y=(py + cy) / 2,
                text="1", showarrow=False,
                font=dict(size=12, color='blue', weight='bold'),
                bgcolor='white'
            )
    
    # Draw nodes
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    hover_text = []
    
    for node_id in positions:
        node = nodes[node_id]
        px, py = positions[node_id]
        node_x.append(px)
        node_y.append(py)
        
        # Show char:freq for leaves, just freq for internal
        if node['is_leaf']:
            display_char = node['char'] if node['char'] != ' ' else '␣'
            node_text.append(f"{display_char}\n{node['freq']}")
            node_colors.append('lightgreen')
        else:
            node_text.append(f"{node['freq']}")
            node_colors.append('lightblue')
        
        hover_text.append(f"Char: {node['char']}, Freq: {node['freq']}")
    
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(size=45, color=node_colors, line=dict(color='black', width=2)),
        text=node_text,
        textposition='middle center',
        textfont=dict(size=11, color='black'),
        hoverinfo='text',
        hovertext=hover_text,
        showlegend=False
    ))
    
    fig.update_layout(
        title=title,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def bst_page():
    """Binary Search Tree visualization."""
    st.subheader("🌳 Binary Search Tree")
    
    if 'bst_commands' not in st.session_state:
        st.session_state.bst_commands = []
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Insert Values**")
        values = st.text_input("Values (space-separated)", value="50 30 70 20 40 60 80", key="bst_values")
        if st.button("Insert All", use_container_width=True):
            # Split values and create individual insert commands
            st.session_state.bst_commands = []
            for v in values.strip().split():
                if v.lstrip('-').isdigit():
                    st.session_state.bst_commands.append(f"INSERT {v}")
        
        st.markdown("**Single Operations**")
        val = st.number_input("Value", value=0, step=1, key="bst_val")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Insert", use_container_width=True, key="bst_insert"):
                st.session_state.bst_commands.append(f"INSERT {val}")
        with col_b:
            if st.button("Delete", use_container_width=True, key="bst_delete"):
                st.session_state.bst_commands.append(f"DELETE {val}")
        
        if st.button("Search", use_container_width=True, key="bst_search"):
            st.session_state.bst_commands.append(f"SEARCH {val}")
        
        st.markdown("**Traversals**")
        col_c, col_d = st.columns(2)
        with col_c:
            if st.button("Inorder", use_container_width=True):
                st.session_state.bst_commands.append("INORDER")
            if st.button("Preorder", use_container_width=True):
                st.session_state.bst_commands.append("PREORDER")
        with col_d:
            if st.button("Postorder", use_container_width=True):
                st.session_state.bst_commands.append("POSTORDER")
            if st.button("Level Order", use_container_width=True):
                st.session_state.bst_commands.append("LEVELORDER")
        
        if st.button("Clear", use_container_width=True):
            st.session_state.bst_commands = []
            st.rerun()
    
    with col2:
        if st.session_state.bst_commands:
            success, stdout, stderr = run_dsa_bst(st.session_state.bst_commands)
            
            if success:
                # Parse tree states from output
                states = parse_tree_output(stdout)
                
                if states:
                    # Animation slider
                    step = st.slider("Step", 1, len(states), len(states), key="bst_step")
                    current_state = states[step - 1]
                    
                    # Show current operation
                    st.markdown(f"**Operation:** `{current_state['operation']}`")
                    
                    # Check for traversal result in meta field
                    if current_state.get('meta'):
                        meta = current_state['meta']
                        if 'TRAVERSAL=' in meta:
                            match = re.search(r'TRAVERSAL=\[([^\]]*)\]', meta)
                            if match:
                                traversal = match.group(1)
                                if traversal:
                                    st.success(f"**Traversal Result:** `{traversal}`")
                    
                    # Draw tree
                    if current_state['tree_nodes']:
                        # Extract highlight node from meta
                        highlight = None
                        if current_state.get('meta'):
                            for kv in current_state['meta'].split(','):
                                if kv.startswith('CUR=') or kv.startswith('PATH='):
                                    v = kv.split('=')[1].split('->')[-1]
                                    if v.lstrip('-').isdigit():
                                        highlight = int(v)
                        
                        draw_bst_tree(
                            current_state['tree_nodes'], 
                            f"BST (Step {step}/{len(states)})",
                            highlight_node=highlight
                        )
                    else:
                        st.info("Tree is empty")
                    
                    with st.expander("View Raw Output"):
                        st.code(stdout, language="text")
                else:
                    st.code(stdout, language="text")
            else:
                st.error(f"Error: {stderr}")
        else:
            st.info("Enter values and click Insert to build a BST")


def avl_page():
    """AVL Tree visualization."""
    st.subheader("⚖️ AVL Tree (Self-Balancing)")
    
    if 'avl_commands' not in st.session_state:
        st.session_state.avl_commands = []
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Insert Values**")
        values = st.text_input("Values (space-separated)", value="10 20 30 40 50 25", key="avl_values")
        if st.button("Insert All", use_container_width=True, key="avl_insert_all"):
            # Split values and create individual insert commands
            st.session_state.avl_commands = []
            for v in values.strip().split():
                if v.lstrip('-').isdigit():
                    st.session_state.avl_commands.append(f"INSERT {v}")
        
        val = st.number_input("Single Value", value=0, step=1, key="avl_val")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Insert", use_container_width=True, key="avl_insert"):
                st.session_state.avl_commands.append(f"INSERT {val}")
        with col_b:
            if st.button("Delete", use_container_width=True, key="avl_delete"):
                st.session_state.avl_commands.append(f"DELETE {val}")
        
        if st.button("Clear", use_container_width=True, key="avl_clear"):
            st.session_state.avl_commands = []
            st.rerun()
    
    with col2:
        if st.session_state.avl_commands:
            success, stdout, stderr = run_dsa_avl(st.session_state.avl_commands)
            
            if success:
                st.markdown("**Watch the rotations as the tree self-balances!**")
                
                # Parse tree states from output
                states = parse_tree_output(stdout)
                
                if states:
                    # Animation slider
                    step = st.slider("Step", 1, len(states), len(states), key="avl_step")
                    current_state = states[step - 1]
                    
                    # Show current operation
                    st.markdown(f"**Operation:** `{current_state['operation']}`")
                    
                    # Draw tree
                    if current_state['tree_nodes']:
                        # Extract highlight and balance factors
                        highlight = None
                        balance_factors = {}
                        if current_state.get('meta'):
                            for kv in current_state['meta'].split(','):
                                if kv.startswith('CUR='):
                                    v = kv.split('=')[1].split('->')[-1]
                                    if v.lstrip('-').isdigit():
                                        highlight = int(v)
                                # Parse balance factors like BF=30:1,20:-1
                                if kv.startswith('BF='):
                                    bf_str = kv.split('=')[1]
                                    for item in bf_str.split(';'):
                                        if ':' in item:
                                            node_val, bf = item.split(':')
                                            if node_val.lstrip('-').isdigit() and bf.lstrip('-').isdigit():
                                                balance_factors[int(node_val)] = int(bf)
                        
                        draw_bst_tree(
                            current_state['tree_nodes'], 
                            f"AVL Tree (Step {step}/{len(states)})",
                            highlight_node=highlight,
                            balance_factors=balance_factors
                        )
                    else:
                        st.info("Tree is empty")
                    
                    with st.expander("View Raw Output"):
                        st.code(stdout, language="text")
                else:
                    st.code(stdout, language="text")
            else:
                st.error(f"Error: {stderr}")
        else:
            st.info("Insert values to see AVL tree rotations")


def heap_page():
    """Heap visualization."""
    st.subheader("🏔️ Heap (Priority Queue)")
    
    if 'heap_commands' not in st.session_state:
        st.session_state.heap_commands = []
    if 'heap_type' not in st.session_state:
        st.session_state.heap_type = "MAX"
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        heap_type = st.selectbox("Heap Type", ["MAX", "MIN"], key="heap_type_select")
        
        st.markdown("**Insert Values**")
        values = st.text_input("Values (space-separated)", value="10 20 15 30 40", key="heap_values")
        if st.button("Build Heap", use_container_width=True):
            st.session_state.heap_commands = [f"BUILD {values}"]
            st.session_state.heap_type = heap_type
        
        val = st.number_input("Value", value=0, step=1, key="heap_val")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Insert", use_container_width=True, key="heap_insert"):
                st.session_state.heap_commands.append(f"INSERT {val}")
        with col_b:
            if st.button("Extract", use_container_width=True, key="heap_extract"):
                st.session_state.heap_commands.append("EXTRACT")
        
        if st.button("Heap Sort", use_container_width=True):
            st.session_state.heap_commands.append("SORT")
        
        if st.button("Clear", use_container_width=True, key="heap_clear"):
            st.session_state.heap_commands = []
            st.rerun()
    
    with col2:
        if st.session_state.heap_commands:
            success, stdout, stderr = run_dsa_heap(st.session_state.heap_type, st.session_state.heap_commands)
            
            if success:
                # Check for sorted result in output
                sorted_result = None
                if 'SORTED=[' in stdout:
                    match = re.search(r'SORTED=\[([^\]]*)\]', stdout)
                    if match:
                        sorted_result = match.group(1)
                
                # Display sorted result prominently if heap sort was performed
                if sorted_result:
                    st.success(f"**🎯 Heap Sort Result:** `{sorted_result}`")
                
                # Extract all heap states for step-by-step visualization
                lines = stdout.split('\n')
                heap_states = []
                current_heap = []
                current_op = "INIT"
                sorted_so_far = []
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('ARRAY:'):
                        parts = line.replace('ARRAY:', '').strip().split()
                        current_heap = [int(x) for x in parts if x.lstrip('-').isdigit()]
                        heap_states.append({
                            'heap': current_heap.copy(),
                            'operation': current_op,
                            'sorted': sorted_so_far.copy()
                        })
                    elif line.startswith('BUILD_HEAP:'):
                        current_op = "BUILD HEAP"
                    elif line.startswith('HEAPIFY:'):
                        current_op = line.replace('HEAPIFY:', '').strip()
                    elif line.startswith('SWAP:'):
                        current_op = line
                    elif line.startswith('INSERT:'):
                        current_op = line
                    elif line.startswith('EXTRACT:'):
                        current_op = line
                    elif line.startswith('SORTED_SO_FAR:'):
                        parts = line.replace('SORTED_SO_FAR:', '').strip().split()
                        sorted_so_far = [int(x) for x in parts if x.lstrip('-').isdigit()]
                    elif line.startswith('HEAP_SORT:'):
                        current_op = "HEAP SORT - Starting"
                
                if heap_states:
                    # Animation slider (only show if more than 1 step)
                    if len(heap_states) > 1:
                        step = st.slider("Step", 1, len(heap_states), len(heap_states), key="heap_step")
                    else:
                        step = 1
                    current_state = heap_states[step - 1]
                    
                    # Show current operation
                    st.markdown(f"**Operation:** `{current_state['operation']}`")
                    
                    # Show sorted elements so far during heap sort
                    if current_state['sorted']:
                        st.info(f"**Sorted so far:** `{current_state['sorted']}`")
                    
                    # Draw heap tree
                    if current_state['heap']:
                        draw_heap_tree(current_state['heap'], st.session_state.heap_type == "MAX")
                        st.markdown(f"**Array:** `{current_state['heap']}`")
                    else:
                        st.info("Heap is empty")
                else:
                    # Fallback - just show last heap state
                    for line in reversed(lines):
                        if line.startswith('ARRAY:'):
                            parts = line.replace('ARRAY:', '').strip().split()
                            current_heap = [int(x) for x in parts if x.lstrip('-').isdigit()]
                            break
                    
                    if current_heap:
                        draw_heap_tree(current_heap, st.session_state.heap_type == "MAX")
                
                with st.expander("View Output"):
                    st.code(stdout, language="text")
            else:
                st.error(f"Error: {stderr}")
        else:
            st.info("Enter values and click Build Heap")


def dijkstra_page():
    """Dijkstra's algorithm visualization."""
    st.subheader("🗺️ Dijkstra's Shortest Path")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        num_vertices = st.number_input("Number of Vertices", value=5, min_value=2, max_value=10, key="dj_vertices")
        
        st.markdown("**Add Edges**")
        edge_input = st.text_area(
            "Edges (from to weight, one per line)",
            value="0 1 4\n0 2 1\n1 3 1\n2 1 2\n2 3 5\n3 4 3",
            height=150,
            key="dj_edges"
        )
        
        source = st.number_input("Source Vertex", value=0, min_value=0, max_value=num_vertices-1, key="dj_source")
        
        run_dijkstra = st.button("Run Dijkstra", use_container_width=True)
    
    with col2:
        if run_dijkstra:
            # Parse edges
            edges = []
            for line in edge_input.strip().split('\n'):
                parts = line.strip().split()
                if len(parts) == 3:
                    u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
                    edges.append((u, v, w))
            
            success, stdout, stderr = run_dsa_dijkstra(num_vertices, edges, source)
            
            if success:
                result = parse_dijkstra_output(stdout)
                
                # Draw graph with distances
                draw_graph(num_vertices, edges, result['distances'], source)
                
                # Show results table
                st.markdown("**Shortest Distances from Source:**")
                dist_data = []
                distances = result['distances']
                if isinstance(distances, list):
                    for v, d in enumerate(distances):
                        dist_data.append({
                            "Vertex": v,
                            "Distance": d if d != float('inf') else "∞"
                        })
                else:
                    for v, d in distances.items():
                        dist_data.append({
                            "Vertex": v,
                            "Distance": d if d != float('inf') else "∞"
                        })
                st.dataframe(dist_data, use_container_width=True)
                
                with st.expander("View Steps"):
                    st.code(stdout, language="text")
            else:
                st.error(f"Error: {stderr}")
        else:
            st.info("Configure the graph and click Run Dijkstra")


def huffman_page():
    """Huffman coding visualization."""
    st.subheader("🗜️ Huffman Coding")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        text = st.text_input("Text to encode", value="hello world", key="huffman_text")
        run_huffman = st.button("Build Huffman Tree", use_container_width=True)
    
    with col2:
        if run_huffman and text:
            success, stdout, stderr = run_dsa_huffman(text)
            
            if success:
                result = parse_huffman_output(stdout)
                
                # Parse tree states for step-by-step visualization
                tree_states = []
                lines = stdout.split('\n')
                for line in lines:
                    line = line.strip()
                    if ' | ' not in line:
                        continue
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 4:
                        operation = parts[1].strip()
                        state = parts[3].strip()
                        
                        # Extract tree from TREE_STATE or BUILD_COMPLETE
                        if state.startswith('TREE:'):
                            tree_str = state[5:]
                            tree_states.append({
                                'operation': operation,
                                'tree': tree_str
                            })
                
                # Show step-by-step tree building
                if tree_states:
                    st.markdown("### 🌳 Tree Building Animation")
                    if len(tree_states) > 1:
                        step = st.slider("Build Step", 1, len(tree_states), len(tree_states), key="huffman_step")
                    else:
                        step = 1
                    current = tree_states[step - 1]
                    
                    st.markdown(f"**Step {step}/{len(tree_states)}:** `{current['operation']}`")
                    draw_huffman_tree(current['tree'], f"Huffman Tree (Step {step})")
                
                # Show frequencies and codes in columns
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("**Character Frequencies:**")
                    freq_data = [{"Char": k if k != ' ' else '␣', "Freq": v} for k, v in result['frequencies'].items()]
                    st.dataframe(freq_data, use_container_width=True, height=200)
                
                with col_b:
                    st.markdown("**Huffman Codes:**")
                    code_data = [{"Char": k if k != ' ' else '␣', "Code": v, "Bits": len(v)} for k, v in result['codes'].items()]
                    st.dataframe(code_data, use_container_width=True, height=200)
                
                # Show encoded result
                if result['encoded']:
                    st.success(f"**✨ Encoded:** `{result['encoded']}`")
                    original_bits = len(text) * 8
                    compressed_bits = len(result['encoded'])
                    savings = ((original_bits - compressed_bits) / original_bits) * 100
                    st.info(f"**Original:** {original_bits} bits → **Compressed:** {compressed_bits} bits | **Savings:** {savings:.1f}%")
                
                with st.expander("View Raw Output"):
                    st.code(stdout, language="text")
            else:
                st.error(f"Error: {stderr}")
        else:
            st.info("Enter text and click Build Huffman Tree")


def main():
    """Main function for tree/graph visualizations."""
    st.title("🌲 Trees & Graphs Visualizer")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "BST", "AVL Tree", "Heap", "Dijkstra", "Huffman"
    ])
    
    with tab1:
        bst_page()
    
    with tab2:
        avl_page()
    
    with tab3:
        heap_page()
    
    with tab4:
        dijkstra_page()
    
    with tab5:
        huffman_page()


if __name__ == "__main__":
    main()
