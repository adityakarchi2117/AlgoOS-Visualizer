// File: backend/dsa/stack/stack.cpp
// Stack implementation with step-by-step visualization output
// Format: STEP | OPERATION | LINE | STATE | META

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
using namespace std;

class VisualStack {
private:
    vector<int> data;
    int capacity;
    int step;
    
    string getState() const {
        stringstream ss;
        ss << "STACK:[";
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

public:
    VisualStack(int cap = 100) : capacity(cap), step(1) {
        output("INIT", 1, "CAPACITY=" + to_string(cap) + ",EMPTY=true");
    }
    
    bool isEmpty() const {
        return data.empty();
    }
    
    bool isFull() const {
        return data.size() >= capacity;
    }
    
    void push(int value) {
        if (isFull()) {
            output("PUSH_FAIL " + to_string(value), 3, "ERROR=OVERFLOW,FULL=true");
            return;
        }
        data.push_back(value);
        string meta = "TOP=" + to_string(value) + ",SIZE=" + to_string(data.size());
        if (data.size() == capacity) meta += ",FULL=true";
        output("PUSH " + to_string(value), 3, meta);
    }
    
    int pop() {
        if (isEmpty()) {
            output("POP_FAIL", 5, "ERROR=UNDERFLOW,EMPTY=true");
            return -1;
        }
        int value = data.back();
        data.pop_back();
        string meta = "POPPED=" + to_string(value);
        if (isEmpty()) {
            meta += ",EMPTY=true";
        } else {
            meta += ",TOP=" + to_string(data.back());
        }
        meta += ",SIZE=" + to_string(data.size());
        output("POP", 5, meta);
        return value;
    }
    
    int peek() {
        if (isEmpty()) {
            output("PEEK_FAIL", 7, "ERROR=EMPTY,EMPTY=true");
            return -1;
        }
        int value = data.back();
        output("PEEK", 7, "TOP=" + to_string(value) + ",SIZE=" + to_string(data.size()));
        return value;
    }
    
    int size() {
        output("SIZE", 9, "SIZE=" + to_string(data.size()) + ",EMPTY=" + (isEmpty() ? "true" : "false"));
        return data.size();
    }
    
    void clear() {
        data.clear();
        output("CLEAR", 11, "EMPTY=true,SIZE=0");
    }
    
    void display() {
        string meta = "SIZE=" + to_string(data.size());
        if (!isEmpty()) {
            meta += ",TOP=" + to_string(data.back()) + ",BOTTOM=" + to_string(data.front());
        } else {
            meta += ",EMPTY=true";
        }
        output("DISPLAY", 13, meta);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int capacity = 100;
    string line;
    
    // Check for capacity specification
    if (getline(cin, line)) {
        stringstream ss(line);
        string cmd;
        ss >> cmd;
        
        if (cmd == "CAPACITY") {
            int cap;
            if (ss >> cap && cap > 0) {
                capacity = cap;
            }
        }
    }
    
    VisualStack stack(capacity);
    
    // Process first line if it wasn't CAPACITY
    if (line != "" && line.substr(0, 8) != "CAPACITY") {
        stringstream ss(line);
        string cmd;
        ss >> cmd;
        
        if (cmd == "PUSH") {
            int value;
            if (ss >> value) {
                stack.push(value);
            }
        } else if (cmd == "POP") {
            stack.pop();
        } else if (cmd == "PEEK" || cmd == "TOP") {
            stack.peek();
        } else if (cmd == "SIZE") {
            stack.size();
        } else if (cmd == "CLEAR") {
            stack.clear();
        } else if (cmd == "DISPLAY" || cmd == "SHOW") {
            stack.display();
        }
    }
    
    // Process remaining commands
    while (getline(cin, line)) {
        if (line.empty() || line == "END" || line == "QUIT" || line == "EXIT") {
            break;
        }
        
        stringstream ss(line);
        string cmd;
        ss >> cmd;
        
        // Convert to uppercase for case-insensitive matching
        transform(cmd.begin(), cmd.end(), cmd.begin(), ::toupper);
        
        if (cmd == "PUSH") {
            int value;
            if (ss >> value) {
                stack.push(value);
            }
        } else if (cmd == "POP") {
            stack.pop();
        } else if (cmd == "PEEK" || cmd == "TOP") {
            stack.peek();
        } else if (cmd == "SIZE") {
            stack.size();
        } else if (cmd == "CLEAR") {
            stack.clear();
        } else if (cmd == "DISPLAY" || cmd == "SHOW") {
            stack.display();
        }
    }
    
    return 0;
}
