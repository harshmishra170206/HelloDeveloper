# -*- coding: utf-8 -*-
from __future__ import print_function

"""
Mana Duel — two wizards drain a shared ley-line network.
(Python 2.7 Compatible Version)
"""

class ManaDuel(object):
    def __init__(self, graph, values):
        self.graph = graph      # {node: [neighbors]}
        self.values = values    # {node: mana value}

    def get_moves(self, removed, current):
        """Nodes available to channel next."""
        if current is None:
            return [n for n in self.graph if n not in removed]
        return [n for n in self.graph[current] if n not in removed]

    def minimax(self, removed, current, scores, turn, alpha, beta):
        moves = self.get_moves(removed, current)
        if not moves:
            return scores[0] - scores[1], None

        best_move = None
        if turn == 0:  # Player 1 maximizes P1 - P2
            best_val = float('-inf') # Fixed for Python 2.7
            for m in moves:
                new_removed = removed | frozenset([m])
                new_scores = (scores[0] + self.values[m], scores[1])
                val, _ = self.minimax(new_removed, m, new_scores, 1, alpha, beta)
                if val > best_val:
                    best_val, best_move = val, m
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break  # beta cutoff
            return best_val, best_move
        else:  # Player 2 minimizes P1 - P2
            best_val = float('inf') # Fixed for Python 2.7
            for m in moves:
                new_removed = removed | frozenset([m])
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
            return " [X] "  
        elif node_name == current:
            return "<{}:{}>".format(node_name, values[node_name])
        else:
            return " {}:{} ".format(node_name, values[node_name])
            
    n = {k: format_node(k) for k in values.keys()}
    
    print("\n--- CURRENT BOARD MAP ---")
    print("        {}".format(n['E']))
    print("          |")
    print("        {}".format(n['B']))
    print("          |")
    print("        {} --- {}".format(n['A'], n['D']))
    print("          |             |")
    print("        {} --- {}".format(n['C'], n['F']))
    print("          |             |")
    print("        {} -------------+".format(n['G']))
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
                print("{} is cut off — no reachable nodes left.".format(names[turn]))
            break

        _, best_move = game.minimax(removed, current, tuple(scores), turn, float('-inf'), float('inf'))
        scores[turn] += values[best_move]
        removed = removed | frozenset([best_move])
        if verbose:
            print("{} channels '{}' (+{} mana) -> P1={}, P2={}".format(
                  names[turn], best_move, values[best_move], scores[0], scores[1]))
        current = best_move
        turn = 1 - turn

    winner = "Player 1" if scores[0] > scores[1] else ("Player 2" if scores[1] > scores[0] else "Tie")
    if verbose:
        print("\nFinal Scores -> P1: {}, P2: {}".format(scores[0], scores[1]))
        print("Winner: {}".format(winner))
    
    return scores, winner


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
            print("\n{} is cut off — no reachable nodes left.".format(names[turn]))
            break

        if turn == human_turn:
            print("Available moves: {}".format(moves))
            choice = None
            while choice not in moves:
                # Fixed for Python 2.7
                prompt = "{}, channel a node: ".format(names[turn])
                choice = raw_input(prompt).strip().upper() 
            move = choice
        else:
            _, move = game.minimax(removed, current, tuple(scores), turn, float('-inf'), float('inf'))
            print("\n{} is thinking...".format(names[turn]))

        scores[turn] += values[move]
        removed = removed | frozenset([move])
        print("{} channels '{}' (+{} mana) -> P1={}, P2={}".format(
              names[turn], move, values[move], scores[0], scores[1]))
        current = move
        turn = 1 - turn

    winner = "Player 1" if scores[0] > scores[1] else ("Player 2" if scores[1] > scores[0] else "Tie")
    print("\nFinal Scores -> P1: {}, P2: {}".format(scores[0], scores[1]))
    print("Winner: {}".format(winner))
    
    return scores, winner


if __name__ == "__main__":
    graph = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'E'],
        'C': ['A', 'F', 'G'],
        'D': ['A', 'F'],
        'E': ['B'],          
        'F': ['C', 'D', 'G'],
        'G': ['C', 'F']
    }
    values = {'A': 2, 'B': 7, 'C': 5, 'D': 6, 'E': 1, 'F': 8, 'G': 3}

    print("Ley-line network loaded.")

    # Fixed for Python 2.7
    mode = raw_input("\nChoose mode: (1) AI vs AI  (2) Human vs AI: ").strip()
    if mode == "2":
        pick = raw_input("Play as Player 1 (moves first) or Player 2? [1/2]: ").strip()
        human_turn = 0 if pick == "1" else 1
        play_human_vs_ai(graph, values, human_turn)
    else:
        play_game(graph, values)
      
