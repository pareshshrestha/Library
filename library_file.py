from book import Book
from user import User
from librarian import Librarian
import utils as action
import typing

class Library:
    '''
    Creates an object library.
    The object has a library name, list of Book objects and list of User and Librarian objects.
    It takes in a list of dictionaries as inputs for books, users and librarins then initializes the objects. (csv file input)
    It allows users and librarians to search for, borrow and return books. 
    Librarians can additionally add or remove books and users from the library.
    '''

    def __init__(self, name:str, books:list[dict] = [], users:list[dict]=[], librarians:list[dict]=[]):
        self.name = name
        self._book_index = {}

        self.books = books
        self._build_book_index()

        self.users = users
        self.librarians = librarians       
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, lib_name):
        self._name = lib_name

    @property
    def books(self) -> list[Book]:
        return self._books

    @books.setter
    def books(self, books_list:list[dict]):
        '''
        Takes in a list of dicts which describe a book at a time. 
        Instantiates Book objects with the information in the dict and appends to a list. 
        The list if finally assigned as a propety of library object.  
        '''
        book_list = [] #list of Book objects
        for book in books_list: #getting a dict at a time for each book
            temp_book = Book(book["title"], book["author"], book["status"]) #initializing Book object
            book_list.append(temp_book) 
        self._books = book_list

    @property
    def users(self):
        return self._users

    @users.setter
    def users(self, user_dict:list[dict]):
        '''
        Takes in a list of dicts which describe a user at a time. 
        Instantiates User objects with the information in the dict and appends to a list. 
        The list if finally assigned as a propety of library object.  
        '''
        user_list = [] #list of User objects
        for user in user_dict:
            #finding the corresponding book objects for the user
            userbooks = []
            for book in user["books"]: #looping through user books
                bookobj = self.search_book(book["title"], book["author"])
                if bookobj != None: #checking if book or not (None)
                    userbooks.append(bookobj)
            user_list.append(User(user["name"], user["password"], userbooks)) #creating user object and adding it to the list
        
        self._users = user_list 

    @property
    def librarians(self):
        return self._librarians
    
    @librarians.setter
    def librarians(self, librarian_dict:list[dict]):
        '''
        Takes in a list of dicts which describe a librarian at a time. 
        Instantiates librarian objects with the information in the dict and appends to a list. 
        The list if finally assigned as a propety of library object. 
        Code comments same as user. 
        '''
        librarian_list = []
        for librarian in librarian_dict:
            lib_books = []
            for book in librarian["books"]:
                bookobj = self.search_book(book["title"], book["author"])
                if bookobj is not None:
                    lib_books.append(bookobj)
            librarian_list.append(Librarian(librarian["name"], librarian["password"], lib_books))
        self._librarians = librarian_list

    def _build_book_index(self):
        """
        Creates a dictionary (_book_index) where the keys are tuples of book title and author name (both in lowercase),
        and the values are the corresponding book objects. This allows for easy retrieval of book objects using just the 
        title and author. This method is intended to support a search function.
        """
        for book in self.books:
            titlekey = book.title.lower()
            authorkey = book.author.lower()
            key = (titlekey, authorkey)
            self._book_index[key] = book

    @property
    def book_index(self):
        return self._book_index
    
    def search_book(self, title:str, author:str) -> typing.Optional[Book]:
        '''
        Returns the Book object corresponding to the passed title and author. 
        If there is no equivalency, returns None.
        '''
        key = (title.lower(), author.lower())
        try:
            return self.book_index[key]
        except KeyError:
            return None
    
    def add_user(self, name:str, password:str)->User:
        user = User(name,password,[]) #creating user object
        self._users.append(user) #adds a user to the library
        return user #returns the object for use in main
    
    def return_book(self, current_user:User, keyword:str):
        '''
        Takes in the User object returning the book and the keyword denoting the book object.
        Searches for the book and if found, calls the return book method in book object. 
        Also, removes the book objects from the books list inside the User object. 
        '''
        keyword = keyword.strip().lower()
        for book in current_user.books:  #looping through the books in User object
            if keyword in book.title.lower() or keyword in book.author.lower(): #matching the keyword to book title or author
                print(book) #displaying the book that matches keyword
                if action.is_yes("Is the book you want to return?(Y/N) "): #confirming if it is the book to be returned
                    current_user.return_book(book) #returns the book - removes the book from User booklist, calls return book method in Book object 
                    found = True 
                    break
        if found != True:
            print("You have borrowed no books that matches the search parameters.")

    def keyword_search(self, keyword:str) -> Book:
        '''
        Uses the user input as a keyword and searches throught the keys of the book index dict.
        Returns Book oject or None.
        '''
        keyword = keyword.lower()
        for key in self._book_index.keys(): #looping through the keys in book index dict
            title, author = key #assigning the tuple
            if keyword in title.lower() or keyword in author.lower(): #checking if keyword matches 
                print(self._book_index[key]) #printing the corresponding book
                if action.is_yes("Is this the book?(Y/N) "): #confirming the chosen book
                    return self._book_index[key]
                else:
                    return None
        
    def borrow_book(self, current_user, keyword):
        book = self.keyword_search(keyword)
        if book != None:
            current_user.borrow_book(book) 
        else:
            print("The search parameters returns no results.")

    def add_book(self, librarian:Librarian):
        '''
        Only for librarian. 
        Accepts input for book title and author and creates a book object. 
        Adds it to the library object. 
        '''
        while True:
            book_title = input("Please enter the title of the book: ").title()
            book_author = input("Please enter the author of the book: ").title()
            if action.is_yes(f"Is the book you want to add {book_title} by {book_author}?(Y/N) "): #confirming book details
                book = Book(book_title,book_author)
                librarian.add_book(self, book)
                break
            else:
                if action.is_yes("Do you want to try again? (Y/N)"): 
                    print("Okay, let's try again!")
                else:
                    print("Okay, let's go back to main menu.")
                    break
    
    def remove_book(self, librarian):
        while True:
            keyword = input("Which book would you like to remove? ")
            book = self.keyword_search(keyword)
            if book != None:
                librarian.remove_book(self, book)
                break           
            else:
                print("Your search parameters returned no results.")
                if action.is_yes("Would you like to try again?(Y/N) "):
                    print("Okay, let's try again.")
                else:
                    print("Okay. Returning you to main menu.")
                    break
        
    def remove_user(self, librarian):
        while True:
            username = input("Enter the username of the user you want to remove: ")
            found = False
            for user in self.users:
                if user.name == username:
                    found = True
                    if action.is_yes("Did the user return the books?(Y/N) "):
                        for book in user.books:
                            book.return_book()
                        librarian.remove_user(self, user)
                    else:
                        for book in user.books:
                            librarian.remove_book(self, book)
                        librarian.remove_user(self, user)
            if found:
                print("User removed.")
                break

            if not found:
                if action.is_yes("The username entered does not exist. Would you like to try again?(Y/N) "):
                    print("Let's try again.")
                else:
                    print("Okay, returning to main menu.")
                    break

