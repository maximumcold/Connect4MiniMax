from board import Board
import random
import pygame
import time
import pickle
import multiprocessing

PLAYER_1 = 1
PLAYER_2 = -1

def save_cache(cache, filename="cached_moves.pkl"):
    try:
        with open(filename, "rb") as f:
            existing_cache = pickle.load(f)
    except FileNotFoundError:
        existing_cache = {}
    
    # Merge new cache with existing cache
    existing_cache.update(cache)
    
    with open(filename, "wb") as f:
        pickle.dump(existing_cache, f)

def load_cache(filename="cached_moves.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

def minimax(board: Board, depth, alpha, beta, maximisingPlayer, cache):
    # * Hashes the board (the state of the current board in a tuple(tuple())) format
    board_hash = board.hash_board()
    
    # * Checks if the current board state is in the cached memory
    if cache and board_hash in cache:
        # print("Cached result: ", cache[board_hash])
        return cache[board_hash]
    
        
    # * Gets all the valid locations on the current board
    locations = board.find_all_valid_moves(board)
    is_terminal = board.is_terminal_node(board)
            
    # * If the depth is reached or the board is unplayable, evaluate
    if depth <= 0 or is_terminal:
        if is_terminal:
            if board.check_win(board, PLAYER_1):
                result =  (None, 99999)
            elif board.check_win(board, PLAYER_2):
                result = (None, -99999)
            else:
                result = (None, 0)
        else:
            result = (None, board.score_position(board, PLAYER_1 if maximisingPlayer else PLAYER_2))  
    
        if result[0] is not None:
            cache[board_hash] = result
        return result
    # * If the current player is the maximising player  
    if maximisingPlayer:
        value = -float('inf')
        column = None
        
        # * Explore every possible move
        for col in locations:
            board_copy = board.copy_board()
            row = board_copy.get_next_open_row(board, col)
            
            if row is None:
                continue
        
            board_copy.play_move(col, PLAYER_1)
            # * Call minimax recursively 
            new_score = minimax(board_copy, depth - 1, alpha, beta, False, cache)[1]
            
            if new_score > value:
                value = new_score
                column = col
                
            if value > beta:
                break
            
            alpha = max(alpha, value)
        result = (column, value)
    
    else:
        value = float('inf')
        column = None
        
        for col in locations:
            board_copy = board.copy_board()
            row = board_copy.get_next_open_row(board, col)
            if row is None:
                continue
            
            board_copy.play_move(col, PLAYER_2)
            new_score = minimax(board_copy, depth - 1, alpha, beta, True, cache)[1]
        
        
            if new_score < value:
                value = new_score
                column = col
                
            if value < alpha:
                break
            
            beta = min(beta, value)
        result = (column, value)
    cache[board_hash] = result
    
    return result

def main():
    pygame.init()
    running = True
    turn = 1
    screen = pygame.display.set_mode((700, 600))
    pygame.display.set_caption("Drawing with Pygame")
    
    max_player = True
    min_player = False
    depth = 7
    
    cache = load_cache()
    board = Board(screen)
    board.draw_board()
    while running:
    
        # if turn == 1:  # AI player's turn
        #     col, value = minimax(board, depth, alpha= -float('inf'), beta = float('inf'), maximisingPlayer=max_player, cache=cache)
        #     print(f"Maximizing move score: {value}")
            
        #     board.play_move(col, turn)
        #     if board.check_win(board, turn):
        #         print("AI player one wins")
        #         running = False
        #     turn *= -1 # Switch to human player
        #     board.draw_board()
        if turn == 1: # Human player's turn
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]
                    column = x // 100
                    row = board.valid_move(board, column)
                    if row != None:  
                        board.play_move(column, turn)
                        board.score_position(board, PLAYER_1)
                        # print(f"Human move score: {score}")
                        
                        if  board.check_win(board, turn):
                            print("Human player wins")
                            running = False
                        turn *= -1 # Switch to AI
                        board.draw_board()
        
        if turn == -1:  # AI player's turn
        
            col, value = minimax(board, depth, alpha= -float('inf'), beta = float('inf'), maximisingPlayer=min_player, cache=cache)
            board.play_move(col, turn)
            print(f"Minimizing move score: {value}")
            if board.check_win(board, turn):
                print("AI player two wins")
                running = False
            turn *= -1  # Switch to human player
            board.draw_board()
        # * Checks for a tie in the game
        if len(board.find_all_valid_moves(board)) == 0 and board.is_terminal_node:
            print("Tie!")
            running = False
        
        board.draw_board()
        
    end = True
    save_cache(cache)
    
    while end:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
    pygame.quit()      

if __name__ == "__main__":
    main()


