import sys
import os
import pytest
import unittest.mock as mock
# Add the library directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library.library_file import Library
from library.book import Book
from library.user import User
from library.librarian import Librarian

def test_library_creation():
    lib = Library("Test Library")
    assert lib.name == "Test Library"
    assert lib.books == []
    assert lib.users == []
    assert lib.librarians == []

def test_library_creation_2():
    name = "Test Library"
    books = [{"title":"Book1", "author":"Author1", "status":"Available"}, {"title":"Book2", "author":"Author2", "status":"Borrowed"}]
    user = [{"name":"User1", "password":"Password1", "books":[{"title":"Book1", "author":"Author1"}]}]
    librarian = [{"name":"Librarian1", "password":"Password1", "books":[]}]
    lib = Library(name, books, user, librarian)

    assert lib.books[0].title == "Book1"
    assert lib.books[0].author == "Author1"
    for user in lib.users:
        assert user.name == "User1"
        assert user.password == "Password1"
        assert user.books[0].title == "Book1"
        assert user.books[0].author == "Author1"
    for librarian in lib.librarians:
        assert librarian.name == "Librarian1"
        assert librarian.password == "Password1"
        assert librarian.books == []
    
def test_library_add_user():
    lib = Library("Test Library 2")
    user = lib.add_user("UserOne", "PasswordOne")
    assert user.name == "UserOne"
    assert user.password == "PasswordOne"

def test_return_book():
    users = [{"name":"Harry", "password":"Potter", "books":[{"title":"Philosopher Stone", "author":"Rowling"}]}]
    books = [{"title":"Philosopher Stone", "author":"Rowling", "status":"borrowed"}]
    lib = Library("Test Library", books, users)
    user = lib.users[0]
    with mock.patch("library.utils.is_yes", return_value=True):
        lib.return_book(user, "Philosopher Stone")
    for book in lib.books:
        assert book.status == "available"

def test_borrow_book():
    user = [{"name":"Ron", "password":"Weasley", "books":[]}]
    books = [{"title":"Philosopher Stone", "author":"Rowling", "status":"available"}]
    lib = Library("Test Library", books, user)
    user = lib.users[0]
    lib.borrow_book(user, "Philosopher Stone")
    for book in lib.books:
        assert book.status == "borrowed"

def test_add_book():
    lib = Library("Test Library",[],[],[{"name":"LibrarianAdd", "password":"Password1", "books":[]}])
    lib.add_book(lib.librarians[0])
    assert lib.books[0].title == "Philosopher Stone"
    assert lib.books[0].author == "Rowling"
    assert lib.books[0].status == "available" 

def test_remove_book():
    books = [{"title":"Philosopher Stone", "author":"Rowling", "status":"available"}]
    lib = Library("Test Library",books,[],[{"name":"LibrarianRemove", "password":"Password1", "books":[]}])
    lib.remove_book(lib.librarians[0])
    assert lib.books == []

def test_remove_user_nobooks():
    user = [{"name":"Hermione", "password":"Notknownbyme", "books":[]}]
    lib = Library("Test Library",[],user,[{"name":"LibrarianRemoveUser", "password":"Password1", "books":[]}])
    lib.remove_user(lib.librarians[0])
    assert lib.users == []