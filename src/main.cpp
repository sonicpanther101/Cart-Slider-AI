#include "neural_network.hpp"
#include "physics.hpp"
#include <iostream>
#include <chrono>
#include <vector>
using namespace std;

auto previousTime = high_resolution_clock::now();
auto currentTime = high_resolution_clock::now();
long double deltaTime = 1 / 100;

vector<Agent> agents[1000];
int subSteps = 1;
int frames = 0;

size_t threadsToUse = 1;
int step = (int)(agents[0].generation.size() / threadsToUse);

int main() {

    while (frames <= 1000) {
        //++frames;

        /*currentTime = high_resolution_clock::now();
        deltaTime = duration_cast<duration<long double>>(currentTime - previousTime).count();
        previousTime = currentTime;

        if (deltaTime >= 0.01) {
            deltaTime = 0;
        }*/

        for (size_t i = 0; i < agents.size(); i++) {

            agents[i].environment.update(deltaTime);

            agents[i].brain[0].value = agents[i].environment.balls[0].position[0];
            agents[i].brain[1].value = agents[i].environment.balls[0].position[0];
            agents[i].brain[2].value = agents[i].environment.balls[0].position[0];
            agents[i].brain[3].value = agents[i].environment.balls[0].position[0];
        }


        environment.cartVelocity = 10;

        return 0;
    }
