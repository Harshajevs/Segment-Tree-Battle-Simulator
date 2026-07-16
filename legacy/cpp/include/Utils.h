#ifndef UTILS_H
#define UTILS_H

#include <vector>

namespace GameUtils {
    int gcd(int a, int b);
    long long lcm(int a, int b);
    int gcdRange(const std::vector<int>& nums, int l, int r);
    long long lcmRange(const std::vector<int>& nums, int l, int r);
}

#endif
