#include "SegmentTree.h"
#include <algorithm>  // For std::gcd
using namespace std;

// Constructor implementation only
SegmentTree::SegmentTree(const vector<pair<int, int>>& values) : a(values) {
    int n = values.size();
    
    // Initialize all segment trees
    sumAttackTree.resize(4 * n);
    sumHealthTree.resize(4 * n);
    maxAttackTreeIndex.resize(4 * n);
    maxHealthTreeIndex.resize(4 * n);
    minAttackTreeIndex.resize(4 * n);
    minHealthTreeIndex.resize(4 * n);
    gcdAttackTree.resize(4 * n);
    gcdHealthTree.resize(4 * n);
    lcmAttackTree.resize(4 * n);
    lcmHealthTree.resize(4 * n);

    // Build calls (implementations in BuildOperations.cpp)
    buildSumAttack(1, 0, n-1);
    buildSumHealth(1, 0, n-1);
    buildMaxAttack(1, 0, n-1);
    buildMaxHealth(1, 0, n-1);
    buildMinAttack(1, 0, n-1);
    buildMinHealth(1, 0, n-1);
    buildGcdAttack(1, 0, n-1);
    buildGcdHealth(1, 0, n-1);
    buildLcmAttack(1, 0, n-1);
    buildLcmHealth(1, 0, n-1);
}

// Unique utility function
long long SegmentTree::lcm(int a, int b) {
    if(a == 0 || b == 0) return 0;
    return (long long)a * (b / gcd(a, b));
}

// Public update interface (implementation in UpdateOperations.cpp)
void SegmentTree::update(int pos, int attack, int health) {
    a[pos] = {attack, health};
    
    updateSumAttack(1, 0, a.size()-1, pos, attack);
    updateSumHealth(1, 0, a.size()-1, pos, health);
    updateMaxAttackIndex(pos, attack, a, 0, a.size()-1, 0);
    updateMaxHealthIndex(pos, health, a, 0, a.size()-1, 0);
    updateMinAttackIndex(pos, attack, a, 0, a.size()-1, 0);
    updateMinHealthIndex(pos, health, a, 0, a.size()-1, 0);
    updateGcdAttack(1, 0, a.size()-1, pos, attack);
    updateGcdHealth(1, 0, a.size()-1, pos, health);
    updateLcmAttack(1, 0, a.size()-1, pos, attack);
    updateLcmHealth(1, 0, a.size()-1, pos, health);
}
