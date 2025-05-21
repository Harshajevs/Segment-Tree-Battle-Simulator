# ⚔️ Segment Tree Battle Simulator

A high-performance, data structure-focused battle simulation using advanced segment trees for real-time range queries and updates. Designed to handle large-scale combat between two massive teams, this simulator is ideal for testing algorithmic efficiency and strategic planning using core C++17 features.

---

## 📦 Dataset

- `data/team1.txt`  
- `data/team2.txt`  

Each file contains **100,000** entries in the format:
attack_value health_value

yaml
Copy
Edit

---

## 🚀 Features

- **Efficient Segment Trees**: Support for sum, min, max, GCD, and LCM operations  
- **Logarithmic Querying**: All updates and queries perform in O(log N)  
- **Modular Design**: Clear separation of logic into `include`, `src`, and `app`  
- **Massive Scale Simulation**: Handles 100K soldiers per team with ease  
- **Bonus Rounds**: GCD/LCM-based rounds for strategic advantage

---

## 🧠 Technology Stack

- **C++17**: Core implementation language  
- **CMake**: Build configuration and dependency management  
- **Custom Segment Trees**: Optimized for real-time game scenarios  
- **File I/O**: Reads team data from pre-loaded `.txt` files

---

## 🗂️ Project Structure

segment_tree_game/
├── include/
│ ├── SegmentTree.h # Main class declaration
│ ├── TreeOperations.h # Operation-specific functions
│ └── Utils.h # Utility helpers
│
├── src/
│ ├── SegmentTree.cpp # Core SegmentTree logic
│ ├── TreeOperations/
│ │ ├── BuildOperations.cpp
│ │ ├── QueryOperations.cpp
│ │ └── UpdateOperations.cpp
│ └── Utils.cpp # Utility function implementations
│
├── app/
│ └── main.cpp # Battle simulation entry point
│
├── data/
│ ├── team1.txt
│ └── team2.txt
│
├── CMakeLists.txt
└── README.md

yaml
Copy
Edit

---

## ⚙️ Getting Started

### 📋 Prerequisites

- C++17 compatible compiler (GCC, Clang, MSVC)  
- CMake 3.10 or higher

### 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/Harshajevs/segment-tree-game.git
cd segment_tree_game

# Build the project
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
🕹️ How It Works
Load soldier stats from team1.txt and team2.txt

Build segment trees for attack and health attributes

For each round (up to 100 rounds/team):

Input attack and defense ranges

Compute total and bonus damage (Sum, Max, Min, GCD, LCM)

Update tree values accordingly

Track health depletion and determine the winner

📈 Sample Stats (Example)
Operation	Complexity	Use Case
Sum	O(log N)	Total damage calculation
Max/Min	O(log N)	Identify MVP/weakest units
GCD/LCM	O(log N)	Bonus damage in special rounds

🧪 Example Input Format
team1.txt and team2.txt:

python-repl
Copy
Edit
120 1000
85  900
140 750
...
📝 Notes
Input ranges are zero-indexed

Ensure all data files are properly formatted

All segment trees are initialized during the build phase

🛠️ Future Enhancements
GUI integration using Qt/SDL for visualizing battles

Replay functionality for previous rounds

Extend support for multi-team tournaments

👨‍💻 Author
Kammari HarshaVardhan
GitHub

📜 License
This project is licensed under the MIT License – see the LICENSE file for details.
