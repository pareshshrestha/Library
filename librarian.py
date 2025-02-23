from user import User
from book import Book

class Librarian(User):
    '''
    Special class inside the class User.
    Has only 3 functions but each has a line of code that directly accesses the attributes in library to make changes. 
    Adds or removes books and can also remove users. 
    '''
    def __init__(self, name:str, password:str, books:list[Book]):
        super().__init__(name, password, books) 

    #adding a new book to the library
    def add_book(self, library, book:Book):
        library._books.append(book)

    #removing a book from the library
    def remove_book(self, library, book:Book):
        library._books.remove(book)

    #removing the user 
    def remove_user(self, library, user):
        library._users.remove(user)