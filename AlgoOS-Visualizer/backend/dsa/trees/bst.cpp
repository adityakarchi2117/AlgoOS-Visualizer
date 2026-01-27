#include <iostream>
#include <string>
#include <sstream>
using namespace std;

struct Node {
    int data;
    Node* left;
    Node* right;
    Node(int val) : data(val), left(nullptr), right(nullptr) {}
};

int step = 0;
Node* root = nullptr;

void collectNodes(Node* node, string& result) {
    if (!node) return;
    
    // Add current node
    if (!result.empty()) result += ",";
    result += to_string(node->data) + "(";
    result += node->left ? to_string(node->left->data) : "_";
    result += ",";
    result += node->right ? to_string(node->right->data) : "_";
    result += ")";
    
    // Recursively add children
    collectNodes(node->left, result);
    collectNodes(node->right, result);
}

string treeToString(Node* node) {
    if (!node) return "EMPTY";
    string result;
    collectNodes(node, result);
    return result;
}

void printState(const string& operation, const string& meta = "") {
    string tree = treeToString(root);
    cout << step++ << " | " << operation << " | 101 | TREE:" << tree;
    if (!meta.empty()) {
        cout << " | " << meta;
    }
    cout << endl;
}

Node* insert(Node* node, int value, int& height) {
    if (!node) {
        Node* newNode = new Node(value);
        printState("INSERT " + to_string(value), "VALUE=" + to_string(value) + ",HEIGHT=" + to_string(height));
        return newNode;
    }
    
    if (value < node->data) {
        height++;
        node->left = insert(node->left, value, height);
    } else if (value > node->data) {
        height++;
        node->right = insert(node->right, value, height);
    }
    
    return node;
}

Node* findMin(Node* node) {
    while (node->left) {
        node = node->left;
    }
    return node;
}

Node* deleteNode(Node* node, int value, bool& found) {
    if (!node) return nullptr;
    
    if (value < node->data) {
        node->left = deleteNode(node->left, value, found);
    } else if (value > node->data) {
        node->right = deleteNode(node->right, value, found);
    } else {
        found = true;
        if (!node->left && !node->right) {
            delete node;
            printState("DELETE " + to_string(value), "TYPE=LEAF");
            return nullptr;
        } else if (!node->left) {
            Node* temp = node->right;
            delete node;
            printState("DELETE " + to_string(value), "TYPE=ONE_CHILD");
            return temp;
        } else if (!node->right) {
            Node* temp = node->left;
            delete node;
            printState("DELETE " + to_string(value), "TYPE=ONE_CHILD");
            return temp;
        } else {
            Node* minNode = findMin(node->right);
            int minVal = minNode->data;
            node->data = minVal;
            printState("DELETE " + to_string(value), "REPLACED_WITH=" + to_string(minVal));
            node->right = deleteNode(node->right, minVal, found);
        }
    }
    
    return node;
}

bool search(Node* node, int value, int depth = 0) {
    if (!node) {
        printState("SEARCH " + to_string(value), "FOUND=NO,DEPTH=" + to_string(depth));
        return false;
    }
    if (node->data == value) {
        printState("SEARCH " + to_string(value), "FOUND=YES,DEPTH=" + to_string(depth));
        return true;
    }
    if (value < node->data) {
        return search(node->left, value, depth + 1);
    }
    return search(node->right, value, depth + 1);
}

int main() {
    string line;
    
    while (getline(cin, line)) {
        if (line == "END") break;
        
        istringstream iss(line);
        string command;
        iss >> command;
        
        if (command == "INSERT") {
            int value;
            iss >> value;
            int height = 0;
            root = insert(root, value, height);
        } 
        else if (command == "DELETE") {
            int value;
            iss >> value;
            bool found = false;
            root = deleteNode(root, value, found);
            if (!found) {
                printState("DELETE " + to_string(value), "FOUND=NO");
            }
        }
        else if (command == "SEARCH") {
            int value;
            iss >> value;
            search(root, value);
        }
    }
    
    return 0;
}
