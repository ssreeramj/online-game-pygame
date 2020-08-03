class RPSGame:
    def __init__(self, id):
        self.did_p1_play = False
        self.did_p2_play = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, player):
        return self.moves[player]

    def update_move(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.did_p1_play = True
        else:
            self.did_p2_play = True

    def is_connected(self):
        return self.ready

    def did_both_play(self):
        return self.did_p1_play and self.did_p2_play

    def get_winner(self):
        p1_move = self.moves[0].upper()[0]
        p2_move = self.moves[1].upper()[0]
        move = p1_move + p2_move

        winner_dict = {
            'RS': 0,
            'SR': 1,
            'PR': 0,
            'RP': 1,
            'SP': 0,
            'PS': 1,
        }

        result = winner_dict.get(move, -1)

        if result != -1:
            self.wins[result] += 1

        return result

    def reset(self):
        self.did_p1_play = False
        self.did_p2_play = False
