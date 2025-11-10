from rich.console import Console
from rich.table import Table
from rich.text import Text
from word_search_generator import WordSearch

WORD_SEARCH_SIZE = 20
WORD_SEARCH_LEVEL = 4  # All directions including complex diagonals (hardest)

console = Console()


def rgb_to_hex(rgb):
    """Convert RGB floats (0-1) to hex string for Rich."""
    r, g, b = rgb
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return f"#{r:02X}{g:02X}{b:02X}"


class WordSearchCompetition:
    def __init__(self, words: set[str]) -> None:
        self.score = 0
        self._puzzle = WordSearch(", ".join(words), level=WORD_SEARCH_LEVEL, size=WORD_SEARCH_SIZE)
        self._cells: set[tuple[int, int]] = set()
        self._correct_cells: set[tuple[int, int]] = set()

        # Determine solution cells
        for word in self._puzzle.placed_words:
            assert word.direction is not None
            assert word.start_row is not None
            assert word.start_column is not None
            dy, dx = word.direction.value
            for offset in range(len(word)):
                wx = word.start_column + (offset * dx)
                wy = word.start_row + (offset * dy)
                self._cells.add((wx, wy))

    def words(self) -> set[str]:
        """Get the set of words to be found in the puzzle.

        Returns:
            set[str]: The set of words.
        """
        return set(word.text for word in self._puzzle.placed_words)

    def width(self) -> int:
        """Get the width of the word search puzzle.

        Returns:
            int: The number of columns in the puzzle.
        """
        return len(self._puzzle.cropped_puzzle[0])

    def height(self) -> int:
        """Get the height of the word search puzzle.

        Returns:
            int: The number of rows in the puzzle.
        """
        return len(self._puzzle.cropped_puzzle)

    def access_cell(self, x: int, y: int) -> str:
        """Access the character from a cell. Accessing a character increases the score by 1.

        Args:
            x (int): The row index of the cell.
            y (int): The column index of the cell.

        Returns:
            str: The character in the specified cell.
        """
        self.score += 1
        return self._puzzle.cropped_puzzle[x][y]

    def submit(self, cell: tuple[int, int]) -> bool:
        """Submit a word guess for the puzzle. If the submission is incorrect, the score is increased by 10.

        Args:
            cell (tuple[int, int]): The (x, y) coordinates of the cell being submitted.

        Returns:
            bool: True if the word was found and submitted successfully, False otherwise.
        """
        if cell in self._cells:
            self._correct_cells.add(cell)
            return True
        self.score += 10
        return False

    def is_solved(self) -> bool:
        """Get whether the puzzle has been completely solved.

        Returns:
            bool: True if all solution cells have been correctly identified, False otherwise.
        """
        return self._cells == self._correct_cells

    def print_puzzle(self) -> None:
        """Print the puzzle to the console, highlighting correct cells. Should only be used for debugging."""
        char_table = Table(show_header=False, show_lines=False, box=None, padding=(0, 1))
        words_table = Table(show_header=True, show_lines=False, box=None, padding=(0, 1))
        words_table.add_column("Word")
        words_table.add_column("Start Position")
        words_table.add_column("Direction")

        debug_cell_colors: dict[tuple[int, int], str] = {}

        for word in self._puzzle.placed_words:
            assert word.direction is not None
            assert word.start_row is not None
            assert word.start_column is not None
            dy, dx = word.direction.value
            color = rgb_to_hex(word.color)

            for offset in range(len(word)):
                wx = word.start_column + (offset * dx)
                wy = word.start_row + (offset * dy)
                debug_cell_colors[(wx, wy)] = color

        # Print the puzzle
        for y, row in enumerate(self._puzzle.cropped_puzzle):
            row_cells = []
            for x, char in enumerate(row):
                color = debug_cell_colors.get((x, y))
                if color:
                    row_cells.append(Text(char, style=f"bold {color}"))
                else:
                    row_cells.append(Text(char))
            char_table.add_row(*row_cells)

        # Optional: word list table with matching colors
        words_table = Table(show_header=True, show_lines=False, box=None, padding=(0, 1))
        words_table.add_column("Word")
        words_table.add_column("Start Position")
        words_table.add_column("Direction")
        for word in self._puzzle.placed_words:
            color = rgb_to_hex(word.color)
            words_table.add_row(
                Text(word.text, style=color),
                Text(f"({word.start_column}, {word.start_row})", style=color),
                Text(f"{word.direction}", style=color),
            )

        console.print(char_table)
        console.print(words_table)
