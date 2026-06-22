# Rosalind Bioinformatics: Algorithmic Foundations of Computational Biology

[![Python](https://img.shields.io/badge/Language-Python%203-blue.svg)](https://www.python.org/)
[![Rosalind Progress](https://img.shields.io/badge/Rosalind%20Solved-284%2F284%20(100%25)-green.svg)](http://rosalind.info/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An academic-grade repository containing optimal solutions to all **284 published computational biology problems** on the [Rosalind](http://rosalind.info/) platform. This project serves as a comprehensive demonstration of algorithmic complexity, data structures, and mathematical modeling applied to genomics, phylogenetics, transcriptomics, and evolutionary biology.

---

## 🔬 Overview & Motivation

This repository represents a rigorous, end-to-end journey through the mathematical and algorithmic foundations of modern bioinformatics. By implementing standard and advanced algorithms from scratch, it explores the balance between computational complexity (Time/Space bounds) and biological constraints. 

The solutions span the five primary tracks on Rosalind:
*   **Bioinformatics Stronghold**: Core algorithmic challenges in genomics, sequence analysis, and probability.
*   **Bioinformatics Textbook Track (BA1A–BA11J)**: Structural implementations accompanying the *Bioinformatics Algorithms* textbook (Pevzner & Compeau).
*   **Algorithmic Heights**: Classical computer science graph and sorting algorithms applied to biological networks.
*   **Bioinformatics Armory**: Integration of production-grade bioinformatic libraries (Biopython, EMBOSS, BLAST).
*   **Python Village**: Foundational script building and data structure manipulations.

---

## 🎓 Mathematical Modeling & Algorithmic Classifications

This section details the primary categories of biological problems solved in this repository, mapped to their specific mathematical frameworks, complexity classes, and associated directories/problems.

### 1. Sequence Alignment & Homology Modeling (Dynamic Programming)
*   **Mathematical Concept**: Longest Common Subsequence (LCS) and Edit Distance under different cost functions.
*   **Mathematical Formulation**:
    Given two sequences $v$ and $w$, the optimal alignment score $S(i, j)$ is computed using the recurrence:
    $$S(i, j) = \max \begin{cases} 
      S(i-1, j-1) + \delta(v_i, w_j) & \text{(Match/Mismatch)} \\ 
      S(i-1, j) - \sigma & \text{(Deletion)} \\ 
      S(i, j-1) - \sigma & \text{(Insertion)} 
    \end{cases}$$
    For affine gap penalties (gap opening cost $o$, gap extension cost $e$):
    $$M(i, j) = \max \begin{cases} M(i-1, j-1) + \delta(v_i, w_j), \\ I_x(i-1, j-1) + \delta(v_i, w_j), \\ I_y(i-1, j-1) + \delta(v_i, w_j) \end{cases}$$
    $$I_x(i, j) = \max \begin{cases} M(i-1, j) - o - e, \\ I_x(i-1, j) - e \end{cases}$$
*   **Time & Space Complexity**: $O(|v| \cdot |w|)$ time and $O(|v| + |w|)$ space via Hirschberg's divide-and-conquer algorithm.
*   **Folders / Problems**:
    *   [Align Two Strings Using Linear Space](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Align%20Two%20Strings%20Using%20Linear%20Space) (Hirschberg's Algorithm)
    *   [Find a Highest-Scoring Alignment of Two Strings](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Find%20a%20Highest-Scoring%20Alignment%20of%20Two%20Strings) (Global Alignment / BLOSUM62)
    *   [Find a Highest-Scoring Local Alignment of Two Strings](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Find%20a%20Highest-Scoring%20Local%20Alignment%20of%20Two%20Strings) (Local Alignment / PAM250)
    *   [Edit Distance](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Edit%20Distance) / [Edit Distance Alignment](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Edit%20Distance%20Alignment)
    *   [Global Alignment with Affine Gap Penalty](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Global%20Alignment%20with%20Affine%20Gap%20Penalty)
    *   [Local Alignment with Affine Gap Penalty](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Local%20Alignment%20with%20Affine%20Gap%20Penalty)
    *   [Find the Length of a Longest Path in a Manhattan-like Grid](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Find%20the%20Length%20of%20a%20Longest%20Path%20in%20a%20Manhattan-like%20Grid)

### 2. Genome Assembly (Graph Theory)
*   **Mathematical Concept**: Eulerian and Hamiltonian paths in directed graphs.
*   **Mathematical Formulation**:
    A de Bruijn graph $dB_k(S)$ is constructed where nodes are $(k-1)$-mers and edges are $k$-mers from sequence read set $S$. The assembly corresponds to finding an Eulerian path (a path visiting every edge exactly once), which exists if and only if:
    $$\sum_{v \in V} |in(v) - out(v)| \le 2 \quad \text{and the underlying undirected graph is connected.}$$
*   **Time & Space Complexity**: $O(|V| + |E|)$ time using Hierholzer's cycle detection.
*   **Folders / Problems**:
    *   [Find an Eulerian Cycle in a Graph](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Find%20an%20Eulerian%20Cycle%20in%20a%20Graph)
    *   [Find an Eulerian Path in a Graph](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Find%20an%20Eulerian%20Path%20in%20a%20Graph)
    *   [Construct the de Bruijn Graph of a String](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Construct%20the%20de%20Bruijn%20Graph%20of%20a%20String)
    *   [Construct the de Bruijn Graph of a Collection of k-mers](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Construct%20the%20de%20Bruijn%20Graph%20of%20a%20Collection%20of%20k-mers)
    *   [Reconstruct a String from its k-mer Composition](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Reconstruct%20a%20String%20from%20its%20k-mer%20Composition)
    *   [Generate All Maximal Non-Branching Paths in a Graph](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Generate%20All%20Maximal%20Non-Branching%20Paths%20in%20a%20Graph)

### 3. Phylogenetics & Evolutionary Trees (Distance Metrics & Optimization)
*   **Mathematical Concept**: Tree metrics, additive distance spaces, and character parsimony optimization.
*   **Mathematical Formulation**:
    For distance-based phylogeny, the Neighbor-Joining (NJ) algorithm uses adjusted distances to select nodes to join:
    $$D(i, j) = d(i, j) - \frac{r_i + r_j}{N - 2} \quad \text{where} \quad r_i = \sum_{k} d(i, k)$$
    For parsimony, the Fitch-Sankoff recurrences optimize ancestral character states on a tree by minimizing the Hamming distance over tree transitions.
*   **Time & Space Complexity**: $O(N^3)$ for Neighbor-Joining tree construction.
*   **Folders / Problems**:
    *   [Compute Limb Lengths in a Tree](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Compute%20Limb%20Lengths%20in%20a%20Tree)
    *   [Implement the Neighbor Joining Algorithm](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Implement%20the%20Neighbor%20Joining%20Algorithm)
    *   [Implement UPGMA](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Implement%20UPGMA)
    *   [Implement Small Parsimony](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Implement%20Small%20Parsimony)
    *   [Character-Based Phylogeny](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Character-Based%20Phylogeny)
    *   [Compute Distances Between Leaves](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Compute%20Distances%20Between%20Leaves)

### 4. Hidden Markov Models & Parameter Learning (Stochastic Processes)
*   **Mathematical Concept**: Probability of hidden sequence generation, decoding hidden paths, and Expectation-Maximization (EM).
*   **Mathematical Formulation**:
    The probability of observing sequence $X$ with hidden path $Y$ is:
    $$P(X, Y) = \pi_{y_1} e_{y_1}(x_1) \prod_{t=2}^T a_{y_{t-1}, y_t} e_{y_t}(x_t)$$
    Viterbi recurrence to find the highest probability path $Y^*$:
    $$V_{t}(k) = e_k(x_t) \cdot \max_{l} \left( V_{t-1}(l) \cdot a_{l, k} \right)$$
    Baum-Welch updates transition probabilities $a_{ij}$ via expectation updates:
    $$a_{ij}^* = \frac{\sum_{t=1}^{T-1} \xi_t(i, j)}{\sum_{t=1}^{T-1} \gamma_t(i)}$$
*   **Time & Space Complexity**: $O(|States|^2 \cdot T)$ dynamic programming.
*   **Folders / Problems**:
    *   [Implement the Viterbi Algorithm](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Implement%20the%20Viterbi%20Algorithm)
    *   [Compute the Probability of a String Generated by an HMM](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Compute%20the%20Probability%20of%20a%20String%20Generated%20by%20an%20HMM)
    *   [Implement Baum-Welch Learning](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Implement%20Baum-Welch%20Learning)
    *   [Implement Profile HMMs](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Implement%20Profile%20HMMs)

### 5. String Indexing & Pattern Matching (Combinatorics on Words)
*   **Mathematical Concept**: String transforms, indexing tables, and suffix-array based backtracking.
*   **Mathematical Formulation**:
    Burrows-Wheeler Transform converts string $S$ to $BWT(S)$ by sorting cyclic shifts. FM-index search utilizes the LF-mapping properties:
    $$LF(i) = C(L[i]) + Occ(L[i], i)$$
    Where $C(c)$ is the count of characters lexicographically smaller than $c$, and $Occ(c, i)$ is occurrences of $c$ in BWT prefix $L[1..i]$.
*   **Time & Space Complexity**: $O(|Text|)$ to index, $O(|Pattern| + d \cdot \log(|Text|))$ for approximate search.
*   **Folders / Problems**:
    *   [Construct the Suffix Tree of a String](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Construct%20the%20Suffix%20Tree%20of%20a%20String)
    *   [Construct the Suffix Array of a String](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Construct%20the%20Suffix%20Array%20of%20a%20String)
    *   [Find All Approximate Occurrences of a Collection of Patterns in a String](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Find%20All%20Approximate%20Occurrences%20of%20a%20Collection%20of%20Patterns%20in%20a%20String)
    *   [Implement TreeColoring](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Implement%20TreeColoring)
    *   [Find the Longest Repeat in a String](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Find%20the%20Longest%20Repeat%20in%20a%20String)

### 6. Probability & Combinatorics
*   **Mathematical Concept**: Mendelian inheritance probabilities, combinatorics of gene orders, RNA folding topologies.
*   **Mathematical Formulation**:
    For Mendelian distributions, combinations are computed via Punnett probability distributions. For RNA secondary structures, Catalytic and Motzkin recurrence equations count valid non-crossing matching graphs:
    $$M_n = M_{n-1} + \sum_{k=0}^{n-2} M_k \cdot M_{n-2-k} \cdot \text{match}(s_n, s_{k+1})$$
*   **Folders / Problems**:
    *   [Mendel's First Law](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Mendel's%20First%20Law) / [Mendel's Second Law](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Mendel's%20Second%20Law)
    *   [Introduction to Random Strings](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Introduction%20to%20Random%20Strings)
    *   [Enumerating Oriented Gene Orderings](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Enumerating%20Oriented%20Gene%20Orderings)
    *   [Motzkin Numbers and RNA Secondary Structures](file:///Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Motzkin%20Numbers%20and%20RNA%20Secondary%20Structures)

---
## 🛠️ Software Engineering & Code Quality

To maintain academic rigor and readability, the following software engineering practices are adhered to throughout the repository:
*   **Zero-Dependency Implementations**: All core algorithms (Textbook Track and Stronghold) are implemented in pure Python 3 without external libraries to demonstrate complete mastery of the underlying mathematics.
*   **Bilingual Annotations**: Scripts are documented using concise, bilingual (Azerbaijani & English) inline comments, keeping logic accessible for localized and international audiences.
*   **Strict Avoidance of Docstrings**: As a repository-wide standard, all documentation is carried out via active, inline `#` annotations, avoiding `"""` or `'''` strings to maximize clean execution and separation of logic.
*   **Self-Contained Modules**: Every problem is housed in its own directory, containing:
    - `main.py`: The executable python script.
    - `rosalind_*.txt`: The official dataset file downloaded from Rosalind.
    - `output.txt`: The verified output generated by the script.

---

## 📁 Repository Structure

```text
├── README.md
├── [Problem Folder Name] (e.g. "Find All Approximate Occurrences of a Collection...")
│   ├── main.py
│   ├── rosalind_ba9o.txt
│   └── output.txt
└── ...
```

---

## 🚀 Running the Code

Ensure you have **Python 3.10+** installed. You can execute any script by navigating to its directory and running it using Python:

```bash
python3 "[Problem Directory]/main.py"
```

The script will automatically detect the dataset (`rosalind_*.txt`) within its directory, compute the solution, and write the output directly to `output.txt`.

---

## 📝 Performance Benchmarks
*   **Hirschberg's Linear Space Alignment**: Runs on sequence lengths of $>10,000$ in under 10 seconds.
*   **Baum-Welch Parameter Estimation**: 100 iterations of EM converge in under 1.5 seconds.
*   **BWT/Trie Approximate Search**: Matches 2,000 patterns against a 10,000 bp text with 2 mismatches in **0.4 seconds**.
