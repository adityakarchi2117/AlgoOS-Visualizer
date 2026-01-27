// File: backend/os/deadlock/bankers.cpp
// Banker's Algorithm for Deadlock Avoidance
#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>
using namespace std;

int main() {
    int n, m;  // n processes, m resource types
    cin >> n >> m;
    
    vector<vector<int>> allocation(n, vector<int>(m));
    vector<vector<int>> maximum(n, vector<int>(m));
    vector<vector<int>> need(n, vector<int>(m));
    vector<int> available(m);
    
    // Read allocation matrix
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> allocation[i][j];
        }
    }
    
    // Read maximum matrix
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> maximum[i][j];
        }
    }
    
    // Read available
    for (int j = 0; j < m; j++) {
        cin >> available[j];
    }
    
    // Calculate need matrix
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            need[i][j] = maximum[i][j] - allocation[i][j];
        }
    }
    
    // Output header
    cout << "PROCESSES: " << n << endl;
    cout << "RESOURCES: " << m << endl;
    cout << "---" << endl;
    
    // Output matrices
    cout << "ALLOCATION:" << endl;
    for (int i = 0; i < n; i++) {
        cout << "  P" << i << " [";
        for (int j = 0; j < m; j++) {
            if (j > 0) cout << ",";
            cout << allocation[i][j];
        }
        cout << "]" << endl;
    }
    
    cout << "MAXIMUM:" << endl;
    for (int i = 0; i < n; i++) {
        cout << "  P" << i << " [";
        for (int j = 0; j < m; j++) {
            if (j > 0) cout << ",";
            cout << maximum[i][j];
        }
        cout << "]" << endl;
    }
    
    cout << "NEED:" << endl;
    for (int i = 0; i < n; i++) {
        cout << "  P" << i << " [";
        for (int j = 0; j < m; j++) {
            if (j > 0) cout << ",";
            cout << need[i][j];
        }
        cout << "]" << endl;
    }
    
    cout << "AVAILABLE: [";
    for (int j = 0; j < m; j++) {
        if (j > 0) cout << ",";
        cout << available[j];
    }
    cout << "]" << endl;
    
    cout << "---" << endl;
    cout << "SAFETY CHECK:" << endl;
    
    // Safety algorithm
    vector<int> work = available;
    vector<bool> finish(n, false);
    vector<int> safeSequence;
    int step = 0;
    
    while (safeSequence.size() < n) {
        bool found = false;
        
        for (int i = 0; i < n; i++) {
            if (finish[i]) continue;
            
            // Check if need <= work
            bool canAllocate = true;
            for (int j = 0; j < m; j++) {
                if (need[i][j] > work[j]) {
                    canAllocate = false;
                    break;
                }
            }
            
            step++;
            
            if (canAllocate) {
                cout << step << " | CHECK P" << i << " | NEED=[";
                for (int j = 0; j < m; j++) {
                    if (j > 0) cout << ",";
                    cout << need[i][j];
                }
                cout << "] <= WORK=[";
                for (int j = 0; j < m; j++) {
                    if (j > 0) cout << ",";
                    cout << work[j];
                }
                cout << "] | CAN_ALLOCATE" << endl;
                
                // Release resources
                for (int j = 0; j < m; j++) {
                    work[j] += allocation[i][j];
                }
                
                step++;
                cout << step << " | RELEASE P" << i << " | WORK=[";
                for (int j = 0; j < m; j++) {
                    if (j > 0) cout << ",";
                    cout << work[j];
                }
                cout << "]" << endl;
                
                finish[i] = true;
                safeSequence.push_back(i);
                found = true;
                break;
            } else {
                cout << step << " | CHECK P" << i << " | NEED=[";
                for (int j = 0; j < m; j++) {
                    if (j > 0) cout << ",";
                    cout << need[i][j];
                }
                cout << "] > WORK=[";
                for (int j = 0; j < m; j++) {
                    if (j > 0) cout << ",";
                    cout << work[j];
                }
                cout << "] | CANNOT_ALLOCATE" << endl;
            }
        }
        
        if (!found) {
            break;
        }
    }
    
    cout << "---" << endl;
    
    if (safeSequence.size() == n) {
        cout << "STATE: SAFE" << endl;
        cout << "SAFE_SEQUENCE: ";
        for (int i = 0; i < safeSequence.size(); i++) {
            if (i > 0) cout << "->";
            cout << "P" << safeSequence[i];
        }
        cout << endl;
    } else {
        cout << "STATE: UNSAFE" << endl;
        cout << "BLOCKED_PROCESSES: ";
        bool first = true;
        for (int i = 0; i < n; i++) {
            if (!finish[i]) {
                if (!first) cout << ",";
                cout << "P" << i;
                first = false;
            }
        }
        cout << endl;
    }
    
    return 0;
}
