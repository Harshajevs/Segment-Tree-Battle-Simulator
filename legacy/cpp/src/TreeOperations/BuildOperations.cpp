#include "SegmentTree.h"
#include <algorithm>
#include <numeric>

using namespace std;

// Build sum attack segment tree
void SegmentTree::buildSumAttack(int node, int start, int end) {
    if (start == end) {
        sumAttackTree[node] = a[start].first;
        return;
    }
    int mid = (start + end) / 2;
    buildSumAttack(2 * node, start, mid);
    buildSumAttack(2 * node + 1, mid + 1, end);
    sumAttackTree[node] = sumAttackTree[2 * node] + sumAttackTree[2 * node + 1];
}

// Build sum health segment tree
void SegmentTree::buildSumHealth(int node, int start, int end) {
    if (start == end) {
        sumHealthTree[node] = a[start].second;
        return;
    }
    int mid = (start + end) / 2;
    buildSumHealth(2 * node, start, mid);
    buildSumHealth(2 * node + 1, mid + 1, end);
    sumHealthTree[node] = sumHealthTree[2 * node] + sumHealthTree[2 * node + 1];
}

// Build max attack index segment tree
void SegmentTree::buildMaxAttack(int node, int start, int end) {
    if (start == end) {
        maxAttackTreeIndex[node] = start;
        return;
    }
    int mid = (start + end) / 2;
    buildMaxAttack(2 * node, start, mid);
    buildMaxAttack(2 * node + 1, mid + 1, end);
    int leftIdx = maxAttackTreeIndex[2 * node];
    int rightIdx = maxAttackTreeIndex[2 * node + 1];
    maxAttackTreeIndex[node] = (a[leftIdx].first > a[rightIdx].first) ? leftIdx : rightIdx;
}

// Build max health index segment tree
void SegmentTree::buildMaxHealth(int node, int start, int end) {
    if (start == end) {
        maxHealthTreeIndex[node] = start;
        return;
    }
    int mid = (start + end) / 2;
    buildMaxHealth(2 * node, start, mid);
    buildMaxHealth(2 * node + 1, mid + 1, end);
    int leftIdx = maxHealthTreeIndex[2 * node];
    int rightIdx = maxHealthTreeIndex[2 * node + 1];
    maxHealthTreeIndex[node] = (a[leftIdx].second > a[rightIdx].second) ? leftIdx : rightIdx;
}

// Build min attack index segment tree
void SegmentTree::buildMinAttack(int node, int start, int end) {
    if (start == end) {
        minAttackTreeIndex[node] = start;
        return;
    }
    int mid = (start + end) / 2;
    buildMinAttack(2 * node, start, mid);
    buildMinAttack(2 * node + 1, mid + 1, end);
    int leftIdx = minAttackTreeIndex[2 * node];
    int rightIdx = minAttackTreeIndex[2 * node + 1];
    minAttackTreeIndex[node] = (a[leftIdx].first < a[rightIdx].first) ? leftIdx : rightIdx;
}

// Build min health index segment tree
void SegmentTree::buildMinHealth(int node, int start, int end) {
    if (start == end) {
        minHealthTreeIndex[node] = start;
        return;
    }
    int mid = (start + end) / 2;
    buildMinHealth(2 * node, start, mid);
    buildMinHealth(2 * node + 1, mid + 1, end);
    int leftIdx = minHealthTreeIndex[2 * node];
    int rightIdx = minHealthTreeIndex[2 * node + 1];
    minHealthTreeIndex[node] = (a[leftIdx].second < a[rightIdx].second) ? leftIdx : rightIdx;
}

// Build GCD attack segment tree
void SegmentTree::buildGcdAttack(int node, int start, int end) {
    if (start == end) {
        gcdAttackTree[node] = a[start].first;
        return;
    }
    int mid = (start + end) / 2;
    buildGcdAttack(2 * node, start, mid);
    buildGcdAttack(2 * node + 1, mid + 1, end);
    gcdAttackTree[node] = std::gcd(gcdAttackTree[2 * node], gcdAttackTree[2 * node + 1]);
}

// Build GCD health segment tree
void SegmentTree::buildGcdHealth(int node, int start, int end) {
    if (start == end) {
        gcdHealthTree[node] = a[start].second;
        return;
    }
    int mid = (start + end) / 2;
    buildGcdHealth(2 * node, start, mid);
    buildGcdHealth(2 * node + 1, mid + 1, end);
    gcdHealthTree[node] = std::gcd(gcdHealthTree[2 * node], gcdHealthTree[2 * node + 1]);
}

// Build LCM attack segment tree
void SegmentTree::buildLcmAttack(int node, int start, int end) {
    if (start == end) {
        lcmAttackTree[node] = a[start].first;
        return;
    }
    int mid = (start + end) / 2;
    buildLcmAttack(2 * node, start, mid);
    buildLcmAttack(2 * node + 1, mid + 1, end);
    lcmAttackTree[node] = lcm(lcmAttackTree[2 * node], lcmAttackTree[2 * node + 1]);
}

// Build LCM health segment tree
void SegmentTree::buildLcmHealth(int node, int start, int end) {
    if (start == end) {
        lcmHealthTree[node] = a[start].second;
        return;
    }
    int mid = (start + end) / 2;
    buildLcmHealth(2 * node, start, mid);
    buildLcmHealth(2 * node + 1, mid + 1, end);
    lcmHealthTree[node] = lcm(lcmHealthTree[2 * node], lcmHealthTree[2 * node + 1]);
}
