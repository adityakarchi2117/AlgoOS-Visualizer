// File: backend/os/memory/lru.cpp
// LRU (Least Recently Used) Page Replacement
#include <iostream>
#include <vector>
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
    
    cout << "ALGORITHM: LRU" << endl;
    cout << "FRAMES: " << numFrames << endl;
    cout << "PAGES: " << pages.size() << endl;
    cout << "---" << endl;
    
    vector<int> frames(numFrames, -1);
    vector<int> lastUsed(numFrames, -1);  // Time when each frame was last used
    int faults = 0;
    int hits = 0;
    
    for (int i = 0; i < pages.size(); i++) {
        int p = pages[i];
        
        // Check if page is in frames
        int foundIdx = -1;
        for (int j = 0; j < numFrames; j++) {
            if (frames[j] == p) {
                foundIdx = j;
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
        
        if (foundIdx != -1) {
            hits++;
            lastUsed[foundIdx] = i;
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
                lastUsed[emptyIdx] = i;
            } else {
                // Find LRU frame
                int lruIdx = 0;
                for (int j = 1; j < numFrames; j++) {
                    if (lastUsed[j] < lastUsed[lruIdx]) {
                        lruIdx = j;
                    }
                }
                replaced = frames[lruIdx];
                frames[lruIdx] = p;
                lastUsed[lruIdx] = i;
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
