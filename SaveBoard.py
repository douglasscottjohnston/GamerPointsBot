import os
import sqlite3

class SaveBoard:

    path = "./data/scoreboard.sqlite"

    def __init__(self, board):
        self.board = board
        self.main(self.board)
        
    def main(self, board):
        #SQLite database
        #Establishes sql connection
        con = sqlite3.connect(self.path)
        cur = con.cursor()

        if self.table_exists(cur):
            print("main(): Table exists.")
            cur.execute("DROP TABLE scoreboard")
            self.create_table(board, cur)

        else:
            print("main(): Table does not exist")
            self.create_table(board, cur)


        #commit changes to db
        con.commit()
        #close the connection
        con.close()

    def create_table(self, board, cur):
        table = '''CREATE TABLE scoreboard(user VARChar(255), score int)'''
        cur.execute(table)

        insert = '''INSERT INTO scoreboard(user, score) VALUES(?, ?)'''

        for member in board:
            print(member)
            print(board[member])
            data_tuple = (member, board[member])
            print(data_tuple)
            cur.execute(insert, data_tuple)
        
        query_table = "SELECT * from scoreboard"
        query_results = cur.execute(query_table)

        #prints the vaules in the table to the console
        print("(user, score)")
        for result in query_results:
            print(result)

    #returns a dictionary with the values in the table
    def get_values(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        values = {}

        if self.table_exists(cur):
            query_users = "SELECT user from scoreboard"
            user_results = cur.execute(query_users)
            query_scores = "SELECT score from scoreboard"
            score_results = cur.execute(query_scores)
            r = cur.fetchone()
            users = []
            scores = []

            # for 

            values = dict(zip(user_results, score_results))
        else:
            print("get_values(): Table does not exist")
            self.create_table(values, cur)
            values = self.get_values()

        con.close()
        return values

    def table_exists(self, cur):
        table_list = cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='scoreboard' ''')

        if table_list == []:
            print("def table_exists(): Table does not exist")
            return False
        else:
            print("def table_exists(): Table does exist")
            return True