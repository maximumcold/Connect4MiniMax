"""Board logic for the Connect 4 game"""
import pygame
import sys
import copy
import hashlib

class Board:
    
    BOARD = [[0 for _ in range(7)] for _ in range(6)]
    
    # Player numbers, used for drawing and evaluation
    PLAYER_ONE = 1
    PLAYER_TWO = -1
   
   # Color values
    WHITE =(255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    
    def __init__(self, screen) -> None:
        #Assign a screen to the board
        self.screen = screen
    
    def draw_board(self) -> None:
        self.screen.fill(self.WHITE)
        
        # Grid using lines
        for i in range(7):
            pygame.draw.line(self.screen, self.BLACK, (i * 100, 0), (i * 100, 600), 2)        
        for i in range(6):
            pygame.draw.line(self.screen, self.BLACK, (0, i * 100), (700, i * 100), 2)

        # Loops through the board, drawing any pieces it finds
        for i in range(6):  
            for j in range(7):  
                if self.BOARD[i][j] == self.PLAYER_ONE:
                    pygame.draw.circle(self.screen, self.RED, (j * 100 + 50, i * 100 + 50), 45)
                elif self.BOARD[i][j] == self.PLAYER_TWO:
                    pygame.draw.circle(self.screen, self.BLUE, (j * 100 + 50, i * 100 + 50), 45)
                else:
                    continue
        pygame.display.flip()
        
    def play_move(self, column, player) -> None:
        # Check if the column index is within the valid range
        if column is None:
            return
        if column < 0 or column >= 7:
            raise ValueError("Column index out of range")
    
        # Plays the move on the inputted column
        for i in range(5, -1, -1):
            # Makes sure it plays it at the lowest possible position
            # print(i)
            if self.BOARD[i][column] == 0:
                self.BOARD[i][column] = player
                break
            
        
    def check_win(self, board, player) -> bool:
        
        # Easier to store the grid as a single variable
        map = board.BOARD
        
        count = 0
        # Checks for wins for the player that just made a move, scanning whole map
        # Could be faster as it really only needs to check the area that a piece was just placed
        # TODO: Make check faster
        for i in range(7):
            count = 0
            for j in range(6):
                if map[j][i] == player:
                    count += 1
                    if count == 4:
                        
                        return True
                else:
                    count = 0
                    
        count = 0
        for i in range(6):
            count = 0
            for j in range(7):
                if map[i][j] == player:
                    count += 1  
                    if count == 4:
                        return True
                else:
                    count = 0
                    
        count = 0
        for i in range(6):
            for j in range(7):
                if i + 3 < 6 and j + 3 < 7:
                    if map[i][j] == player and map[i + 1][j + 1] == player and map[i + 2][j + 2] == player and map[i + 3][j + 3] == player:
                        return True
                if i + 3 < 6 and j - 3 >= 0:
                    if map[i][j] == player and map[i + 1][j - 1] == player and map[i + 2][j - 2] == player and map[i + 3][j - 3] == player:
                        return True
        return False
    
    def valid_move(self, board, column):
        for i in range(5, -1, -1):  # Start checking from the bottom row upwards, does this in play_move as well
            if board.BOARD[i][column] == 0:
                return i
        return None
    def find_all_valid_moves(self, board) -> list[int]:
        # * Finds all the columns that can be played ons
        valid_moves = []
        for col in range(7):
            if self.valid_move(board, col) is not None:  # Check if there's a valid row
                valid_moves.append(col)
        return valid_moves
    
    def score_position(self, board, piece):
        # * Counts up the number of pieces in each 4x4 block
        # * Then it passes the sum through the evaluation method to score the position
        score = 0
        opp_piece = self.PLAYER_ONE if piece == self.PLAYER_TWO else self.PLAYER_TWO

        board = board.BOARD

        # Score centre column
        centre_array = [board[r][7 // 2] for r in range(6)]
        score += centre_array.count(piece) * 10

        # Horizontal scoring
        for row in range(6):
            for col in range(4):  # Only need to check up to the 4th column
                count_piece = sum(1 for i in range(4) if board[row][col + i] == piece)
                count_opp = sum(1 for i in range(4) if board[row][col + i] == opp_piece)
                count_empty = sum(1 for i in range(4) if board[row][col + i] == 0)
                score += self.evaluate_counts(count_piece, count_opp, count_empty)
        # Vertical scoring
        for col in range(7):
            for row in range(3):  # Only need to check up to the 3rd row
                count_piece = sum(1 for i in range(4) if board[row + i][col] == piece)
                count_opp = sum(1 for i in range(4) if board[row + i][col] == opp_piece)
                count_empty = sum(1 for i in range(4) if board[row + i][col] == 0)
                score += self.evaluate_counts(count_piece, count_opp, count_empty)
        # Positive diagonal scoring
        for row in range(6 - 3):  # Ensure the diagonal doesn't go out of bounds vertically
            for col in range(7 - 3):  # Ensure the diagonal doesn't go out of bounds horizontally
                count_piece = sum(1 for i in range(4) if board[row + i][col + i] == piece)
                count_opp = sum(1 for i in range(4) if board[row + i][col + i] == opp_piece)
                count_empty = sum(1 for i in range(4) if board[row + i][col + i] == 0)
                score += self.evaluate_counts(count_piece, count_opp, count_empty)
        # Negative diagonal scoring
        for row in range(3, 6):  # Start from the 3rd row to avoid out-of-bounds diagonals
            for col in range(7 - 3):  # Ensure the diagonal doesn't go out of bounds horizontally
                count_piece = sum(1 for i in range(4) if board[row - i][col + i] == piece)
                count_opp = sum(1 for i in range(4) if board[row - i][col + i] == opp_piece)
                count_empty = sum(1 for i in range(4) if board[row - i][col + i] == 0)
                score += self.evaluate_counts(count_piece, count_opp, count_empty)
        # Block opponent's diagonal win
        for row in range(6 - 3):
            for col in range(7 - 3):
                # Check for opponent's diagonal threat and block it
                if sum(1 for i in range(4) if board[row + i][col + i] == opp_piece) == 3 and \
                sum(1 for i in range(4) if board[row + i][col + i] == 0) == 1:
                    score -= 100  # Penalty for not blocking
                if sum(1 for i in range(4) if board[row + 3 - i][col + i] == opp_piece) == 3 and \
                sum(1 for i in range(4) if board[row + 3 - i][col + i] == 0) == 1:
                    score -= 100  # Penalty for not blocking
        
        if piece == -1:
            score *= -1
        return score

    def evaluate_counts(self, count_piece, count_opp, count_empty):
        score = 0
        # * Scores each direction
        # * Score goes up if you are closer to a win and down if you allow the opponent to win
        
        if count_piece == 3 and count_empty == 1:
            score += 5
        elif count_piece == 2 and count_empty == 2:
            score += 2
        elif count_opp == 3 and count_empty == 1:
            score -= -4
        return score        
    
    def is_terminal_node(self, board):
        # * Checks if there are any available moves left
        return board.check_win(board, self.PLAYER_ONE) or board.check_win(board, self.PLAYER_TWO) or len(self.find_all_valid_moves(board)) == 0
            
    def copy_board(self):
        # * Manually copy only necessary attributes to avoid pygame surfaces
        new_board = Board(self.screen)
        new_board.BOARD = [row[:] for row in self.BOARD]  # Copy the grid state
        return new_board
    
    def get_next_open_row(self, board, col):
        # * Finds the next available row that can be played
        return self.valid_move(board, col)
            
    def hash_board(self):
        return tuple(tuple(row) for row in self.BOARD)