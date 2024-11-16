from board import Board
import random
import pygame
import time

PLAYER_1 = 1
PLAYER_2 = -1
    
def minimax(board: Board, depth, alpha, beta, maximisingPlayer):
    # * Gets all the valid locations on the current board
    locations = board.find_all_valid_moves(board)
    is_terminal = board.is_terminal_node(board)
    
    # * If the depth is reached or the board is unplayable, evaluate
    if depth <= 0 or is_terminal:
        if is_terminal:
            if board.check_win(board, PLAYER_1):
                return (None, 99999)
            elif board.check_win(board, PLAYER_2):
                return (None, -99999)
            else:
                return (None, 0)
        else:
            return (None, board.score_position(board, PLAYER_1 if maximisingPlayer else PLAYER_2))  
    
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
            new_score = minimax(board_copy, depth - 1, alpha, beta, False)[1]
            
            if new_score > value:
                value = new_score
                column = col
                
            if value > beta:
                break
            
            alpha = max(alpha, value)
          
        if column is None:
            column = locations[0]

        return (column, value)
    
    else:
        value = float('inf')
        column = None
        
        for col in locations:
            board_copy = board.copy_board()
            row = board_copy.get_next_open_row(board, col)
            if row is None:
                continue
            
            board_copy.play_move(col, PLAYER_2)
            
            new_score = minimax(board_copy, depth - 1, alpha, beta, True)[1]
        
            if new_score < value:
                value = new_score
                column = col
                
            if value < alpha:
                break
            
            beta = min(beta, value)
            
        if column is None:
            column = locations[0]
        return (column, value)
         
def main():
    pygame.init()
    running = True
    turn = 1
    screen = pygame.display.set_mode((700, 600))
    pygame.display.set_caption("Drawing with Pygame")
    
    max_player = True
    min_player = False
    
    board = Board(screen)

    while running:
        if turn == 1:
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
                            print("Human wins!")
                            running = False
                        turn *= -1
       
        if turn == -1:  # AI player's turn
            start_time = time.time()
            col = minimax(board, depth=8, alpha= -float('inf'), beta = float('inf'), maximisingPlayer=min_player)[0]
            end_time = time.time()
            print(end_time - start_time)
            if col is not None:
                board.play_move(col, turn)
                if board.check_win(board, turn):
                    print("AI wins!")
                    running = False
                turn *= -1  # Switch to human player
                    
        board.draw_board()
    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    pygame.quit()      

if __name__ == "__main__":
    main()