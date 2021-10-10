
#include <fstream>
#include <iostream>
#include <iterator>
#include <numeric>
#include <vector>
#include <set>

using namespace std;

namespace day01 {

    void calculate() {
        cout << "Day 01" << endl;

        std::ifstream infile("input01.txt");
        vector<int> inputs(std::istream_iterator<int>{infile}, {});

        auto sum = accumulate(inputs.begin(), inputs.end(), 0, 
            [](int sum, int v) { 
            return sum + v; 
        });

        cout << "Part1: " << sum << endl;

        auto len = inputs.size();

        set<int> visited;

        int current = 0;
        int idx = 0;

        while (visited.find(current) == visited.end()) {
            visited.insert(current);
            current += inputs[idx];
            idx = (idx + 1) % len;
        }

        cout << "Part2: " << current << endl;
    };

};
