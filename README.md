# Segment-Tree-Battle-Simulator
A high-performance battle simulation game using advanced segment trees for real-time range queries and combat dynamics involving attack and health attributes.


[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/Harshajevs/segment-Tree-Battle-Simulator)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![C++17](https://img.shields.io/badge/C%2B%2B-17-blue.svg)](https://isocpp.org/wiki/faq/cpp17)

A high-performance, modular battle simulation leveraging advanced segment trees for efficient range queries and updates, designed for real-time strategic analysis in large-scale combat scenarios.

---

## 🚀 Features

- 🔄 **Efficient Range Queries**: Compute sum, max, min, GCD, and LCM across segments
- ⏱ **Logarithmic Time Complexity**: All queries and updates operate in O(log N)
- 🧩 **Robust Modular Design**: Clear separation between game logic and data structures
- ⚔️ **Scalable Combat Simulation**: Supports up to 100,000 soldiers per team
- 🛠 **CMake Build System**: Easy to build and run on all major platforms

---

## 📦 Installation

```bash
git clone https://github.com/Harshajevs/segment-Tree-Battle-Simulator.git
cd segment-tree-battle
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
🎮 Game Mechanics & Dynamics
🧠 Overview
Two armies, each consisting of 100,000 soldiers, engage in turn-based strategic combat. Each soldier possesses:

Attack value

Health value

The simulation spans 100 rounds per team, and each round includes:

Range-based attack and defense operations

Bonus challenge rounds utilizing GCD and LCM segment trees

Real-time attribute updates and score tracking

🔁 Core Operations
Range Sum: Total attack or health values in a specified range

Range Max/Min: Identify the strongest or weakest soldier in a range

GCD/LCM Queries: Used in bonus rounds for strategic scoring

🖥️ Sample Interaction
Prompted for input ranges during each round

View real-time updates of health and attack values

Receive bonus points during GCD/LCM rounds

Game declares the winning team based on accumulated scores

📂 Data Files Format
Your input files should be placed in the data/ directory:

data/team1.txt

data/team2.txt

Each file must contain 100,000 lines with the format:

php-template
Copy
Edit
<attack_value> <health_value>
Example:

python-repl
Copy
Edit
10 100
15 85
...
🧭 Usage
bash
Copy
Edit
./BattleSimulator
Follow the on-screen prompts to input attack and defense ranges. The game processes data using segment trees and outputs the result of each round dynamically.

📝 Notes
Ensure input files exist in the data/ directory and are formatted properly.

Indexing is zero-based.

Designed for optimal performance on large datasets.

🤝 Contributing
Contributions are welcome! To contribute:

Fork the repository

Create a feature branch (git checkout -b feature-name)

Commit your changes

Push to the branch (git push origin feature-name)

Submit a Pull Request

Please adhere to code formatting guidelines and include appropriate test cases.

📜 License
This project is licensed under the MIT License.
See the LICENSE file for more information.
