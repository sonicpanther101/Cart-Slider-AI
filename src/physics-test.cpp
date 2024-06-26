#include "physics.hpp"
#include <iostream>
#include <chrono>
#include <SDL2/SDL.h>
using namespace std;
using namespace chrono;

int update(long double deltaTime = 0.01) {

    Environment tempEnv = environment;

    tempEnv.cartVelocity = 0;

    if (deltaTime != 0) {
        for (int i = 0; i < subSteps; ++i) {
            tempEnv.balls = tempEnv.update(deltaTime / subSteps);
        }
    }


    return 0;
}

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
        result[i] = vec1[i] - vec2[i];
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

    balls.emplace_back(Ball(50, { 0, 0 }, { 0, 0 }, { 0, 0 }, { 255, 0, 0 }, 0));
    balls.emplace_back(Ball(50, { 100, 0 }, { 0, 0 }, { 0, 0 }, { 0, 0, 255 }, 1));

    return balls;
}

void DrawCircle(SDL_Renderer* renderer, int32_t x, int32_t y, int32_t radius) {
    int offsetx, offsety, d;
    int status;

    //CHECK_RENDERER_MAGIC(renderer, -1);

    offsetx = 0;
    offsety = radius;
    d = radius - 1;
    status = 0;

    while (offsety >= offsetx) {

        status += SDL_RenderDrawLine(renderer, x - offsety, y + offsetx, x + offsety, y + offsetx);
        status += SDL_RenderDrawLine(renderer, x - offsetx, y + offsety, x + offsetx, y + offsety);
        status += SDL_RenderDrawLine(renderer, x - offsetx, y - offsety, x + offsetx, y - offsety);
        status += SDL_RenderDrawLine(renderer, x - offsety, y - offsetx, x + offsety, y - offsetx);

        if (status < 0) {
            status = -1;
            break;
        }

        if (d >= 2 * offsetx) {
            d -= 2 * offsetx + 1;
            offsetx += 1;
        } else if (d < 2 * (radius - offsety)) {
            d += 2 * offsety - 1;
            offsety -= 1;
        } else {
            d += 2 * (offsety - offsetx - 1);
            offsety -= 1;
            offsetx += 1;
        }
    }
}

auto previousTime = high_resolution_clock::now();
auto currentTime = high_resolution_clock::now();
long double deltaTime;

Environment environment;
int subSteps = 1;
int frames = 0;
//size_t threadsToUse = 1;
//int step = static_cast<int>(generation.size() / threadsToUse);

int main() {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        std::cout << "Failed to initialize the SDL2 library\n";
        return -1;
    }

    SDL_Window* window = SDL_CreateWindow("SDL2 Window",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        680, 480,
        0);

    if (!window) {
        std::cout << "Failed to create window\n";
        return -1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);  // Corrected line

    if (!renderer) {
        std::cout << "Failed to create renderer\n";
        return -1;
    }

    // Set the render draw color (optional)
    SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255); // Red color

    // Clear the renderer with the draw color
    //SDL_RenderClear(renderer);

    while (frames <= 1000) {
        //++frames;

        currentTime = high_resolution_clock::now();
        deltaTime = duration_cast<duration<long double>>(currentTime - previousTime).count();
        previousTime = currentTime;

        if (deltaTime >= 0.01) {
            deltaTime = 0;
        }

        cout << environment.balls[0].position[0] << " : " << -environment.balls[0].position[1] << endl;
        cout << environment.balls[1].position[0] << " : " << -environment.balls[1].position[1] << endl;
        //cout << deltaTime << endl;

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);

        DrawCircle(renderer, environment.balls[0].position[0] + 340, -environment.balls[0].position[1] + 340, 30);
        DrawCircle(renderer, environment.balls[1].position[0] + 340, -environment.balls[1].position[1] + 340, 30);

        SDL_RenderPresent(renderer);

        environment.cartVelocity = 10;

        environment.update(deltaTime);
    }

    SDL_Delay(1000);

    return 0;
}