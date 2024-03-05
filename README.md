# Puzzle Capture Automation

An automation tool for "Le CDV" student newspaper, designed to capture and save puzzles like Sudoku and Loopy from the web using Selenium WebDriver. It supports various puzzles, streamlining content gathering for the publication. Some puzzles are not currently supported due to solution access limitations.


[Le CDV](https://cdv.resel.fr/)

## Captured Puzzles

The following 16 images are automatically captured from various puzzle websites using this project:

- `loopy.png` / `loopy_solution.png`
- `sudoku_killer.png` / `sudoku_killer_solution.png`
- `sudoku_moyen.png` / `sudoku_moyen_solution.png`
- `sudoku_difficile.png`/ `sudoku_difficile_solution.png`
- `sudoku_diabolique.png` / `sudoku_diabolique_solution.png`
- `irregulier_moyen.png` / `irregulier_moyen_solution.png`
- `unequal_extreme.png` / `unequal_extreme_solution.png`
- `adjacent_tricky.png` / `adjacent_tricky_solution.png`

### Currently Unsupported Puzzles

The following puzzles are not supported due to the absence of a direct solution provision mechanism on their respective websites:

- `kakuro.png` / `kakuro_solution.png`
- `hanjie.png` / `hanjie_solution.png`
- `light_up.png` / `light_up_solution.png`
- `mots_meles.png` / `mots_meles_solution.png`
- `mots_fleches.png` / `mots_fleches_solution.png`

### Source Websites

The puzzles are captured from the following websites:

- [Loopy](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/loopy.html)
- [Sudoku Killer](https://www.e-sudoku.fr/sudoku-killer.php)
- [Sudoku Solo](https://www.e-sudoku.fr/jouer-sudoku-solo.php)
- [Irregular Sudoku](https://www.e-sudoku.fr/sudoku-irregulier.php)
- [Unequal](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unequal.html)

## Getting Started

### Prerequisites

- Python 3.x
- Selenium WebDriver

## Installation

1. **Clone the repository:**

`git clone https://github.com/matdou/CDVPuzzles`

2. **Navigate to the project directory:**

`cd CDVPuzzles`

3. **Install the required dependencies:**

`pip install -r requirements.txt`

## Usage

To run the script and start capturing puzzles:

`python main.py`

The script navigates through specified websites, captures images of puzzles and their solutions, and saves them to the specified directory.

## Contributing

Contributions to enhance the functionality or extend the range of supported puzzles are welcome. Please fork the repository and submit a pull request with your changes.

## Contact

[Mathis Doutre](mailto:mathis.doutre@imt-atlantique.net)
