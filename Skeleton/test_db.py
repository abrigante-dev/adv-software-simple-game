import unittest
from Gameboard import Gameboard
from flask import Flask
import db
import sqlite3
from sqlite3 import Error
import ast


# test case class for the db class
class Test_Testdb(unittest.TestCase):

    # clears the db for each test
    def setUp(self):
        db.clear()
        db.init_db()
        self.game = Gameboard()
        self.app = Flask(__name__)
        self.game = Gameboard()
        self.testEntry = ['p2', self.game.board, "", 'red', 'yellow', 41]

    # clears the db after each test, really only matters on the final test
    def tearDown(self):
        db.clear()
        # db.init_db()

    # ensure the addMove happy path function properly adds the move to the DB
    def test_addMove(self):
        db.add_move(self.testEntry)
        # query the db to ensure the move was added, checks last entry
        conn = None
        try:
            conn = sqlite3.connect('sqlite_db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM GAME")
            result = cur.fetchall()
            # ensure the entry is the db
            self.assertGreater(len(result), 0)
            # ensure the record is correct
            lastEntry = result[len(result)-1]
            for x in range(len(lastEntry)-1):
                # handles the 2d board array
                if x == 1:
                    self.assertEqual(
                        self.testEntry[x],
                        ast.literal_eval(lastEntry[x])
                        )
                else:
                    self.assertEqual(
                        lastEntry[x],
                        self.testEntry[x],
                        "Not equal: {}".format(lastEntry[x])
                        )
            print('addMove Passed')
        except Error as e:
            print(e)

        finally:
            if conn:
                conn.close()

    # ensure getMove properly returns a value
    def test_getMove(self):
        # adds a move to the db
        db.add_move(self.testEntry)
        lastEntry = db.getMove()
        # checks if the returned move is correct
        for x in range(len(lastEntry)-1):
            if x == 1:
                self.assertEqual(
                    self.testEntry[x],
                    ast.literal_eval(lastEntry[x])
                    )
            else:
                self.assertEqual(
                    lastEntry[x],
                    self.testEntry[x],
                    "Not equal: {}".format(lastEntry[x])
                    )
        print('test_getMove: Passed')

    # ensure the db is initialized correctly
    def test_init_db(self):
        # first clear and ensure there is not current db
        db.clear()
        db.init_db()
        # check if the db table excists
        result = ''
        conn = None
        try:
            conn = sqlite3.connect('sqlite_db')
            cur = conn.cursor()
            cur.execute(
                """ SELECT name FROM sqlite_master
                WHERE type='table' AND name='GAME'; """
                )
            result = cur.fetchall()
        except Error as e:
            self.fail
            print(e)

        finally:
            if conn:
                conn.close()
        self.assertGreater(len(result), 0)

    # ensure the db clears correctly
    def test_clear(self):
        db.clear()
        result = ''
        conn = None
        try:
            conn = sqlite3.connect('sqlite_db')
            cur = conn.cursor()
            cur.execute(
                """ SELECT name FROM sqlite_master
                WHERE type='table' AND name='GAME'; """
                )
            result = cur.fetchall()
        except Error as e:
            self.fail
            print(e)

        finally:
            if conn:
                conn.close()
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
    # db.clear()
