import db
from flask import jsonify
import ast


class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42
        self.checkSave()

    # checks if there is a saved game and runs it if there is
    def checkSave(self):
        result = db.getMove()
        if result is not None:
            self.current_turn = result[0]
            self.board = ast.literal_eval(result[1])
            self.player1 = result[3]
            self.player2 = result[4]
            self.remaining_moves = result[5]

    def setP1(self, color):
        self.player1 = color
        if self.player1 == 'red':
            self.player2 = 'yellow'
        else:
            self.player2 = 'red'

    def getP1(self):
        return self.player1

    def getP2(self):
        return self.player2

    # returns number of remaining moves
    def getRemainingMoves(self):
        movesLeft = 0
        for rows in self.board:
            for elem in rows:
                if elem == 0:
                    movesLeft += 1
        return movesLeft

    # makes a move
    def makeMove(self, colIn):
        # check if both players have picked a color already
        if self.player1 == '':
            return jsonify(
                move=self.board,
                invalid=True, reason="player 1 must chose a color", winner="")
        # if someone has already won
        elif self.remaining_moves == 0:
            return jsonify(
                move=self.board,
                invalid=False, winner=self.game_result)

        col = int(list(colIn)[3]) - 1
        x = 5
        while x > -1:
            if self.board[x][col] == 0:
                toReturn = ''
                if self.current_turn == 'p1':
                    self.board[x][col] = self.player1
                    toReturn = self.checkWinner()
                    self.current_turn = 'p2'
                else:
                    self.board[x][col] = self.player2
                    toReturn = self.checkWinner()
                    self.current_turn = 'p1'
                return toReturn
            else:
                x -= 1
        return jsonify(
            move=self.board, invalid=True, reason="column full", winner="")

    # checks if someone won the game
    def checkWinner(self):
        next_turn = ''
        if self.current_turn == 'p1':
            colorCheck = self.player1
            next_turn = 'p2'
        else:
            colorCheck = self.player2
            next_turn = 'p1'

        # check horizontal
        for c in range(7-3):
            for r in range(6):
                if (self.board[r][c] == colorCheck
                        and self.board[r][c+1] == colorCheck
                        and self.board[r][c+2] == colorCheck
                        and self.board[r][c+3] == colorCheck):
                    self.game_result = self.current_turn
                    db.add_move([next_turn, self.board, self.current_turn,
                                self.player1, self.player2,
                                self.getRemainingMoves()])
                    self.remaining_moves = 0
                    return jsonify(
                        move=self.board,
                        invalid=False, winner=self.current_turn)

        # Check vertical locations for win
        for c in range(7):
            for r in range(6-3):
                if (self.board[r][c] == colorCheck
                        and self.board[r+1][c] == colorCheck
                        and self.board[r+2][c] == colorCheck
                        and self.board[r+3][c] == colorCheck):
                    self.game_result = self.current_turn
                    db.add_move([next_turn, self.board, self.current_turn,
                                self.player1, self.player2,
                                self.getRemainingMoves()])
                    self.remaining_moves = 0
                    return jsonify(
                        move=self.board,
                        invalid=False, winner=self.current_turn)

        # Check positively sloped diaganols
        for c in range(7-3):
            for r in range(6-3):
                if (self.board[r][c] == colorCheck
                        and self.board[r+1][c+1] == colorCheck
                        and self.board[r+2][c+2] == colorCheck
                        and self.board[r+3][c+3] == colorCheck):
                    self.game_result = self.current_turn
                    db.add_move([next_turn, self.board, self.current_turn,
                                self.player1, self.player2,
                                self.getRemainingMoves()])
                    self.remaining_moves = 0
                    return jsonify(
                        move=self.board,
                        invalid=False, winner=self.current_turn)

        # Check negatively sloped diaganols
        for c in range(7-3):
            for r in range(3, 6):
                if (self.board[r][c] == colorCheck
                        and self.board[r-1][c+1] == colorCheck
                        and self.board[r-2][c+2] == colorCheck
                        and self.board[r-3][c+3] == colorCheck):
                    self.game_result = self.current_turn
                    db.add_move([next_turn, self.board, self.current_turn,
                                self.player1, self.player2,
                                self.getRemainingMoves()])
                    self.remaining_moves = 0
                    return jsonify(
                        move=self.board,
                        invalid=False, winner=self.current_turn)

        # returns when a player makes a valid move but doesn't win
        db.add_move([next_turn, self.board, "", self.player1, self.player2,
                    self.getRemainingMoves()])
        self.remaining_moves -= 1
        return jsonify(move=self.board, invalid=False, winner="")


'''
Add Helper functions as needed to handle moves and update board and turns
'''
