import gym
import numpy as np

import random
import itertools

from gym import error, spaces, utils
from gym.utils import seeding

class BlockSudoku(gym.Env):
    metadata = {'render.modes': ['human']}


    def __init__(self):
        self.game = BlockSudokuGame()
        self.factory = BlockFactory()

        # Generate first three blocks and game board
        self.main_board = self.game.new_board()
        self.block_queue = self.factory.generate_3blocks()

        # reset total score
        self.is_running = True
        self.total_score = 0


    # Returns state, reward, done, and {}
    def step(self, action):
        reward = 0
        done = not self.is_running
        state = self.game.get_state(self.block_queue, self.main_board)

        # Extra sanity check
        if done:
            print('Game is already finished! Please call reset() to restart');
            return state, 0, done, {}

        # Sanity check
        if(action.shape[0] != 3 and action.shape[1] != 9):
            print("Invalid dimensions for action! Expected 3x9 array.")
            return None

        # Translate to block and board position
        action_input = np.argmax(action, axis=1)
        queue_pos = action_input[0]
        # Make sure we have that block in queue or punish the user.
        if(queue_pos >= len(self.block_queue)):
            return state, -1, done, {}

        selected_block = self.block_queue[queue_pos]
        x_pos = action_input[1]
        y_pos = action_input[2]

        # Make sure we can make that move or punish the user
        if(not self.game.check_if_valid_move(x_pos, y_pos, selected_block, self.main_board)):
            return state, -1, done, {}

        # Commit the action to board
        if not self.game.place_block(x_pos, y_pos, selected_block, self.main_board):
            print('this error should never occur since move should always be valid at this point')
            return state, -1, done, {}

        # Calculate our new score. Calculate our reward too.
        new_score = self.game.clear_blocks_and_score(self.main_board)
        self.total_score += new_score
        reward = new_score

        # Pop out queue position
        self.block_queue.pop(queue_pos)

        # If we're out of blocks, regenerate our blocks
        if(len(self.block_queue) == 0):
            self.block_queue = self.factory.generate_3blocks()

        # Regenerate our state
        state = self.game.get_state(self.block_queue, self.main_board)

        # Calculate our game over state
        done = self.game.check_game_over_state(self.block_queue, self.main_board)

        # Return everything
        return state, reward, done, {}

    # Returns state
    def reset(self):

        # Generate first three blocks and game board
        self.main_board = self.game.new_board()
        self.block_queue = self.factory.generate_3blocks()

        # reset total score
        self.total_score = 0
        self.is_running = True

        return self.game.get_state(self.block_queue, self.main_board)

    # Returns self.view.render()?
    def render(self, mode='human'):
        if(mode == 'human'):
            print ('------------')
            print( 'Score: ' + str(self.total_score))
            print('Board')
            print ('------------')
            print(str(self.main_board))
            print('-------------')
            print('Block Queue: ')
            print('-------------')
            for n in range(len(self.block_queue)):
                print('Block ' + str(n) + ':')
                print(str(self.block_queue[n]))

    def close(self):
        pass



# Block Factory
class BlockFactory:

    def create_random_block(self):
        # List to hold our possible blocks
        block_list = []

        # 1 block
        block_list.append( [[1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])

        # 2 blocks
        block_list.append( [[1,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [0,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,1,0,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        
            
        # 3 blocks
        block_list.append( [[1,0,0,0,0],
                            [1,0,0,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,0,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,0,0,0],
                            [0,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,1,0,0,0],
                            [1,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [1,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [0,1,0,0,0],
                            [0,0,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,0,1,0,0],
                            [0,1,0,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        
        
        # 4 blocks
        block_list.append( [[1,0,0,0,0],
                            [1,0,0,0,0],
                            [1,0,0,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,1,1,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [1,0,0,0,0],
                            [1,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,0,1,0,0],
                            [1,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,0,0,0],
                            [0,1,0,0,0],
                            [0,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,1,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,0,0,0],
                            [0,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,1,0,0,0],
                            [1,1,0,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [1,1,0,0,0],
                            [0,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,1,1,0,0],
                            [1,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,0,0,0],
                            [1,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,1,0,0,0],
                            [1,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [1,1,0,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,1,0,0],
                            [0,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,1,0,0,0],
                            [1,1,0,0,0],
                            [0,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,1,0,0,0],
                            [0,1,0,0,0],
                            [1,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,1,0,0],
                            [0,0,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,0,0,0],
                            [1,0,0,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [1,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        
        # 5 blocks
        block_list.append( [[1,0,0,0,0],
                            [1,0,0,0,0],
                            [1,0,0,0,0],
                            [1,0,0,0,0],
                            [1,0,0,0,0]])
        block_list.append( [[1,1,1,1,1],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [1,0,0,0,0],
                            [1,0,0,0,0],
                            [1,1,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,0,0,1,0],
                            [1,1,1,1,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,0,0,0],
                            [0,1,0,0,0],
                            [0,1,0,0,0],
                            [0,1,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,1,1,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,1,0,0],
                            [1,0,0,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,1,0,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [1,0,0,0,0],
                            [1,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,0,1,0,0],
                            [0,0,1,0,0],
                            [1,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,1,0,0,0],
                            [0,1,0,0,0],
                            [0,1,0,0,0],
                            [1,1,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [1,1,1,1,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,0,0,0],
                            [1,0,0,0,0],
                            [1,0,0,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,1,1,0],
                            [0,0,0,1,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,0,0,0],
                            [0,1,0,0,0],
                            [0,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,0,1,0,0],
                            [1,1,1,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,1,1,0,0],
                            [0,1,0,0,0],
                            [1,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [1,1,1,0,0],
                            [0,0,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,1,0,0,0],
                            [1,1,1,0,0],
                            [0,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,1,0,0],
                            [0,1,0,0,0],
                            [0,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,0,0,0],
                            [1,1,1,0,0],
                            [1,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,1,0,0,0],
                            [0,1,0,0,0],
                            [1,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[0,0,1,0,0],
                            [1,1,1,0,0],
                            [0,0,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,1,0,0],
                            [1,0,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,0,0,0],
                            [1,0,0,0,0],
                            [1,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,0,1,0,0],
                            [1,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        block_list.append( [[1,1,0,0,0],
                            [0,1,0,0,0],
                            [1,1,0,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]])
        
        self.block_list = block_list      
        return np.matrix(random.choice(block_list))

    def generate_3blocks(self):
        return list([
            self.create_random_block(),
            self.create_random_block(),
            self.create_random_block()
        ])
    
# Game Class
class BlockSudokuGame:

    def new_board(self):
        # Even though our board is only 9x9, we leave some room for overflow for block checking
        # It makes the math much more elegant for checking if we can place a block on the board
        return np.matrix([
            [0,0,0,0,0,0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1]
        ])

    # Expensive operation to check all possible placements
    def get_all_valid_moves(self, block, board):
        valid_moves = (9,9)
        valid_moves = np.zeros(valid_moves)
        for x in range(9):
            for y in range(9):
                valid_moves[x][y] = self.check_if_valid_move(x, y, block, board)
        return valid_moves

    # Grab the current state
    def get_state(self, blocks, board):
        state = np.zeros((15,15))
        # Copy across board
        state[:9,:9] = board[:9,:9]
        for n in range(len(blocks)):
            x = n*5
            state[x:x+blocks[n].shape[0], 10:10+blocks[n].shape[1]] = blocks[n]
        return state

    # Check to see if we have a game over state
    def check_game_over_state(self, blocks, board):
        for n in range(len(blocks)):
            for x in range(9):
                for y in range(9):
                    if self.check_if_valid_move(x, y, blocks[n], board):
                        return False
        return True

    # This function mutates the board
    # Returns 
    def clear_blocks_and_score(self, board):

        # Score the rows first
        score = 0
        row_mask = np.floor(board[:9,:9].sum(axis=0)/9)
        score += row_mask.sum()
        row_array = np.repeat(row_mask, repeats=9, axis=0)

        # Score the columns next 
        column_mask = np.floor(board[:9,:9].sum(axis=1)/9)
        score += column_mask.sum()
        column_array = np.repeat(column_mask, repeats=9, axis=1)

        # Score the subblocks last
        sub_matrix_mask = [[0,0,0],[0,0,0],[0,0,0]]
        sub_matrix_array = np.matrix(np.zeros((9,9)))
        for i in range(3):
            for j in range(3):
                sub_matrix_mask[i][j] = np.floor(board[(i*3):(i*3)+3,(j*3):(j*3)+3].sum() / 9)
                if(sub_matrix_mask[i][j] == 1):
                    sub_matrix_array[(i*3):(i*3)+3,(j*3):(j*3)+3] = 1
        sub_matrix_mask = np.matrix(sub_matrix_mask)
        score += sub_matrix_mask.sum()

        # Add the arrays together to figure out how to clear the board
        combined_array = np.add(row_array, column_array)
        combined_array = np.add(combined_array, sub_matrix_array)
        combined_array = 1-np.clip(combined_array, 0, 1)

        # Finally commit to the new board
        board[:9, :9] = np.multiply(board[:9,:9], combined_array)

        return score*score

    # Checks if we can place a block on the board
    def check_if_valid_move(self, x, y, block, board):
        # Make sure it's not outside our bounds
        if(x < 0 or x >= 9):
            return False
        if(y < 0 or y >= 9):
            return False

        result_board = board.copy()
        result_board[x:x+block.shape[0], y:y+block.shape[1]] += block

        if(result_board.max() > 1):
            return False
        return True


    # Note this function mutates the board
    def place_block(self, x, y, block, board):
        if not self.check_if_valid_move(x, y, block, board):
            return False
            
        board[x:x+block.shape[0], y:y+block.shape[1]] += block
        return True

    
    # Recursive method for counting number of moves. Python sucks with recursion
    def iter_valid_overall_valid_moves(self, blocks, board):
        # Base case
        if(len(blocks) == 1):
            s_board = board.copy()
            svalid_moves = game.get_all_valid_moves(blocks[0], s_board)
            return svalid_moves.sum()

        # Recursion case
        sum_valid_moves = 0
        for i in range(9):
            for j in range(9):
                s_board = board.copy()
                if(game.place_block(i, j, blocks[0], s_board)):
                    cblocks = []
                    for i in range(len(blocks)):
                        cblocks.append(blocks[i].copy())
                    cblocks.pop(0)
                    sum_valid_moves += 1
                    sum_valid_moves += self.iter_valid_overall_valid_moves(cblocks, s_board)
        return sum_valid_moves

    # Lists number of overall valid moves. EXPENSIVE operation.
    def list_overall_valid_moves(self, block_queue, board):
        # Run through all different permutations of the blocks
        block_permutations = list(itertools.permutations(block_queue))
        overall_valid_moves = 0
        for n in range(len(block_permutations)):
            permutation_valid_moves =  self.iter_valid_overall_valid_moves(block_permutations[n], board)
            overall_valid_moves += permutation_valid_moves
            print('---------------------------')
            print('Combination ' + str(n) + ':')
            print('---------------------------')
            for u in range(len(block_permutations[n])):
                print('Block ' + str(u) + ':')
                print(block_permutations[n][u])
            print('Total possible moves: ' + str(permutation_valid_moves))

        print('Overall possible moves: ' + str(overall_valid_moves))
        
    # Crappy iterative way of running thru valid moves. Keeping it here for reference.
    # Do not recommend using
    def get_overall_valid_moves(self, block_queue, board):
        # Even though it looks general, this expects 3 blocks in the block queue.
        bqueue_combos = list(itertools.permutations(block_queue))
        overall_valid_moves = 0
        for n in range(len(bqueue_combos)):
            valid_moves = game.get_all_valid_moves(bqueue_combos[n][0], board)
            sum_valid_moves = valid_moves.sum()
            for i in range(9):
                for j in range(9):
                    s_board = board.copy()
                    if(game.place_block(i, j, bqueue_combos[n][0], s_board)):
                        svalid_moves = game.get_all_valid_moves(bqueue_combos[n][1], s_board)
                        tot_svalid_moves = svalid_moves.sum()
                        sum_valid_moves += tot_svalid_moves
                        for j in range(9):
                            for k in range(9):
                                ss_board = s_board.copy()
                                if(game.place_block(i, j, bqueue_combos[n][1], ss_board)):
                                    ssvalid_moves = game.get_all_valid_moves(bqueue_combos[n][1], s_board)
                                    tot_ssvalid_moves = ssvalid_moves.sum()
                                    sum_valid_moves += tot_ssvalid_moves
            overall_valid_moves += sum_valid_moves.sum()
            print('---------------------------')
            print('Combination ' + str(n) + ':')
            print('---------------------------')
            for u in range(len(bqueue_combos[n])):
                print('Block ' + str(u) + ':')
                print(bqueue_combos[n][u])
            print('Total possible moves: ' + str(sum_valid_moves.sum()))

        print('Overall possible moves: ' + str(overall_valid_moves))
        return overall_valid_moves
