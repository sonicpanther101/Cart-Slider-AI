#include <vector>
#include <string>
#include <random>
#include <cmath>
#include <iostream>
#include <sstream>
#include <algorithm>
#include<ctime>
#include "NodeClass.h"
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
string join(const vector<T>& vector, const string& delimiter) {
    stringstream ss;
    for (const auto& element : vector) {
        ss << element << delimiter;
    }
    string result = ss.str();
    if (!result.empty()) {
        result.erase(result.size() - delimiter.size()); // Remove the last delimiter
    }
    return result;
}

size_t getIndexFromID(vector<NodeClass> nodes, int id) {
    for (size_t i = 0; i < nodes.size(); ++i) {
        if (nodes[i].id == id) {
            return i;
        }
    }

    return static_cast<size_t>(-1);
}

vector<NodeClass> calculate(vector<NodeClass> nodes, NodeClass node) {
    node.value += node.bias;

    if (node.type == "output") { // hyperbolic tangent
        node.value = tanh(node.value);
    } else { // ReLU
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
    vector<NodeClass> tempNodes(nodes);

    tempNodes.erase(tempNodes.begin() + static_cast<int>(nodeIndex));

    for (const double& childID : nodes[nodeIndex].children) {

        for (NodeClass& childNode : tempNodes) {
            if (childNode.id == childID) {

                childNode.parents.erase(find(childNode.parents.begin(), childNode.parents.end(), nodes[nodeIndex].id));
            }
        }
    }

    return tempNodes;
}

vector<NodeClass> sortNodes(vector<NodeClass> nodes) {

    vector<NodeClass> tempNodes(nodes);
    vector<NodeClass> sortedNodes;

    while (tempNodes.size() > 0) {
                
        vector<NodeClass> nodesToProcess;
        vector<int> nodeIndexesToRemove;

        for (size_t i = 0; i < tempNodes.size(); ++i) {
            if ((tempNodes)[i].parents.empty()) {

                size_t realIndex = getIndexFromID(nodes, (tempNodes)[i].id);
                nodesToProcess.push_back(nodes[realIndex]);
                nodeIndexesToRemove.push_back(static_cast<int>(i));
            }
        }

        sort(nodeIndexesToRemove.begin(), nodeIndexesToRemove.end(), greater<>());
        for (const int& nodeIndex : nodeIndexesToRemove) {
            tempNodes = removeNode(tempNodes, static_cast<size_t>(nodeIndex));
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

struct Agent {
  vector<NodeClass> brain = sortNodes(createNodes(4));
  //vector</*Physics environment type*/> environment;  // Replace with the environment type
  double fitness = 0;
  string mostRecentMutation = "";
};

bool anyBrainHasChildren(const Agent& agent) {
    for (const NodeClass& node : agent.brain) {
        if (!node.children.empty()) {
            return true;
        }
    }
    return false;
}

vector<Agent> mutateAgents(vector<Agent> agentsToMutate) {
    
    vector<Agent> mutatedAgents;

    for (Agent& agentTemp : agentsToMutate) {
        Agent agent(agentTemp);

        vector<int> options = {0,1,4};
        vector<int> unusableNodes;
        int tries = 0;
        size_t randomNodeIndexBias;
        size_t node1Index;
        size_t node2Index;
        size_t randomNode1Index;
        size_t randomNode2Index;
        size_t childIndex;
        int randomNode1ID;
        int randomNode2ID;
        int newNodeID;

        if (anyBrainHasChildren(agent)) {
            options.push_back(2);
            options.push_back(3);
        }

        switch ((size_t)rand() % options.size()) {
            case 0:
                //cout << "Nothing" << endl;
                agent.mostRecentMutation = "Nothing";
                break;
            
            case 1:
                //cout << "New Connection" << endl;

                while (tries < 100) {
                    ++tries;

                    node1Index = (size_t)rand() % agent.brain.size();
                    node2Index = (size_t)rand() % agent.brain.size();

                    if (node1Index < node2Index 
&& ((agent.brain[node1Index].type == "input") + (agent.brain[node2Index].type == "input") <= 1)
&& ((agent.brain[node1Index].type == "output") + (agent.brain[node2Index].type == "output") <= 1)
&& (find(agent.brain[node1Index].children.begin(), agent.brain[node1Index].children.end(), agent.brain[node2Index].id) == agent.brain[node1Index].children.end())
&& (find(agent.brain[node2Index].parents.begin(), agent.brain[node2Index].parents.end(), agent.brain[node1Index].id) == agent.brain[node2Index].parents.end())) {
                        break;
                    }
                }

                if (tries != 100) {
                    agent.brain[node1Index].children.push_back(agent.brain[node2Index].id);
                    agent.brain[node1Index].connectionWeights.push_back((((double)rand() / (RAND_MAX))*2.0) - 1.0);
                    agent.brain[node2Index].parents.push_back(agent.brain[node1Index].id);

                    agent.mostRecentMutation = "New Connection between nodes " + to_string(agent.brain[node1Index].id) + " and " + to_string(agent.brain[node2Index].id);
                }
                break;

            case 2:
                //cout << "New Node" << endl;

                while (unusableNodes.size() != agent.brain.size() && tries < 100) {
                    ++tries;

                    randomNode1Index = (size_t)rand() % (agent.brain.size() - 1); // -1 to avout output node

                    if (agent.brain[randomNode1Index].children.empty()) {
                        unusableNodes.push_back(agent.brain[randomNode1Index].id);
                        continue;
                    }

                    randomNode2ID = agent.brain[randomNode1Index].children[(size_t)rand() % agent.brain[randomNode1Index].children.size()];
                    randomNode2Index = getIndexFromID(agent.brain, randomNode2ID);
                    randomNode1ID = agent.brain[randomNode1Index].id;
                    newNodeID = static_cast<int>(agent.brain.size());
                    
                    // check if nodes are connected
                    if (
(find(agent.brain[randomNode1Index].children.begin(), agent.brain[randomNode1Index].children.end(), randomNode2ID) == agent.brain[randomNode1Index].children.end()) || 
(find(agent.brain[randomNode2Index].parents.begin(), agent.brain[randomNode2Index].parents.end(), randomNode1ID) == agent.brain[randomNode2Index].parents.end())) {
                        continue;
                    }

                    // Break the old connection
                    childIndex = static_cast<size_t>(find(agent.brain[randomNode1Index].children.begin(), agent.brain[randomNode1Index].children.end(), randomNode2ID) - (agent.brain[randomNode1Index].children.begin()));
                    agent.brain[randomNode1Index].children.erase(agent.brain[randomNode1Index].children.begin() + static_cast<int>(childIndex));
                    agent.brain[randomNode1Index].connectionWeights.erase(agent.brain[randomNode1Index].connectionWeights.begin() + static_cast<int>(childIndex));
                    agent.brain[randomNode2Index].parents.erase(find(agent.brain[randomNode2Index].parents.begin(), agent.brain[randomNode2Index].parents.end(), randomNode1ID));

                    // Add the new connection
                    agent.brain[randomNode1Index].children.push_back(newNodeID);
                    agent.brain[randomNode1Index].connectionWeights.push_back((((double)rand() / (RAND_MAX))*2.0) - 1.0);
                    agent.brain[randomNode2Index].parents.push_back(randomNode1ID);

                    // Add the new node
                    agent.brain.push_back(NodeClass(newNodeID));
                    agent.brain[agent.brain.size() - 1].parents.push_back(randomNode1ID);
                    agent.brain[agent.brain.size() - 1].children.push_back(randomNode2ID);
                    agent.brain[agent.brain.size() - 1].connectionWeights.push_back((((double)rand() / (RAND_MAX))*2.0) - 1.0);
                    agent.mostRecentMutation = "New Node between nodes " + to_string(randomNode1ID) + " and " + to_string(randomNode2ID);

                }

                break;

            case 3:
                //cout << "Weight Modification" << endl;

                while (unusableNodes.size() != agent.brain.size() && tries < 100) {
                    ++tries;

                    size_t randomNodeIndex = (size_t)rand() % (agent.brain.size() - 1); // -1 to avout output node

                    if (agent.brain[randomNodeIndex].connectionWeights.empty()) {
                        unusableNodes.push_back(agent.brain[randomNodeIndex].id);
                        continue;
                    }

                    size_t randomWeightIndex = (size_t)rand() % agent.brain[randomNodeIndex].connectionWeights.size();

                    agent.brain[randomNodeIndex].connectionWeights[randomWeightIndex] += (((double)rand() / (RAND_MAX))*2.0) - 1.0;
                    agent.mostRecentMutation = "Weight Modification of node " + to_string(agent.brain[randomNodeIndex].id) + " connection " + to_string(agent.brain[randomNodeIndex].connectionWeights[randomWeightIndex]);
                }
                break;

            case 4:
                //cout << "Bias Modification" << endl;
                randomNodeIndexBias = (size_t)rand() % agent.brain.size();

                agent.brain[randomNodeIndexBias].bias = (((double)rand() / (RAND_MAX))*2.0) - 1.0;
                agent.mostRecentMutation = "Bias Modification of node " + to_string(agent.brain[randomNodeIndexBias].id);
                break;

            default:
                cout << "Bug" << endl;
                break;
        }
    }

    return mutatedAgents;
}

int main() {

    srand(static_cast<unsigned int>(time(0)));

    // Create nodes (call the function to create and initialize nodes)
    const int populationSize = 1000;
    vector<Agent> generation(populationSize);
    /*for (int i = 0; i < 4; ++i) {
        nodes.emplace_back(i+5);
    }
    nodes[0].children = {5,7};
    nodes[1].children = {7};
    nodes[2].children = {8};
    nodes[3].children = {7,8};

    nodes[7].parents = {0,1,3};
    nodes[7].children = {5,6,8};

    nodes[5].parents = {0,7};
    nodes[5].children = {4};
    nodes[6].parents = {7};
    nodes[6].children = {4};
    nodes[8].parents = {2,3,7};
    nodes[8].children = {4};

    nodes[4].parents = {5,6,8};*/

    // Print node information (id, type, color)
    cout << "Nodes:" << endl;
    printNodesInfo(generation[0].brain);
    generation[0].brain = sortNodes(generation[0].brain);
    printNodesOrder(generation[0].brain);

    return 0;
}