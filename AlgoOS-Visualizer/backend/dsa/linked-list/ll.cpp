// File: backend/dsa/linked-list/ll.cpp
// Singly Linked List implementation with step-by-step visualization output
// Format: STEP | OPERATION | LINE | STATE | META

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
using namespace std;

struct Node {
    int data;
    Node* next;
    
    Node(int val) : data(val), next(nullptr) {}
};

class VisualLinkedList {
private:
    Node* head;
    int step;
    int size_;
    
    string getState() const {
        stringstream ss;
        ss << "LIST:";
        Node* current = head;
        if (!current) {
            ss << "NULL";
        } else {
            while (current) {
                ss << current->data;
                current = current->next;
                if (current) ss << "->";
            }
            ss << "->NULL";
        }
        return ss.str();
    }
    
    void output(const string& operation, int line, const string& meta) {
        cout << step++ << " | " << operation << " | " << line << " | " 
             << getState() << " | " << meta << endl;
    }

public:
    VisualLinkedList() : head(nullptr), step(1), size_(0) {
        output("INIT", 1, "SIZE=0");
    }
    
    ~VisualLinkedList() {
        while (head) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }
    
    void insertFront(int value) {
        Node* newNode = new Node(value);
        newNode->next = head;
        head = newNode;
        size_++;
        output("INSERT_FRONT " + to_string(value), __LINE__, "VALUE=" + to_string(value) + ",SIZE=" + to_string(size_));
    }
    
    void insertEnd(int value) {
        Node* newNode = new Node(value);
        size_++;
        
        if (!head) {
            head = newNode;
            output("INSERT_END " + to_string(value), __LINE__, "VALUE=" + to_string(value) + ",SIZE=" + to_string(size_));
            return;
        }
        
        Node* current = head;
        while (current->next) {
            current = current->next;
        }
        current->next = newNode;
        output("INSERT_END " + to_string(value), __LINE__, "VALUE=" + to_string(value) + ",SIZE=" + to_string(size_));
    }
    
    void insertAt(int pos, int value) {
        if (pos < 0 || pos > size_) {
            output("INSERT_AT " + to_string(pos) + " " + to_string(value), __LINE__, "ERROR=INVALID_POSITION,SIZE=" + to_string(size_));
            return;
        }
        
        if (pos == 0) {
            insertFront(value);
            return;
        }
        
        Node* newNode = new Node(value);
        Node* current = head;
        for (int i = 0; i < pos - 1; i++) {
            current = current->next;
        }
        newNode->next = current->next;
        current->next = newNode;
        size_++;
        output("INSERT_AT " + to_string(pos) + " " + to_string(value), __LINE__, "VALUE=" + to_string(value) + ",POS=" + to_string(pos) + ",SIZE=" + to_string(size_));
    }
    
    void deleteFront() {
        if (!head) {
            output("DELETE_FRONT", __LINE__, "ERROR=LIST_EMPTY,SIZE=0");
            return;
        }
        
        int value = head->data;
        Node* temp = head;
        head = head->next;
        delete temp;
        size_--;
        output("DELETE_FRONT", __LINE__, "DELETED=" + to_string(value) + ",SIZE=" + to_string(size_));
    }
    
    void deleteEnd() {
        if (!head) {
            output("DELETE_END", __LINE__, "ERROR=LIST_EMPTY,SIZE=0");
            return;
        }
        
        if (!head->next) {
            int value = head->data;
            delete head;
            head = nullptr;
            size_--;
            output("DELETE_END", __LINE__, "DELETED=" + to_string(value) + ",SIZE=" + to_string(size_));
            return;
        }
        
        Node* current = head;
        while (current->next->next) {
            current = current->next;
        }
        int value = current->next->data;
        delete current->next;
        current->next = nullptr;
        size_--;
        output("DELETE_END", __LINE__, "DELETED=" + to_string(value) + ",SIZE=" + to_string(size_));
    }
    
    void deleteAt(int pos) {
        if (pos < 0 || pos >= size_ || !head) {
            output("DELETE_AT " + to_string(pos), __LINE__, "ERROR=INVALID_POSITION,SIZE=" + to_string(size_));
            return;
        }
        
        if (pos == 0) {
            deleteFront();
            return;
        }
        
        Node* current = head;
        for (int i = 0; i < pos - 1; i++) {
            current = current->next;
        }
        Node* toDelete = current->next;
        int value = toDelete->data;
        current->next = toDelete->next;
        delete toDelete;
        size_--;
        output("DELETE_AT " + to_string(pos), __LINE__, "DELETED=" + to_string(value) + ",POS=" + to_string(pos) + ",SIZE=" + to_string(size_));
    }
    
    void deleteValue(int value) {
        if (!head) {
            output("DELETE_VALUE " + to_string(value), __LINE__, "ERROR=LIST_EMPTY,SIZE=0");
            return;
        }
        
        if (head->data == value) {
            deleteFront();
            return;
        }
        
        Node* current = head;
        while (current->next && current->next->data != value) {
            current = current->next;
        }
        
        if (!current->next) {
            output("DELETE_VALUE " + to_string(value), __LINE__, "ERROR=NOT_FOUND,SIZE=" + to_string(size_));
            return;
        }
        
        Node* toDelete = current->next;
        current->next = toDelete->next;
        delete toDelete;
        size_--;
        output("DELETE_VALUE " + to_string(value), __LINE__, "DELETED=" + to_string(value) + ",SIZE=" + to_string(size_));
    }
    
    void search(int value) {
        Node* current = head;
        int pos = 0;
        while (current) {
            if (current->data == value) {
                output("SEARCH " + to_string(value), __LINE__, "FOUND=true,POSITION=" + to_string(pos) + ",SIZE=" + to_string(size_));
                return;
            }
            current = current->next;
            pos++;
        }
        output("SEARCH " + to_string(value), __LINE__, "FOUND=false,SIZE=" + to_string(size_));
    }
    
    void reverse() {
        if (!head || !head->next) {
            output("REVERSE", __LINE__, "STATUS=DONE,SIZE=" + to_string(size_));
            return;
        }
        
        Node* prev = nullptr;
        Node* current = head;
        Node* next = nullptr;
        
        while (current) {
            next = current->next;
            current->next = prev;
            prev = current;
            current = next;
        }
        head = prev;
        output("REVERSE", __LINE__, "STATUS=DONE,SIZE=" + to_string(size_));
    }
    
    void detailed() {
        output("DETAILED", __LINE__, "SIZE=" + to_string(size_) + ",HEAD=" + (head ? to_string(head->data) : "NULL"));
    }
};

int main() {
    VisualLinkedList list;
    string command;
    
    while (cin >> command) {
        if (command == "INSERT_FRONT") {
            int value;
            cin >> value;
            list.insertFront(value);
        }
        else if (command == "INSERT_END") {
            int value;
            cin >> value;
            list.insertEnd(value);
        }
        else if (command == "INSERT_AT") {
            int pos, value;
            cin >> pos >> value;
            list.insertAt(pos, value);
        }
        else if (command == "DELETE_FRONT") {
            list.deleteFront();
        }
        else if (command == "DELETE_END") {
            list.deleteEnd();
        }
        else if (command == "DELETE_AT") {
            int pos;
            cin >> pos;
            list.deleteAt(pos);
        }
        else if (command == "DELETE_VALUE") {
            int value;
            cin >> value;
            list.deleteValue(value);
        }
        else if (command == "SEARCH") {
            int value;
            cin >> value;
            list.search(value);
        }
        else if (command == "REVERSE") {
            list.reverse();
        }
        else if (command == "DETAILED") {
            list.detailed();
        }
        else if (command == "END") {
            break;
        }
    }
    
    return 0;
}
