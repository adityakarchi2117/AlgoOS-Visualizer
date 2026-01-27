// File: backend/os/cpu/round_robin.cpp
// Round Robin CPU Scheduling with Time Quantum
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <iomanip>
#include <sstream>
#include <climits>
using namespace std;

struct Process {
    int id;
    int arrival;
    int burst;
    int remaining;
    int start;
    int finish;
    int waiting;
    int turnaround;
    bool started;
};

int main() {
    int n, quantum;
    cin >> n >> quantum;
    
    vector<Process> processes(n);
    for (int i = 0; i < n; i++) {
        processes[i].id = i + 1;
        cin >> processes[i].arrival >> processes[i].burst;
        processes[i].remaining = processes[i].burst;
        processes[i].started = false;
        processes[i].start = -1;
    }
    
    // Sort by arrival
    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.arrival < b.arrival;
    });
    
    cout << "ALGORITHM: Round Robin" << endl;
    cout << "QUANTUM: " << quantum << endl;
    cout << "PROCESSES: " << n << endl;
    cout << "---" << endl;
    
    queue<int> readyQueue;
    vector<bool> inQueue(n, false);
    
    int currentTime = 0;
    int completedCount = 0;
    int step = 0;
    int contextSwitches = 0;
    int lastProcess = -1;
    stringstream gantt;
    
    // Add first arriving processes
    for (int i = 0; i < n; i++) {
        if (processes[i].arrival <= currentTime && !inQueue[i]) {
            readyQueue.push(i);
            inQueue[i] = true;
        }
    }
    
    while (completedCount < n) {
        if (readyQueue.empty()) {
            // Find next arriving process
            int nextArrival = INT_MAX;
            int nextIdx = -1;
            for (int i = 0; i < n; i++) {
                if (processes[i].remaining > 0 && processes[i].arrival < nextArrival) {
                    nextArrival = processes[i].arrival;
                    nextIdx = i;
                }
            }
            
            if (nextIdx != -1) {
                step++;
                cout << step << " | IDLE | TIME=" << currentTime << "-" << nextArrival 
                     << " | GANTT:IDLE" << endl;
                currentTime = nextArrival;
                readyQueue.push(nextIdx);
                inQueue[nextIdx] = true;
            }
            continue;
        }
        
        int idx = readyQueue.front();
        readyQueue.pop();
        
        Process& p = processes[idx];
        
        if (!p.started) {
            p.start = currentTime;
            p.started = true;
        }
        
        if (lastProcess != -1 && lastProcess != p.id) {
            contextSwitches++;
        }
        lastProcess = p.id;
        
        int execTime = min(quantum, p.remaining);
        int startTime = currentTime;
        currentTime += execTime;
        p.remaining -= execTime;
        
        step++;
        cout << step << " | EXEC P" << p.id << " | TIME=" << startTime << "-" << currentTime 
             << " | REMAINING=" << p.remaining << endl;
        
        if (gantt.str().length() > 0) gantt << ",";
        gantt << "P" << p.id;
        
        // Add newly arrived processes to queue
        for (int i = 0; i < n; i++) {
            if (!inQueue[i] && processes[i].arrival <= currentTime && processes[i].remaining > 0) {
                readyQueue.push(i);
                inQueue[i] = true;
            }
        }
        
        if (p.remaining == 0) {
            p.finish = currentTime;
            p.turnaround = p.finish - p.arrival;
            p.waiting = p.turnaround - p.burst;
            completedCount++;
        } else {
            readyQueue.push(idx);
        }
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
    
    return 0;
}
