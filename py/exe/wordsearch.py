from typing import Tuple, List
import random

class WordSearch:
    def __init__(self, grid_size: Tuple, words: List, ):
        self.grid_size = grid_size
        # NOTE: size tuple is (cols, rows) so 10,5 will be 10 wide and 5 tall
        self.words = words

    def _create_empty_grid(self) -> List:
        rows = self.grid_size[0]
        cols = self.grid_size[1]
        self.grid = [["" for row in range(rows)] for col in range(cols)]
        return self.grid

    def _get_coordinate(self, direction: str, word: str) -> Tuple:
        '''
        Get a random coordinate but only if viable based on direction and word length
        '''
        # TODO: seems not working properly, sometimes giving invalid coords (example was with diag up issue with row too high, check/test overall though, prob all need fixing...)
        if direction == "across":
            row_range = (0, len(self.grid[0]) - len(word) - 1)
            col_range = (0, len(self.grid))
        elif direction == "down":
            row_range = (0, len(self.grid[0]))
            col_range = (0, len(self.grid) - len(word) - 1)
        elif direction == "diag_up":
            row_range = (0, len(self.grid[0]) - len(word) - 1)
            col_range = (len(self.grid) - len(word), len(self.grid))
        elif direction == "diag_down":
            row_range = (0, len(self.grid[0]) - len(word) - 1)
            col_range = (0, len(self.grid) - len(word) - 1)
        random_col = random.randrange(col_range[0], col_range[1])
        random_row = random.randrange(row_range[0], row_range[1])
        return random_col, random_row

    def _place_word(self, location: Tuple, direction: str, word: str) -> List:
        '''
        Add the word to self.grid
        '''
        row = location[0]
        col = location[1]
        for letter in word:
            element_at_loc = self.grid[row][col]
            # if element_at_loc != "":
            #     print(f"ELEMENT AT LOC WHEN PLACING: {element_at_loc}")
            self.grid[row][col] = letter
            # increment row/col based on direction
            if direction == "across":
                col += 1
            if direction == "down":
                row += 1
            if direction == "diag_up":
                row -= 1
                col += 1
            if direction == "diag_down":
                row += 1
                col += 1
        return self.grid
    
    def _check_overlap(self, location: Tuple, direction: str, word: str) -> bool:
        '''
        If either there isn't a letter already at loc and not the same letter, true else false
        '''
        row = location[0]
        col = location[1]
        for letter in word:
            element_at_loc = self.grid[row][col]
            # TODO: sometimes not handling overlaps properly, need to fix!
            if element_at_loc == "" or element_at_loc == letter:
                # if element_at_loc != "":
                #     print(f"ELEMENT AT LOC: {element_at_loc}")
                #     print(f"LETTER: {letter}")
                # increment row/col based on direction
                if direction == "across":
                    col += 1
                if direction == "down":
                    row += 1
                if direction == "diag_up":
                    row -= 1
                    col += 1
                if direction == "diag_down":
                    row += 1
                    col += 1
            else:
                return True
                
        return False

    def _fill_grid(self) -> List:
        new_grid = []
        for row in self.grid:
            new_row = [i if i != "" else random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in row]
            new_grid.append(new_row)
        self.grid = new_grid
        return self.grid

    def create_word_search(self) -> List:
        self._create_empty_grid()
        self.words_placed = {} # storing the locations of words for solution
        # max_tries = 100
        # TODO: system to save the best and return that if perfect grid not found in n attempts?
        for word in self.words:
            invalid_location = True
            while invalid_location:
                direction = random.choice(["across", "down", "diag_up", "diag_down"])
                coord = self._get_coordinate(direction, word)
                invalid_location = self._check_overlap(coord, direction, word)
            self._place_word(coord, direction, word)
            self.words_placed[word] = {"direction": direction, "coord": coord}
        self._fill_grid()
        return self.grid

    def return_grid(self) -> List:
        print(self.grid)
        return self.grid

    def return_solution(self) -> str:
        grid_joined = []
        for row in self.grid:
            row_joined = "".join(row)
            grid_joined.append(row_joined)
        output_grid = "\n".join(grid_joined)
        print(output_grid)
        return output_grid

if __name__ == "__main__":
    word_list = ["testing", "example", "interesting", "redacted", "fun", "more", "words", "searching"]
    max_len = max([len(i) for i in word_list])
    size = (int(max_len * 1.5), int(max_len * 1.5))
    print("wordsearch_output")
    search = WordSearch(size, word_list)
    search.create_word_search()
    search.return_solution()
    print("****")
    print(search.words_placed)