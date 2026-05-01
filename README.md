
# Chess Opening Move Advisor

Chess Opening Move Advisor is an interactive Python application that analyzes chess positions and recommends optimal opening moves using AI search algorithms. It features a graphical user interface (GUI) built with Tkinter and demonstrates the efficiency of Alpha-Beta Pruning compared to standard Minimax search.

## Features

- **Visual Chessboard GUI:**
   - Built with Tkinter, displays the current board state using Unicode chess symbols.
   - Interactive interface with buttons to calculate best moves and restart analysis.
   - Colorful, user-friendly layout.

- **Move Recommendation:**
   - Calculates and displays the best move for the current position, along with the top 3 alternative moves.
   - Uses advanced evaluation based on both material and positional factors (Piece-Square Tables).

- **AI Algorithms:**
   - Implements both Pure Minimax and Alpha-Beta Pruning search algorithms.
   - Compares node counts and efficiency between the two algorithms in real time.

- **Statistics & Analysis:**
   - Shows the number of nodes evaluated by each algorithm, nodes saved, and pruning efficiency percentage.
   - Presents move scores and recommendations in a clear, readable format.

## How It Works

### 1. Board Evaluation
The engine evaluates the board using both material values and positional bonuses/penalties (Piece-Square Tables) for each piece type. The evaluation function rewards good piece placement and penalizes poor positioning.

### 2. Search Algorithms
- **Pure Minimax:** Explores all possible moves to a fixed depth, selecting the move that maximizes the minimum gain.
- **Alpha-Beta Pruning:** Optimizes the search by pruning branches that cannot affect the outcome, greatly reducing computation.

### 3. Move Calculation
When you click "Calculate Best Moves":
1. The app runs Minimax and Alpha-Beta searches to a set depth.
2. It evaluates all legal moves from the current position.
3. The best move and top alternatives are displayed, and the board updates to reflect the recommended move.
4. Node statistics and pruning efficiency are shown in the side panel.

### 4. Restarting Analysis
Click "Restart Analysis" to reset the board to the starting position and clear previous results.

## Application Screenshot

> ![Chess Advisor Screenshot](Images\screenshot.png)

## Installation & Usage

1. **Clone the repository:**
    ```bash
    git clone https://github.com/A7medF0uad/Chess_Openin_Advisor.git
    cd Chess_Openin_Advisor
    ```
2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Run the application:**
    ```bash
    python Chess_Advisor.py
    ```

## Requirements

- Python 3.x
- [python-chess](https://pypi.org/project/python-chess/) (install via `pip install python-chess`)
- Tkinter (usually included with Python; if missing, install via your OS package manager, e.g., `sudo apt-get install python3-tk` on Ubuntu)

## File Structure

- `Chess_Advisor.py` — Main application code (GUI, AI logic, evaluation, and search algorithms)
- `requirements.txt` — Python dependencies
- `Images/` — Contains icon and screenshots for the GUI
- `README.md` — Project documentation

## Code Overview

- **Piece Values & Piece-Square Tables:** Assigns values to each piece and uses tables to evaluate piece positions.
- **Evaluation Function:** Calculates a static score for the board, considering both material and position.
- **Minimax & Alpha-Beta Functions:** Implements recursive search to determine the best move, with Alpha-Beta pruning for efficiency.
- **Tkinter GUI:** Provides an interactive chessboard, control buttons, and a statistics panel.

## License

This project is open-source and available under the MIT License.
