@echo off
REM Build script for AlgoOS Visualizer (Windows)
REM Run this script from the AlgoOS-Visualizer directory

echo ========================================
echo Building AlgoOS Visualizer...
echo ========================================

REM Create build directory
if not exist "build" mkdir build

echo.
echo Compiling DSA modules...
echo ----------------------------------------

g++ -std=gnu++17 -o build/stack.exe backend/dsa/stack/stack.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: stack.cpp) else (echo SUCCESS: stack.cpp)

g++ -std=gnu++17 -o build/queue.exe backend/dsa/queue/queue.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: queue.cpp) else (echo SUCCESS: queue.cpp)

g++ -std=gnu++17 -o build/ll.exe backend/dsa/linked-list/ll.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: ll.cpp) else (echo SUCCESS: ll.cpp)

g++ -std=gnu++17 -o build/binary_tree.exe backend/dsa/trees/binary_tree.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: binary_tree.cpp) else (echo SUCCESS: binary_tree.cpp)

g++ -std=gnu++17 -o build/avl.exe backend/dsa/trees/avl.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: avl.cpp) else (echo SUCCESS: avl.cpp)

g++ -std=gnu++17 -o build/heap.exe backend/dsa/heap/heap.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: heap.cpp) else (echo SUCCESS: heap.cpp)

g++ -std=gnu++17 -o build/dijkstra.exe backend/dsa/graphs/dijkstra.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: dijkstra.cpp) else (echo SUCCESS: dijkstra.cpp)

g++ -std=gnu++17 -o build/huffman.exe backend/dsa/huffman/huffman.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: huffman.cpp) else (echo SUCCESS: huffman.cpp)

echo.
echo Compiling OS modules...
echo ----------------------------------------

g++ -std=gnu++17 -o build/fcfs.exe backend/os/cpu/fcfs.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: fcfs.cpp) else (echo SUCCESS: fcfs.cpp)

g++ -std=gnu++17 -o build/sjf.exe backend/os/cpu/sjf.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: sjf.cpp) else (echo SUCCESS: sjf.cpp)

g++ -std=gnu++17 -o build/round_robin.exe backend/os/cpu/round_robin.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: round_robin.cpp) else (echo SUCCESS: round_robin.cpp)

g++ -std=gnu++17 -o build/fifo.exe backend/os/memory/fifo.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: fifo.cpp) else (echo SUCCESS: fifo.cpp)

g++ -std=gnu++17 -o build/lru.exe backend/os/memory/lru.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: lru.cpp) else (echo SUCCESS: lru.cpp)

g++ -std=gnu++17 -o build/optimal.exe backend/os/memory/optimal.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: optimal.cpp) else (echo SUCCESS: optimal.cpp)

g++ -std=gnu++17 -o build/scan.exe backend/os/disk/scan.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: scan.cpp) else (echo SUCCESS: scan.cpp)

g++ -std=gnu++17 -o build/bankers.exe backend/os/deadlock/bankers.cpp
if %ERRORLEVEL% NEQ 0 (echo FAILED: bankers.cpp) else (echo SUCCESS: bankers.cpp)

echo.
echo ========================================
echo Build complete!
echo ========================================
echo.
echo To run the application:
echo   cd frontend
echo   streamlit run app.py
echo.
pause
