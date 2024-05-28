#include <vector>
#include <iostream>
#include <math.h>
#include <cmath>
#include <map>
using namespace std;

vector<long double> add(const vector<long double>& vec1, const vector<long double>& vec2) {
    if (vec1.size() != vec2.size()) {
        throw length_error("Vectors must have the same size for addition");
    }
    vector<long double> result(vec1.size());
    for (size_t i = 0; i < vec1.size(); ++i) {
        result[i] = vec1[i] + vec2[i];
    }
    return result;
}

vector<long double> subtract(const vector<long double>& vec1, const vector<long double>& vec2) {
    if (vec1.size() != vec2.size()) {
        throw length_error("Vectors must have the same size for subtraction");
    }
    vector<long double> result(vec1.size());
    for (size_t i = 0; i < vec1.size(); ++i) {
        result[i] = vec1[i] + vec2[i];
    }
    return result;
}

vector<long double> multiply(const vector<long double>& vec1, const vector<long double>& vec2) {
  if (vec1.size() != vec2.size()) {
    // Handle different sizes (throw exception or return empty vector)
    throw length_error("Vectors must have the same size for element-wise multiplication");
  }
  vector<long double> result(vec1.size());
  for (size_t i = 0; i < vec1.size(); ++i) {
    result[i] = vec1[i] * vec2[i];
  }
  return result;
}

vector<long double> divide(const vector<long double>& vec1, const vector<long double>& vec2) {
  if (vec1.size() != vec2.size()) {
    // Handle different sizes (throw exception or return empty vector)
    throw length_error("Vectors must have the same size for element-wise division");
  }
  vector<long double> result(vec1.size());
  for (size_t i = 0; i < vec1.size(); ++i) {
    result[i] = vec1[i] / vec2[i];
  }
  return result;
}

long double norm(const vector<long double> a) {
    long double total = 0;
    size_t length = a.size();
    for (size_t i = 0; i < length; i++) {
        total += a[i] * a[i];
    }
    return sqrt(total);
}

long double calculateAngle(const vector<long double> coord) {

    long double x = coord[0];
    long double y = coord[1];

    if (x == 0 && y == 0) {
        return 0;
    }
    if (x == 0) {
        if (y > 0) {
            return M_PI / 2;
        } else {
            return 3 * M_PI / 2;
        }
    }
    if (y == 0) {
        if (x > 0) {
            return 0.0;
        } else {
            return M_PI;
        }
    }

    long double angle = atan2(y, x);

    if (angle < 0) {
        angle += 2 * M_PI;
    }

    return angle;
}

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

        map<string, vector<long double>> updatePosition(long double deltaTime, Ball cart, vector<long double> cartVelocity) {
            vector<long double> velocity = subtract(position, oldPosition);
            oldPosition = position;

            if (id == 0) {
                position = add(position, multiply(cartVelocity, {deltaTime,deltaTime}));
                cout << position[0] << endl;
                if (-250 > position[0]) {
                    position[0] = -250;
                } else if (250 < position[0]) {
                    position[0] = 250;
                }
            }
            if (id == 1) {
                position = add(position, add(velocity, multiply(acceleration, {deltaTime*deltaTime,deltaTime*deltaTime})));
                vector<long double> linearVelocity = divide(velocity, {deltaTime,deltaTime});
                long double theta = (M_PI - calculateAngle(subtract(position, cart.position))) - (M_PI - calculateAngle(linearVelocity));
                long double velocityTangential = sin(theta) * norm(linearVelocity);
                angularVelocity = velocityTangential / norm(subtract(position, cart.position));
            }

            map<string, vector<long double>> mapOfValues;
            mapOfValues["position"] = position;
            mapOfValues["oldPosition"] = oldPosition;
            mapOfValues["angularVelocity"] = {angularVelocity, angularVelocity};
            return mapOfValues;
        }

        Ball accelerate(vector<long double> acc) {
            acceleration = add(acceleration, acc);
            return *this;
        }
};

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

        vector<Ball> update(vector<Link> links, vector<Ball> balls, long double deltaTime, long double cartVelocity) {
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
                map<string, vector<long double>> mapOfValues = ball.updatePosition(deltaTime, balls[0], {cartVelocity, 0});

                ball.position = mapOfValues["position"];
                ball.oldPosition = mapOfValues["oldPosition"];
                ball.angularVelocity = mapOfValues["angularVelocity"][0];
            }
            return balls;
        }
};


// Function to create and initialize balls
vector<Ball> createBalls() {
    vector<Ball> balls;

    balls.emplace_back(Ball(50, {0, 0}, {0, 0}, {0, 0}, {255, 0, 0}, 0));
    balls.emplace_back(Ball(50, {0, -101}, {0, 0}, {0, 0}, {0, 0, 255}, 1));

  return balls;
}

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

int main() {

    Environment environment = Environment();
    environment.cartVelocity = 1234;
    long double deltaTime = 0.01;
    int subSteps = 1;

    if (deltaTime != 0) {
        for (int i = 0; i < 10; ++i) {
            environment.balls = environment.update(deltaTime / subSteps);
        }
    }

    cout << environment.balls[0].position[0] << endl;

    return 0;
}