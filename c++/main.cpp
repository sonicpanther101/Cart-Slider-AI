#include "neural_network.h"
#include "physics.h"
#include <iostream>
#include <chrono>
using namespace std;

long double previousTime = 0;
long double startTime
    = chrono::duration_cast<chrono::duration<long double>>(
        chrono::system_clock::now().time_since_epoch()).count();
long double deltaTime = 0;
size_t threadsToUse = 1;
int step = static_cast<int>(generation.size()/threadsToUse);

int main() {


    return 0;
}