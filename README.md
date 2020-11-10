
# Overview

The BlockSudoku environment is for use with [OpenAI Gym](https://github.com/openai/gym). Yoiu can find more details about the implementation from [this webpage](https://drakeor.com/2020/11/01/block-sudoku/).

Block Sudoku is a game arranged like a traditional Sudoku board, and each "round", you place 3 tetris-like blocks on the board. They can be anywhere on the board as long as they don't collide with an existing piece on the board. An example is below:

![Sample Board Arrangement](https://drakeor.com/content/images/2020/10/BlockSudokuBoard.PNG)


But unlike Tetris, you cannot rotate the blocks. You gain points by clearing the blocks off the board. You can clear blocks either filling up a row, column, or one of the 3x3 squares. All of the following arrangements below are valid for clearing a line or block of blocks.

![Valid Clears](https://drakeor.com/content/images/2020/10/validclears.PNG)


The game ends when you cannot place all three of the blocks you were given that round such as being left with the T-block on the board below :

![invalid move example](https://drakeor.com/content/images/2020/11/invalidmove_fixed.png)


# States / Actions
Coming soon!

# Installation
### Installing from PyPI
	pip install gym-blocksudoku
	
### Installing from Source

	git clone https://github.com/drakeor/gym-blocksudoku
	cd gym-blocksudoku
	pip install -e .

