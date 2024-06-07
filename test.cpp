#include <vector>
#include <iostream>
using namespace std;

int main() {
    vector<int> test = {1,2,3,4,5};
    vector<int> test2 = {6,7,8,9,10};
    vector<int> test3 = {11,12,13,14,15};

    test2 = test3;
    test3[0] = 0;

    cout << test2[0] << endl;
    cout << test3[0] << endl;

    return 0;
}