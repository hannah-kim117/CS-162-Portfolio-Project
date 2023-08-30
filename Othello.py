# Author: Hannah Kim
# GitHub username: hannah-kim117
# Date: 6/11/2023
# Description: write a class called Othello that allows two people to play the game of text-based Othello.
# The goal is to capture the opponent's pieces and have a majority of your own pieces at the end of the game.


class Player:
    '''A class to represent the players playing in the game'''

    def __init__(self, name, color):
        '''Initializes the data members. All data members are private.'''
        self._name = name
        self._color = color

    def get_name(self):
        '''Get method for the player's name'''
        return self._name

    def get_color(self):
        '''Get method for the player's piece color'''
        return self._color


class Othello:
    '''A class to represent Othello objects which contains info about players and the board'''

    def __init__(self):
        '''Initializes the data members. All data members are private.
        Takes no parameters.
        '''

        # "." for the entire board
        self._board = []
        for row in range(10):
            row_list = []
            if row == 0 or row == 9:
                row_list = ["*" for edge in range(10)]
            else:
                for col in range(10):
                    if col == 0 or col == 9:
                        row_list.append('*')
                    else:
                        row_list.append('.')
            self._board.append(row_list)

        self._board[4][4] = "O"  # starting white piece
        self._board[5][5] = "O"  # starting white piece
        self._board[4][5] = "X"  # starting black piece
        self._board[5][4] = "X"  # starting black piece
        self._players = []  # empty list to store player objects

    def print_board(self):
        '''Prints out the current board, including the boundaries
        Takes no parameters.
        '''

        print(" 0 1 2 3 4 5 6 7 8 9")  # numbers for top column
        for row in range(10):
            print(row, end=" ")

            for column in range(10):
                print(self._board[row][column], end=" ")

            print()

    def create_player(self, player_name, color):
        '''Creates a player object with the given name and color (black or white) and adds it to the player list
        Communicates with the class "Player"
        Takes two parameters:
        player_name - Represents the name of the player playing
        color - Represents the color of the piece the player is playing with
        '''

        player = Player(player_name, color)
        self._players.append(player)  # add player object to list

    def return_winner(self):
        '''Returns whether white or black player wins the game or tie
        Purpose: to determine the winner of the game or if it's a tie
        Takes no parameters.
        '''

        black_count = 0
        white_count = 0
        for row in self._board[0:10]:
            for piece in row[0:10]:
                if piece == "O":
                    white_count += 1
                if piece == "X":
                    black_count += 1

        if black_count > white_count:
            winner = [player for player in self._players if player.get_color() == "black"][0]
            return f"Winner is black player: {winner.get_name()}"
        if white_count > black_count:
            winner = [player for player in self._players if player.get_color() == "white"][0]
            return f"Winner is white player: {winner.get_name()}"
        else:
            return "It's a tie."

    def return_available_positions(self, color):
        '''Returns a list of possible positions for the player to move on the board
        Takes one parameter:
        color - Represents the color of the piece the player is playing with
        '''

        available_positions = []  # empty list to store available positions
        for row in range(10):
            for column in range(10):
                if self._board[row][column] == "." and self.valid_move(color, (row, column)):
                    available_positions.append((row, column))
        return available_positions

    def make_move(self, color, piece_position):
        '''Puts a piece at selected position, flips the opponent's piece, and updates the board
        Takes two parameters:
        color - Represents the color of the piece at the given position
        piece_position - Represents the position of the specified color piece
        '''

        row, column = piece_position

        my_piece = self.get_my_piece(color)
        opponent_piece = self.get_opponent_piece(color)

        self._board[row][column] = my_piece # Flip

        for row_direction in [-1, 0, 1]:
            for col_direction in [-1, 0, 1]:
                if row_direction == 0 and col_direction == 0:
                    continue
                surrounding_row = row + row_direction
                surrounding_col = column + col_direction
                if self._board[surrounding_row][surrounding_col] == opponent_piece:
                    while self._board[surrounding_row][surrounding_col] == opponent_piece:
                        surrounding_col += col_direction
                        surrounding_row += row_direction
                    if self._board[surrounding_row][surrounding_col] == my_piece:
                        # Backtrack
                        surrounding_row -= row_direction
                        surrounding_col -= col_direction
                        while self._board[surrounding_row][surrounding_col] == opponent_piece:
                            self._board[surrounding_row][surrounding_col] = self.get_my_piece(color) # FLIP
                            surrounding_col -= col_direction
                            surrounding_row -= row_direction
        return self._board

    def valid_move(self, color, piece_position):
        ''' Returns True or False depending on whether the move is valid
        Takes two parameters:
        color - Represents the color of the piece the player is playing with
        piece_position - Represents the position of the given color piece on the board
        Purpose: To determine whether the move chosen by the player is a valid move
        '''

        row, column = piece_position

        opponent_piece = self.get_opponent_piece(color)
        my_piece = self.get_my_piece(color)

        for row_direction in [-1, 0, 1]:
            for col_direction in [-1, 0, 1]:
                if row_direction == 0 and col_direction == 0:
                    continue
                surrounding_row = row + row_direction
                surrounding_col = column + col_direction
                if self._board[surrounding_row][surrounding_col] == opponent_piece:
                    while self._board[surrounding_row][surrounding_col] == opponent_piece:
                        surrounding_col += col_direction
                        surrounding_row += row_direction
                    if self._board[surrounding_row][surrounding_col] == my_piece:
                        return True
        return False

    def play_game(self, player_color, piece_position):
        '''Makes a move at the specified position or if invalid, returns invalid message and provides possible positions
        Takes two parameters:
        player_color - Represents the color of the piece played by the player
        piece_position - Represents the position of the given color piece
        Reference to valid_move method to check whether the move the player chose is valid or invalid
        '''

        valid_moves = self.return_available_positions(player_color)
        if piece_position not in valid_moves:
            print("Invalid move")
            print("Here are the valid moves: ", valid_moves)
            return "Invalid move"

        # If position valid, make the move and update the board
        self.make_move(player_color, piece_position)

        # If game is ended:
        if len(valid_moves) == 0:
            print("Game is ended.")
            print(self.return_winner())

    def get_opponent_piece(self, color):
        '''get method that gets the opponent's piece'''
        return 'O' if color == 'black' else 'X'

    def get_my_piece(self, color):
        '''get method that gets my piece'''
        return 'O' if color == 'white' else 'X'


# game = Othello()
# game.print_board()
# game.create_player("Helen", "white")
# game.create_player("Leo", "black")
# game.play_game("black", (6, 5))
# game.play_game("white", (6000,40000))
# game.print_board()
# game.play_game("white", (6, 6))
# game.print_board()
# game.play_game("white", (7, 5))
# game.print_board()
