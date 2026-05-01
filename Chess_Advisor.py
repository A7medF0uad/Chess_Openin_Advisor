import chess  
from tkinter import * 

# --- PIECE VALUES & TABLES ---
PIECE_VALUES = {
    chess.PAWN: 1, 
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0  # King has no material value because its loss ends the game
}

# Piece-Square Tables (PST): These 64-item lists represent the 8x8 board.
# High numbers = Good squares for that piece. Low/Negative = Squares to avoid.
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,    # Rank 8 (Promotion zone)
    50, 50, 50, 50, 50, 50, 50, 50,  # Rank 7 (Strongly pushed)
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,   # Rank 5 (Central presence)
    0,  0,  0, 20, 20,  0,  0,  0,   # Rank 4 (Initial push)
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0    # Rank 1 (Starting line)
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50, # Corners are bad for Knights
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30, # Center squares have highest value
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [-10]*64

ROOK_TABLE = [0]*64

QUEEN_TABLE = [-10, -5, -5, 0, 0, -5, -5, -10] * 8

KING_TABLE = [
    20, 30, 10,  0,  0, 10, 30, 20, # King wants to stay in the corners during openings
    20, 20,  0,  0,  0,  0, 20, 20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30
]

# Map piece types to their tables for easy lookup during evaluation
TABLES = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
    chess.KING: KING_TABLE
}

# --- AI LOGIC ---
def evaluate(board):
    """Calculates the static score of the board state."""
    if board.is_checkmate():
        return -9999 if board.turn == chess.WHITE else 9999
    
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            val = PIECE_VALUES[piece.piece_type] 
            
            idx = square if piece.color == chess.WHITE else chess.square_mirror(square)
            pos_bonus = TABLES[piece.piece_type][idx]
            
            if piece.color == chess.WHITE:
                score += (val + pos_bonus)
            else:
                score -= (val + pos_bonus)
    return score

minimax_nodes = 0 
def pure_minimax(board, depth, maximizing):
    global minimax_nodes
    minimax_nodes += 1
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    if maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval_score = pure_minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval_score)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval_score = pure_minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval_score)
        return min_eval

ab_nodes = 0 
def alpha_beta(board, depth, alpha, beta, maximizing):
    global ab_nodes
    ab_nodes += 1
    
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing:
        v = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            v = max(v, alpha_beta(board, depth - 1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, v) 
            if beta <= alpha: 
                break
        return v
    else:
        v = float('inf')
        for move in board.legal_moves:
            board.push(move)
            v = min(v, alpha_beta(board, depth - 1, alpha, beta, True))
            board.pop()
            beta = min(beta, v) 
            if beta <= alpha: 
                break
        return v

# --- GUI & APPLICATION ---
class ChessAdvisorGUI:
    def __init__(self, root):
        self.root = root 
        icon = PhotoImage(file='Images\\Icon.png')
        # self.root.iconphoto(True, icon)
        self.root.title("Chess Opening Advisor [Alpha-Beta]")
        self.root.geometry("750x600")
        self.root.config(bg="#2c3e50")
        
        self.board = chess.Board() 
        self.setup_ui() 

    def setup_ui(self):
        Label(self.root, text="Chess Opening Advisor", font=("Helvetica", 30, "bold"), fg="white", bg="#2c3e50", bd=10, relief=RAISED).pack(pady=10)
        
        self.main_frame = Frame(self.root, bg="#2c3e50")
        self.main_frame.pack(expand=True, fill="both", padx=20)

        self.board_canvas = Frame(self.main_frame, bg="#34495e", bd=2, relief=SUNKEN)
        self.board_canvas.grid(row=0, column=0, padx=20)
        self.cells = {} 
        self.draw_board() 

        self.res_frame = Frame(self.main_frame, bg="#2c3e50")
        self.res_frame.grid(row=0, column=1, sticky="n")
        
        self.calc_btn = Button(self.res_frame, text="Calculate Best Moves", command=self.calculate, 
                               font=("Helvetica", 12, "bold"), bg="#27ae60", fg="white", padx=20)
        self.calc_btn.pack(pady=10)

        self.restart_btn = Button(self.res_frame, text="Restart Analysis", command=self.restart, 
                                  font=("Helvetica", 12, "bold"), bg="#e74c3c", fg="white", padx=20)
        self.restart_btn.pack(pady=10)

        self.stats_label = Label(self.res_frame, text="Press calculate to start...", font=("Consolas", 11), 
                                 fg="#ecf0f1", bg="#34495e", justify=LEFT, padx=10, pady=10)
        self.stats_label.pack(pady=10)

    def draw_board(self):
        symbols = {
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟'
        }
        for r in range(8):
            for c in range(8):
                square = chess.square(c, 7-r)
                color = "#ecf0f1" if (r + c) % 2 == 0 else "#95a5a6"
                piece = self.board.piece_at(square)
                txt = symbols.get(piece.symbol(), "") if piece else ""
                
                lbl = Label(self.board_canvas, text=txt, font=("DejaVu Sans", 32), 
                            width=2, height=1, bg=color, fg="black")
                lbl.grid(row=r, column=c)

    def restart(self):
        self.board.reset()
        self.draw_board()
        self.stats_label.config(text="Press calculate to start again")

    def calculate(self):
        global minimax_nodes, ab_nodes
        minimax_nodes = 0 
        ab_nodes = 0
        
        pure_minimax(self.board, 4, True)
        
        move_results = []
        for move in self.board.legal_moves:
            self.board.push(move)
            score = alpha_beta(self.board, 3, float('-inf'), float('inf'), False)
            move_results.append((move, score))
            self.board.pop()
        
        move_results.sort(key=lambda x: x[1], reverse=True)
        
        recommended = move_results[0]

        self.board.push(recommended)
        self.draw_board()

        alternatives = move_results[1:4] 
        
        saved = minimax_nodes - ab_nodes
        perc = (saved / minimax_nodes) * 100 if minimax_nodes > 0 else 0
        
        output = f"--- NODE STATISTICS ---\n"
        output += f"Minimax Nodes: {minimax_nodes}\n"
        output += f"Alpha-Beta Nodes: {ab_nodes}\n"
        output += f"Nodes Saved: {saved}\n"
        output += f"Pruning Efficiency: {perc:.2f}%\n\n"
        
        output += f"--- RECOMMENDATION ---\n"
        output += f"RANK 1: {recommended[0]} (Score: {recommended[1]})\n\n"
        
        output += f"--- TOP 3 ALTERNATIVES ---\n"
        for i, (m, s) in enumerate(alternatives):
            output += f"Alt {i+1}: {m} (Score: {s})\n"
            
        self.stats_label.config(text=output)

if __name__ == "__main__":
    root = Tk()
    app = ChessAdvisorGUI(root)
    root.mainloop()