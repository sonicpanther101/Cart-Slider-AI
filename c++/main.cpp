#include <vector>
#include <string>
#include <random>
#include <cmath>

class Node {
public:
    Node(int id, const std::string& type = "hidden");  // Constructor

    int id;
    // Bias initialization omitted (unclear behavior in Python code)
    std::vector<int> parents;
    std::vector<int> children;
    std::vector<double> connectionWeights;
    double value;
    std::string type;
    std::string colour;  // Renamed for C++ convention

    void calculate(const std::vector<Node>& nodes);

private:
    // Helper function to set colour based on type
    void setColor();
    static std::vector<Node> nodes;
};

Node::Node(int id, const std::string& type) : id(id), type(type) {
    setColor();
};

void Node::setColor() {
    if (type == "input") {
        colour = "blue";
    } else if (type == "output") {
        colour = "red";
    } else if (type == "hidden") {
        colour = "green";
    } else {
        // Handle invalid type (optional: throw an exception)
    }
}

void Node::calculate(const std::vector<Node>& nodes) {
    // Bias initialization omitted (unclear behavior in Python code)

    if (children.empty()) {
        value = tanh(value);
    } else if (!parents.empty()) {
        value = relu(value);
    }

    for (int childID : children) {
        for (const Node& childNode : nodes) {
            if (childNode.id == childID) {
                childNode.value += value * connectionWeights[children.indexOf(childID)];
                break;  // Optimization: Exit inner loop once child is found
            }
        }
    }
}

// Implement tanh and relu functions here (replace with your preferred implementations)
double tanh(double x) {
    return std::tanh(x);
}

double relu(double x) {
    return std::max(0.0, x);
}