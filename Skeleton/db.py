import sqlite3
from sqlite3 import Error

'''
Initializes the Table GAME
Do not modify
'''


def init_db():
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('CREATE TABLE GAME(current_turn TEXT, board TEXT,' +
                     'winner TEXT, player1 TEXT, player2 TEXT' +
                     ', remaining_moves INT)')
        print('Database Online, table created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
move is a tuple (current_turn, board, winner, player1, player2,
remaining_moves)
Insert Tuple into table
'''


def add_move(move):  # will take in a tuple
    sql = ('''INSERT INTO GAME (current_turn, board, winner, player1, player2,
            remaining_moves) VALUES (?,?,?,?,?,?);''')
    data = (str(move[0]), str(move[1]), move[2], move[3], move[4], move[5])
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute(sql, data)
        conn.commit()
    except Error as e:
        return False
        print(e)

    finally:
        if conn:
            conn.close()


'''
Get the last move played
return (current_turn, board, winner, player1, player2, remaining_moves)
'''


def getMove():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM GAME")
        result = cur.fetchall()
        if len(result) > 0:
            lastEntry = result[len(result)-1]
            return lastEntry
        else:
            return None
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
Clears the Table GAME
Do not modify
'''


def clear():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE GAME")
        print('Database Cleared')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()
