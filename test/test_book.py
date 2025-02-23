import pytest
from library.book import Book

@pytest.fixture
def book():
    return Book("Test Title", "Test Author")

@pytest.fixture
def book2():
    return Book("test title", "test author")

@pytest.fixture
def book3():
    return Book("Fail test","fail author")

def test_creation(book):
    assert book.title == "Test Title"
    assert book.author == "Test Author"
    assert book.status == "available"

def test_creation2(book2):
    assert book2.title == "Test Title"  # Ensure consistency
    assert book2.author == "Test Author"
    assert book2.status == "available"

def test_borrow_book(book):
    book.borrow_book()
    assert book.status == "borrowed"

def test_return_book(book):
    book.borrow_book()
    book.return_book()
    assert book.status == "available"

def test_equal(book, book2):
    assert book == book2

def test_str_return(book):
    assert str(book) == "Test Title by Test Author:available"

def test_not_equal(book, book3):
    assert book != book3
