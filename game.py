"""
Mana Duel — two wizards drain a shared ley-line network.

Rules:
- The network is a graph of nodes, each holding a mana value.
- On your turn you "channel" any node adjacent to the last-channeled node
  (the first move can be any node), remove it from the graph, and add its
  value to your score.
- If the current node has no un-channeled neighbors left, that player is
  cut off and the game ends.
- Eval function = score differential (P1 score - P2 score), not just win/lose.
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
    
    # Helper function to format a single node
    def format_node(node_name):
        if node_name in removed and node_name != current:
            return " [X] "  # Crossed out / removed
        elif node_name == current:
            return f"<{node_name}:{values[node_name]}>" # Current location
        else:
            return f" {node_name}:{values[node_name]} " # Available to move
            
    # Format all nodes to exactly 5 characters wide for alignment
    n = {k: format_node(k) for k in values.keys()}
    
    print("\n--- CURRENT BOARD MAP ---")
    print(f"        {n['E']}")
    print( "          |")
    print(f"        {n['B']}")
    print( "          |")
    print(f"        {n['A']} --- {n['D']}")
    print( "          |             |")
    print(f"        {n['C']} --- {n['F']}")
    print( "          |             |")
    print(f"        {n['G']} -------------+")
    print("-------------------------\n")


def play_game(graph, values, verbose=True):
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
            if verbose:
                print(f"{names[turn]} is cut off — no reachable nodes left.")
            break

        _, best_move = game.minimax(removed, current, tuple(scores), turn, -math.inf, math.inf)
        scores[turn] += values[best_move]
        removed = removed | {best_move}
        if verbose:
            print(f"{names[turn]} channels '{best_move}' (+{values[best_move]} mana) "
                  f"-> P1={scores[0]}, P2={scores[1]}")
        current = best_move
        turn = 1 - turn

    winner = "Player 1" if scores[0] > scores[1] else ("Player 2" if scores[1] > scores[0] else "Tie")
    if verbose:
        print(f"\nFinal Scores -> P1: {scores[0]}, P2: {scores[1]}")
        print(f"Winner: {winner}")
    
    return scores, winner


def play_human_vs_ai(graph, values, human_turn=0):
    """
    human_turn: 0 -> human is Player 1 (moves first), 1 -> human is Player 2
    """
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
                choice = input(f"{names[turn]}, channel a node: ").strip().upper() # Auto uppercase
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


if __name__ == "__main__":
    # The "Bait and Trap" ley-line network
    graph = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'E'],
        'C': ['A', 'F', 'G'],
        'D': ['A', 'F'],
        'E': ['B'],          # The dead-end!
        'F': ['C', 'D', 'G'],
        'G': ['C', 'F']
    }
    values = {'A': 2, 'B': 7, 'C': 5, 'D': 6, 'E': 1, 'F': 8, 'G': 3}

    print("Ley-line network loaded.")

    mode = input("\nChoose mode: (1) AI vs AI  (2) Human vs AI: ").strip()
    if mode == "2":
        pick = input("Play as Player 1 (moves first) or Player 2? [1/2]: ").strip()
        human_turn = 0 if pick == "1" else 1
        play_human_vs_ai(graph, values, human_turn)
    else:
        play_game(graph, values)
        
