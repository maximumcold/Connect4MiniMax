from board import Board
import random
import pygame
import time
import pickle

PLAYER_1 = 1
PLAYER_2 = -1

def save_cache(cache, filename="cached_moves.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(cache, f)

def load_cache(filename="cached_moves.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

def minimax(board: Board, depth, alpha, beta, maximisingPlayer, cache):
    # * Hashes the board (the state of the current board in a tuple(tuple())) format
    board_hash = board.hash_board()
    # print(board_hash) 
    # * Checks if the current board state is in the cached memory
    if board_hash in cache:
        cached_result = cache[board_hash]
        # print("Cached result: ", cached_result)
        if cached_result is not None:
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
          
        if column is None:
            column = locations[0]

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
            
        if column is None:
            column = locations[0]
        result = (column, value)
    cache[board_hash] = result
    return result
    
# def iterative_deeping_search(board : Board, time_limit, max_depth, player):
#     start_time = time.time()
#     best_move = None
#     # board_copy = board.copy_board()
#     vaild_moves = board.find_all_valid_moves(board)
#     for depth in range(1, max_depth + 1):
#         print("Entering depth: ", depth)
        
#         if time.time() - start_time > time_limit:
#             print("Time limit reached.")
#             break
#         best_eval = float('-inf')
        
#         for move in vaild_moves:
#             board_copy = board.copy_board()
#             board_copy.play_move(move, player)
#             best_move, eval = minimax(board_copy, depth, float('-inf'), float('inf'), False)

#             if eval < best_eval:
#                 best_eval = eval
#                 best_move = move
                
#         if depth == max_depth:
#             print("Max depth reached. Best move:", best_move)
#             return best_move
#     return best_move
  
def main():
    pygame.init()
    running = True
    turn = 1
    screen = pygame.display.set_mode((700, 600))
    pygame.display.set_caption("Drawing with Pygame")
    
    max_player = True
    min_player = False
    
    cache = load_cache()
    board = Board(screen)
    
    while running:
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
                        if  board.check_win(board, turn):
                            print("Human player wins")
                            running = False
                        turn *= -1 # Switch to AI
                        board.draw_board()
       
        if turn == -1:  # AI player's turn
            col = minimax(board, depth=7, alpha= -float('inf'), beta = float('inf'), maximisingPlayer=min_player, cache=cache)[0]
            end_time = time.time()
            board.play_move(col, turn)
            if board.check_win(board, turn):
                print("AI player wins")
                running = False
            turn *= -1  # Switch to human player
        # * Checks for a tie in the game
        if len(board.find_all_valid_moves(board)) == 0 and board.is_terminal_node:
            print("Tie!")
            running = False
        
        board.draw_board()
        save_cache(cache)
    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    pygame.quit()      

if __name__ == "__main__":
    main()