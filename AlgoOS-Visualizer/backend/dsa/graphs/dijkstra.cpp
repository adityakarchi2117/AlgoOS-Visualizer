// File: backend/dsa/graphs/dijkstra.cpp
// Dijkstra's Shortest Path Algorithm with step-by-step visualization output
// Format: STEP | OPERATION | LINE | STATE | META

#include <iostream>
#include <vector>
#include <queue>
#include <climits>
#include <string>
#include <sstream>
using namespace std;

struct Edge {
    int to, weight;
    Edge(int t, int w) : to(t), weight(w) {}
};

class VisualDijkstra {
private:
    vector<vector<Edge>> graph;
    vector<int> dist;
    vector<int> parent;
    vector<bool> visited;
    int vertices;
    int step;
    
    string getDistState() const {
        stringstream ss;
        ss << "DIST:[";
        for (int i = 0; i < vertices; i++) {
            if (i > 0) ss << ",";
            if (dist[i] == INT_MAX) {
                ss << "INF";
            } else {
                ss << dist[i];
            }
        }
        ss << "]";
        return ss.str();
    }
    
    string getVisitedState() const {
        stringstream ss;
        ss << "VISITED:[";
        for (int i = 0; i < vertices; i++) {
            if (i > 0) ss << ",";
            ss << (visited[i] ? "T" : "F");
        }
        ss << "]";
        return ss.str();
    }
    
    void output(const string& operation, int line, const string& meta) {
        cout << step++ << " | " << operation << " | " << line << " | " 
             << getDistState() << "," << getVisitedState() << " | " << meta << endl;
    }

public:
    VisualDijkstra(int v) : vertices(v), step(1) {
        graph.resize(v);
        dist.resize(v, INT_MAX);
        parent.resize(v, -1);
        visited.resize(v, false);
        output("INIT", __LINE__, "VERTICES=" + to_string(v));
    }
    
    void addEdge(int from, int to, int weight) {
        graph[from].push_back(Edge(to, weight));
        output("ADD_EDGE", __LINE__, "FROM=" + to_string(from) + ",TO=" + to_string(to) + ",WEIGHT=" + to_string(weight));
    }
    
    void dijkstra(int source) {
        // Initialize
        fill(dist.begin(), dist.end(), INT_MAX);
        fill(parent.begin(), parent.end(), -1);
        fill(visited.begin(), visited.end(), false);
        
        dist[source] = 0;
        output("SET_SOURCE", __LINE__, "SOURCE=" + to_string(source) + ",DISTANCE=0");
        
        // Priority queue: pair<distance, vertex>
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        pq.push({0, source});
        
        while (!pq.empty()) {
            int u = pq.top().second;
            int d = pq.top().first;
            pq.pop();
            
            if (visited[u]) {
                output("SKIP", __LINE__, "VERTEX=" + to_string(u) + ",REASON=ALREADY_VISITED");
                continue;
            }
            
            visited[u] = true;
            output("VISIT", __LINE__, "VERTEX=" + to_string(u) + ",DISTANCE=" + to_string(d));
            
            // Explore neighbors
            for (const Edge& edge : graph[u]) {
                int v = edge.to;
                int weight = edge.weight;
                
                if (!visited[v]) {
                    int newDist = dist[u] + weight;
                    string oldDist = (dist[v] == INT_MAX) ? "INF" : to_string(dist[v]);
                    
                    if (newDist < dist[v]) {
                        dist[v] = newDist;
                        parent[v] = u;
                        pq.push({newDist, v});
                        output("RELAX", __LINE__, "FROM=" + to_string(u) + ",TO=" + to_string(v) + ",OLD=" + oldDist + ",NEW=" + to_string(newDist) + ",UPDATED=true");
                    } else {
                        output("CHECK", __LINE__, "FROM=" + to_string(u) + ",TO=" + to_string(v) + ",CURRENT=" + oldDist + ",NEW=" + to_string(newDist) + ",UPDATED=false");
                    }
                }
            }
        }
        
        output("COMPLETE", __LINE__, "SOURCE=" + to_string(source));
        
        // Print paths
        for (int i = 0; i < vertices; i++) {
            if (i != source) {
                stringstream path;
                vector<int> pathNodes;
                int curr = i;
                while (curr != -1) {
                    pathNodes.push_back(curr);
                    curr = parent[curr];
                }
                
                for (int j = pathNodes.size() - 1; j >= 0; j--) {
                    if (j < (int)pathNodes.size() - 1) path << "->";
                    path << pathNodes[j];
                }
                
                string distStr = (dist[i] == INT_MAX) ? "INF" : to_string(dist[i]);
                output("PATH", __LINE__, "TO=" + to_string(i) + ",DISTANCE=" + distStr + ",PATH=" + path.str());
            }
        }
    }
};

int main() {
    int vertices, edges;
    cin >> vertices >> edges;
    
    VisualDijkstra graph(vertices);
    
    for (int i = 0; i < edges; i++) {
        int from, to, weight;
        cin >> from >> to >> weight;
        graph.addEdge(from, to, weight);
    }
    
    int source;
    cin >> source;
    
    graph.dijkstra(source);
    
    return 0;
}
