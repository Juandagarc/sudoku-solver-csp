import pytest
from sudoku import CSP
import os

# Fixture to manage the creation and deletion of a temporary sudoku file
@pytest.fixture
def sudoku_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "solve.txt"
    p.write_text("0\n3\n0\n0\n0\n0\n0\n0\n0\n" * 9)  # Simple unsolved sudoku puzzle
    return p

# Happy path tests
@pytest.mark.parametrize("file_content,expected", [
    ("0\n3\n0\n0\n0\n0\n0\n0\n0\n" * 9, True, "HP_01"),
    ("0\n0\n0\n0\n0\n0\n0\n0\n0\n" * 9, True, "HP_02"),
    ("1\n2\n3\n4\n5\n6\n7\n8\n9\n" * 9, True, "HP_03")
], ids=["Minimal", "Empty", "Full"])
def test_happy_paths(sudoku_file, file_content, expected):
    # Arrange
    sudoku_file.write_text(file_content)
    sudoku = CSP()
    sudoku.Vars_Doms()
    sudoku.initBoard(str(sudoku_file))

    # Act
    result = sudoku.is_solved()

    # Assert
    assert result == expected

# Edge cases
@pytest.mark.parametrize("file_content,expected", [
    ("9\n8\n7\n6\n5\n4\n3\n2\n1\n" * 9, False, "EC_01"),
    ("1\n1\n1\n1\n1\n1\n1\n1\n1\n" * 9, False, "EC_02")
], ids=["Reverse", "AllOnes"])
def test_edge_cases(sudoku_file, file_content, expected):
    # Arrange
    sudoku_file.write_text(file_content)
    sudoku = CSP()
    sudoku.Vars_Doms()
    sudoku.initBoard(str(sudoku_file))

    # Act
    result = sudoku.is_solved()

    # Assert
    assert result == expected

# Error cases
@pytest.mark.parametrize("file_content,exception,expected", [
    ("", ValueError, "EC_01"),
    ("a\nb\nc\n", ValueError, "EC_02")
], ids=["EmptyFile", "InvalidCharacters"])
def test_error_cases(sudoku_file, file_content, exception, expected):
    # Arrange
    sudoku_file.write_text(file_content)
    sudoku = CSP()

    # Act & Assert
    with pytest.raises(exception):
        sudoku.initBoard(str(sudoku_file))
