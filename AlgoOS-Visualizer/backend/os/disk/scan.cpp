// File: backend/os/disk/scan.cpp
// Disk Scheduling: SCAN, C-SCAN, LOOK, C-LOOK
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <sstream>
using namespace std;

void runSCAN(int head, int maxCylinder, string direction, vector<int>& requests) {
    cout << "ALGORITHM: SCAN" << endl;
    cout << "HEAD: " << head << endl;
    cout << "DIRECTION: " << direction << endl;
    cout << "MAX_CYLINDER: " << maxCylinder << endl;
    cout << "---" << endl;
    
    vector<int> sequence;
    sequence.push_back(head);
    
    vector<int> left, right;
    for (int r : requests) {
        if (r < head) left.push_back(r);
        else right.push_back(r);
    }
    
    sort(left.begin(), left.end());
    sort(right.begin(), right.end());
    
    int totalSeek = 0;
    int step = 0;
    
    if (direction == "UP") {
        for (int r : right) {
            step++;
            int seek = abs(r - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->" << r 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
            sequence.push_back(r);
        }
        
        if (!left.empty()) {
            step++;
            int seek = abs(maxCylinder - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->" << maxCylinder 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << " (boundary)" << endl;
            sequence.push_back(maxCylinder);
            
            for (int i = left.size() - 1; i >= 0; i--) {
                step++;
                seek = abs(left[i] - sequence.back());
                totalSeek += seek;
                cout << step << " | MOVE " << sequence.back() << "->" << left[i] 
                     << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
                sequence.push_back(left[i]);
            }
        }
    } else {
        for (int i = left.size() - 1; i >= 0; i--) {
            step++;
            int seek = abs(left[i] - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->" << left[i] 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
            sequence.push_back(left[i]);
        }
        
        if (!right.empty()) {
            step++;
            int seek = abs(0 - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->0 | SEEK=" << seek 
                 << " | TOTAL=" << totalSeek << " (boundary)" << endl;
            sequence.push_back(0);
            
            for (int r : right) {
                step++;
                seek = abs(r - sequence.back());
                totalSeek += seek;
                cout << step << " | MOVE " << sequence.back() << "->" << r 
                     << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
                sequence.push_back(r);
            }
        }
    }
    
    cout << "---" << endl;
    cout << "SEQUENCE: ";
    for (int i = 0; i < sequence.size(); i++) {
        if (i > 0) cout << ",";
        cout << sequence[i];
    }
    cout << endl;
    
    cout << "TOTAL_SEEK: " << totalSeek << endl;
    cout << fixed << setprecision(2);
    cout << "AVG_SEEK: " << (double)totalSeek / requests.size() << endl;
}

void runCSCAN(int head, int maxCylinder, string direction, vector<int>& requests) {
    cout << "ALGORITHM: C-SCAN" << endl;
    cout << "HEAD: " << head << endl;
    cout << "DIRECTION: " << direction << endl;
    cout << "---" << endl;
    
    vector<int> sequence;
    sequence.push_back(head);
    
    vector<int> left, right;
    for (int r : requests) {
        if (r < head) left.push_back(r);
        else right.push_back(r);
    }
    
    sort(left.begin(), left.end());
    sort(right.begin(), right.end());
    
    int totalSeek = 0;
    int step = 0;
    
    if (direction == "UP") {
        for (int r : right) {
            step++;
            int seek = abs(r - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->" << r 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
            sequence.push_back(r);
        }
        
        if (!left.empty()) {
            step++;
            int seek = abs(maxCylinder - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->" << maxCylinder 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << " (boundary)" << endl;
            sequence.push_back(maxCylinder);
            
            step++;
            cout << step << " | JUMP " << maxCylinder << "->0 | SEEK=0 | TOTAL=" << totalSeek 
                 << " (circular jump)" << endl;
            sequence.push_back(0);
            
            for (int r : left) {
                step++;
                seek = abs(r - sequence.back());
                totalSeek += seek;
                cout << step << " | MOVE " << sequence.back() << "->" << r 
                     << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
                sequence.push_back(r);
            }
        }
    } else {
        for (int i = left.size() - 1; i >= 0; i--) {
            step++;
            int seek = abs(left[i] - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->" << left[i] 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
            sequence.push_back(left[i]);
        }
        
        if (!right.empty()) {
            step++;
            int seek = abs(0 - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->0 | SEEK=" << seek 
                 << " | TOTAL=" << totalSeek << " (boundary)" << endl;
            sequence.push_back(0);
            
            step++;
            cout << step << " | JUMP 0->" << maxCylinder << " | SEEK=0 | TOTAL=" << totalSeek 
                 << " (circular jump)" << endl;
            sequence.push_back(maxCylinder);
            
            for (int i = right.size() - 1; i >= 0; i--) {
                step++;
                seek = abs(right[i] - sequence.back());
                totalSeek += seek;
                cout << step << " | MOVE " << sequence.back() << "->" << right[i] 
                     << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
                sequence.push_back(right[i]);
            }
        }
    }
    
    cout << "---" << endl;
    cout << "SEQUENCE: ";
    for (int i = 0; i < sequence.size(); i++) {
        if (i > 0) cout << ",";
        cout << sequence[i];
    }
    cout << endl;
    
    cout << "TOTAL_SEEK: " << totalSeek << endl;
    cout << fixed << setprecision(2);
    cout << "AVG_SEEK: " << (double)totalSeek / requests.size() << endl;
}

void runLOOK(int head, string direction, vector<int>& requests) {
    cout << "ALGORITHM: LOOK" << endl;
    cout << "HEAD: " << head << endl;
    cout << "DIRECTION: " << direction << endl;
    cout << "---" << endl;
    
    vector<int> sequence;
    sequence.push_back(head);
    
    vector<int> left, right;
    for (int r : requests) {
        if (r < head) left.push_back(r);
        else right.push_back(r);
    }
    
    sort(left.begin(), left.end());
    sort(right.begin(), right.end());
    
    int totalSeek = 0;
    int step = 0;
    
    if (direction == "UP") {
        for (int r : right) {
            step++;
            int seek = abs(r - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->" << r 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
            sequence.push_back(r);
        }
        
        for (int i = left.size() - 1; i >= 0; i--) {
            step++;
            int seek = abs(left[i] - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->" << left[i] 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
            sequence.push_back(left[i]);
        }
    } else {
        for (int i = left.size() - 1; i >= 0; i--) {
            step++;
            int seek = abs(left[i] - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->" << left[i] 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
            sequence.push_back(left[i]);
        }
        
        for (int r : right) {
            step++;
            int seek = abs(r - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->" << r 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
            sequence.push_back(r);
        }
    }
    
    cout << "---" << endl;
    cout << "SEQUENCE: ";
    for (int i = 0; i < sequence.size(); i++) {
        if (i > 0) cout << ",";
        cout << sequence[i];
    }
    cout << endl;
    
    cout << "TOTAL_SEEK: " << totalSeek << endl;
    cout << fixed << setprecision(2);
    cout << "AVG_SEEK: " << (double)totalSeek / requests.size() << endl;
}

void runCLOOK(int head, string direction, vector<int>& requests) {
    cout << "ALGORITHM: C-LOOK" << endl;
    cout << "HEAD: " << head << endl;
    cout << "DIRECTION: " << direction << endl;
    cout << "---" << endl;
    
    vector<int> sequence;
    sequence.push_back(head);
    
    vector<int> left, right;
    for (int r : requests) {
        if (r < head) left.push_back(r);
        else right.push_back(r);
    }
    
    sort(left.begin(), left.end());
    sort(right.begin(), right.end());
    
    int totalSeek = 0;
    int step = 0;
    
    if (direction == "UP") {
        for (int r : right) {
            step++;
            int seek = abs(r - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->" << r 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
            sequence.push_back(r);
        }
        
        if (!left.empty()) {
            step++;
            int seek = abs(left[0] - sequence.back());
            totalSeek += seek;
            cout << step << " | JUMP " << sequence.back() << "->" << left[0] 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << " (circular jump)" << endl;
            sequence.push_back(left[0]);
            
            for (int i = 1; i < left.size(); i++) {
                step++;
                seek = abs(left[i] - sequence.back());
                totalSeek += seek;
                cout << step << " | MOVE " << sequence.back() << "->" << left[i] 
                     << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
                sequence.push_back(left[i]);
            }
        }
    } else {
        for (int i = left.size() - 1; i >= 0; i--) {
            step++;
            int seek = abs(left[i] - sequence.back());
            totalSeek += seek;
            cout << step << " | MOVE " << sequence.back() << "->" << left[i] 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
            sequence.push_back(left[i]);
        }
        
        if (!right.empty()) {
            step++;
            int seek = abs(right.back() - sequence.back());
            totalSeek += seek;
            cout << step << " | JUMP " << sequence.back() << "->" << right.back() 
                 << " | SEEK=" << seek << " | TOTAL=" << totalSeek << " (circular jump)" << endl;
            sequence.push_back(right.back());
            
            for (int i = right.size() - 2; i >= 0; i--) {
                step++;
                seek = abs(right[i] - sequence.back());
                totalSeek += seek;
                cout << step << " | MOVE " << sequence.back() << "->" << right[i] 
                     << " | SEEK=" << seek << " | TOTAL=" << totalSeek << endl;
                sequence.push_back(right[i]);
            }
        }
    }
    
    cout << "---" << endl;
    cout << "SEQUENCE: ";
    for (int i = 0; i < sequence.size(); i++) {
        if (i > 0) cout << ",";
        cout << sequence[i];
    }
    cout << endl;
    
    cout << "TOTAL_SEEK: " << totalSeek << endl;
    cout << fixed << setprecision(2);
    cout << "AVG_SEEK: " << (double)totalSeek / requests.size() << endl;
}

int main() {
    string algorithm;
    int head, maxCylinder;
    string direction;
    
    cin >> algorithm >> head >> maxCylinder >> direction;
    
    vector<int> requests;
    int r;
    while (cin >> r) {
        requests.push_back(r);
    }
    
    if (algorithm == "SCAN") {
        runSCAN(head, maxCylinder, direction, requests);
    } else if (algorithm == "C-SCAN") {
        runCSCAN(head, maxCylinder, direction, requests);
    } else if (algorithm == "LOOK") {
        runLOOK(head, direction, requests);
    } else if (algorithm == "C-LOOK") {
        runCLOOK(head, direction, requests);
    }
    
    return 0;
}
