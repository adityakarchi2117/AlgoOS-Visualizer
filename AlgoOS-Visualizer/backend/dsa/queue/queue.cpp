// File: backend/dsa/queue/queue.cpp
// Queue (Linear & Circular) implementation with step-by-step visualization output
// Format: STEP | OPERATION | LINE | STATE | META

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

class VisualQueue {
private:
    vector<int> data;
    int front, rear, capacity;
    int step;
    bool isCircular;
    int count;
    
    string getState() const {
        stringstream ss;
        ss << "QUEUE:[";
        if (count == 0) {
            ss << "]";
            return ss.str();
        }
        
        bool first = true;
        if (isCircular) {
            int i = front;
            for (int c = 0; c < count; c++) {
                if (!first) ss << ",";
                ss << data[i];
                i = (i + 1) % capacity;
                first = false;
            }
        } else {
            for (int i = front; i <= rear; i++) {
                if (!first) ss << ",";
                ss << data[i];
                first = false;
            }
        }
        ss << "]";
        return ss.str();
    }
    
    void output(const string& operation, int line, const string& meta) {
        cout << step++ << " | " << operation << " | " << line << " | " 
             << getState() << " | " << meta << endl;
    }

public:
    VisualQueue(int cap, bool circular) 
        : capacity(cap), isCircular(circular), front(0), rear(-1), step(1), count(0) {
        data.resize(cap);
        string type = circular ? "CIRCULAR" : "LINEAR";
        output("INIT", __LINE__, "CAPACITY=" + to_string(cap) + ",TYPE=" + type);
    }
    
    bool isEmpty() const {
        return count == 0;
    }
    
    bool isFull() const {
        return count >= capacity;
    }
    
    void enqueue(int value) {
        if (isFull()) {
            output("ENQUEUE " + to_string(value), __LINE__, "ERROR=QUEUE_FULL,SIZE=" + to_string(count));
            return;
        }
        
        if (isCircular) {
            rear = (rear + 1) % capacity;
        } else {
            rear++;
        }
        
        data[rear] = value;
        count++;
        output("ENQUEUE " + to_string(value), __LINE__, "VALUE=" + to_string(value) + ",REAR=" + to_string(rear) + ",SIZE=" + to_string(count));
    }
    
    void dequeue() {
        if (isEmpty()) {
            output("DEQUEUE", __LINE__, "ERROR=QUEUE_EMPTY,SIZE=0");
            return;
        }
        
        int value = data[front];
        
        if (isCircular) {
            front = (front + 1) % capacity;
        } else {
            front++;
        }
        count--;
        
        // Reset if queue becomes empty
        if (count == 0) {
            front = 0;
            rear = -1;
        }
        
        output("DEQUEUE", __LINE__, "REMOVED=" + to_string(value) + ",FRONT=" + to_string(front) + ",SIZE=" + to_string(count));
    }
    
    void peek() {
        if (isEmpty()) {
            output("PEEK", __LINE__, "ERROR=QUEUE_EMPTY");
            return;
        }
        output("PEEK", __LINE__, "FRONT_VALUE=" + to_string(data[front]) + ",SIZE=" + to_string(count));
    }
    
    void size() {
        output("SIZE", __LINE__, "COUNT=" + to_string(count));
    }
    
    void display() {
        output("DISPLAY", __LINE__, "FRONT=" + to_string(front) + ",REAR=" + to_string(rear) + ",SIZE=" + to_string(count));
    }
};

int main() {
    string typeStr;
    int capacity;
    
    cin >> typeStr >> capacity;
    
    bool isCircular = (typeStr == "circular" || typeStr == "CIRCULAR");
    
    VisualQueue queue(capacity, isCircular);
    
    string command;
    while (cin >> command) {
        if (command == "ENQUEUE") {
            int value;
            cin >> value;
            queue.enqueue(value);
        }
        else if (command == "DEQUEUE") {
            queue.dequeue();
        }
        else if (command == "PEEK") {
            queue.peek();
        }
        else if (command == "SIZE") {
            queue.size();
        }
        else if (command == "DISPLAY") {
            queue.display();
        }
        else if (command == "END") {
            break;
        }
    }
    
    return 0;
}
