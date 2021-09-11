import unittest
from Gameboard import Gameboard
from flask import Flask, app, render_template, request, redirect, jsonify


# test case class for the Gameboard
class Test_TestGameboard(unittest.TestCase):

    def test_move(self):
        game = Gameboard()
        app = Flask(__name__)
        with app.app_context():
            print(game.makeMove('col1').get_data())


if __name__ == '__main__':
    unittest.main()
