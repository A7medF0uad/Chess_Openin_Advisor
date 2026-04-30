# Chess Opening Move Advisor

An interactive Python application designed to evaluate chess positions and recommend optimal moves using AI search algorithms. The tool specifically highlights the efficiency gains of **Alpha-Beta Pruning** over standard **Minimax** search.

## Features
*   **Visual Board:** A GUI built with Tkinter that displays the current board state using Unicode chess symbols.
*   **Move Recommendation:** Identifies the top-ranked move and three alternative suggestions.
*   **Algorithm Comparison:** Real-time statistics showing the number of nodes evaluated by pure Minimax versus the Alpha-Beta optimized version.
*   **Position Evaluation:** Uses Piece-Square Tables (PST) to calculate the strategic value of piece placement, not just material count.

## Technical Logic

### The Evaluation Function
The engine calculates a "Static Evaluation" score for the board. White's advantage is represented by a positive score, while Black's is negative[cite: 1]. The formula follows:

$$Score = \sum_{white} (Material + Position) - \sum_{black} (Material + Position)$$

*   **Material:** Points assigned to piece types (e.g., Pawn = 1, Queen = 9)[cite: 1].
*   **Position:** Bonuses or penalties based on the square a piece occupies (e.g., Knights are penalized for being on the edge of the board)[cite: 1].

### Search Algorithms
1.  **Pure Minimax:** An exhaustive search that explores every possible legal move to a specified depth[cite: 1].
2.  **Alpha-Beta Pruning:** An optimization that "prunes" (discards) branches in the search tree that cannot possibly influence the final decision, significantly reducing computation time[cite: 1].

## Output

Below is a preview of the application in action. It shows the visual board, the efficiency comparison between algorithms, and the recommended moves for the current position.

![Chess Advisor Screenshot](Images\screenshot.png)

## Installation & Usage
1. Clone this repository to your local machine.
2. Ensure you have the required dependencies:
   ```bash
   pip install -r requirements.txt