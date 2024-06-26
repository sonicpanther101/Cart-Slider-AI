#include <iostream>
#include <vector>
#include <cmath>
using namespace std;
#pragma once

vector<long double> add(const vector<long double>& vec1, const vector<long double>& vec2);
vector<long double> subtract(const vector<long double>& vec1, const vector<long double>& vec2);
vector<long double> multiply(const vector<long double>& vec1, const vector<long double>& vec2);
vector<long double> divide(const vector<long double>& vec1, const vector<long double>& vec2);
long double norm(const vector<long double> a);
long double calculateAngle(const vector<long double> coord);

class Ball {
public:

    Ball(int inputSize, vector<long double> inputPosition, vector<long double> intputVelocity, vector<long double> inputAcceleration, vector<int> inputColour, int inputId) :
        size(inputSize), position(inputPosition), acceleration(inputAcceleration), colour(inputColour), id(inputId) {
        oldPosition = subtract(position, multiply(intputVelocity, { (1 / 1000),(1 / 1000) }));
    }

    int size;
    vector<long double> position, oldPosition, acceleration;
    vector<int> colour;
    int id;
    long double angularVelocity = 0;

    Ball updatePosition(long double deltaTime, Ball cart, vector<long double> cartVelocity) {
        vector<long double> velocity = subtract(this->position, this->oldPosition);
        this->oldPosition = this->position;
        const vector<long double> dampingFactor = { 0.9997, 0.9997 };

        if (id == 0) {
            this->position = add(this->position, multiply(cartVelocity, { deltaTime,deltaTime }));
            if (-250 > this->position[0]) {
                this->position[0] = -250;
            } else if (250 < this->position[0]) {
                this->position[0] = 250;
            }
        }
        if (id == 1) {
            this->position = add(this->position, multiply(add(velocity, multiply(this->acceleration, { deltaTime * deltaTime,deltaTime * deltaTime })), dampingFactor));
            vector<long double> linearVelocity = divide(velocity, { deltaTime,deltaTime });
            long double theta = (M_PI - calculateAngle(subtract(this->position, cart.position))) - (M_PI - calculateAngle(linearVelocity));
            long double velocityTangential = sin(theta) * norm(linearVelocity);
            this->angularVelocity = velocityTangential / norm(subtract(this->position, cart.position));
        }

        return *this;
    }

    Ball accelerate(vector<long double> acc) {
        this->acceleration = add(this->acceleration, acc);
        return *this;
    }
};

vector<Ball> createBalls();

class Link {
public:
    Link(size_t inputBall1ID, size_t inputBall2ID, int inputTargetDistance, int inputThickness, vector<int> inputColour) :
        ball1ID(inputBall1ID), ball2ID(inputBall2ID), targetDistance(inputTargetDistance), thickness(inputThickness), colour(inputColour) { }

    size_t ball1ID, ball2ID;
    int targetDistance;
    int thickness;
    vector<int> colour;

    vector<Ball> apply(vector<Ball> balls) {
        vector<long double> axis = subtract(balls[ball1ID].position, balls[ball2ID].position);
        long double distance = norm(axis);
        vector<long double> normal = divide(axis, { distance, distance });
        long double delta = targetDistance - distance;

        balls[ball2ID].position = subtract(balls[ball2ID].position, multiply(normal, { delta, delta }));

        return balls;
    }
};

class Solver {
public:
    vector<long double> gravity = { 0, -0.1 };

    vector<Ball> update(vector<Link> links, vector<Ball>& balls, long double deltaTime, long double cartVelocity) {
        balls = applyGravity(balls);
        balls = solveLinks(links, balls);
        balls = updatePositions(balls, deltaTime, cartVelocity);
        return balls;
    }

    vector<Ball> applyGravity(vector<Ball>& balls) {
        for (Ball& ball : balls) {
            ball = ball.accelerate(gravity);
        }
        return balls;
    }

    vector<Ball> solveLinks(vector<Link>& links, vector<Ball> balls) {
        for (Link& link : links) {
            balls = link.apply(balls);
        }
        return balls;
    }

    vector<Ball> updatePositions(vector<Ball>& balls, long double deltaTime, long double cartVelocity) {
        for (Ball& ball : balls) {
            ball = ball.updatePosition(deltaTime, balls[0], { cartVelocity, 0 });
        }
        return balls;
    }
};

struct Environment {
    vector<Ball> balls = createBalls();
    vector<Link> links = { Link(0, 1, 100, 5, {0, 0, 255}) };
    Solver solver = Solver();
    long double cartVelocity = 0;

    vector<Ball> update(long double deltaTime) {
        balls = solver.update(links, balls, deltaTime, cartVelocity);
        return balls;
    }
};

extern Environment environment;
extern int subSteps;