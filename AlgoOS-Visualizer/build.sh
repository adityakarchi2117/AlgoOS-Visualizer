#!/bin/bash
# Build script for AlgoOS Visualizer (Linux/macOS)
# Run this script from the AlgoOS-Visualizer directory

echo "========================================"
echo "Building AlgoOS Visualizer..."
echo "========================================"

# Create build directory
mkdir -p build

echo ""
echo "Compiling DSA modules..."
echo "----------------------------------------"

g++ -std=c++17 -o build/stack backend/dsa/stack/stack.cpp && echo "SUCCESS: stack.cpp" || echo "FAILED: stack.cpp"
g++ -std=c++17 -o build/queue backend/dsa/queue/queue.cpp && echo "SUCCESS: queue.cpp" || echo "FAILED: queue.cpp"
g++ -std=c++17 -o build/ll backend/dsa/linked-list/ll.cpp && echo "SUCCESS: ll.cpp" || echo "FAILED: ll.cpp"
g++ -std=c++17 -o build/binary_tree backend/dsa/trees/binary_tree.cpp && echo "SUCCESS: binary_tree.cpp" || echo "FAILED: binary_tree.cpp"
g++ -std=c++17 -o build/avl backend/dsa/trees/avl.cpp && echo "SUCCESS: avl.cpp" || echo "FAILED: avl.cpp"
g++ -std=c++17 -o build/heap backend/dsa/heap/heap.cpp && echo "SUCCESS: heap.cpp" || echo "FAILED: heap.cpp"
g++ -std=c++17 -o build/dijkstra backend/dsa/graphs/dijkstra.cpp && echo "SUCCESS: dijkstra.cpp" || echo "FAILED: dijkstra.cpp"
g++ -std=c++17 -o build/huffman backend/dsa/huffman/huffman.cpp && echo "SUCCESS: huffman.cpp" || echo "FAILED: huffman.cpp"

echo ""
echo "Compiling OS modules..."
echo "----------------------------------------"

g++ -std=c++17 -o build/fcfs backend/os/cpu/fcfs.cpp && echo "SUCCESS: fcfs.cpp" || echo "FAILED: fcfs.cpp"
g++ -std=c++17 -o build/sjf backend/os/cpu/sjf.cpp && echo "SUCCESS: sjf.cpp" || echo "FAILED: sjf.cpp"
g++ -std=c++17 -o build/round_robin backend/os/cpu/round_robin.cpp && echo "SUCCESS: round_robin.cpp" || echo "FAILED: round_robin.cpp"
g++ -std=c++17 -o build/fifo backend/os/memory/fifo.cpp && echo "SUCCESS: fifo.cpp" || echo "FAILED: fifo.cpp"
g++ -std=c++17 -o build/lru backend/os/memory/lru.cpp && echo "SUCCESS: lru.cpp" || echo "FAILED: lru.cpp"
g++ -std=c++17 -o build/optimal backend/os/memory/optimal.cpp && echo "SUCCESS: optimal.cpp" || echo "FAILED: optimal.cpp"
g++ -std=c++17 -o build/scan backend/os/disk/scan.cpp && echo "SUCCESS: scan.cpp" || echo "FAILED: scan.cpp"
g++ -std=c++17 -o build/bankers backend/os/deadlock/bankers.cpp && echo "SUCCESS: bankers.cpp" || echo "FAILED: bankers.cpp"

echo ""
echo "========================================"
echo "Build complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  cd frontend"
echo "  streamlit run app.py"
