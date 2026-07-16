#include "SegmentTree.h"
#include <algorithm>

// Update sum attack at position
void SegmentTree::updateSumAttack(int node, int start, int end, int pos, int value) {
    if (start == end) {
        sumAttackTree[node] = value;
        return;
    }
    int mid = (start + end) / 2;
    if (pos <= mid)
        updateSumAttack(2 * node, start, mid, pos, value);
    else
        updateSumAttack(2 * node + 1, mid + 1, end, pos, value);
    sumAttackTree[node] = sumAttackTree[2 * node] + sumAttackTree[2 * node + 1];
}

// Update sum health at position
void SegmentTree::updateSumHealth(int node, int start, int end, int pos, int value) {
    if (start == end) {
        sumHealthTree[node] = value;
        return;
    }
    int mid = (start + end) / 2;
    if (pos <= mid)
        updateSumHealth(2 * node, start, mid, pos, value);
    else
        updateSumHealth(2 * node + 1, mid + 1, end, pos, value);
    sumHealthTree[node] = sumHealthTree[2 * node] + sumHealthTree[2 * node + 1];
}

// Update max attack index
void SegmentTree::updateMaxAttackIndex(int index, int value, vector<pair<int, int>> &a, int start, int end, int node) {
    if (start == end) {
        a[index].first = value;
        maxAttackTreeIndex[node] = index;
        return;
    }
    int mid = (start + end) / 2;
    if (index <= mid)
        updateMaxAttackIndex(index, value, a, start, mid, 2 * node);
    else
        updateMaxAttackIndex(index, value, a, mid + 1, end, 2 * node + 1);
    int leftIdx = maxAttackTreeIndex[2 * node];
    int rightIdx = maxAttackTreeIndex[2 * node + 1];
    maxAttackTreeIndex[node] = (a[leftIdx].first > a[rightIdx].first) ? leftIdx : rightIdx;
}

// Update max health index
void SegmentTree::updateMaxHealthIndex(int index, int value, vector<pair<int, int>> &a, int start, int end, int node) {
    if (start == end) {
        a[index].second = value;
        maxHealthTreeIndex[node] = index;
        return;
    }
    int mid = (start + end) / 2;
    if (index <= mid)
        updateMaxHealthIndex(index, value, a, start, mid, 2 * node);
    else
        updateMaxHealthIndex(index, value, a, mid + 1, end, 2 * node + 1);
    int leftIdx = maxHealthTreeIndex[2 * node];
    int rightIdx = maxHealthTreeIndex[2 * node + 1];
    maxHealthTreeIndex[node] = (a[leftIdx].second > a[rightIdx].second) ? leftIdx : rightIdx;
}

// Update min attack index
void SegmentTree::updateMinAttackIndex(int index, int value, vector<pair<int, int>> &a, int start, int end, int node) {
    if (start == end) {
        a[index].first = value;
        minAttackTreeIndex[node] = index;
        return;
    }
    int mid = (start + end) / 2;
    if (index <= mid)
        updateMinAttackIndex(index, value, a, start, mid, 2 * node);
    else
        updateMinAttackIndex(index, value, a, mid + 1, end, 2 * node + 1);
    int leftIdx = minAttackTreeIndex[2 * node];
    int rightIdx = minAttackTreeIndex[2 * node + 1];
    minAttackTreeIndex[node] = (a[leftIdx].first < a[rightIdx].first) ? leftIdx : rightIdx;
}

// Update min health index
void SegmentTree::updateMinHealthIndex(int index, int value, vector<pair<int, int>> &a, int start, int end, int node) {
    if (start == end) {
        a[index].second = value;
        minHealthTreeIndex[node] = index;
        return;
    }
    int mid = (start + end) / 2;
    if (index <= mid)
        updateMinHealthIndex(index, value, a, start, mid, 2 * node);
    else
        updateMinHealthIndex(index, value, a, mid + 1, end, 2 * node + 1);
    int leftIdx = minHealthTreeIndex[2 * node];
    int rightIdx = minHealthTreeIndex[2 * node + 1];
    minHealthTreeIndex[node] = (a[leftIdx].second < a[rightIdx].second) ? leftIdx : rightIdx;
}

// Update GCD attack (corrected parameter names)
void SegmentTree::updateGcdAttack(int node, int start, int end, int pos, int value) {
    if (start == end) {
        gcdAttackTree[node] = value;
        return;
    }
    
    int mid = (start + end) / 2;
    if (pos <= mid)
        updateGcdAttack(2 * node, start, mid, pos, value);
    else
        updateGcdAttack(2 * node + 1, mid + 1, end, pos, value);
    
    gcdAttackTree[node] = gcd(gcdAttackTree[2 * node], gcdAttackTree[2 * node + 1]);
}

// Update GCD health (corrected parameter names)
void SegmentTree::updateGcdHealth(int node, int start, int end, int pos, int value) {
    if (start == end) {
        gcdHealthTree[node] = value;
        return;
    }
    
    int mid = (start + end) / 2;
    if (pos <= mid)
        updateGcdHealth(2 * node, start, mid, pos, value);
    else
        updateGcdHealth(2 * node + 1, mid + 1, end, pos, value);
    
    gcdHealthTree[node] = gcd(gcdHealthTree[2 * node], gcdHealthTree[2 * node + 1]);
}

// Update LCM attack (corrected parameter names)
void SegmentTree::updateLcmAttack(int node, int start, int end, int pos, int value) {
    if (start == end) {
        lcmAttackTree[node] = value;
        return;
    }
    
    int mid = (start + end) / 2;
    if (pos <= mid)
        updateLcmAttack(2 * node, start, mid, pos, value);
    else
        updateLcmAttack(2 * node + 1, mid + 1, end, pos, value);
    
    lcmAttackTree[node] = lcm(lcmAttackTree[2 * node], lcmAttackTree[2 * node + 1]);
}

// Update LCM health (corrected parameter names)
void SegmentTree::updateLcmHealth(int node, int start, int end, int pos, int value) {
    if (start == end) {
        lcmHealthTree[node] = value;
        return;
    }
    
    int mid = (start + end) / 2;
    if (pos <= mid)
        updateLcmHealth(2 * node, start, mid, pos, value);
    else
        updateLcmHealth(2 * node + 1, mid + 1, end, pos, value);
    
    lcmHealthTree[node] = lcm(lcmHealthTree[2 * node], lcmHealthTree[2 * node + 1]);
}