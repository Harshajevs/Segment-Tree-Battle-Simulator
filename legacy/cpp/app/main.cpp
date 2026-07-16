#include <iostream>
#include <fstream>
#include <vector>
#include <utility>
#include "SegmentTree.h" // Your class header
using namespace std;

int main() {
    const int NUM_SOLDIERS = 100000;
    vector<pair<int, int>> team1(NUM_SOLDIERS);
    vector<pair<int, int>> team2(NUM_SOLDIERS);

    // Read team1 data
    ifstream infile1("data/team1.txt");
    if (!infile1.is_open()) {
        cerr << "Error opening team1.txt" << endl;
        return 1;
    }
    for (int i = 0; i < NUM_SOLDIERS; ++i) {
        int attack, health;
        infile1 >> attack >> health;
        team1[i] = make_pair(attack, health);
    }
    infile1.close();

    // Read team2 data
    ifstream infile2("data/team2.txt");
    if (!infile2.is_open()) {
        cerr << "Error opening team2.txt" << endl;
        return 1;
    }
    for (int i = 0; i < NUM_SOLDIERS; ++i) {
        int attack, health;
        infile2 >> attack >> health;
        team2[i] = make_pair(attack, health);
    }
    infile2.close();

    // Initialize segment trees
    SegmentTree segtree1(team1);
    SegmentTree segtree2(team2);

    int rounds = 100; // or any number of rounds you want
    int teamA_score = 0;
    int teamB_score = 0;

    cout << "Simulation starts with " << NUM_SOLDIERS << " soldiers each.\n";

    for (int round = 1; round <= rounds; ++round) {
        cout << "\n--- Round " << round << " ---\n";

        int l1, r1, l2, r2;

        // Team 1 attack range
        cout << "Enter attack range for Team 1 (start end): ";
        cin >> l1 >> r1;
        l1 = max(0, min(l1, NUM_SOLDIERS - 1));
        r1 = max(0, min(r1, NUM_SOLDIERS - 1));
        long long sumAttack1 = segtree1.querySumAttack(l1, r1);
        cout << "Team 1 attack sum in range [" << l1 << ", " << r1 << "] = " << sumAttack1 << "\n";

        // Team 2 defense range
        cout << "Enter defense range for Team 2 (start end): ";
        cin >> l2 >> r2;
        l2 = max(0, min(l2, NUM_SOLDIERS - 1));
        r2 = max(0, min(r2, NUM_SOLDIERS - 1));
        long long sumHealth2 = segtree2.querySumHealth(l2, r2);
        cout << "Team 2 health sum in range [" << l2 << ", " << r2 << "] = " << sumHealth2 << "\n";

        // Update attack for team1 at a specific index (simulate attack)
        int attack_idx = (l1 + r1) / 2; // Example index
        segtree1.update(attack_idx, 100, team1[attack_idx].second); // Increase attack

        // Update health for team2 at a specific index (simulate defense)
        int health_idx = (l2 + r2) / 2; // Example index
        segtree2.update(health_idx, team2[health_idx].first, 200); // Increase health

        // Calculate scores
        teamA_score += static_cast<int>(sumAttack1 - sumHealth2);
        teamB_score += static_cast<int>(sumAttack1 - sumHealth2); // or any logic

        // GCD and LCM surprise rounds
        if (round % 10 == 0) {
            cout << "Surprise round! Enter ranges for GCD and LCM.\n";
            cout << "Team 1 range (start end): ";
            int g1l, g1r; cin >> g1l >> g1r;
            cout << "Team 2 range (start end): ";
            int g2l, g2r; cin >> g2l >> g2r;
            g1l = max(0, min(g1l, NUM_SOLDIERS - 1));
            g1r = max(0, min(g1r, NUM_SOLDIERS - 1));
            g2l = max(0, min(g2l, NUM_SOLDIERS - 1));
            g2r = max(0, min(g2r, NUM_SOLDIERS - 1));

            int gcdA = segtree1.queryGcdAttack(g1l, g1r);
            int gcdH = segtree2.queryGcdHealth(g2l, g2r);
            cout << "GCD Attack (Team 1): " << gcdA << "\n";
            cout << "GCD Health (Team 2): " << gcdH << "\n";

            int lcmA = segtree1.queryLcmAttack(g1l, g1r);
            int lcmH = segtree2.queryLcmHealth(g2l, g2r);
            cout << "LCM Attack (Team 1): " << lcmA << "\n";
            cout << "LCM Health (Team 2): " << lcmH << "\n";

            if (gcdA > gcdH) {
                teamA_score += 50;
                cout << "Team A gains 50 points for GCD advantage!\n";
            } else if (gcdH > gcdA) {
                teamB_score += 50;
                cout << "Team B gains 50 points for GCD advantage!\n";
            } else {
                cout << "GCD is tied, no points awarded.\n";
            }
        }
    }

    // Final results
    cout << "\n--- Final Results ---\n";
    cout << "Team A Score: " << teamA_score << endl;
    cout << "Team B Score: " << teamB_score << endl;
    if (teamA_score > teamB_score)
        cout << "Team A wins!\n";
    else if (teamB_score > teamA_score)
        cout << "Team B wins!\n";
    else
        cout << "It's a tie!\n";

    return 0;
}
