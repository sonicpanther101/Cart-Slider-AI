#include <neural_network.hpp>
#include <physics.hpp>
#include <iostream>
#include <chrono>
using namespace std;

long double previousTime = 0;
long double startTime
    = std::chrono::duration_cast<std::chrono::duration<long double>>(
        std::chrono::system_clock::now().time_since_epoch()).count();
long double deltaTime = 0;
int threadsToUse = 1;
int step = static_cast<int>(nn.generation.size()/threadsToUse);

int main() {


    return 0;
}