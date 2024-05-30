#include <vector>
#include <iostream>
#include "physics.h"
using namespace std;

Environment environment = Environment();
long double deltaTime = 0.01;
int subSteps = 1;

int main() {

    environment.cartVelocity = 1234;

    if (deltaTime != 0) {
        for (int i = 0; i < 10; ++i) {
            cout << environment.balls[0].position[0] << endl;
            environment.balls = environment.update(deltaTime / subSteps);
        }
    }


    return 0;
}