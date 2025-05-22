#ifndef TREE_OPERATIONS_H
#define TREE_OPERATIONS_H

#include <vector>
#include <algorithm>
#include <numeric>
#include <utility>
#include <climits>


namespace TreeOperations {

// Base operations structure
struct BaseOps {
    static int mid(int start, int end) { return start + (end - start)/2; }
    static int left(int node) { return 2 * node + 1; }
    static int right(int node) { return 2 * node + 2; }
};

// Utility functions
namespace Utils {
    static int gcd(int a, int b) { return std::gcd(a, b); }
    
    static long long lcm(int a, int b) {
        if(a == 0 || b == 0) return 0;
        return (long long)a * (b / std::gcd(a, b));
    }
};

// Sum operations template
template<typename DataType, typename ValueType>
struct Sum {
    static void build(int node, int start, int end, 
                    std::vector<int>& tree, 
                    const std::vector<DataType>& data,
                    ValueType (DataType::*valueMember)() const) {
        if(start == end) {
            tree[node] = (data[start].*valueMember)();
            return;
        }
        int m = BaseOps::mid(start, end);
        build(BaseOps::left(node), start, m, tree, data, valueMember);
        build(BaseOps::right(node), m+1, end, tree, data, valueMember);
        tree[node] = tree[BaseOps::left(node)] + tree[BaseOps::right(node)];
    }

    static int query(int node, int start, int end, int l, int r,
                    const std::vector<int>& tree) {
        if(start > r || end < l) return 0;
        if(l <= start && end <= r) return tree[node];
        
        int m = BaseOps::mid(start, end);
        return query(BaseOps::left(node), start, m, l, r, tree) +
               query(BaseOps::right(node), m+1, end, l, r, tree);
    }

    static void update(int node, int start, int end, int pos, int value,
                      std::vector<int>& tree) {
        if(start == end) {
            tree[node] = value;
            return;
        }
        
        int m = BaseOps::mid(start, end);
        if(pos <= m)
            update(BaseOps::left(node), start, m, pos, value, tree);
        else
            update(BaseOps::right(node), m+1, end, pos, value, tree);
        
        tree[node] = tree[BaseOps::left(node)] + tree[BaseOps::right(node)];
    }
};

// Max/Min index operations template
template<typename DataType, typename ValueType, bool IsMax>
struct IndexOp {
    static void build(int node, int start, int end,
                     std::vector<int>& tree,
                     const std::vector<DataType>& data,
                     ValueType (DataType::*valueMember)() const) {
        if(start == end) {
            tree[node] = start;
            return;
        }
        
        int m = BaseOps::mid(start, end);
        build(BaseOps::left(node), start, m, tree, data, valueMember);
        build(BaseOps::right(node), m+1, end, tree, data, valueMember);
        
        const auto& leftVal = (data[tree[BaseOps::left(node)]].*valueMember)();
        const auto& rightVal = (data[tree[BaseOps::right(node)]].*valueMember)();
        
        if constexpr (IsMax) {
            tree[node] = (leftVal > rightVal) ? tree[BaseOps::left(node)] 
                                            : tree[BaseOps::right(node)];
        } else {
            tree[node] = (leftVal < rightVal) ? tree[BaseOps::left(node)] 
                                            : tree[BaseOps::right(node)];
        }
    }

    static int query(int node, int start, int end, int l, int r,
                    const std::vector<int>& tree,
                    const std::vector<DataType>& data,
                    ValueType (DataType::*valueMember)() const) {
        if(start > r || end < l) return -1;
        if(l <= start && end <= r) return tree[node];
        
        int m = BaseOps::mid(start, end);
        int left = query(BaseOps::left(node), start, m, l, r, tree, data, valueMember);
        int right = query(BaseOps::right(node), m+1, end, l, r, tree, data, valueMember);
        
        if(left == -1) return right;
        if(right == -1) return left;
        
        const auto& leftVal = (data[left].*valueMember)();
        const auto& rightVal = (data[right].*valueMember)();
        
        if constexpr (IsMax) {
            return (leftVal > rightVal) ? left : right;
        } else {
            return (leftVal < rightVal) ? left : right;
        }
    }

    static void update(int index, int value, 
                      std::vector<DataType>& data,
                      int start, int end, int node,
                      std::vector<int>& tree,
                      void (DataType::*setter)(ValueType),
                      ValueType (DataType::*getter)() const) {
        if(start == end) {
            (data[index].*setter)(value);
            tree[node] = index;
            return;
        }
        
        int m = BaseOps::mid(start, end);
        if(index <= m)
            update(index, value, data, start, m, BaseOps::left(node), tree, setter, getter);
        else
            update(index, value, data, m+1, end, BaseOps::right(node), tree, setter, getter);
        
        const auto& leftVal = (data[tree[BaseOps::left(node)]].*getter)();
        const auto& rightVal = (data[tree[BaseOps::right(node)]].*getter)();
        
        if constexpr (IsMax) {
            tree[node] = (leftVal > rightVal) ? tree[BaseOps::left(node)] 
                                            : tree[BaseOps::right(node)];
        } else {
            tree[node] = (leftVal < rightVal) ? tree[BaseOps::left(node)] 
                                            : tree[BaseOps::right(node)];
        }
    }
};

// GCD operations
struct GCD {
    template<typename DataType, typename ValueType>
    static void build(int node, int start, int end,
                     std::vector<int>& tree,
                     const std::vector<DataType>& data,
                     ValueType (DataType::*valueMember)() const) {
        if(start == end) {
            tree[node] = (data[start].*valueMember)();
            return;
        }
        
        int m = BaseOps::mid(start, end);
        build(BaseOps::left(node), start, m, tree, data, valueMember);
        build(BaseOps::right(node), m+1, end, tree, data, valueMember);
        tree[node] = Utils::gcd(tree[BaseOps::left(node)], 
                              tree[BaseOps::right(node)]);
    }

    static int query(int node, int start, int end, int l, int r,
                    const std::vector<int>& tree) {
        if(start > r || end < l) return 0;
        if(l <= start && end <= r) return tree[node];
        
        int m = BaseOps::mid(start, end);
        return Utils::gcd(query(BaseOps::left(node), start, m, l, r, tree),
                        query(BaseOps::right(node), m+1, end, l, r, tree));
    }

    template<typename DataType, typename ValueType>
    static void update(int node, int start, int end, int pos, int value,
                      std::vector<int>& tree,
                      std::vector<DataType>& data,
                      void (DataType::*setter)(ValueType),
                      ValueType (DataType::*getter)() const) {
        if(start == end) {
            (data[pos].*setter)(value);
            tree[node] = value;
            return;
        }
        
        int m = BaseOps::mid(start, end);
        if(pos <= m)
            update(BaseOps::left(node), start, m, pos, value, tree, data, setter, getter);
        else
            update(BaseOps::right(node), m+1, end, pos, value, tree, data, setter, getter);
        
        tree[node] = Utils::gcd(tree[BaseOps::left(node)], 
                              tree[BaseOps::right(node)]);
    }
};

// LCM operations
struct LCM {
    template<typename DataType, typename ValueType>
    static void build(int node, int start, int end,
                     std::vector<int>& tree,
                     const std::vector<DataType>& data,
                     ValueType (DataType::*valueMember)() const) {
        if(start == end) {
            tree[node] = (data[start].*valueMember)();
            return;
        }
        
        int m = BaseOps::mid(start, end);
        build(BaseOps::left(node), start, m, tree, data, valueMember);
        build(BaseOps::right(node), m+1, end, tree, data, valueMember);
        tree[node] = Utils::lcm(tree[BaseOps::left(node)], 
                              tree[BaseOps::right(node)]);
    }

    static int query(int node, int start, int end, int l, int r,
                    const std::vector<int>& tree) {
        if(start > r || end < l) return 1;
        if(l <= start && end <= r) return tree[node];
        
        int m = BaseOps::mid(start, end);
        return Utils::lcm(query(BaseOps::left(node), start, m, l, r, tree),
                        query(BaseOps::right(node), m+1, end, l, r, tree));
    }

    template<typename DataType, typename ValueType>
    static void update(int node, int start, int end, int pos, int value,
                      std::vector<int>& tree,
                      std::vector<DataType>& data,
                      void (DataType::*setter)(ValueType),
                      ValueType (DataType::*getter)() const) {
        if(start == end) {
            (data[pos].*setter)(value);
            tree[node] = value;
            return;
        }
        
        int m = BaseOps::mid(start, end);
        if(pos <= m)
            update(BaseOps::left(node), start, m, pos, value, tree, data, setter, getter);
        else
            update(BaseOps::right(node), m+1, end, pos, value, tree, data, setter, getter);
        
        tree[node] = Utils::lcm(tree[BaseOps::left(node)], 
                              tree[BaseOps::right(node)]);
    }
};

} // namespace TreeOperations

#endif // TREE_OPERATIONS_H
