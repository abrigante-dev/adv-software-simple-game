import unittest
from Gameboard import Gameboard
from flask import Flask
import db


# test case class for the db class
class Test_Testdb(unittest.TestCase):

    # clears the db for each test
    def setUp(self):
        self.game = Gameboard
        db.clear()
        db.init_db()
        self.game = Gameboard()
        self.app = Flask(__name__)

    # clears the db after each test, really only matters on the final test
    def tearDown(self):
        db.clear()
        # db.init_db()

    # ensure the addMove function properly adds the move to the DB
    def test_addMove(self):
        db.add_move('p2', self.game.board, "", 'red', 'yellow', 41)


if __name__ == '__main__':
    unittest.main()
    # db.clear()
