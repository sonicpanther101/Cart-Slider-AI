#include <vector>
#include <string>
#include <random>
#include <cmath>
#include <iostream>
using namespace std;

class Node {
    public:
        // Constructor with basic initialization
        Node(int nodeID, const string& nodeType = "hidden") : id(nodeID), type(nodeType) {
            if (type == "input") {
                colour = "red";
            } else if (type == "output") {
                colour = "blue";
            } else if (type == "hidden") {
                colour = "green";
            } else {
                colour = "unknown"; // Handle unexpected node types
            }
        }

        int id;
        int value = 0;
        vector<int> parents;
        vector<int> children;
        vector<double> connectionWeights;
        string type;
        string colour;
};

// Function to create and initialize nodes
vector<Node> createNodes() {
    vector<Node> nodes;

    for (int i = 0; i < 4; ++i) {
        nodes.emplace_back(i, "input");
    }

    nodes.emplace_back(4, "output");

  return nodes;
}

int main() {
  // Create nodes (call the function to create and initialize nodes)
  vector<Node> nodes = createNodes();

  // Print node information (id, type, color)
  cout << "Nodes:" << endl;
  for (const auto& node : nodes) {
    cout << node.id <<  " " << node.type << " " << node.colour << endl;
  }

  return 0;
}
