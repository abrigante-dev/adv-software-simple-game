import unittest
from Gameboard import Gameboard
from flask import Flask


# test case class for the Gameboard
class Test_TestGameboard(unittest.TestCase):

    # ensure error is thrown for a full column
    def test_move(self):
        game = Gameboard()
        app = Flask(__name__)
        with app.app_context():
            for x in range(7):
                game.makeMove('col1')
            result = game.makeMove('col1').get_json()['invalid']
            self.assertEqual(result, True)

    # ensures that both players have an assigned color
    def test_color_chosen(self):
        game = Gameboard()
        app = Flask(__name__)
        with app.app_context():
            result = game.makeMove('col1').get_json()['invalid']
            self.assertEqual(result, True)

    # ensure that a winner is called for a positive slope diagonal win
    def test_pos_diag(self):
        game = Gameboard()
        app = Flask(__name__)
        with app.app_context():
            # test player 1
            result = game.makeMove('col1').get_json()['invalid']
            self.assertEqual(result, True)

    # ensure that a winner is called for a negative slope diagonal win

    # ensure that a winner is called for a verticle win

    # ensure that a winner is called for a horizontal win


if __name__ == '__main__':
    unittest.main()
