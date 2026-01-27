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

    AVLNode* rightRotate(AVLNode* y) {
        cout << "ROTATION: Right rotation at node " << y->data << endl;
        AVLNode* x = y->left;
        AVLNode* T2 = x->right;

        x->right = y;
        y->left = T2;

        updateHeight(y);
        updateHeight(x);

        return x;
    }

    AVLNode* leftRotate(AVLNode* x) {
        cout << "ROTATION: Left rotation at node " << x->data << endl;
        AVLNode* y = x->right;
        AVLNode* T2 = y->left;

        y->left = x;
        x->right = T2;

        updateHeight(x);
        updateHeight(y);

        return y;
    }

    AVLNode* insertHelper(AVLNode* node, int val) {
        if (!node) {
            cout << "INSERT: Node " << val << " created" << endl;
            return new AVLNode(val);
        }

        if (val < node->data) {
            cout << "TRAVERSE: Going left from " << node->data << endl;
            node->left = insertHelper(node->left, val);
        } else if (val > node->data) {
            cout << "TRAVERSE: Going right from " << node->data << endl;
            node->right = insertHelper(node->right, val);
        } else {
            cout << "INSERT: Duplicate value " << val << " ignored" << endl;
            return node;
        }

        updateHeight(node);
        int balance = getBalance(node);

        cout << "BALANCE: Node " << node->data << " has balance factor " << balance << endl;

        // Left Left Case
        if (balance > 1 && val < node->left->data) {
            cout << "CASE: Left-Left imbalance at " << node->data << endl;
            return rightRotate(node);
        }

        // Right Right Case
        if (balance < -1 && val > node->right->data) {
            cout << "CASE: Right-Right imbalance at " << node->data << endl;
            return leftRotate(node);
        }

        // Left Right Case
        if (balance > 1 && val > node->left->data) {
            cout << "CASE: Left-Right imbalance at " << node->data << endl;
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }

        // Right Left Case
        if (balance < -1 && val < node->right->data) {
            cout << "CASE: Right-Left imbalance at " << node->data << endl;
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
            cout << "DELETE: Found node " << val << endl;
            
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

        cout << "BALANCE: Node " << node->data << " has balance factor " << balance << endl;

        // Left Left Case
        if (balance > 1 && getBalance(node->left) >= 0) {
            cout << "REBALANCE: Left-Left case at " << node->data << endl;
            return rightRotate(node);
        }

        // Left Right Case
        if (balance > 1 && getBalance(node->left) < 0) {
            cout << "REBALANCE: Left-Right case at " << node->data << endl;
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }

        // Right Right Case
        if (balance < -1 && getBalance(node->right) <= 0) {
            cout << "REBALANCE: Right-Right case at " << node->data << endl;
            return leftRotate(node);
        }

        // Right Left Case
        if (balance < -1 && getBalance(node->right) > 0) {
            cout << "REBALANCE: Right-Left case at " << node->data << endl;
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

    void printTreeHelper(AVLNode* node, string prefix, bool isLeft) {
        if (!node) return;
        cout << prefix;
        cout << (isLeft ? "├──" : "└──");
        cout << node->data << "(h=" << node->height << ",bf=" << getBalance(node) << ")" << endl;
        printTreeHelper(node->left, prefix + (isLeft ? "│   " : "    "), true);
        printTreeHelper(node->right, prefix + (isLeft ? "│   " : "    "), false);
    }

    void destroyTree(AVLNode* node) {
        if (!node) return;
        destroyTree(node->left);
        destroyTree(node->right);
        delete node;
    }

public:
    AVLTree() : root(nullptr) {}
    ~AVLTree() { destroyTree(root); }

    void insert(int val) {
        cout << "--- INSERT " << val << " ---" << endl;
        root = insertHelper(root, val);
    }

    void remove(int val) {
        cout << "--- DELETE " << val << " ---" << endl;
        bool found = false;
        root = deleteHelper(root, val, found);
        if (!found) {
            cout << "DELETE: Value " << val << " not found" << endl;
        }
    }

    void inorder() {
        vector<int> result;
        inorderHelper(root, result);
        cout << "INORDER:";
        for (int val : result) cout << " " << val;
        if (result.empty()) cout << " EMPTY";
        cout << endl;
    }

    void levelorder() {
        cout << "LEVELORDER:";
        if (!root) {
            cout << " EMPTY" << endl;
            return;
        }
        queue<AVLNode*> q;
        q.push(root);
        int level = 0;
        while (!q.empty()) {
            int size = q.size();
            cout << " [L" << level << ":";
            for (int i = 0; i < size; i++) {
                AVLNode* node = q.front();
                q.pop();
                cout << " " << node->data << "(bf=" << getBalance(node) << ")";
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            cout << "]";
            level++;
        }
        cout << endl;
    }

    void printTree() {
        cout << "AVL_TREE_STRUCTURE:" << endl;
        if (!root) {
            cout << "  (empty)" << endl;
            return;
        }
        printTreeHelper(root, "  ", false);
    }

    void printState() {
        levelorder();
        printTree();
    }
};

int main() {
    cout << "AVL_VISUALIZER_START" << endl;
    
    AVLTree avl;
    string line;
    
    cout << "INIT: AVL Tree initialized" << endl;
    
    while (getline(cin, line)) {
        if (line.empty() || line == "END") break;
        
        istringstream iss(line);
        string command;
        iss >> command;
        transform(command.begin(), command.end(), command.begin(), ::toupper);
        
        if (command == "INSERT") {
            int val;
            while (iss >> val) {
                avl.insert(val);
                avl.printState();
            }
        } else if (command == "DELETE" || command == "REMOVE") {
            int val;
            if (iss >> val) {
                avl.remove(val);
            }
        } else if (command == "INORDER") {
            avl.inorder();
        } else if (command == "LEVELORDER") {
            avl.levelorder();
        } else if (command == "PRINT" || command == "DISPLAY") {
            avl.printTree();
        } else {
            cout << "ERROR: Unknown command: " << command << endl;
        }
        
        avl.printState();
    }
    
    cout << "AVL_VISUALIZER_END" << endl;
    return 0;
}
