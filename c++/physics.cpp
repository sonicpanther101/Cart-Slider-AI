#include <vector>
#include <iostream>
#include "physics.h"
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

vector<Ball> createBalls() {
    vector<Ball> balls;

    balls.emplace_back(Ball(50, {0, 0}, {0, 0}, {0, 0}, {255, 0, 0}, 0));
    balls.emplace_back(Ball(50, {0, -101}, {0, 0}, {0, 0}, {0, 0, 255}, 1));

  return balls;
}

int update(long double deltaTime = 0.01) {

    environment.cartVelocity = 1234;

    if (deltaTime != 0) {
        for (int i = 0; i < 10; ++i) {
            cout << environment.balls[0].position[0] << endl;
            environment.balls = environment.update(deltaTime / subSteps);
        }
    }


    return 0;
}

Environment environment;
int subSteps;

int main() {
    environment = Environment();
    subSteps = 1;
    update(0.01);
    return 0;
}