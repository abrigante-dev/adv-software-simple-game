import unittest
from Gameboard import Gameboard
from flask import Flask
import db


# test case class for the Gameboard
class Test_TestGameboard(unittest.TestCase):

    # clears the db for each test
    def setUp(self):
        db.clear()
        db.init_db()
        self.game = Gameboard()
        self.app = Flask(__name__)

    # ensure error is thrown for a full column
    def test_move(self):
        with self.app.app_context():
            for x in range(7):
                self.game.makeMove('col1')
            result = self.game.makeMove('col1').get_json()['invalid']
            self.assertEqual(result, True)
        print('test_move: Passed')

    # ensures that both players have an assigned color
    def test_color_chosen(self):
        with self.app.app_context():
            result = self.game.makeMove('col1').get_json()['invalid']
            self.assertEqual(result, True)
        print('test_color_chosen: Passed')

    # ensure that a winner is called for a positive slope diagonal win
    def test_pos_diag(self):
        self.game.setP1('red')
        with self.app.app_context():
            self.game.makeMove('col1')
            self.game.makeMove('col2')
            self.game.makeMove('col2')
            self.game.makeMove('col3')
            self.game.makeMove('col3')
            self.game.makeMove('col4')
            self.game.makeMove('col3')
            self.game.makeMove('col4')
            self.game.makeMove('col4')
            self.game.makeMove('col6')
            # winning move
            result = self.game.makeMove('col4').get_json()['winner']
            self.assertEqual(result, 'p1')
        print('test_pos_diag: Passed')

    # ensure that a winner is called for a negative slope diagonal win
    def test_neg_diag(self):
        self.game.setP1('red')
        with self.app.app_context():
            for x in range(4):
                self.game.makeMove('col4')
            self.game.makeMove('col3')
            self.game.makeMove('col3')
            self.game.makeMove('col2')
            self.game.makeMove('col3')
            self.game.makeMove('col6')
            self.game.makeMove('col2')
            self.game.makeMove('col6')
            # winning move
            result = self.game.makeMove('col1').get_json()['winner']
            self.assertEqual(result, 'p2')
        print('test_neg_diag: Passed')

    # ensure that a winner is called for a verticle win
    def test_vert(self):
        self.game.setP1('red')
        with self.app.app_context():
            for x in range(3):
                self.game.makeMove('col1')
                self.game.makeMove('col2')
            # winning move
            result = self.game.makeMove('col1').get_json()['winner']
            self.assertEqual(result, 'p1')
        print('test_vert: Passed')

    # ensure that a winner is called for a horizontal win
    def test_horizontal(self):
        self.game.setP1('red')
        with self.app.app_context():
            for x in range(1, 4):
                self.game.makeMove('col{}'.format(x))
                self.game.makeMove('col{}'.format(x))
            # winning move
            result = self.game.makeMove('col4').get_json()['winner']
            self.assertEqual(result, 'p1')
        print('test_horizontal: Passed')

    # ensure the game starts and saves correctly
    def test_save(self):
        self.game.setP1('red')
        with self.app.app_context():
            for x in range(1, 4):
                self.game.makeMove('col{}'.format(x))
                self.game.makeMove('col{}'.format(x))
                self.game = Gameboard()
            result = self.game.makeMove('col4').get_json()['winner']
            self.assertEqual(result, 'p1')
        print('test_save: Passed')

    # ensure the game starts with the correct player's turn after load
    def test_starting_player(self):
        self.game.setP1('red')
        with self.app.app_context():
            self.game.makeMove('col1')
            self.game = Gameboard()
            self.assertEqual(self.game.current_turn, 'p2')
        print('test_starting_player: Passed')


if __name__ == '__main__':
    unittest.main()
    db.clear()
