import sys

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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        for variable, domain in self.domains.items():
            inconsistent = set()
            for element in domain:
                # Mark elements that dont fulfill unary constraints as inconsistent
                if len(element) != variable.length:
                    inconsistent.add(element)
            
            # Update variable domain set removing inconsistentcies
            self.domains[variable] = (domain.difference(inconsistent))  
            
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        index_x, index_y = self.crossword.overlaps[(x, y)]
        consistent = set()
        
        for element_x in self.domains[x]:
            for element_y in self.domains[y]:
                if element_x[index_x] == element_y[index_y]:
                    consistent.add(element_x)

        # Check if there are inconsistences. If any remove it and set revised True
        if self.domains[x] != consistent:
            self.domains[x] = self.domains[x].intersection(consistent)
            revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = list()
        
        if arcs is None:
            # Add to queue all valid arcs in the problem
            for x in self.domains:
                for y in self.domains:
                    # Filter all valid arcs before adding to queue
                    if x != y and self.crossword.overlaps[(x, y)] is not None:
                        # Append arc to the left by adding lists
                        queue = [(x, y)] + queue
        else:
            # Add to queue list of arcs
            for arc in arcs:
                # Append arc to the left by adding lists
                queue = [arc] + queue
    
        while queue:
            # Dequeue last arc from queue (first added)
            x, y = queue.pop()
            
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                # Enqueue all valid neghbor arcs
                for z in self.crossword.neighbors(x):
                    if z != y and self.crossword.overlaps[(x, z)] is not None:
                        queue = [(x, z)] + queue
        return True
              
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check if all variables have assignments
        for variable in self.crossword.variables:
            if variable not in assignment or assignment[variable] is None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for variable, value in assignment.items():
            # Check if value has correct lenght
            if variable.length != len(value):
                return False
            # Check if all values are distinct
            for distinct_variable, distinct_value in assignment.items():
                if variable != distinct_variable:
                    if value == distinct_value:
                        return False              
                    # Check for conflicts between neighboring variables (overlaps)
                    overlap = self.crossword.overlaps[variable, distinct_variable]                   
                    if overlap:
                        if value[overlap[0]] != distinct_value[overlap[1]]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Find and store neighbors of var
        neighbors = self.crossword.neighbors(var)
        domain_value_x_ruled_out = list()

        for var_value in self.domains[var]:
            # Keep track of how many values are ruled out from neighbor for each 
            ruled_out_count = 0      
            for neighbor in neighbors:
                # If neighbor already in assignment, disregard it
                if neighbor not in assignment:
                    # Get overslap indexes between var and neighbor
                    index_var, index_neighbor = self.crossword.overlaps[var,neighbor]    
                    
                    for neighbor_value in self.domains[neighbor]:
                        if var_value[index_var] != neighbor_value[index_neighbor]:
                            ruled_out_count += 1

            domain_value_x_ruled_out.append((var_value, ruled_out_count))
            ruled_out_count = 0
        
        domain_value_x_ruled_out.sort(key=lambda x: x[1])
        ordered_domain_values = [x[0] for x in domain_value_x_ruled_out]

        return ordered_domain_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """ 
        # List  variables
        preference_order = list()
        
        for variable in self.domains:
            # Heuristic (MRV) to keep track of smallest domain
            domain_size = len(self.domains[variable])
            
            # Heuristic (Degree) to keep track of most neighbors
            degree = len(self.crossword.neighbors(variable))

            if variable not in assignment:
                preference_order.append({"variable": variable, "domain_size": domain_size, "degree": degree})
                
        # Sort preference by "domain_size" followed by inverted "degree"
        preference_order.sort(key=lambda x: (x["domain_size"], -x["degree"]))
        
        # Select first variable from list (preferred taking heuristic into account)
        selected_variable = preference_order[0]["variable"]
    
        return selected_variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment
        
        # Select unassigned variable to test-assign
        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
        #for value in self.domains[variable]:
            assignment[variable] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                # result is not failure, return result
                if result:
                    return result
                # result is a failure, remove variable/value from assignment                           
                assignment.pop(variable)
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
