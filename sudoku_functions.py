"""Sudoku Solver Functions

This module provides functions to solve Sudoku puzzles using a backtracking algorithm.

Functions:
- print_matrix(matrix):
  Prints the Sudoku matrix.

- find_box(square):
  Finds the box (3x3 subgrid) that contains a given square.

- find_empty_squares(matrix):
  Finds the empty squares in the Sudoku matrix.

- find_possible_solutions(matrix, empty_squares):
  Finds the possible solutions for each empty square in the Sudoku matrix.

- compare_solutions(possible_solutions, square):
  Compares the possible solutions for a square with the solutions of other squares and returns a unique solution if one
  exists.

- check_boxes(possible_solutions):
  Checks each box in the Sudoku matrix to find any solutions uniquely determined by a row or a column.

- update_possible_solutions(possible_solutions, row_results, col_results):
  Updates the possible solutions for each square based on the solutions uniquely determined by rows and columns.

- check_paradox(possible_solutions):
  Checks if there are any squares with no possible solutions.

- check_possible_scenarios(matrix, possible_solutions):
  Checks the possible scenarios for filling in the Sudoku matrix and recursively solves the puzzle.

"""

from collections import defaultdict
from copy import deepcopy
from typing import List, Tuple, Dict, Union


def print_matrix(matrix: List[List[str]]) -> None:
    """
    Prints the given Sudoku matrix in a human-readable format.

    Args:
        matrix: A 9x9 Sudoku matrix represented as a list of lists of strings.

    Returns:
        None
    """

    for row in matrix:
        print(row)
    print("")


def find_box(square: Tuple[int, int]) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    """
    Finds the box (3x3 subgrid) that contains the given square.

    Args:
        square: A tuple representing the (row, column) indices of a square in the Sudoku matrix.

    Returns:
        A tuple containing two tuples. The first tuple represents the rows in the box, and the second tuple
        represents the columns in the box.
    """

    i, j = square

    if 0 <= i <= 2:
        rows = (0, 1, 2)
    elif 3 <= i <= 5:
        rows = (3, 4, 5)
    else:
        rows = (6, 7, 8)

    if 0 <= j <= 2:
        cols = (0, 1, 2)
    elif 3 <= j <= 5:
        cols = (3, 4, 5)
    else:
        cols = (6, 7, 8)

    return rows, cols


def find_empty_squares(matrix: List[List[str]]) -> List[Tuple[int, int]]:
    """
    Finds the empty squares in the Sudoku matrix.

    Args:
        matrix: A 9x9 Sudoku matrix represented as a list of lists of strings.

    Returns:
        A list of tuples representing the (row, column) indices of the empty squares in the Sudoku matrix.
    """

    empty_squares = []

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if not matrix[i][j].isdigit():
                empty_squares.append((i, j))

    return empty_squares


def find_possible_solutions(matrix: List[List[str]],
                            empty_squares: List[Tuple[int, int]]) -> Dict[Tuple[int, int], List[str]]:
    """
    Finds the possible solutions for each empty square in the Sudoku matrix.

    Args:
        matrix: A 9x9 Sudoku matrix represented as a list of lists of strings.
        empty_squares: A list of tuples representing the (row, column) indices of the empty squares.

    Returns:
        A dictionary where the keys are the empty squares and the values are lists of possible solutions for each
        square.
    """

    possible_solutions = {}
    for empty_square in empty_squares:
        possible_solutions[empty_square] = [str(x) for x in range(1, 10)]

    for empty_square in empty_squares:
        i, j = empty_square

        for element in matrix[i]:
            if element in possible_solutions[empty_square]:
                possible_solutions[empty_square].remove(element)

        for row in matrix:
            if row[j] in possible_solutions[empty_square]:
                possible_solutions[empty_square].remove(row[j])

        rows, cols = find_box(empty_square)

        for x in rows:
            for y in cols:
                if matrix[x][y] in possible_solutions[empty_square]:
                    possible_solutions[empty_square].remove(matrix[x][y])

    return possible_solutions


def compare_solutions(possible_solutions: Dict[Tuple[int, int], List[str]],
                      square: Tuple[int, int]) -> Union[str, None]:
    """
    Compares the possible solutions for a given square with the solutions of other squares in the same row, column,
    and box, and returns a unique solution if one exists.

    Args:
        possible_solutions: A dictionary containing the possible solutions for each square in the Sudoku matrix.
        square: A tuple representing the (row, column) indices of a square in the Sudoku matrix.

    Returns:
        If a unique solution exists for the given square, it returns the solution as a string. Otherwise, it returns
        None.
    """

    i, j = square

    solutions = possible_solutions[square]

    # Check solutions in the same row
    for solution in solutions:
        for other_square, other_solutions in possible_solutions.items():
            # Skip the current square and squares that are in different rows
            if other_square != square and other_square[0] == i:
                if solution in other_solutions:
                    break
        else:
            return solution

    # Check solutions in the same column
    for solution in solutions:
        for other_square, other_solutions in possible_solutions.items():
            # Skip the current square and squares that are in different columns
            if other_square != square and other_square[1] == j:
                if solution in other_solutions:
                    break
        else:
            return solution

    # Check solutions in the same box
    rows, cols = find_box(square)

    for solution in solutions:
        solution_exists = True
        for x in rows:
            for y in cols:
                # Skip the current square and squares that are not empty
                if (x, y) != square and (x, y) in possible_solutions:
                    if solution in possible_solutions[(x, y)]:
                        solution_exists = False

        if solution_exists:
            return solution


def check_boxes(possible_solutions: Dict[Tuple[int, int], List[str]]) \
        -> Tuple[List[Tuple[str, int, List[Tuple[int, int, int]]]], List[Tuple[str, int, List[Tuple[int, int, int]]]]]:
    """
    Checks each box in the Sudoku matrix to find any solutions that are uniquely determined by a row or a column.

    Args:
        possible_solutions: A dictionary containing the possible solutions for each square in the Sudoku matrix.

    Returns:
        A tuple of two lists. The first list contains tuples representing the solutions uniquely determined by a row,
        and the second list contains tuples representing the solutions uniquely determined by a column. Each tuple
        contains the solution as a string, the row or column index, and the indices of the squares in the box.
    """

    boxes = [[(0, 1, 2), (0, 1, 2)], [(0, 1, 2), (3, 4, 5)], [(0, 1, 2), (6, 7, 8)], [(3, 4, 5), (0, 1, 2)],
             [(3, 4, 5), (3, 4, 5)], [(3, 4, 5), (6, 7, 8)], [(6, 7, 8), (0, 1, 2)], [(6, 7, 8), (3, 4, 5)],
             [(6, 7, 8), (6, 7, 8)]]

    row_results = []  # Stores solutions uniquely determined by a row
    col_results = []  # Stores solutions uniquely determined by a column

    for box in boxes:
        rows_dict = defaultdict(list)  # Stores the row indices for each solution
        cols_dict = defaultdict(list)  # Stores the column indices for each solution

        # Iterate through each square in the current box
        for x in box[0]:
            for y in box[1]:
                if (x, y) in possible_solutions:
                    for solution in possible_solutions[(x, y)]:
                        rows_dict[solution].append(x)  # Add row index for the solution in the row_dict
                        cols_dict[solution].append(y)  # Add column index for the solution in the cols_dict

        # Check for solutions uniquely determined by a row
        for solution, rows in rows_dict.items():
            if all((z == rows[0] for z in rows[1:])):
                row_results.append((solution, rows[0], box))

        # Check for solutions uniquely determined by a column
        for solution, cols in cols_dict.items():
            if all((z == cols[0] for z in cols[1:])):
                col_results.append((solution, cols[0], box))

    return row_results, col_results


def update_possible_solutions(possible_solutions: Dict[Tuple[int, int], List[str]],
                              row_results: List[Tuple[str, int, List[Tuple[int, int, int]]]],
                              col_results: List[Tuple[str, int, List[Tuple[int, int, int]]]]) \
        -> Dict[Tuple[int, int], List[str]]:
    """
    Updates the possible solutions for each square in the Sudoku matrix based on the solutions uniquely determined
    by rows and columns.

    Args:
        possible_solutions: A dictionary containing the possible solutions for each square in the Sudoku matrix.
        row_results: A list of tuples representing the solutions uniquely determined by a row. Each tuple contains
            the solution as a string, the row index, and the indices of the squares in the box.
        col_results: A list of tuples representing the solutions uniquely determined by a column. Each tuple contains
            the solution as a string, the column index, and the indices of the squares in the box.

    Returns:
        The updated dictionary of possible solutions.
    """

    possible_solutions = deepcopy(possible_solutions)

    # Update possible solutions based on row results
    for result in row_results:
        solution, row, box = result
        for j in range(9):
            # Skip if (row, j) is in the box of the row results or if it is not empty
            if j in box[1] or (row, j) not in possible_solutions:
                continue
            elif solution in possible_solutions[(row, j)]:
                possible_solutions[(row, j)].remove(solution)

    # Update possible solutions based on column results
    for result in col_results:
        solution, col, box = result
        for i in range(9):
            # Skip if (row, j) is in the box of the column results or if it is not empty
            if i in box[0] or (i, col) not in possible_solutions:
                continue
            elif solution in possible_solutions[(i, col)]:
                possible_solutions[(i, col)].remove(solution)

    return possible_solutions


def check_paradox(possible_solutions: Dict[Tuple[int, int], List[str]]) -> bool:
    """
    Checks if there are any squares in the Sudoku matrix with no possible solutions.

    Args:
        possible_solutions: A dictionary containing the possible solutions for each square in the Sudoku matrix.

    Returns:
        True if there is at least one square with no possible solutions, False otherwise.
    """

    for square, solutions in possible_solutions.items():
        if not solutions:
            return True
    return False


def check_possible_scenarios(matrix: List[List[str]],
                             possible_solutions: Dict[Tuple[int, int], List[str]]) -> Union[List[List[str]], None]:
    """
    Creates copies of the matrix with only one square updated. It makes one copy for each possible solution of the
    updated square. Then it restarts the main algorithm for each copy until the correct solution is found.

    Args:
        matrix: The Sudoku matrix represented as a 9x9 list of strings.
        possible_solutions: A dictionary containing the possible solutions for each square in the Sudoku matrix.

    Returns:
        If a solution is found, it returns the completed Sudoku matrix as a list of lists. If no solution is found,
        it returns None.
    """

    # Determine what is the minimum number of possible solutions for a square in the sudoku matrix
    min_solutions = len(min(possible_solutions.values(), key=len))
    # Create a list with as many matrix copies as the minimum solutions
    matrix_copies = [deepcopy(matrix) for _ in range(min_solutions)]

    # Create all the possible versions of the matrix by setting the value of a square, with the minimum number of
    # possible values, to all the possible values, one for each copy. So for sure one of these copies will be the right
    # one
    for square, solutions in possible_solutions.items():
        if len(solutions) == min_solutions:
            i, j = square
            for n in range(min_solutions):
                matrix_copies[n][i][j] = solutions[n]
            break

    # Iterate through each matrix copy
    for matrix_copy in matrix_copies:
        empty_squares_copy = find_empty_squares(matrix_copy)
        possible_solutions_copy = find_possible_solutions(matrix_copy, empty_squares_copy)
        finished = True  # If finished is True after the "while" loop beneath is complete, that means that the
        # check_possible_scenarios function has solved the Sudoku matrix, and it can return it
        if check_paradox(possible_solutions_copy):
            continue

        while empty_squares_copy:
            min_solutions = len(min(possible_solutions_copy.values(), key=len))

            # 1. If there is a square with only one possible solution, fill it in.
            if min_solutions == 1:
                for square, solutions in possible_solutions_copy.items():
                    if len(solutions) == 1:
                        i, j = square
                        matrix_copy[i][j] = solutions[0]
                        empty_squares_copy.remove(square)
                        possible_solutions_copy = find_possible_solutions(matrix_copy, empty_squares_copy)
                        break
            # 2. If not, check if any square has a unique possible solution that no other square in its row, column, or
            # box has, and if so, fill it in.
            else:
                for length in range(2, 10):
                    break_both = False
                    for square, solutions in possible_solutions_copy.items():
                        if len(solutions) == length:
                            i, j = square
                            solution = compare_solutions(possible_solutions_copy, square)
                            if solution is not None:
                                matrix_copy[i][j] = solution
                                empty_squares_copy.remove(square)
                                possible_solutions_copy = find_possible_solutions(matrix_copy, empty_squares_copy)
                                break_both = True
                                break
                    if break_both:
                        break
                # 3. If the above steps don't yield a solution, check if any box has a solution that can only fit in a
                # single row or column. Remove this solution from the possible solutions of other squares in the same
                # row or column outside of that box.
                else:
                    row_results, col_results = check_boxes(possible_solutions_copy)

                    old_possible_solutions = deepcopy(possible_solutions_copy)
                    possible_solutions_copy = update_possible_solutions(possible_solutions_copy, row_results,
                                                                        col_results)
                    # 4. If none of the previous steps provide a solution, create copies of the current matrix with only
                    # one square updated. Make one copy for each possible solution of the updated square. Then restart
                    # the algorithm for each copy until the correct solution is found.
                    if old_possible_solutions == possible_solutions_copy:
                        matrix_copy = check_possible_scenarios(matrix_copy, possible_solutions_copy)
                        # If the recursive call of the function didn't succeed, that means that all the possible
                        # scenarios of the current matrix copy led to a paradox which means that this copy isn't the
                        # right one and the function shouldn't return it and instead move to the next matrix copy. So
                        # set finished = False
                        if matrix_copy is None:
                            finished = False
                            break
                        else:
                            return matrix_copy

        if finished:
            return matrix_copy
