// File: backend/os/memory/fifo.cpp
// FIFO Page Replacement Algorithm
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <iomanip>
#include <sstream>
using namespace std;

int main() {
    int numFrames;
    cin >> numFrames;
    
    vector<int> pages;
    int page;
    while (cin >> page) {
        pages.push_back(page);
    }
    
    cout << "ALGORITHM: FIFO" << endl;
    cout << "FRAMES: " << numFrames << endl;
    cout << "PAGES: " << pages.size() << endl;
    cout << "---" << endl;
    
    vector<int> frames(numFrames, -1);
    queue<int> fifoOrder;
    int faults = 0;
    int hits = 0;
    
    for (int i = 0; i < pages.size(); i++) {
        int p = pages[i];
        
        // Check if page is in frames
        bool found = false;
        for (int f : frames) {
            if (f == p) {
                found = true;
                break;
            }
        }
        
        // Build frames string
        stringstream frameStr;
        frameStr << "[";
        for (int j = 0; j < numFrames; j++) {
            if (j > 0) frameStr << ",";
            if (frames[j] == -1) frameStr << "-";
            else frameStr << frames[j];
        }
        frameStr << "]";
        
        if (found) {
            hits++;
            cout << (i + 1) << " | PAGE " << p << " | HIT | FRAMES:" << frameStr.str() << endl;
        } else {
            faults++;
            int replaced = -1;
            
            // Check for empty frame
            int emptyIdx = -1;
            for (int j = 0; j < numFrames; j++) {
                if (frames[j] == -1) {
                    emptyIdx = j;
                    break;
                }
            }
            
            if (emptyIdx != -1) {
                frames[emptyIdx] = p;
                fifoOrder.push(p);
            } else {
                replaced = fifoOrder.front();
                fifoOrder.pop();
                fifoOrder.push(p);
                
                for (int j = 0; j < numFrames; j++) {
                    if (frames[j] == replaced) {
                        frames[j] = p;
                        break;
                    }
                }
            }
            
            // Build new frames string
            stringstream newFrameStr;
            newFrameStr << "[";
            for (int j = 0; j < numFrames; j++) {
                if (j > 0) newFrameStr << ",";
                if (frames[j] == -1) newFrameStr << "-";
                else newFrameStr << frames[j];
            }
            newFrameStr << "]";
            
            cout << (i + 1) << " | PAGE " << p << " | FAULT | FRAMES:" << newFrameStr.str();
            if (replaced != -1) {
                cout << " | REPLACED:" << replaced;
            }
            cout << endl;
        }
    }
    
    cout << "---" << endl;
    cout << "TOTAL_FAULTS: " << faults << endl;
    cout << "TOTAL_HITS: " << hits << endl;
    cout << fixed << setprecision(2);
    cout << "FAULT_RATE: " << (100.0 * faults / pages.size()) << endl;
    cout << "HIT_RATE: " << (100.0 * hits / pages.size()) << endl;
    
    return 0;
}
