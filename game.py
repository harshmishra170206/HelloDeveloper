"""
Mana Duel — two wizards drain a shared ley-line network.
"""

import math

class ManaDuel:
    def __init__(self, graph, values):
        self.graph = graph      # {node: [neighbors]}
        self.values = values    # {node: mana value}

    def get_moves(self, removed, current):
        """Nodes available to channel next."""
        if current is None:
            return [n for n in self.graph if n not in removed]
        return [n for n in self.graph[current] if n not in removed]

    def minimax(self, removed, current, scores, turn, alpha, beta):
        """
        turn: 0 = Player 1 (maximizer), 1 = Player 2 (minimizer)
        scores: (p1_score, p2_score)
        Returns (best_score_diff, best_move)
        """
        moves = self.get_moves(removed, current)
        if not moves:
            return scores[0] - scores[1], None

        best_move = None
        if turn == 0:  # Player 1 maximizes P1 - P2
            best_val = -math.inf
            for m in moves:
                new_removed = removed | {m}
                new_scores = (scores[0] + self.values[m], scores[1])
                val, _ = self.minimax(new_removed, m, new_scores, 1, alpha, beta)
                if val > best_val:
                    best_val, best_move = val, m
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break  # beta cutoff
            return best_val, best_move
        else:  # Player 2 minimizes P1 - P2
            best_val = math.inf
            for m in moves:
                new_removed = removed | {m}
                new_scores = (scores[0], scores[1] + self.values[m])
                val, _ = self.minimax(new_removed, m, new_scores, 0, alpha, beta)
                if val < best_val:
                    best_val, best_move = val, m
                beta = min(beta, best_val)
                if beta <= alpha:
                    break  # alpha cutoff
            return best_val, best_move


def draw_ascii_map(values, removed, current):
    """Draws the map directly in the terminal using ASCII text."""
    
    def format_node(node_name):
        if node_name in removed and node_name != current:
            return " [X] "  
        elif node_name == current:
            return f"<{node_name}:{values[node_name]}>" 
        else:
            return f" {node_name}:{values[node_name]} " 
            
    n = {k: format_node(k) for k in values.keys()}
    
    print("\n--- CURRENT BOARD MAP ---")
    print(f"         {n['A']}                              {n['F']}-------{n['G']}")
    print( "       /       \\                            |           |")
    print(f"  {n['B']}---------{n['C']}-------{n['D']}-------{n['E']}-------{n['H']}")
    print("-------------------------\n")


def play_human_vs_ai(graph, values, human_turn=0):
    game = ManaDuel(graph, values)
    removed = frozenset()
    current = None
    scores = [0, 0]
    turn = 0
    names = ["Player 1 (You)" if human_turn == 0 else "Player 1 (AI)",
             "Player 2 (AI)" if human_turn == 0 else "Player 2 (You)"]

    while True:
        draw_ascii_map(values, removed, current)

        moves = game.get_moves(removed, current)
        if not moves:
            print(f"\n{names[turn]} is cut off — no reachable nodes left.")
            break

        if turn == human_turn:
            print(f"Available moves: {moves}")
            choice = None
            while choice not in moves:
                choice = input(f"{names[turn]}, channel a node: ").strip().upper() 
            move = choice
        else:
            _, move = game.minimax(removed, current, tuple(scores), turn, -math.inf, math.inf)
            print(f"\n{names[turn]} is thinking...")

        scores[turn] += values[move]
        removed = removed | {move}
        print(f"{names[turn]} channels '{move}' (+{values[move]} mana) "
              f"-> P1={scores[0]}, P2={scores[1]}")
        current = move
        turn = 1 - turn

    winner = "Player 1" if scores[0] > scores[1] else ("Player 2" if scores[1] > scores[0] else "Tie")
    print(f"\nFinal Scores -> P1: {scores[0]}, P2: {scores[1]}")
    print(f"Winner: {winner}")
    
    return scores, winner


def play_game(graph, values, verbose=True):
    # (Kept just in case you want AI vs AI mode)
    game = ManaDuel(graph, values)
    removed = frozenset()
    current = None
    scores = [0, 0]
    turn = 0
    names = ["Player 1", "Player 2"]

    while True:
        draw_ascii_map(values, removed, current)
        moves = game.get_moves(removed, current)
        if not moves:
            break
        _, best_move = game.minimax(removed, current, tuple(scores), turn, -math.inf, math.inf)
        scores[turn] += values[best_move]
        removed = removed | {best_move}
        current = best_move
        turn = 1 - turn

    return scores


if __name__ == "__main__":
    # The "Zugzwang Bridge" ley-line network
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'C'],
        'C': ['A', 'B', 'D'],
        'D': ['C', 'E'],        # The Choke Point Bridge!
        'E': ['D', 'F', 'H'],
        'F': ['E', 'G'],
        'G': ['F', 'H'],
        'H': ['E', 'G']
    }
    values = {'A': 4, 'B': 5, 'C': 2, 'D': 1, 'E': 3, 'F': 8, 'G': 9, 'H': 6}

    print("Ley-line network loaded.")

    pick = input("Play as Player 1 (moves first) or Player 2? [1/2]: ").strip()
    human_turn = 0 if pick == "1" else 1
    play_human_vs_ai(graph, values, human_turn)
