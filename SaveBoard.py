import os
import pickle


class SaveBoard:
    board = {}

    def __init__(self, board):
        self.board = board

    def save_obj(self, obj):
        with open("./obj/scoreboard.pkl", 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def load_obj(self):
        try:
            with open("./obj/scoreboard.pkl", 'rb') as f:
                return pickle.load(f)
        except (OSError, IOError) as e:
            foo = {}
            return foo
