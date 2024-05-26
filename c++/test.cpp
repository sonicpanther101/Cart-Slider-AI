#include <vector>
#include <string>
#include <random>
#include <cmath>
#include <iostream>
#include <bits/stdc++.h> 
using namespace std;

template <typename S>
ostream& operator<<(ostream& os, const vector<S>& vector) {
    // Printing all the elements
    // using <<
    for (auto element : vector) {
        os << element << " ";
    }
    return os;
}

template <typename T>
std::string join(const std::vector<T>& vector, const std::string& delimiter) {
    std::stringstream ss;
    for (const auto& element : vector) {
        ss << element << delimiter;
    }
    std::string result = ss.str();
    if (!result.empty()) {
        result.erase(result.size() - delimiter.size()); // Remove the last delimiter
    }
    return result;
}

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
        mt19937 mt{};
        double bias = mt();
        double value = 0;
        vector<int> parents;
        vector<int> children;
        vector<double> connectionWeights;
        string type;
        string colour;
};

size_t getIndexFromID(vector<NodeClass> nodes, int id) {
    for (size_t i = 0; i < nodes.size(); ++i) {
        if (nodes[i].id == id) {
            return i;
        }
    }

    return static_cast<size_t>(-1);
}

vector<NodeClass> calculate(vector<NodeClass> nodes, NodeClass node) {
    cout << "Calculating node " << node.id << endl;

    if (node.type == "output") {
        node.value = tanh(node.value);
    } else {
        node.value = max(0.0, node.value);
    }

    for (int& childID : node.children) {
        for (NodeClass& childNode : nodes) {
            if (childNode.id == childID) {
                childNode.value += node.value * node.connectionWeights[static_cast<vector<double>::size_type>(find(node.connectionWeights.begin(), node.connectionWeights.end(), childID) - node.connectionWeights.begin())];
            }
        }
    }

    return nodes;
}

vector<NodeClass> removeNode(vector<NodeClass> nodes, size_t nodeIndex) {
    unique_ptr<vector<NodeClass>> tempNodes = make_unique<vector<NodeClass>>(move(nodes));

    tempNodes->erase(tempNodes->begin() + static_cast<int>(nodeIndex));

    for (const double& childID : nodes[nodeIndex].children) {

        for (NodeClass& childNode : *tempNodes) {
            if (childNode.id == childID) {

                childNode.parents.erase(find(childNode.parents.begin(), childNode.parents.end(), nodes[nodeIndex].id));
            }
        }
    }

    return *tempNodes;
}

vector<NodeClass> sortNodes(vector<NodeClass> nodes) {

    vector<NodeClass> sortedNodes;
    unique_ptr<vector<NodeClass>> tempNodes = make_unique<vector<NodeClass>>(move(nodes));

    while (tempNodes->size() > 0) {
        
        vector<NodeClass> nodesToProcess;
        vector<int> nodeIndexesToRemove;

        for (size_t i = 0; i < nodes.size(); ++i) {
            if ((*tempNodes)[i].parents.empty()) {

                size_t realIndex = getIndexFromID(nodes, (*tempNodes)[i].id);
                nodesToProcess.push_back(nodes[realIndex]);
                nodeIndexesToRemove.push_back(static_cast<int>(i));
            }
        }

        sort(nodeIndexesToRemove.begin(), nodeIndexesToRemove.end(), greater<>());
        for (const int& nodeIndex : nodeIndexesToRemove) {
            *tempNodes = removeNode(*tempNodes, static_cast<size_t>(nodeIndex));
        }

        for (const NodeClass& node : nodesToProcess) {
            sortedNodes.push_back(node);
        }
    }

    return sortedNodes;
}



// Function to create and initialize nodes
vector<NodeClass> createNodes(int inputNodes) {
    vector<NodeClass> nodes;

    for (int i = 0; i < inputNodes; ++i) {
        nodes.emplace_back(i, "input");
    }

    nodes.emplace_back(4, "output");

  return nodes;
}

void printNodeInfo(NodeClass node) {
    vector<pair<string, string>> variableMap = {
        {"id", to_string(node.id)},
        {"parents", "[" + join(node.parents, ", ") + "]"},
        {"children", "[" + join(node.children, ", ") + "]"},
        {"connectionWeights", "[" + join(node.connectionWeights, ", ") + "]"},
        {"bias", to_string(node.bias)},
        {"type", node.type},
        {"value", to_string(node.value)},
        {"colour", node.colour}
    };

    cout << "{ ";
    for (const auto& pair : variableMap) {
        cout << pair.first << ": " << pair.second << ", ";
    }
    cout << "\b\b }" << endl; // Remove the last ", " and print the closing brace
}

void printNodesInfo(vector<NodeClass> nodes) {
    for (NodeClass& node : nodes) {
        printNodeInfo(node);
    }
}

vector<NodeClass> calculateNodes(vector<NodeClass> nodes) {
    for (NodeClass& node : nodes) {
        nodes = calculate(nodes, node);
    }
    return nodes;
}

vector<NodeClass> resetNodes(vector<NodeClass> nodes) {
    for (NodeClass& node : nodes) {
        node.value = 0;
    }
    return nodes;
}

void printNodesOrder(vector<NodeClass> nodes) {
    vector<int> nodesOrder;

    for (NodeClass& node : nodes) {
        nodesOrder.push_back(node.id);
    }

    cout << "[" << join(nodesOrder, ", ") << "]" << endl;
}

int main() {
    // Create nodes (call the function to create and initialize nodes)
    vector<NodeClass> nodes = createNodes(4);
    nodes[0].connectionWeights = {1.0, 1.0, 1.0, 1.0};
    nodes[0].children = {4};
    nodes[4].parents = {0};
    nodes[0].value = 5.0;

    // Print node information (id, type, color)
    cout << "Nodes:" << endl;
    nodes = sortNodes(nodes);
    printNodesOrder(nodes);

    return 0;
}