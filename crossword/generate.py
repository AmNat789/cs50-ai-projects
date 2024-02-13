import copy
import math
import sys
import queue
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        domain_copy = copy.deepcopy(self.domains)
        for variable in self.crossword.variables:
            for word in self.crossword.words:
                if variable.length != len(word):
                    domain_copy[variable].remove(word)

        self.domains = domain_copy

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        domain_copy = copy.deepcopy(self.domains)

        revised = False
        overlap = self.crossword.overlaps[x, y]
        for x_word in self.domains[x]:
            x_word_satisfies_constraint = False
            for y_word in self.domains[y]:
                if x_word[overlap[0]] == y_word[overlap[1]]:
                    x_word_satisfies_constraint = True
                    break
            if not x_word_satisfies_constraint:
                domain_copy[x].remove(x_word)
                revised = True
        self.domains = domain_copy
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        q = queue.Queue()

        # if arcs is not None, add them to the queue
        if arcs is not None:
            list(map(q.put, arcs))
        # if no arcs are provided, add all overlaps as arcs
        else:
            for variable in self.crossword.variables:
                neighbors = self.crossword.neighbors(variable)
                for neighbor in neighbors:
                    q.put((variable, neighbor))

        while not q.empty():
            (X, Y) = q.get()
            if self.revise(X, Y):
                if len(self.domains[X]) == 0:
                    return False
                for Z in self.crossword.neighbors(X):
                    if not Z == Y:
                        q.put((Z, X))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            if variable not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # check if all values in assignment are unique
        unique_words = {}
        for variable in assignment:
            unique_words[assignment[variable]] = True
        if len(unique_words) != len(assignment):
            return False

        # check if all words are the right length
        for variable in assignment:
            if len(assignment[variable]) != variable.length:
                return False

        # check for conflicts with neighbor
        for variable in assignment:
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[variable, neighbor]
                    if assignment[variable][overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = []
        neighbors = self.crossword.neighbors(var)

        for value in self.domains[var]:
            eliminations = 0
            for neighbor in neighbors:
                if neighbor in assignment:
                    continue

                overlap = self.crossword.overlaps[var, neighbor]
                for neighbor_value in self.domains[neighbor]:
                    if value[overlap[0]] != neighbor_value[overlap[1]]:
                        eliminations += 1
            values.append((eliminations, value))

        sorted_values = sorted(values, key=lambda x: x[0])
        return [v[1] for v in sorted_values]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        mrv_heuristic_values = []
        min_domain_size = math.inf
        for var in self.crossword.variables:
            if var not in assignment:
                domain_size = len(self.domains[var])
                if domain_size < min_domain_size:
                    min_domain_size = domain_size
                    mrv_heuristic_values = [var]
                elif domain_size == min_domain_size:
                    mrv_heuristic_values.append(var)


        if len(mrv_heuristic_values) == 1:
            return mrv_heuristic_values[0]

        max_degrees = 0
        degree_heuristic_value = None
        for var in mrv_heuristic_values:
            degrees = len(self.crossword.neighbors(var))
            if degrees > max_degrees:
                max_degrees = degrees
                degree_heuristic_value = var

        return degree_heuristic_value


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            new_assignment = copy.deepcopy(assignment)
            new_assignment[variable] = value
            if self.consistent(new_assignment):
                assignment[variable] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                else:
                    del assignment[variable]
        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
