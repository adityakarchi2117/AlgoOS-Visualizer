// File: backend/os/cpu/sjf.cpp
// Shortest Job First (Non-Preemptive) and SRTF (Preemptive)
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <climits>
#include <iomanip>
#include <sstream>
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

void runNonPreemptive(vector<Process>& processes) {
    int n = processes.size();
    vector<bool> completed(n, false);
    int currentTime = 0;
    int completedCount = 0;
    int step = 0;
    int contextSwitches = 0;
    int lastProcess = -1;
    stringstream gantt;
    
    cout << "ALGORITHM: SJF (Non-Preemptive)" << endl;
    cout << "PROCESSES: " << n << endl;
    cout << "---" << endl;
    
    while (completedCount < n) {
        int shortest = -1;
        int minBurst = INT_MAX;
        
        for (int i = 0; i < n; i++) {
            if (!completed[i] && processes[i].arrival <= currentTime) {
                if (processes[i].burst < minBurst) {
                    minBurst = processes[i].burst;
                    shortest = i;
                }
            }
        }
        
        if (shortest == -1) {
            // Find next arriving process
            int nextArrival = INT_MAX;
            for (int i = 0; i < n; i++) {
                if (!completed[i] && processes[i].arrival < nextArrival) {
                    nextArrival = processes[i].arrival;
                }
            }
            step++;
            cout << step << " | IDLE | TIME=" << currentTime << "-" << nextArrival 
                 << " | GANTT:IDLE" << endl;
            currentTime = nextArrival;
            continue;
        }
        
        Process& p = processes[shortest];
        p.start = currentTime;
        p.finish = currentTime + p.burst;
        p.waiting = p.start - p.arrival;
        p.turnaround = p.finish - p.arrival;
        
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
        completed[shortest] = true;
        completedCount++;
    }
    
    cout << "---" << endl;
    cout << "RESULTS:" << endl;
    
    double totalWaiting = 0, totalTurnaround = 0;
    
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
}

void runPreemptive(vector<Process>& processes) {
    int n = processes.size();
    int currentTime = 0;
    int completedCount = 0;
    int step = 0;
    int contextSwitches = 0;
    int lastProcess = -1;
    stringstream gantt;
    
    for (auto& p : processes) {
        p.remaining = p.burst;
        p.started = false;
        p.start = -1;
    }
    
    cout << "ALGORITHM: SRTF (Preemptive SJF)" << endl;
    cout << "PROCESSES: " << n << endl;
    cout << "---" << endl;
    
    while (completedCount < n) {
        int shortest = -1;
        int minRemaining = INT_MAX;
        
        for (int i = 0; i < n; i++) {
            if (processes[i].arrival <= currentTime && processes[i].remaining > 0) {
                if (processes[i].remaining < minRemaining) {
                    minRemaining = processes[i].remaining;
                    shortest = i;
                }
            }
        }
        
        if (shortest == -1) {
            int nextArrival = INT_MAX;
            for (int i = 0; i < n; i++) {
                if (processes[i].remaining > 0 && processes[i].arrival < nextArrival) {
                    nextArrival = processes[i].arrival;
                }
            }
            currentTime = nextArrival;
            continue;
        }
        
        Process& p = processes[shortest];
        
        if (!p.started) {
            p.start = currentTime;
            p.started = true;
        }
        
        if (lastProcess != -1 && lastProcess != p.id) {
            contextSwitches++;
        }
        lastProcess = p.id;
        
        // Find when we might need to switch
        int runUntil = currentTime + p.remaining;
        for (int i = 0; i < n; i++) {
            if (i != shortest && processes[i].arrival > currentTime && 
                processes[i].arrival < runUntil && processes[i].remaining > 0) {
                if (processes[i].burst < p.remaining - (processes[i].arrival - currentTime)) {
                    runUntil = processes[i].arrival;
                }
            }
        }
        
        int execTime = runUntil - currentTime;
        
        step++;
        cout << step << " | EXEC P" << p.id << " | TIME=" << currentTime << "-" << runUntil 
             << " | REMAINING=" << (p.remaining - execTime) << endl;
        
        if (gantt.str().length() > 0) gantt << ",";
        gantt << "P" << p.id;
        
        p.remaining -= execTime;
        currentTime = runUntil;
        
        if (p.remaining == 0) {
            p.finish = currentTime;
            p.turnaround = p.finish - p.arrival;
            p.waiting = p.turnaround - p.burst;
            completedCount++;
        }
    }
    
    cout << "---" << endl;
    cout << "RESULTS:" << endl;
    
    double totalWaiting = 0, totalTurnaround = 0;
    
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
}

int main() {
    string mode;
    cin >> mode;
    
    int n;
    cin >> n;
    
    vector<Process> processes(n);
    for (int i = 0; i < n; i++) {
        processes[i].id = i + 1;
        cin >> processes[i].arrival >> processes[i].burst;
    }
    
    // Sort by arrival initially
    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.arrival < b.arrival || (a.arrival == b.arrival && a.id < b.id);
    });
    
    if (mode == "PREEMPTIVE") {
        runPreemptive(processes);
    } else {
        runNonPreemptive(processes);
    }
    
    return 0;
}
