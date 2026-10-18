# 🤖 Artificial Intelligence Lab Assignments & Advanced Research

<p align="center">
  <img src="https://img.shields.io/badge/Course-CSE%203811-blue?style=for-the-badge&logo=academic-pages" alt="Course">
  <img src="https://img.shields.io/badge/University-UIU-red?style=for-the-badge" alt="UIU">
  <img src="https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge" alt="Status">
</p>

This repository contains the comprehensive lab implementations, graph-search algorithms, Constraint Satisfaction Problems (CSP), and term research on **Autonomous AI Systems and Labor Economics** for the **Artificial Intelligence (CSE 3811)** course at **United International University (UIU)**.

---

## 📌 Features & Technical Overview

### 1. Constraint Satisfaction Problem (CSP) Solver
* **Core Logic:** Implements constraint satisfaction algorithms in `Solve.py` to process complex structural grid inputs from `puzzles.txt`.
* **Output:** Generates fully verified constraint-satisfied state matrices saved directly into `solutions.txt`.

### 2. Uninformed State-Space Search
* **Breadth-First Search (BFS):** Guarantees optimal pathfinding on unweighted graph structures by exploring state levels systematically.
* **Depth-First Search (DFS):** Explores deeper branches in the search tree for memory-efficient state-space traversal.
* **Implementation:** Located in `Assignment-1/Task1.ipynb`.

### 3. Informed & Heuristic Pathfinding
* **Dijkstra’s Algorithm:** Calculates the exact shortest path across weighted spatial networks.
* **A* Search Algorithm:** Combines path cost $g(n)$ and heuristic estimate $h(n)$ for optimal 3D spatial routing.
* **3D Coordinate Processing:** Reads spatial data matrices from `Coordinates.csv` and `distances.csv`.
* **Implementation:** Located in `Assignment-1/Task2.ipynb`.

---

## 📂 Repository Structure

```text
├── 📂 Assignment-1/
│   ├── 📜 Task1.ipynb                 # BFS & DFS Uninformed Traversal Notebook
│   ├── 📜 Task2.ipynb                 # Dijkstra & A* Pathfinding Notebook
│   ├── 📊 Coordinates.csv             # 3D Coordinates Dataset
│   └── 📊 distances.csv               # Spatial Distance Matrix Dataset
├── 📂 CSPAssignment/
│   ├── 🐍 Solve.py                    # Python CSP Constraint Engine
│   ├── 📝 puzzles.txt                 # Input Puzzle Configurations
│   ├── 📄 solutions.txt               # Solved Grid Output
│   └── 📑 Technical_Report.pdf        # Algorithmic Analysis & Benchmark Documentation
├── 📄 0112330329(Sadia Islam Mim).pdf # Term Report: "AI Agents and the Future of Jobs"
└── 📝 README.md                       # Comprehensive Repository Documentation
