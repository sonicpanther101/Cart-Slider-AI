#include <vector>
#include <string>
#include <random>
#include <cmath>
#include <iostream>
using namespace std;

class NodeClass {
    public:
        // Constructor with basic initialization
        NodeClass(int nodeID, const string& nodeType = "hidden") : id(nodeID), type(nodeType) {
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

        void calculate() const {
            cout << "Calculating node " << id << endl;
            // Add calculation code here
        }
};

// Function to create and initialize nodes
vector<NodeClass> createNodes(int inputNodes) {
    vector<NodeClass> nodes;

    for (int i = 0; i < inputNodes; ++i) {
        nodes.emplace_back(i, "input");
    }

    nodes.emplace_back(4, "output");

  return nodes;
}

int main() {
  // Create nodes (call the function to create and initialize nodes)
  vector<NodeClass> nodes = createNodes(4);

  // Print node information (id, type, color)
  cout << "Nodes:" << endl;
  for (const auto& node : nodes) {
    cout << node.id <<  " " << node.type << " " << node.colour << endl;

    node.calculate();
  }

  return 0;
}
