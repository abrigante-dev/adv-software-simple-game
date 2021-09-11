import unittest
from Gameboard import Gameboard
from flask import Flask
import db


# test case class for the Gameboard
class Test_TestGameboard(unittest.TestCase):

    # ensure error is thrown for a full column
    def test_move(self):
        db.clear()
        db.init_db()
        game = Gameboard()
        app = Flask(__name__)
        with app.app_context():
            for x in range(7):
                game.makeMove('col1')
            result = game.makeMove('col1').get_json()['invalid']
            self.assertEqual(result, True)

    # ensures that both players have an assigned color
    def test_color_chosen(self):
        db.clear()
        db.init_db()
        game = Gameboard()
        app = Flask(__name__)
        with app.app_context():
            result = game.makeMove('col1').get_json()['invalid']
            self.assertEqual(result, True)

    # ensure that a winner is called for a positive slope diagonal win
    def test_pos_diag(self):
        db.clear()
        db.init_db()
        game = Gameboard()
        game.setP1('red')
        app = Flask(__name__)
        with app.app_context():
            game.makeMove('col1')
            game.makeMove('col2')
            game.makeMove('col2')
            game.makeMove('col3')
            game.makeMove('col3')
            game.makeMove('col4')
            game.makeMove('col3')
            game.makeMove('col4')
            game.makeMove('col4')
            game.makeMove('col5')
            # winning move
            result = game.makeMove('col4').get_json()['winner']
            self.assertEqual(result, 'p1')

    # ensure that a winner is called for a negative slope diagonal win
    def test_neg_diag(self):
        db.clear()
        db.init_db()
        game = Gameboard()
        game.setP1('red')
        app = Flask(__name__)
        with app.app_context():
            for x in range(4):
                game.makeMove('col4')
            game.makeMove('col3')
            game.makeMove('col3')
            game.makeMove('col2')
            game.makeMove('col3')
            game.makeMove('col6')
            game.makeMove('col2')
            game.makeMove('col6')
            # winning move
            result = game.makeMove('col1').get_json()['winner']
            self.assertEqual(result, 'p2')
        db.clear()

    # ensure that a winner is called for a verticle win
    def test_vert(self):
        db.clear()
        db.init_db()
        game = Gameboard()
        game.setP1('red')
        app = Flask(__name__)
        with app.app_context():
            for x in range(3):
                game.makeMove('col1')
                game.makeMove('col2')
            # winning move
            result = game.makeMove('col1').get_json()['winner']
            db.clear()
            self.assertEqual(result, 'p1')

    # ensure that a winner is called for a horizontal win
    def test_horizontal(self):
        db.clear()
        db.init_db()
        game = Gameboard()
        game.setP1('red')
        app = Flask(__name__)
        with app.app_context():
            for x in range(1, 4):
                game.makeMove('col{}'.format(x))
                game.makeMove('col{}'.format(x))
            # winning move
            result = game.makeMove('col4').get_json()['winner']
            self.assertEqual(result, 'p1')
        db.clear()

    # ensure the game starts and saves correctly
    def test_save(self):
        db.clear()
        db.init_db()
        game = Gameboard()
        game.setP1('red')
        app = Flask(__name__)
        with app.app_context():
            for x in range(1, 4):
                game.makeMove('col{}'.format(x))
                game.makeMove('col{}'.format(x))
                game = Gameboard()
            result = game.makeMove('col4').get_json()['winner']
            self.assertEqual(result, 'p1')
        db.clear()

    # ensure the game starts with the correct player's turn after load
    def test_starting_player(self):
        db.clear()
        db.init_db()
        game = Gameboard()
        game.setP1('red')
        app = Flask(__name__)
        with app.app_context():
            game.makeMove('col1')
            game = Gameboard()
            self.assertEqual(game.current_turn, 'p2')
        db.clear()


if __name__ == '__main__':
    unittest.main()
    db.clear()
