import random
import re
import time
import argparse
from typing import List, Optional


class Wordsearch:
    def __init__(
        self,
        cols: int,
        rows: int,
        empty_char: str = "-",
        max_loops: int = 2000,
        available_words: List[str] = [],
    ):
        self.cols = cols
        self.rows = rows
        self.empty_char = empty_char
        self.max_loops = max_loops
        self.available_words = available_words
        self.sort_word_list()
        self.current_word_list = []
        self.create_grid()

    def create_grid(self) -> List[List[str]]:
        """
        Populates grid with given dimensions and blank space character,
         stores in self.grid
        Returns
            self.grid (List[List[str]]) - Grid with the empty string character as elements
        """
        self.grid = []
        for row in range(self.rows):
            current_row = []
            for col in range(self.cols):
                current_row.append(self.empty_char)
            self.grid.append(current_row)
        return self.grid

    def sort_word_list(self) -> List[str]:
        """
        Shuffles word list and sorts longest to shortest,
        creates Word object from given words
        Returns
            processed_list (List[str]) - Sorted list of Word objects that make up the wordsearch
        """
        processed_list = []
        for word in self.available_words:
            if isinstance(word, Word):
                processed_list.append(
                    Word(word.word)
                )
            else:
                processed_list.append(
                    Word(word)
                )
        random.shuffle(processed_list)
        processed_list.sort(key=lambda word: len(word.word), reverse=True)
        self.available_words = processed_list

        return processed_list

    def compute_wordsearch(self, time_permitted: float = 1.00, spins: int = 2) -> None:
        """
        Takes maximum time, fits different wordsearchs, setting as self.grid and self.current_word_list if better than all the previous ones
        Args:
            time_permitted (float) - time allowed to try different wordsearch placements
            spins (int) - number of attempts in each iteration
        """
        time_permitted = float(time_permitted)

        count = 0
        xword_copy = Wordsearch(
            self.cols,
            self.rows,
            self.empty_char,
            self.max_loops,
            self.available_words,
        )

        start_time = float(time.time())
        # while time not elapsed
        while (float(time.time()) - start_time) < time_permitted or count == 0:
            xword_copy.current_word_list = []
            xword_copy.create_grid()
            xword_copy.sort_word_list()
            x = 0
            # while not gone over number of attempts
            while x < spins:
                for word in xword_copy.available_words:
                    if word not in xword_copy.current_word_list:
                        xword_copy.fit_and_add(word)
                x += 1
            # if current wordsearch better than saved, set current as saved
            if len(xword_copy.current_word_list) > len(self.current_word_list):
                self.current_word_list = xword_copy.current_word_list
                self.grid = xword_copy.grid
            count += 1
        self.space_around_edges()

    def suggest_coords(self, word) -> List[List[int]]:
        """
        Takes a word and returns a list of possible coords
        Args:
            word (Word) - word object representing word to place
        Returns:
            new_coord_list (List[List[int]]) - list of lists where each sublist a series of ints representing the coord
        """
        coord_list = []
        letter_count = -1
        # go through each letter
        for current_letter in word.word:
            letter_count += 1
            row_count = 0
            # go through each row
            for row in self.grid:
                row_count += 1
                col_count = 0
                # go through each row
                for cell in row:
                    col_count += 1
                    # check current letter matches letter in cell
                    if current_letter == cell:
                        # try to place vertically
                        try:
                            # make sure starting on grid
                            if row_count - letter_count > 0:
                                # make sure ending on grid
                                if (
                                    (row_count - letter_count) + word.length
                                ) <= self.rows:
                                    coord_list.append(
                                        [
                                            col_count,
                                            row_count - letter_count,
                                            1,
                                            col_count + (row_count - letter_count),
                                            0,
                                        ]
                                    )
                        except Exception:
                            pass
                        # try to place horizontally
                        try:
                            # make sure starting on grid
                            if col_count - letter_count > 0:
                                # make sure ending on grid
                                if (
                                    (col_count - letter_count) + word.length
                                ) <= self.cols:
                                    coord_list.append(
                                        [
                                            col_count - letter_count,
                                            row_count,
                                            0,
                                            row_count + (col_count - letter_count),
                                            0,
                                        ]
                                    )
                        except Exception:
                            pass
        new_coord_list = self.sort_coord_list(coord_list, word)
        return new_coord_list

    def sort_coord_list(self, coord_list, word) -> List[List[int]]:
        """
        Takes a list of coordinates and a word, returns list of coordinates based on ranking coordinates by check_fit_score method
        Args:
            coord_list (List[List[int]]) - List of lists of ints representing location information (each sublist is [col, row, vertical, fit score])
            word (Word) - Object representing the word trying to place
        Returns:
            new_coord_list (List[List[int]]) - Sorted and filtered coords based on most viable first
        """
        new_coord_list = []
        for coord in coord_list:
            col, row, vertical = coord[0], coord[1], coord[2]
            coord[4] = self.check_fit_score(col, row, vertical, word)
            # removing if fit score is 0 meaning no fit
            if coord[4]:
                new_coord_list.append(coord)

        # sort to order best scores first
        new_coord_list.sort(key=lambda i: i[4], reverse=True)
        return new_coord_list

    def fit_and_add(self, word) -> None:
        """
        Takes a word and adds to grid based on fit score method
        Args:
            word (Word) - Word object to try and place
        """
        fit = False
        count = 0
        coord_list = self.suggest_coords(word)

        while not fit and count < self.max_loops:

            if len(self.current_word_list) == 0:
                # this is the first word: the seed
                # top left seed of longest word yields best results
                vertical, col, row = random.randrange(0, 2), 1, 1

                if self.check_fit_score(col, row, vertical, word):
                    fit = True
                    self.set_word(col, row, vertical, word)
            else:
                # subsquent words have scores calculated
                try:
                    col, row, vertical = (
                        coord_list[count][0],
                        coord_list[count][1],
                        coord_list[count][2],
                    )
                # no more cordinates, stop trying to fit
                except IndexError:
                    return

                if coord_list[count][4]:
                    fit = True
                    self.set_word(col, row, vertical, word)
            count += 1

    def check_fit_score(self, col: int, row: int, vertical: bool, word) -> int:
        """
        Takes direction and position information plus a word, returns a score to indicate if it can be placed and how many crosses
        Args:
            col (int) - Potential column for the word
            row (int) - Potential row for the word
            vertical (bool) - Whether the word is trying to be placed vertically
            word (Word) - Word object to try to fit
        Returns:
            score (int) - 0 for no fit, 1 for a fit, 2+ for a cross
        """
        if col < 1 or row < 1:
            return 0
        # default score of 1 will change if needed
        count, score = 1, 1
        for letter in word.word:
            try:
                active_cell = self.get_cell(col, row)
            except IndexError:
                return 0

            if active_cell == self.empty_char or active_cell == letter:
                pass
            else:
                return 0

            if active_cell == letter:
                score += 1

            if vertical:
                # check surroundings
                # don't check surroundings if cross point
                if active_cell != letter:
                    # check right cell
                    if not self.check_if_cell_clear(col + 1, row):
                        return 0
                    # check left cell
                    if not self.check_if_cell_clear(col - 1, row):
                        return 0
                # check top cell only on first letter
                if count == 1:
                    if not self.check_if_cell_clear(col, row - 1):
                        return 0
                # check bottom cell only on last letter
                if count == len(word.word):
                    if not self.check_if_cell_clear(col, row + 1):
                        return 0
            else:
                # check surroundings, horizontal
                # don't check surroundings if cross point
                if active_cell != letter:
                    # check top cell
                    if not self.check_if_cell_clear(col, row - 1):
                        return 0
                    # check bottom cell
                    if not self.check_if_cell_clear(col, row + 1):
                        return 0
                # if first letter only check cell to left
                if count == 1:
                    if not self.check_if_cell_clear(col - 1, row):
                        return 0
                # if last letter only check cell to right
                if count == len(word.word):
                    if not self.check_if_cell_clear(col + 1, row):
                        return 0
            # move to next position and letter
            if vertical:
                row += 1
            else:
                col += 1

            count += 1

        return score

    def set_word(self, col: int, row: int, vertical: bool, word) -> None:
        """
        Takes a cell position, direction and word object, adds that word to the grid
        Args:
            col (int) - Column for the word
            row (int) - Row for the word
            vertical (bool) - Whether the word should be vertical
            word (Word) - The word as a word object
        """
        word.col = col
        word.row = row
        word.vertical = vertical
        self.current_word_list.append(word)

        for letter in word.word:
            self.set_cell(col, row, letter)
            if vertical:
                row += 1
            else:
                col += 1

    def set_cell(self, col: int, row: int, value: str) -> None:
        """
        Takes the column and row of a cell, plus a value, sets that value as the value of the given cell
        Args:
            col (int) - The column of the target cell
            row (int) - The row of the target cell
            value (str) - The value to be given to the target cell
        """
        self.grid[row - 1][col - 1] = value

    def get_cell(self, col: int, row: int) -> str:
        """
        Takes a cell from column and row, returns the string value of the cell
        Args:
            col (int) - The column of the target cell
            row (int) - The row of the target cell
        Returns:
            cell (str) - Contents of the cell
        """
        cell = self.grid[row - 1][col - 1]
        return cell

    def check_if_cell_clear(self, col: int, row: int) -> bool:
        """
        Takes a cell from column and row, returns boolean whether it is empty or not
        Args:
            col (int) - The column of the target cell
            row (int) - The row of the target cell
        Returns:
            is_cell_empty (bool) - Whether the cell is empty or not
        """
        is_cell_empty = False
        try:
            cell = self.get_cell(col, row)
            if cell == self.empty_char:
                is_cell_empty = True
        except IndexError:
            pass
        return is_cell_empty

    def wordsearch(self) -> str:
        """
        Return string representation of solution (grid including words in correct place)
        Returns
            out_str (str) - grid of solution including correct words, with pipe char between cells, newline between rows, dashes for empty cells
        """
        alphabet_string = "abcdefghijklmnopqrstuvwxyz"
        out_str = ""
        for r in range(self.rows):
            for c in self.grid[r]:
                if c == "-":
                    random_letter = random.choice(alphabet_string)
                    out_str += f"{random_letter}|"
                else:
                    out_str += f"{c}|"
            out_str += "\n"
        return out_str

    def solution(self) -> str:
        """
        Return string representation of solution (grid including words in correct place)
        Returns
            out_str (str) - grid of solution including correct words, with pipe char between cells, newline between rows, dashes for empty cells
        """
        alphabet_string = "abcdefghijklmnopqrstuvwxyz"
        out_str = ""
        for r in range(self.rows):
            for c in self.grid[r]:
                out_str += f"{c}|"
            out_str += "\n"
        return out_str

    def order_number_words(self) -> None:
        """
        Updates number of words (.number of Word object) based on where they are positioned, in place within self.current_word_list
        """
        self.current_word_list.sort(key=lambda i: (i.col + i.row))
        count, icount = 1, 1
        for word in self.current_word_list:
            word.number = count
            if icount < len(self.current_word_list):
                if (
                    word.col == self.current_word_list[icount].col
                    and word.row == self.current_word_list[icount].row
                ):
                    pass
                else:
                    count += 1
            icount += 1

    def display(self, order: bool = True) -> str:
        """
        Creates and returns the user version of the grid, with numbers but no words
        Args
            order (bool) - whether to order word numbers based on their placement on the grid
        Returns
            out_str (str) - string representation of the grid, newline between each row, each cell separated by pipe char, with either number for where word starts, self.empty_char if no letter or space if there is a letter
        """
        out_str = ""
        if order:
            self.order_number_words()

        xword_copy = self

        for word in self.current_word_list:
            xword_copy.set_cell(word.col, word.row, word.number)

        for r in range(xword_copy.rows):
            for c in xword_copy.grid[r]:
                out_str += f"{c}|"
            out_str += "\n"

        out_str = re.sub(r"[a-z]", "~", out_str)
        return out_str

    def legend(self) -> str:
        """
        Creates and returns the list of clues and their positions
        Returns
            legend_str (str) - Numbered list of clues and directions for each word
        """
        legend_str = ""
        self.order_number_words()

        for word in self.current_word_list:
            legend_str += (
                f"{word.word.upper()}\n"
            )

        return legend_str
    
    def space_around_edges(self):
        dimensions = self.cols 
        # choose random small number to add top and side
        top_rows_to_add = random.choice([0, 1, 2])
        side_cols_to_add = random.choice([0, 1, 2])
        for row in range(top_rows_to_add):
            self.grid.insert(0, ["-"]*dimensions)
        new_height = dimensions + top_rows_to_add
        self.grid = [(["-"] * side_cols_to_add) + row for row in self.grid]
        for word in self.current_word_list:
            word.col, word.row = word.col + side_cols_to_add, word.row + top_rows_to_add

class Word:
    def __init__(
        self,
        word: Optional[str] = None,
    ):
        self.word = re.sub(r"\s", "", word.lower().strip())
        self.length = len(self.word)

        # NOTE: placeholders will be populated once the words are on the grid
        self.row = None
        self.col = None
        self.vertical = None
        self.number = None

    def is_horizontal(self) -> bool:
        """
        Returns boolean for whether word is placed horizontally
        Returns:
            is_horizontal (bool) - True if word is horizontal, False if word is vertical
        """
        is_horizontal = False if self.vertical else True
        return is_horizontal

    def __repr__(self) -> str:
        """
        Returns self.word as the string representation of the object
        """
        return self.word


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates a wordsearch from the given words"
    )
    # NOTE: below nargs allows it to take multiple and make a list
    parser.add_argument("words", nargs="*", type=str)
    args = parser.parse_args()
    all_args = args.words
    words = [i for i in all_args]

    max_word_len = max(
        [len(re.sub(r"\s+", " ", word.lower().strip())) for word in words]
    )
    grid_size = int(max_word_len * 1.5)
    search = Wordsearch(
        grid_size, grid_size, "-", 5000, words
    )
    search.compute_wordsearch(5)
    # NOTE: will be looking for the non-dynamic parts of output when drawing grid
    print("wordsearch_output")
    print(search.wordsearch())
    print("****")
    print(search.solution())
    print("****")
    print(search.legend())
    print("****")
    print(search.display())
    # TODO: could check and do something if not all words placed?
