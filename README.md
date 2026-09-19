# Binary Relation Analyzer & Property Checker

A Discrete Mathematics Python application and interactive web interface for parsing, testing, and visualizing binary relations on a given set $A$.

The application evaluates fundamental mathematical properties, determines whether a relation is an **Equivalence Relation** or a **Partial Order (Poset)**, generates adjacency relation matrices, and renders SVG directed graph diagrams.

---

## 🌟 Features

- **Six Fundamental Relation Properties**:
  - **Reflexive**: $\forall x \in A, (x, x) \in R$
  - **Irreflexive**: $\forall x \in A, (x, x) \notin R$
  - **Symmetric**: $\forall x, y \in A, (x, y) \in R \implies (y, x) \in R$
  - **Antisymmetric**: $\forall x, y \in A, (x, y) \in R \land (y, x) \in R \implies x = y$
  - **Asymmetric**: $\forall x, y \in A, (x, y) \in R \implies (y, x) \notin R$
  - **Transitive**: $\forall x, y, z \in A, (x, y) \in R \land (y, z) \in R \implies (x, z) \in R$

- **Separate Classification Cards**:
  - **Equivalence Relation**: Evaluates $\text{Reflexive} + \text{Symmetric} + \text{Transitive}$.
  - **Partial Order (Poset)**: Evaluates $\text{Reflexive} + \text{Antisymmetric} + \text{Transitive}$.
  - Includes a requirement checklist with green (`✓`) and red (`✗`) indicators for each condition.

- **Dynamic Preset Relation Generator**:
  - Generates relation pairs directly from the elements currently typed in Set A:
    - **Equality ($=$)**: Pairs where $a = b$.
    - **Divides ($\mid$)**: Pairs where $a \mid b$ ($b \bmod a = 0$).
    - **Less than ($<$)**: Pairs where $a < b$.
    - **Greater than ($>$)**: Pairs where $a > b$.
    - **Greater or Equal ($\ge$)**: Pairs where $a \ge b$.
    - **Empty ($\emptyset$)**: Fills empty relation $R = \emptyset$.

- **Visual Representations**:
  - **Adjacency Relation Matrix**: Grid table showing $1$ for pairs in $R$ and $0$ otherwise, with highlighted diagonal self-loop cells.
  - **SVG Directed Graph**: SVG graph diagram arranging nodes on a circle with directed arrows and curved self-loops.

- **User Experience & Themes**:
  - **Live Preview**: Formats $R = \{(1,2), (3,1)\}$ in real-time as you type flat space-separated pairs.
  - **Dark & Light Mode**: Theme toggle button with `localStorage` memory and OS theme detection.
  - **Error Validation**: Displays inline warnings for odd element counts or elements not present in set A.

---

## 📁 Project Structure

```text
RELATONS/
├── relations.py          # Core mathematical parsing & property checking functions
├── app.py                # Flask web server, matrix builder, & SVG graph generator
├── main.py               # Interactive CLI terminal application
├── test_relations.py     # Unit test suite built with Python's unittest module
├── templates/
│   └── index.html        # Web app HTML template with theme switcher & live preview JS
├── static/
│   └── style.css         # CSS design system supporting Dark & Light themes
└── README.md             # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Flask (`pip install flask`)

### 1. Run the Web Application

Start the Flask server:
```bash
python app.py
```
Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

### 2. Run the Command-Line Interface (CLI)

Run the interactive terminal app:
```bash
python main.py
```

Example terminal interaction:
```text
Enter set A: 1, 2, 3
Enter relation R: 1 1 2 2 3 3 1 2 2 3 1 3

R = {(1,1), (1,2), (1,3), (2,2), (2,3), (3,3)}
-----------------------------------------------------------------
ANALYSIS RESULTS:
- Reflexive:     YES
- Irreflexive:   NO
- Symmetric:     NO
- Antisymmetric: YES
- Asymmetric:    NO
- Transitive:    YES
```

---

### 3. Run Automated Unit Tests

Execute the unit test suite built with Python's built-in `unittest` module:
```bash
python test_relations.py
```

Tests cover:
- Equality Relation ($=$)
- Strict Order Relation ($<$)
- Symmetric Non-Transitive Relation
- Divides Relation ($\mid$)
- Empty Relation on Non-Empty Set
- Empty Set ($A = \emptyset$)
- Input errors (odd element count, element not in A, duplicate pairs)

---

## 🛠️ Built With

- **Python**: Core logic & algorithms (no external third-party math libraries)
- **Flask**: Lightweight Web Server
- **HTML5 & Vanilla CSS3**: Responsive UI, CSS Variables, Glassmorphism, Dark/Light Mode
- **SVG**: Pure vector graph rendering
- **unittest**: Native Python test suite
