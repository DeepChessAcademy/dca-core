# DeepChessAcademy (DCA) - Research Lab

Welcome to the DeepChessAcademy (DCA) Research Lab. This repository is at the intersection of chess mastery and state-of-the-art Artificial Intelligence.

More than just a chess engine or a learning platform, the DCA is an R&D lab focused on **Algorithmic Reasoning, Discovery, and Generation**, using chess as our primary testbed.

## The Strategic Shift: From Imitation to Discovery

This project marks a fundamental shift in our learning and development approach.

### Old Approach (Dispersed)

* **Isolated Learning:** Studying foundations (Stats, Linear Algebra, SQL, Rust) and AI (Deep Learning) as separate disciplines.
* **Focus on Imitation:** Building "Kaggle-style" models to imitate human behavior or existing engines (e.g., move prediction).
* **Weak Convergence:** Trying to "fit" tools (like Rust or SQL) into projects artificially, leading to a sense of "jumping between topics."

### New Approach (Total Convergence)

* **Total Convergence in DCA:** The DCA is the *single point of convergence*. Every foundation (SQL, Rust, Optimization) is "pulled" by a complex, real-world project need.
* **Focus on Reasoning & Discovery:** Inspired by cutting-edge research, our goal shifts from *imitation* to *reasoning* and *discovery*. We don't just want to predict the best move; we want the AI to *reason* hierarchically and *discover* new knowledge and strategies.
* **Active Domain:** Chess is not a passive subject. It is the test environment for algorithmic problems that are harder than those found on LeetCode or Kaggle.

## New Objectives (Inspired by State-of-the-Art Research)

Our objectives have evolved to reflect the forefront of AI research:

### 1. From Problems to Discovery (AlphaEvolve)

* **Inspiration:** `AlphaEvolve: A coding agent for scientific and algorithmic discovery`.
* **DCA Objective:** Build an evolutionary agent (LLM or code-model based) that not only *plays* chess but *optimizes* and *discovers* new evaluation algorithms, opening strategies, or even simplifications in existing chess engines.

### 2. Creative Problem Generation (RL + Generative AI)

* **Inspiration:** `Generating Creative Chess Puzzles`.
* **DCA Objective:** Develop a Reinforcement Learning (RL) framework rewarded not for winning, but for generating chess *puzzles* that are novel, aesthetic, counter-intuitive, and instructive for humans.

### 3. From "Deep" to "Recursive" (Tiny & Hierarchical Models)

* **Inspiration:** `Less is More: Recursive Reasoning with Tiny Networks` (TRM) and `Hierarchical Reasoning Model` (HRM).
* **DCA Objective:** Implement and evaluate recursive and hierarchical reasoning models in the chess domain. The challenge is to achieve high-level performance on complex reasoning tasks (e.g., long-form tactics) with extremely low-parameter models (e.g., < 30M).

### 4. From "Imitation" to "Reasoning" (Supervised RL)

* **Inspiration:** `Supervised Reinforcement Learning (SRL): From Expert Trajectories to Step-wise Reasoning`.
* **DCA Objective:** Train models to generate an "internal monologue" of reasoning. Instead of just outputting a puzzle's solution, the model must generate the step-by-step thought process that leads to it, guided by expert demonstrations.

### 5. From "Theory" to "Engineering" (MLOps & DataX)

* **Inspiration:** `Professional Machine Learning Engineer Study Guide` and `CompTIA DataX Exam Objectives`.
* **DCA Objective:** Treat DCA as a professional-grade product. Implement a full MLOps pipeline for data ingestion (e.g., the 10M-game `ChessBench` dataset), training, versioning, deployment, and monitoring of our reasoning and generation models.

## The Applied Foundations Curriculum

This project is the vehicle through which mastery of the foundations will be achieved:

* **Statistics, Linear Algebra, Calculus, Optimization:** The day-to-day work of implementing, debugging, and optimizing the reasoning models (TRM, HRM, SRL).
* **Algorithms:** The core of the discovery agent (AlphaEvolve) and the puzzle generation systems (RL).
* **Software Engineering:** The architecture of the DCA system as a cohesive, scalable, and robust platform.
* **SQL:** The design and optimization of a large-scale database to efficiently store and query billions of generated positions, games, and puzzles.
* **Web Development with Rust:** Building the DCA's backend API (e.g., `dca-api`) with a focus on high performance, safety, and concurrency to serve real-time analyses and puzzles.
* **ARM Development with Rust:** Optimizing and compiling our "Tiny" models (TRM) to run efficiently on edge devices, proving that complex reasoning does not require massive hardware.
