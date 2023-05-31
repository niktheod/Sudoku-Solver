""" Sudoku Solver

This script implements an algorithm to solve a Sudoku puzzle. It takes a user-input Sudoku matrix, finds the empty
squares, and determines the possible solutions for each empty square. It then applies a series of steps to fill in the
squares until the entire Sudoku matrix is solved.

The main steps of the algorithm are as follows:
1. If there is a square with only one possible solution, fill it in.
2. If not, check if any square has a unique possible solution that no other square in its row, column, or box has,
   and if so, fill it in.
3. If the above steps don't yield a solution, check if any box has a solution that can only fit in a single row or
   column. Remove this solution from the possible solutions of other squares in the same row or column outside of
   that box.
4. If none of the previous steps provide a solution, create copies of the current matrix with only one square
   updated. Make one copy for each possible solution of the updated square. Then restart the algorithm for each copy
   until the correct solution is found.

The solved Sudoku matrix is printed to the console.

Usage: python sudoku_solver.py

Note: The code assumes that the Sudoku puzzle has a unique valid solution and does not handle puzzles with multiple
solutions. It also assumes that the input matrix is valid and follows the rules of Sudoku. Finally, it can solve only
the classical 9x9 sudoku matrices and not other variations.

"""

from sudoku_functions import print_matrix, find_empty_squares, find_possible_solutions, compare_solutions, check_boxes,\
    update_possible_solutions, check_possible_scenarios
from copy import deepcopy


def main():
    """
    This function is the entry point of the Sudoku Solver. It prompts the user to enter a Sudoku matrix, solves the
    puzzle, and prints the solution.

    Usage:
        The function prompts the user to enter the Sudoku matrix, row-wise, with empty cells represented as "-".
        The matrix should be entered as a single line of values separated by commas.
        For example: 4,-,3,-,2,-,9,5,-,-,-,6,-,-,-,-,-,-,-,-,-,1,-,-,-,2,-,-,6,-,-,4,-,-,-,-,-,1,-,-,-,-,5,-,-,5,-,4,8,
        -,-,-,-,3,-,5,-,-,-,-,-,-,-,-,-,-,-,-,7,-,-,8,9,-,2,-,1,-,3,-,-

    Returns:
        None

    """

    # Get the Sudoku matrix and transfer it into a 2D list
    users_input = input("Enter the matrix: ").strip()
    raw_matrix = users_input.split(",")
    matrix = [[raw_matrix[i] for i in range(n, n + 9)] for n in range(0, 81, 9)]

    # Find the empty squares of the matrix and all the possible solutions for each one of them
    empty_squares = find_empty_squares(matrix)
    possible_solutions = find_possible_solutions(matrix, empty_squares)

    # Loop through the 4 main steps of the algorithm until you get the solved Sudoku matrix
    while empty_squares:
        min_solutions = len(min(possible_solutions.values(), key=len))

        # 1. If there is a square with only one possible solution, fill it in.
        if min_solutions == 1:
            for square, solutions in possible_solutions.items():
                if len(solutions) == 1:
                    i, j = square
                    matrix[i][j] = solutions[0]
                    empty_squares.remove(square)
                    possible_solutions = find_possible_solutions(matrix, empty_squares)
                    break
        # 2. If not, check if any square has a unique possible solution that no other square in its row, column, or box
        # has, and if so, fill it in.
        else:
            for length in range(2, 10):
                break_both = False
                for square, solutions in possible_solutions.items():
                    if len(solutions) == length:
                        i, j = square
                        solution = compare_solutions(possible_solutions, square)
                        if solution is not None:
                            matrix[i][j] = solution
                            empty_squares.remove(square)
                            possible_solutions = find_possible_solutions(matrix, empty_squares)
                            break_both = True
                            break
                if break_both:
                    break
            # 3. If the above steps don't yield a solution, check if any box has a solution that can only fit in a
            # single row or column. Remove this solution from the possible solutions of other squares in the same row
            # or column outside of that box.
            else:
                row_results, col_results = check_boxes(possible_solutions)
                old_possible_solutions = deepcopy(possible_solutions)
                possible_solutions = update_possible_solutions(possible_solutions, row_results, col_results)

                # 4. If none of the previous steps provide a solution, create copies of the current matrix with only
                # one square updated. Make one copy for each possible solution of the updated square. Then restart the
                # algorithm for each copy until the correct solution is found.
                if old_possible_solutions == possible_solutions:
                    matrix = check_possible_scenarios(matrix, possible_solutions)
                    break

    if matrix is not None:
        print_matrix(matrix)
    else:
        print("There is not a valid solution for this Sudoku matrix")


if __name__ == "__main__":
    main()
