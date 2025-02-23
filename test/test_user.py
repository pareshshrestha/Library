import pytest
from library.user import User
from library.book import Book

@pytest.fixture
def book():
    return Book("Test Title", "Test Author")

@pytest.fixture
def book2():
    return Book("Test Title2", "Test Author2")

@pytest.fixture
def user(book: Book):
    return User("Test", "User", [book])

@pytest.fixture
def user2(book: Book):
    return User("Test", "User", [book])  # Same as `user`, should be equal

@pytest.fixture
def user3(book: Book):
    return User("Fail Test", "Fail User", [])  # Different user

def test_creation(user: User, book: Book):
    """Test that a User is created with correct attributes."""
    assert user.name == "Test"
    assert user.password == "User"
    assert user.books == [book]

def test_borrow_book(user: User, book2: Book):
    """Test borrowing a book updates the user's book list."""
    user.borrow_book(book2)
    assert len(user.books) == 2  # Book2 should be added to the list

def test_return_book(user: User, book: Book, book2: Book):
    """Test returning a book updates the user's book list."""
    user.borrow_book(book2)
    user.return_book(book2)  # Make sure book2 is passed as the instance
    assert len(user.books) == 1  # Book2 should be removed from the list

def test_equal(user: User, user2: User):
    """Test that two users with the same name and password are equal."""
    assert user == user2

def test_not_equal(user: User, user3: User):
    """Test that two different users are not equal."""
    assert user != user3
