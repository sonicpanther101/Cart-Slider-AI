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
            oldPosition = subtract(position, multiply(intputVelocity, {(1/1000),(1/1000)}));
        }

        int size;
        vector<long double> position, oldPosition, acceleration;
        vector<int> colour;
        int id;
        long double angularVelocity = 0;

        Ball updatePosition(Ball ball, long double deltaTime, Ball cart, vector<long double> cartVelocity) {
            vector<long double> velocity = subtract(ball.position, ball.oldPosition);
            ball.oldPosition = ball.position;

            if (id == 0) {
                ball.position = add(ball.position, multiply(cartVelocity, {deltaTime,deltaTime}));
                if (-250 > ball.position[0]) {
                    ball.position[0] = -250;
                } else if (250 < ball.position[0]) {
                    ball.position[0] = 250;
                }
            }
            if (id == 1) {
                ball.position = add(ball.position, add(velocity, multiply(ball.acceleration, {deltaTime*deltaTime,deltaTime*deltaTime})));
                vector<long double> linearVelocity = divide(velocity, {deltaTime,deltaTime});
                long double theta = (M_PI - calculateAngle(subtract(ball.position, cart.position))) - (M_PI - calculateAngle(linearVelocity));
                long double velocityTangential = sin(theta) * norm(linearVelocity);
                ball.angularVelocity = velocityTangential / norm(subtract(ball.position, cart.position));
            }

            return ball;
        }

        Ball accelerate(vector<long double> acc) {
            acceleration = add(acceleration, acc);
            return *this;
        }
};

vector<Ball> createBalls();

class Link {
    public:
        Link(Ball inputBall1, Ball inputBall2, int inputTargetDistance, int inputThickness, vector<int> inputColour) : 
        ball1(inputBall1), ball2(inputBall2), targetDistance(inputTargetDistance), thickness(inputThickness), colour(inputColour) {}

        Ball ball1, ball2;
        int targetDistance;
        int thickness;
        vector<int> colour;

        vector<Ball> apply() {
            vector<long double> axis = subtract(ball1.position, ball2.position);
            long double distance = norm(axis);
            vector<long double> normal = divide(axis, {distance, distance});
            long double delta = targetDistance - distance;

            ball2.position = subtract(ball2.position, multiply(normal, {delta, delta}));

            return {ball1, ball2};
        }
};

class Solver {
    public:
        vector<long double> gravity = {0, -100};

        vector<Ball> update(vector<Link> links, vector<Ball>& balls, long double deltaTime, long double cartVelocity) {
            balls = applyGravity(balls);
            balls = solveLinks(links);
            balls = updatePositions(balls, deltaTime, cartVelocity);
            return balls;
        }

        vector<Ball> applyGravity(vector<Ball>& balls) {
            for (Ball& ball : balls) {
                ball = ball.accelerate(gravity);
            }
            return balls;
        }

        vector<Ball> solveLinks(vector<Link>& links) {
            vector<Ball> balls;
            for (Link& link : links) {
                balls = link.apply();
            }
            return balls;
        }

        vector<Ball> updatePositions(vector<Ball>& balls, long double deltaTime, long double cartVelocity) {
            for (Ball& ball : balls) {
                ball = ball.updatePosition(ball, deltaTime, balls[0], {cartVelocity, 0});
            }
            return balls;
        }
};

struct Environment {
    vector<Ball> balls = createBalls();
    vector<Link> links = {Link(balls[0], balls[1], 100, 5, {0, 0, 255})};
    Solver solver = Solver();
    long double cartVelocity = 0;

    vector<Ball> update(long double deltaTime) {
        balls = solver.update(links, balls, deltaTime, cartVelocity);
        return balls;
    }
};

extern Environment environment;
extern int subSteps;