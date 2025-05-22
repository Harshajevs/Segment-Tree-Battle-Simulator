#ifndef SEGMENTTREE_H
#define SEGMENTTREE_H

#include <vector>
#include <utility>
#include <algorithm>
#include <numeric>
using namespace std;

class SegmentTree {
private:
    vector<pair<int, int>> a; // attack, health
    vector<int> sumAttackTree, sumHealthTree;
    vector<int> maxAttackTreeIndex, maxHealthTreeIndex;
    vector<int> minAttackTreeIndex, minHealthTreeIndex;
    vector<int> gcdAttackTree, gcdHealthTree;
    vector<long long> lcmAttackTree, lcmHealthTree;

    // Build functions
    void buildSumAttack(int node, int start, int end);
    void buildSumHealth(int node, int start, int end);
    void buildMaxAttack(int node, int start, int end);
    void buildMaxHealth(int node, int start, int end);
    void buildMinAttack(int node, int start, int end);
    void buildMinHealth(int node, int start, int end);
    void buildGcdAttack(int node, int start, int end);
    void buildGcdHealth(int node, int start, int end);
    void buildLcmAttack(int node, int start, int end);
    void buildLcmHealth(int node, int start, int end);

    // Query helpers
    int querySumAttack(int node, int start, int end, int l, int r);
    int querySumHealth(int node, int start, int end, int l, int r);
    int queryMaxAttackIndex(int node, int start, int end, int l, int r);
    int queryMaxHealthIndex(int node, int start, int end, int l, int r);
    int queryMinAttackIndex(int node, int start, int end, int l, int r);
    int queryMinHealthIndex(int node, int start, int end, int l, int r);
    long long queryGcdAttack(int node, int start, int end, int l, int r);
    long long queryGcdHealth(int node, int start, int end, int l, int r);
    long long queryLcmAttack(int node, int start, int end, int l, int r);
    long long queryLcmHealth(int node, int start, int end, int l, int r);

    // Update helpers
    void updateSumAttack(int node, int start, int end, int pos, int value);
    void updateSumHealth(int node, int start, int end, int pos, int value);
    void updateMaxAttackIndex(int index, int value, vector<pair<int, int>>& a, int start, int end, int node);
    void updateMaxHealthIndex(int index, int value, vector<pair<int, int>>& a, int start, int end, int node);
    void updateMinAttackIndex(int index, int value, vector<pair<int, int>>& a, int start, int end, int node);
    void updateMinHealthIndex(int index, int value, vector<pair<int, int>>& a, int start, int end, int node);
    void updateGcdAttack(int node, int start, int end, int pos, int value);
    void updateGcdHealth(int node, int start, int end, int pos, int value);
    void updateLcmAttack(int node, int start, int end, int pos, int value);
    void updateLcmHealth(int node, int start, int end, int pos, int value);


    // Utility
    long long lcm(int a, int b);

public:
    explicit SegmentTree(const vector<pair<int, int>>& values);
    long long querySumAttack(int l, int r);
    long long querySumHealth(int l, int r);
    int queryMaxAttackIndex(int l, int r);
    int queryMaxHealthIndex(int l, int r);
    int queryMinAttackIndex(int l, int r);
    int queryMinHealthIndex(int l, int r);
    long long queryGcdAttack(int l, int r);
    long long queryGcdHealth(int l, int r);
    long long queryLcmAttack(int l, int r);
    long long queryLcmHealth(int l, int r);
    void update(int pos, int attack, int health);
};

#endif
