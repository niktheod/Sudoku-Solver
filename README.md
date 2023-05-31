# Sudoku-Solver
A python program that solves sudoku matrices

This script implements an algorithm to solve a Sudoku puzzle. It takes a user-input Sudoku matrix, finds the empty squares, and determines the possible solutions for each empty square. It then applies a series of steps to fill in the squares until the entire Sudoku matrix is solved.

## How to Use
1. Make sure you have Python installed on your system.
2. Run the script using the command: python sudoku_solver.py
3. Enter the Sudoku matrix when prompted, row-wise, with empty cells represented as "-". The matrix should be entered as a single line of values separated by commas. For example: 2,-,-,-,-,1,-,-,-,-,3,-,-,9,4,-,6,-,-,-,5,-,-,-,3,-,-,-,9,-,1,-,-,-,-,-,-,-,-,5,-,-,-,2,-,-,-,7,-,2,9,-,-,4,-,5,-,-,6,3,-,4,-,8,-,-,-,-,-,-,-,7,-,-,-,2,-,-,-,-,-
4. The solved Sudoku matrix will be printed to the console.

Please note that the code assumes that the Sudoku puzzle has a unique valid solution and does not handle puzzles with multiple solutions. It also assumes that the input matrix is valid and follows the rules of Sudoku. Additionally, it can solve only the classical 9x9 Sudoku matrices and not other variations.

## Algorithm Overview
The main steps of the algorithm implemented in this script are as follows:

1. If there is a square with only one possible solution, fill it in.
2. If not, check if any square has a unique possible solution that no other square in its row, column, or box has, and if so, fill it in.
3. If the above steps don't yield a solution, check if any box has a solution that can only fit in a single row or column. Remove this solution from the possible solutions of other squares in the same row or column outside of that box.
4. If none of the previous steps provide a solution, create copies of the current matrix with only one square updated. Make one copy for each possible solution of the updated square. Then restart the algorithm for each copy until the correct solution is found.
