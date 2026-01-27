// File: backend/os/cpu/fcfs.cpp
// First Come First Serve CPU Scheduling with structured output
#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <sstream>
using namespace std;

struct Process {
    int id;
    int arrival;
    int burst;
    int start;
    int finish;
    int waiting;
    int turnaround;
};

int main() {
    int n;
    cin >> n;
    
    vector<Process> processes(n);
    for (int i = 0; i < n; i++) {
        processes[i].id = i + 1;
        cin >> processes[i].arrival >> processes[i].burst;
    }
    
    // Sort by arrival time
    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.arrival < b.arrival;
    });
    
    // Output header
    cout << "ALGORITHM: FCFS" << endl;
    cout << "PROCESSES: " << n << endl;
    cout << "---" << endl;
    
    int currentTime = 0;
    int step = 0;
    stringstream gantt;
    int contextSwitches = 0;
    int lastProcess = -1;
    
    for (auto& p : processes) {
        if (currentTime < p.arrival) {
            // CPU idle
            step++;
            cout << step << " | IDLE | TIME=" << currentTime << "-" << p.arrival 
                 << " | GANTT:IDLE" << endl;
            currentTime = p.arrival;
        }
        
        p.start = currentTime;
        p.finish = currentTime + p.burst;
        p.waiting = p.start - p.arrival;
        p.turnaround = p.finish - p.arrival;
        
        // Count context switch
        if (lastProcess != -1 && lastProcess != p.id) {
            contextSwitches++;
        }
        lastProcess = p.id;
        
        step++;
        cout << step << " | EXEC P" << p.id << " | TIME=" << p.start << "-" << p.finish 
             << " | GANTT:P" << p.id << endl;
        
        if (gantt.str().length() > 0) gantt << ",";
        gantt << "P" << p.id;
        
        currentTime = p.finish;
    }
    
    cout << "---" << endl;
    cout << "RESULTS:" << endl;
    
    double totalWaiting = 0, totalTurnaround = 0;
    
    // Sort by ID for output
    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.id < b.id;
    });
    
    for (const auto& p : processes) {
        cout << "P" << p.id << " | AT=" << p.arrival << " | BT=" << p.burst 
             << " | ST=" << p.start << " | FT=" << p.finish 
             << " | WT=" << p.waiting << " | TAT=" << p.turnaround << endl;
        totalWaiting += p.waiting;
        totalTurnaround += p.turnaround;
    }
    
    cout << "---" << endl;
    cout << fixed << setprecision(2);
    cout << "AVG_WT: " << totalWaiting / n << endl;
    cout << "AVG_TAT: " << totalTurnaround / n << endl;
    cout << "CONTEXT_SWITCHES: " << contextSwitches << endl;
    cout << "TOTAL_TIME: " << currentTime << endl;
    cout << "GANTT: " << gantt.str() << endl;
    
    return 0;
}
