#include <iostream>
#include <vector>
using namespace std;
#pragma once

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
        double bias = (((double)rand() / (RAND_MAX))*2.0) - 1.0;
        double value = 0;
        vector<int> parents;
        vector<int> children;
        vector<double> connectionWeights;
        string type;
        string colour;
};

struct Agent {
  vector<NodeClass> brain = sortNodes(createNodes(4));
  //vector</*Physics environment type*/> environment;  // Replace with the environment type
  double fitness = 0;
  string mostRecentMutation = "";
};

size_t getIndexFromID(vector<NodeClass> nodes, int id);
vector<NodeClass> calculate(vector<NodeClass> nodes, NodeClass node);
vector<NodeClass> removeNode(vector<NodeClass> nodes, size_t nodeIndex);
vector<NodeClass> sortNodes(vector<NodeClass> nodes);
vector<NodeClass> createNodes(int inputNodes);
void printNodeInfo(NodeClass node);
void printNodesInfo(vector<NodeClass> nodes);
vector<NodeClass> calculateNodes(vector<NodeClass> nodes);
vector<NodeClass> resetNodes(vector<NodeClass> nodes);
void printNodesOrder(vector<NodeClass> nodes);
bool anyBrainHasChildren(const Agent& agent);
vector<Agent> mutateAgents(vector<Agent> agentsToMutate);