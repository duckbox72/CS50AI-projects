import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Remove mine from sentence and update it's count
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base
        #    based on the value of `cell` and `count` 
        self.add_sentence(cell, count)
    
        # 4) mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base
        self.mark_known_cells()

        # 5) add any new sentences to the AI's knowledge base
        #    if they can be inferred from existing knowledge        
        new_sentences = self.update_knowledge()

        # Recursively add new inferred sentences to knowledge base 
        # until no more inferences can be made    
        while new_sentences:     
            for sentence in new_sentences:
                self.knowledge.append(sentence)
                self.mark_known_cells()
            
            new_sentences = self.update_knowledge()
    
    def add_sentence(self, cell, count):
        """
        Adds a sentence to knowledge base, based on a given move (cell, count).
        """
        i, j = cell
        neighbors = set()
        cells = set()

        # Generic case finds add all 8 neighbors
        for n in range(-1, 2):
            for m in range(-1, 2):
                # Filter out corner cases (self cell and out of bounds) and add remaining to neighbors:
                if (i + n, j + m) != cell and i + n >= 0 and j + m >= 0 and i + n < self.height and j + m < self.width: 
                    neighbors.add((i + n, j + m))

        # Filter out neighbors whose state is already determined 
        for neighbor in neighbors:
            # When neighbor is known to be a mine, count minus 1 as the cell won't be added to cells set
            if neighbor in self.mines:
                count -= 1 
            if neighbor not in self.safes and neighbor not in self.mines:
                cells.add(neighbor)

        # Create a Sentence instance and add to knowledge base
        sentence = Sentence(cells, count)
        if sentence not in self.knowledge:
            self.knowledge.append(sentence)

    def mark_known_cells(self):
        """
        Finds and mark current known safes and mines 
        cells based on knowledge base.
        """

        known_safe_cells = set()
        known_mine_cells = set()

        for sentence in self.knowledge:
            if sentence.known_safes() != set():
                for cell in sentence.known_safes():
                    known_safe_cells.add(cell)

            if sentence.known_mines() != set():
                for cell in sentence.known_mines():
                    known_mine_cells.add(cell)      
        
        for cell in known_safe_cells:
            self.mark_safe(cell)

        for cell in known_mine_cells:
            self.mark_mine(cell)

    def update_knowledge(self):
        """
        Returns a set of new inferred sentences for a given knowledge base 
        """
        new_sentences = []

        # Remove empty sentences
        for sentence in self.knowledge:
            if sentence.cells == set():
                self.knowledge.remove(sentence)

        # Add new inferred sentences new_sentences list
        for sentenceX in self.knowledge:
            for sentenceY in self.knowledge:
                if sentenceX != sentenceY:
                    if sentenceY.cells.issubset(sentenceX.cells):
                        new_cells = sentenceX.cells - sentenceY.cells
                        new_count = sentenceX.count - sentenceY.count
                        new_sentence = Sentence(new_cells, new_count)
                        if new_sentence not in self.knowledge:
                            new_sentences.append(new_sentence)

        return new_sentences
                    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made and move not in self.mines:
                return move

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        # Find and list all available moves
        available_moves = []
        
        for i in range(self.height):
            for j in range(self.width):
                move = (i, j)
                if move not in self.moves_made and move not in self.mines:
                    available_moves.append(move)

        # Return a random move if at least one move is available or None otherwise
        if available_moves:
            rand_index = random.randint(0, len(available_moves) - 1)
            return available_moves[rand_index]
        
        return None
