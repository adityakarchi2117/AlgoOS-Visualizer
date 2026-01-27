// File: backend/dsa/heap/heap.cpp
// Min/Max Heap with step-by-step visualization showing percolate paths
// Format: STEP | OPERATION | LINE | STATE | META

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
using namespace std;

class VisualHeap {
private:
    vector<int> data;
    int step;
    bool isMinHeap;
    
    string getState() const {
        stringstream ss;
        ss << "HEAP:[";
        for (int i = 0; i < data.size(); i++) {
            if (i > 0) ss << ",";
            ss << data[i];
        }
        ss << "]";
        return ss.str();
    }
    
    void output(const string& operation, int line, const string& meta) {
        cout << step++ << " | " << operation << " | " << line << " | " 
             << getState() << " | " << meta << endl;
    }
    
    bool compare(int a, int b) {
        return isMinHeap ? (a < b) : (a > b);
    }
    
    int parent(int i) { return (i - 1) / 2; }
    int leftChild(int i) { return 2 * i + 1; }
    int rightChild(int i) { return 2 * i + 2; }
    
    void heapifyUp(int idx) {
        while (idx > 0 && compare(data[idx], data[parent(idx)])) {
            int p = parent(idx);
            
            output("SWAP " + to_string(data[idx]) + "<->" + to_string(data[p]), 8, 
                   "IDX=" + to_string(idx) + ",PARENT=" + to_string(p) + 
                   ",PERCOLATE=UP");
            
            swap(data[idx], data[p]);
            idx = p;
        }
    }
    
    void heapifyDown(int idx) {
        int size = data.size();
        
        while (true) {
            int best = idx;
            int left = leftChild(idx);
            int right = rightChild(idx);
            
            if (left < size && compare(data[left], data[best])) {
                best = left;
            }
            if (right < size && compare(data[right], data[best])) {
                best = right;
            }
            
            if (best == idx) break;
            
            output("SWAP " + to_string(data[idx]) + "<->" + to_string(data[best]), 8, 
                   "IDX=" + to_string(idx) + ",CHILD=" + to_string(best) + 
                   ",PERCOLATE=DOWN");
            
            swap(data[idx], data[best]);
            idx = best;
        }
    }

public:
    VisualHeap(bool minHeap = true) : step(1), isMinHeap(minHeap) {
        string type = isMinHeap ? "MIN" : "MAX";
        output("INIT", 1, "TYPE=" + type + "_HEAP,EMPTY=true,SIZE=0");
    }
    
    void insert(int value) {
        data.push_back(value);
        int idx = data.size() - 1;
        
        output("INSERT " + to_string(value), 4, 
               "IDX=" + to_string(idx) + ",SIZE=" + to_string(data.size()));
        
        heapifyUp(idx);
        
        output("INSERT_COMPLETE " + to_string(value), 6, 
               "ROOT=" + to_string(data[0]) + ",SIZE=" + to_string(data.size()));
    }
    
    int extract() {
        if (data.empty()) {
            output("EXTRACT_FAIL", 10, "ERROR=EMPTY,EMPTY=true");
            return -1;
        }
        
        int result = data[0];
        
        output("EXTRACT " + to_string(result), 10, 
               "ROOT=" + to_string(result) + ",SIZE=" + to_string(data.size()));
        
        if (data.size() == 1) {
            data.pop_back();
            output("EXTRACT_COMPLETE", 12, "EXTRACTED=" + to_string(result) + ",EMPTY=true");
            return result;
        }
        
        data[0] = data.back();
        data.pop_back();
        
        output("MOVE_LAST_TO_ROOT", 11, 
               "NEW_ROOT=" + to_string(data[0]) + ",SIZE=" + to_string(data.size()));
        
        heapifyDown(0);
        
        string meta = "EXTRACTED=" + to_string(result) + ",SIZE=" + to_string(data.size());
        if (!data.empty()) {
            meta += ",ROOT=" + to_string(data[0]);
        }
        output("EXTRACT_COMPLETE", 12, meta);
        
        return result;
    }
    
    int peek() {
        if (data.empty()) {
            output("PEEK_FAIL", 14, "ERROR=EMPTY,EMPTY=true");
            return -1;
        }
        output("PEEK", 14, "ROOT=" + to_string(data[0]) + ",SIZE=" + to_string(data.size()));
        return data[0];
    }
    
    void buildHeap(vector<int>& arr) {
        data = arr;
        
        stringstream arrStr;
        arrStr << "INPUT=[";
        for (int i = 0; i < arr.size(); i++) {
            if (i > 0) arrStr << ",";
            arrStr << arr[i];
        }
        arrStr << "]";
        
        output("BUILD_START", 16, arrStr.str() + ",SIZE=" + to_string(data.size()));
        
        // Heapify from last non-leaf node
        for (int i = data.size() / 2 - 1; i >= 0; i--) {
            output("HEAPIFY_NODE " + to_string(data[i]), 17, "IDX=" + to_string(i));
            heapifyDown(i);
        }
        
        output("BUILD_COMPLETE", 18, "ROOT=" + to_string(data[0]) + ",SIZE=" + to_string(data.size()));
    }
    
    void heapSort() {
        if (data.empty()) {
            output("HEAPSORT_FAIL", 20, "ERROR=EMPTY,EMPTY=true");
            return;
        }
        
        vector<int> sorted;
        int originalSize = data.size();
        
        output("HEAPSORT_START", 20, "SIZE=" + to_string(originalSize));
        
        while (!data.empty()) {
            sorted.push_back(data[0]);
            
            data[0] = data.back();
            data.pop_back();
            
            if (!data.empty()) {
                heapifyDown(0);
            }
        }
        
        // Reverse for descending order if min heap (ascending if max heap)
        if (!isMinHeap) {
            reverse(sorted.begin(), sorted.end());
        }
        
        stringstream ss;
        ss << "SORTED=[";
        for (int i = 0; i < sorted.size(); i++) {
            if (i > 0) ss << ",";
            ss << sorted[i];
        }
        ss << "]";
        
        output("HEAPSORT_COMPLETE", 22, ss.str() + ",SIZE=" + to_string(originalSize));
        
        // Restore data
        data = sorted;
        if (!isMinHeap) {
            reverse(data.begin(), data.end());
        }
    }
    
    void display() {
        string meta = "SIZE=" + to_string(data.size());
        if (!data.empty()) {
            meta += ",ROOT=" + to_string(data[0]);
            meta += ",TYPE=" + string(isMinHeap ? "MIN" : "MAX");
            
            // Show tree structure
            meta += ",LEVELS=";
            int level = 0;
            int idx = 0;
            while (idx < data.size()) {
                int levelSize = 1 << level;
                meta += "[";
                for (int i = 0; i < levelSize && idx < data.size(); i++, idx++) {
                    if (i > 0) meta += ",";
                    meta += to_string(data[idx]);
                }
                meta += "]";
                level++;
            }
        } else {
            meta += ",EMPTY=true";
        }
        output("DISPLAY", 24, meta);
    }
    
    void clear() {
        data.clear();
        output("CLEAR", 26, "EMPTY=true,SIZE=0");
    }
    
    int size() {
        output("SIZE", 28, "SIZE=" + to_string(data.size()));
        return data.size();
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    bool isMinHeap = true;
    string line;
    
    // Check for heap type
    if (getline(cin, line)) {
        stringstream ss(line);
        string type;
        ss >> type;
        
        transform(type.begin(), type.end(), type.begin(), ::toupper);
        
        if (type == "MAX" || type == "MAXHEAP" || type == "MAX_HEAP") {
            isMinHeap = false;
        } else if (type == "MIN" || type == "MINHEAP" || type == "MIN_HEAP") {
            isMinHeap = true;
        } else {
            // Not a type specification, will process as command
        }
    }
    
    VisualHeap heap(isMinHeap);
    
    // Process commands
    while (getline(cin, line)) {
        if (line.empty() || line == "END" || line == "QUIT" || line == "EXIT") {
            break;
        }
        
        stringstream ss(line);
        string cmd;
        ss >> cmd;
        
        transform(cmd.begin(), cmd.end(), cmd.begin(), ::toupper);
        
        if (cmd == "INSERT" || cmd == "PUSH" || cmd == "ADD") {
            int value;
            if (ss >> value) heap.insert(value);
        } else if (cmd == "EXTRACT" || cmd == "POP" || cmd == "REMOVE") {
            heap.extract();
        } else if (cmd == "PEEK" || cmd == "TOP") {
            heap.peek();
        } else if (cmd == "BUILD") {
            vector<int> arr;
            int val;
            while (ss >> val) {
                arr.push_back(val);
            }
            if (!arr.empty()) heap.buildHeap(arr);
        } else if (cmd == "HEAPSORT" || cmd == "SORT") {
            heap.heapSort();
        } else if (cmd == "DISPLAY" || cmd == "SHOW") {
            heap.display();
        } else if (cmd == "SIZE") {
            heap.size();
        } else if (cmd == "CLEAR") {
            heap.clear();
        }
    }
    
    return 0;
}
