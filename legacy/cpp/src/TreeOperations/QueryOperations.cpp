#include "SegmentTree.h"
#include <algorithm>

// Public query interfaces
long long SegmentTree::querySumAttack(int l, int r) {
    return querySumAttack(1, 0, a.size()-1, l, r);
}

long long SegmentTree::querySumHealth(int l, int r) {
    return querySumHealth(1, 0, a.size()-1, l, r);
}

int SegmentTree::queryMaxAttackIndex(int l, int r) {
    return queryMaxAttackIndex(1, 0, a.size()-1, l, r);
}

int SegmentTree::queryMaxHealthIndex(int l, int r) {
    return queryMaxHealthIndex(1, 0, a.size()-1, l, r);
}

int SegmentTree::queryMinAttackIndex(int l, int r) {
    return queryMinAttackIndex(1, 0, a.size()-1, l, r);
}

int SegmentTree::queryMinHealthIndex(int l, int r) {
    return queryMinHealthIndex(1, 0, a.size()-1, l, r);
}

long long SegmentTree::queryGcdAttack(int l, int r) {
    return queryGcdAttack(1, 0, a.size()-1, l, r);
}

long long SegmentTree::queryGcdHealth(int l, int r) {
    return queryGcdHealth(1, 0, a.size()-1, l, r);
}

long long SegmentTree::queryLcmAttack(int l, int r) {
    return queryLcmAttack(1, 0, a.size()-1, l, r);
}

long long SegmentTree::queryLcmHealth(int l, int r) {
    return queryLcmHealth(1, 0, a.size()-1, l, r);
}


// Query sum attack
int SegmentTree::querySumAttack(int node, int start, int end, int l, int r) {
    if (start > r || end < l) return 0;
    if (l <= start && end <= r) return sumAttackTree[node];
    int mid = (start + end) / 2;
    return querySumAttack(2 * node, start, mid, l, r) +
           querySumAttack(2 * node + 1, mid + 1, end, l, r);
}

// Query sum health
int SegmentTree::querySumHealth(int node, int start, int end, int l, int r) {
    if (start > r || end < l) return 0;
    if (l <= start && end <= r) return sumHealthTree[node];
    int mid = (start + end) / 2;
    return querySumHealth(2 * node, start, mid, l, r) +
           querySumHealth(2 * node + 1, mid + 1, end, l, r);
}

// Query max attack index
int SegmentTree::queryMaxAttackIndex(int node, int start, int end, int l, int r) {
    if (start > r || end < l) return -1;
    if (l <= start && end <= r) return maxAttackTreeIndex[node];
    int mid = (start + end) / 2;
    int leftIdx = queryMaxAttackIndex(2 * node, start, mid, l, r);
    int rightIdx = queryMaxAttackIndex(2 * node + 1, mid + 1, end, l, r);
    if (leftIdx == -1) return rightIdx;
    if (rightIdx == -1) return leftIdx;
    return (a[leftIdx].first > a[rightIdx].first) ? leftIdx : rightIdx;
}

// Query max health index
int SegmentTree::queryMaxHealthIndex(int node, int start, int end, int l, int r) {
    if (start > r || end < l) return -1;
    if (l <= start && end <= r) return maxHealthTreeIndex[node];
    int mid = (start + end) / 2;
    int leftIdx = queryMaxHealthIndex(2 * node, start, mid, l, r);
    int rightIdx = queryMaxHealthIndex(2 * node + 1, mid + 1, end, l, r);
    if (leftIdx == -1) return rightIdx;
    if (rightIdx == -1) return leftIdx;
    return (a[leftIdx].second > a[rightIdx].second) ? leftIdx : rightIdx;
}

// Query min attack index
int SegmentTree::queryMinAttackIndex(int node, int start, int end, int l, int r) {
    if (start > r || end < l) return -1;
    if (l <= start && end <= r) return minAttackTreeIndex[node];
    int mid = (start + end) / 2;
    int leftIdx = queryMinAttackIndex(2 * node, start, mid, l, r);
    int rightIdx = queryMinAttackIndex(2 * node + 1, mid + 1, end, l, r);
    if (leftIdx == -1) return rightIdx;
    if (rightIdx == -1) return leftIdx;
    return (a[leftIdx].first < a[rightIdx].first) ? leftIdx : rightIdx;
}

// Query min health index
int SegmentTree::queryMinHealthIndex(int node, int start, int end, int l, int r) {
    if (start > r || end < l) return -1;
    if (l <= start && end <= r) return minHealthTreeIndex[node];
    int mid = (start + end) / 2;
    int leftIdx = queryMinHealthIndex(2 * node, start, mid, l, r);
    int rightIdx = queryMinHealthIndex(2 * node + 1, mid + 1, end, l, r);
    if (leftIdx == -1) return rightIdx;
    if (rightIdx == -1) return leftIdx;
    return (a[leftIdx].second < a[rightIdx].second) ? leftIdx : rightIdx;
}

// Query GCD attack
long long SegmentTree::queryGcdAttack(int node, int start, int end, int l, int r) {
    if (start > r || end < l) return 0;
    if (l <= start && end <= r) return gcdAttackTree[node];
    int mid = (start + end) / 2;
    long long leftGcd = queryGcdAttack(2 * node, start, mid, l, r);
    long long rightGcd = queryGcdAttack(2 * node + 1, mid + 1, end, l, r);
    return std::gcd(leftGcd, rightGcd);
}

// Query GCD health
long long SegmentTree::queryGcdHealth(int node, int start, int end, int l, int r) {
    if (start > r || end < l) return 0;
    if (l <= start && end <= r) return gcdHealthTree[node];
    int mid = (start + end) / 2;
    long long leftGcd = queryGcdHealth(2 * node, start, mid, l, r);
    long long rightGcd = queryGcdHealth(2 * node + 1, mid + 1, end, l, r);
    return std::gcd(leftGcd, rightGcd);
}

// Query LCM attack
long long SegmentTree::queryLcmAttack(int node, int start, int end, int l, int r) {
    if (start > r || end < l) return 1;
    if (l <= start && end <= r) return lcmAttackTree[node];
    int mid = (start + end) / 2;
    long long leftLcm = queryLcmAttack(2 * node, start, mid, l, r);
    long long rightLcm = queryLcmAttack(2 * node + 1, mid + 1, end, l, r);
    return lcm(leftLcm, rightLcm);
}

// Query LCM health
long long SegmentTree::queryLcmHealth(int node, int start, int end, int l, int r) {
    if (start > r || end < l) return 1;
    if (l <= start && end <= r) return lcmHealthTree[node];
    int mid = (start + end) / 2;
    long long leftLcm = queryLcmHealth(2 * node, start, mid, l, r);
    long long rightLcm = queryLcmHealth(2 * node + 1, mid + 1, end, l, r);
    return lcm(leftLcm, rightLcm);
}
