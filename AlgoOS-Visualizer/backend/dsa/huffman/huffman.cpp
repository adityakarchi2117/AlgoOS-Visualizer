// File: backend/dsa/huffman/huffman.cpp
// Huffman Coding Algorithm with step-by-step visualization output
// Format: STEP | OPERATION | LINE | STATE | META

#include <iostream>
#include <vector>
#include <queue>
#include <map>
#include <string>
#include <sstream>
using namespace std;

struct HuffmanNode {
    char ch;
    int freq;
    HuffmanNode* left;
    HuffmanNode* right;
    int id;
    
    HuffmanNode(char c, int f, int nodeId) 
        : ch(c), freq(f), left(nullptr), right(nullptr), id(nodeId) {}
};

struct Compare {
    bool operator()(HuffmanNode* a, HuffmanNode* b) {
        return a->freq > b->freq;
    }
};

class VisualHuffman {
private:
    map<char, int> frequencies;
    map<char, string> codes;
    HuffmanNode* root;
    int step;
    int nodeCounter;
    vector<HuffmanNode*> allNodes;
    
    string getTreeState() const {
        // Format: id:char:freq(left,right),...
        if (allNodes.empty()) return "TREE:EMPTY";
        
        stringstream ss;
        ss << "TREE:";
        bool first = true;
        for (HuffmanNode* node : allNodes) {
            if (!first) ss << ",";
            ss << node->id << ":";
            if (node->ch == '\0') {
                ss << "*";  // Internal node
            } else if (node->ch == ' ') {
                ss << "SP";  // Space
            } else {
                ss << node->ch;
            }
            ss << ":" << node->freq << "(";
            if (node->left) ss << node->left->id; else ss << "_";
            ss << ",";
            if (node->right) ss << node->right->id; else ss << "_";
            ss << ")";
            first = false;
        }
        return ss.str();
    }
    
    string getFreqState() const {
        stringstream ss;
        ss << "FREQ:{";
        bool first = true;
        for (const auto& p : frequencies) {
            if (!first) ss << ",";
            if (p.first == ' ') {
                ss << "' ':" << p.second;
            } else {
                ss << p.first << ":" << p.second;
            }
            first = false;
        }
        ss << "}";
        return ss.str();
    }
    
    string getCodesState() const {
        stringstream ss;
        ss << "CODES:{";
        bool first = true;
        for (const auto& p : codes) {
            if (!first) ss << ",";
            if (p.first == ' ') {
                ss << "' ':" << p.second;
            } else {
                ss << p.first << ":" << p.second;
            }
            first = false;
        }
        ss << "}";
        return ss.str();
    }
    
    void output(const string& operation, const string& state, const string& meta) {
        cout << step++ << " | " << operation << " | " << __LINE__ << " | " 
             << state << " | " << meta << endl;
    }
    
    void generateCodes(HuffmanNode* node, string code) {
        if (!node) return;
        
        if (!node->left && !node->right) {
            codes[node->ch] = code.empty() ? "0" : code;
            string charStr = (node->ch == ' ') ? "SPACE" : string(1, node->ch);
            output("CODE " + charStr, getCodesState(), "CHAR=" + charStr + ",CODE=" + codes[node->ch]);
            return;
        }
        
        generateCodes(node->left, code + "0");
        generateCodes(node->right, code + "1");
    }
    
    void deleteTree(HuffmanNode* node) {
        if (!node) return;
        deleteTree(node->left);
        deleteTree(node->right);
        delete node;
    }

public:
    VisualHuffman() : root(nullptr), step(1), nodeCounter(1) {
        output("INIT", "TREE:EMPTY", "READY");
    }
    
    ~VisualHuffman() {
        // Nodes deleted through allNodes vector
        for (HuffmanNode* node : allNodes) {
            delete node;
        }
    }
    
    void calculateFrequencies(const string& text) {
        frequencies.clear();
        for (char ch : text) {
            frequencies[ch]++;
        }
        
        output("FREQ", getFreqState(), "TEXT_LEN=" + to_string(text.length()) + ",UNIQUE=" + to_string(frequencies.size()));
    }
    
    void buildTree() {
        priority_queue<HuffmanNode*, vector<HuffmanNode*>, Compare> pq;
        
        // Create leaf nodes
        for (const auto& p : frequencies) {
            HuffmanNode* node = new HuffmanNode(p.first, p.second, nodeCounter++);
            allNodes.push_back(node);
            pq.push(node);
            string charStr = (p.first == ' ') ? "SPACE" : string(1, p.first);
            output("LEAF " + charStr, getTreeState(), "CHAR=" + charStr + ",FREQ=" + to_string(p.second) + ",ID=" + to_string(node->id));
        }
        
        // Handle single character
        if (pq.size() == 1) {
            HuffmanNode* single = pq.top();
            pq.pop();
            root = new HuffmanNode('\0', single->freq, nodeCounter++);
            root->left = single;
            allNodes.push_back(root);
            output("SINGLE", getTreeState(), "ROOT_ID=" + to_string(root->id));
            return;
        }
        
        // Build tree
        while (pq.size() > 1) {
            HuffmanNode* left = pq.top(); pq.pop();
            HuffmanNode* right = pq.top(); pq.pop();
            
            HuffmanNode* merged = new HuffmanNode('\0', left->freq + right->freq, nodeCounter++);
            merged->left = left;
            merged->right = right;
            allNodes.push_back(merged);
            pq.push(merged);
            
            output("MERGE", getTreeState(), "LEFT_ID=" + to_string(left->id) + ",RIGHT_ID=" + to_string(right->id) + ",NEW_ID=" + to_string(merged->id) + ",FREQ=" + to_string(merged->freq));
        }
        
        root = pq.top();
        output("TREE_DONE", getTreeState(), "ROOT_ID=" + to_string(root->id) + ",ROOT_FREQ=" + to_string(root->freq));
    }
    
    void generateAllCodes() {
        codes.clear();
        generateCodes(root, "");
        
        int totalBits = 0;
        for (const auto& p : frequencies) {
            totalBits += p.second * codes[p.first].length();
        }
        
        output("CODES_DONE", getCodesState(), "TOTAL_CODES=" + to_string(codes.size()) + ",TOTAL_BITS=" + to_string(totalBits));
    }
    
    string encode(const string& text) {
        stringstream encoded;
        for (char ch : text) {
            encoded << codes[ch];
        }
        
        string result = encoded.str();
        int origBits = text.length() * 8;
        int compBits = result.length();
        int ratio = (compBits * 100) / origBits;
        
        output("ENCODE", "ENCODED:" + result, "ORIG_BITS=" + to_string(origBits) + ",COMP_BITS=" + to_string(compBits) + ",COMPRESSION=" + to_string(ratio) + "%");
        
        return result;
    }
    
    string decode(const string& encoded) {
        if (!root) return "";
        
        stringstream decoded;
        HuffmanNode* curr = root;
        
        for (char bit : encoded) {
            if (bit == '0') {
                curr = curr->left;
            } else {
                curr = curr->right;
            }
            
            if (curr && !curr->left && !curr->right) {
                decoded << curr->ch;
                curr = root;
            }
        }
        
        string result = decoded.str();
        output("DECODE", "DECODED:" + result, "ENCODED_LEN=" + to_string(encoded.length()) + ",DECODED_LEN=" + to_string(result.length()));
        
        return result;
    }
    
    void printCodes() {
        for (const auto& p : codes) {
            string charStr = (p.first == ' ') ? "SPACE" : string(1, p.first);
            cout << charStr << " -> " << p.second << endl;
        }
    }
};

int main() {
    VisualHuffman huffman;
    string command;
    string text;
    string encoded;
    
    while (cin >> command) {
        if (command == "TEXT") {
            getline(cin, text);
            // Remove leading space
            if (!text.empty() && text[0] == ' ') {
                text = text.substr(1);
            }
            huffman.calculateFrequencies(text);
            huffman.buildTree();
            huffman.generateAllCodes();
        }
        else if (command == "ENCODE") {
            if (!text.empty()) {
                encoded = huffman.encode(text);
            }
        }
        else if (command == "DECODE") {
            if (!encoded.empty()) {
                string decoded = huffman.decode(encoded);
            }
        }
        else if (command == "CODES") {
            huffman.printCodes();
        }
        else if (command == "END") {
            break;
        }
    }
    
    return 0;
}
