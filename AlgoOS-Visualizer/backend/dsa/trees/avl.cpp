// File: backend/dsa/trees/avl.cpp
#include <iostream>
#include <sstream>
#include <string>
#include <algorithm>
#include <queue>
#include <vector>
using namespace std;

struct AVLNode {
    int data;
    AVLNode* left;
    AVLNode* right;
    int height;
    AVLNode(int val) : data(val), left(nullptr), right(nullptr), height(1) {}
};

class AVLTree {
private:
    AVLNode* root;
    int step;

    int getHeight(AVLNode* node) {
        return node ? node->height : 0;
    }

    int getBalance(AVLNode* node) {
        return node ? getHeight(node->left) - getHeight(node->right) : 0;
    }

    void updateHeight(AVLNode* node) {
        if (node) {
            node->height = 1 + max(getHeight(node->left), getHeight(node->right));
        }
    }

    void collectNodes(AVLNode* node, string& result) {
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

    string treeToString() {
        if (!root) return "EMPTY";
        string result;
        collectNodes(root, result);
        return result;
    }

    void printState(const string& operation, const string& meta = "") {
        string tree = treeToString();
        cout << step++ << " | " << operation << " | 101 | TREE:" << tree;
        if (!meta.empty()) {
            cout << " | " << meta;
        }
        cout << endl;
    }

    AVLNode* rightRotate(AVLNode* y) {
        AVLNode* x = y->left;
        AVLNode* T2 = x->right;

        x->right = y;
        y->left = T2;

        updateHeight(y);
        updateHeight(x);

        printState("ROTATE_RIGHT " + to_string(y->data), "PIVOT=" + to_string(x->data));
        return x;
    }

    AVLNode* leftRotate(AVLNode* x) {
        AVLNode* y = x->right;
        AVLNode* T2 = y->left;

        y->left = x;
        x->right = T2;

        updateHeight(x);
        updateHeight(y);

        printState("ROTATE_LEFT " + to_string(x->data), "PIVOT=" + to_string(y->data));
        return y;
    }

    AVLNode* insertHelper(AVLNode* node, int val) {
        if (!node) {
            printState("INSERT " + to_string(val), "VALUE=" + to_string(val));
            return new AVLNode(val);
        }

        if (val < node->data) {
            node->left = insertHelper(node->left, val);
        } else if (val > node->data) {
            node->right = insertHelper(node->right, val);
        } else {
            return node; // Duplicate
        }

        updateHeight(node);
        int balance = getBalance(node);

        // Left Left Case
        if (balance > 1 && val < node->left->data) {
            return rightRotate(node);
        }

        // Right Right Case
        if (balance < -1 && val > node->right->data) {
            return leftRotate(node);
        }

        // Left Right Case
        if (balance > 1 && val > node->left->data) {
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }

        // Right Left Case
        if (balance < -1 && val < node->right->data) {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }

        return node;
    }

    AVLNode* minValueNode(AVLNode* node) {
        AVLNode* current = node;
        while (current && current->left) {
            current = current->left;
        }
        return current;
    }

    AVLNode* deleteHelper(AVLNode* node, int val, bool& found) {
        if (!node) return nullptr;

        if (val < node->data) {
            node->left = deleteHelper(node->left, val, found);
        } else if (val > node->data) {
            node->right = deleteHelper(node->right, val, found);
        } else {
            found = true;
            printState("DELETE " + to_string(val), "NODE=" + to_string(val));
            
            if (!node->left || !node->right) {
                AVLNode* temp = node->left ? node->left : node->right;
                if (!temp) {
                    temp = node;
                    node = nullptr;
                } else {
                    *node = *temp;
                }
                delete temp;
            } else {
                AVLNode* temp = minValueNode(node->right);
                node->data = temp->data;
                node->right = deleteHelper(node->right, temp->data, found);
            }
        }

        if (!node) return nullptr;

        updateHeight(node);
        int balance = getBalance(node);

        // Left Left Case
        if (balance > 1 && getBalance(node->left) >= 0) {
            return rightRotate(node);
        }

        // Left Right Case
        if (balance > 1 && getBalance(node->left) < 0) {
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }

        // Right Right Case
        if (balance < -1 && getBalance(node->right) <= 0) {
            return leftRotate(node);
        }

        // Right Left Case
        if (balance < -1 && getBalance(node->right) > 0) {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }

        return node;
    }

    void inorderHelper(AVLNode* node, vector<int>& result) {
        if (!node) return;
        inorderHelper(node->left, result);
        result.push_back(node->data);
        inorderHelper(node->right, result);
    }

    void destroyTree(AVLNode* node) {
        if (!node) return;
        destroyTree(node->left);
        destroyTree(node->right);
        delete node;
    }

public:
    AVLTree() : root(nullptr), step(0) {}
    ~AVLTree() { destroyTree(root); }

    void insert(int val) {
        root = insertHelper(root, val);
    }

    void remove(int val) {
        bool found = false;
        root = deleteHelper(root, val, found);
    }
};

int main() {
    AVLTree avl;
    string line;
    
    while (getline(cin, line)) {
        if (line.empty() || line == "END") break;
        
        istringstream iss(line);
        string command;
        iss >> command;
        
        if (command == "INSERT") {
            int val;
            if (iss >> val) {
                avl.insert(val);
            }
        } else if (command == "DELETE") {
            int val;
            if (iss >> val) {
                avl.remove(val);
            }
        }
    }
    
    return 0;
}
