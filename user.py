from library.book import Book
#from __future__ import annotations 

class User:
    '''
    Creates a user object with username, password and list of borrowed books.
    Has methods to borrow and return books.
    '''

    all_usernames = set() #set containing all usernames to make sure there is no duplicate usernames

    def __init__(self, name:str, password:str, books:list[Book]):
        self.name = name
        self.password = password
        self.books = books

    def __str__(self) -> str:
        '''
        Return format:
        {username}, Books borrowed:
        {book title} by {author}: {status}
        {book title} by {author}: {status}
        ...
        '''
        books_str = "\n".join(str(book) for book in self.books) #turns list of book objects to a long string
        return f"{self.name}, Books borrowed:\n{books_str}"
    
    def __eq__(self, other) -> bool:
        '''
        Compares the name and password of the users passed. 
        Both are case sensitive so no modification is done before comparing.
        '''
        return (self.name == other.name and self.password == other.password)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, username:str):
        '''
        Checks if the entered username is unique and does not clash with any existing usernames.
        It sets the username and also adds it to the existing set of usernames. 
        '''
        #checks if username is taken
        if username not in User.all_usernames:  #username available 
            self._name = username
            User.all_usernames.add(username)
        else:  #username already taken
            while True: #loops till a valid unique username is added
                print("Username already taken.") 
                username = input("Please enter another username: ")
                if username not in User.all_usernames:
                    self._name = username
                    User.all_usernames.add(username)
                    break 
        
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, entered_pass):
        self._password = entered_pass
    
    def is_correct_password(self, entered_pass) -> bool: #password check
        return self.password == entered_pass
    
    @property
    def books(self):
        return self._books
    
    @books.setter
    def books(self, book_list):
        '''
        Is a list of book objects.
        The book objects are instantiated in the library object and passed. 
        '''
        self._books = book_list

    def return_book(self, book:Book): 
        '''
        Returning a book according to the book object passed.
        Rechecks if the book exists in the list of books this user has borrowed.
        Calls method in the book object to change the status in the book object.
        Then finally removes the book object from the list of borrowed books of the user. 
        '''
        if book in self.books: #checking if the user has borrowed the passed book or not
            book.return_book() #changes the status in the book object
            self._books.remove(book) #removes the book from the list of borrowed books in the user object

    def borrow_book(self, book:Book):
        '''
        Method borrows the book for the current user. 
        Calls method inside book to change the status of the book.
        Adds the book object to the list of borrowed books inside uesr. 
        '''
        book.borrow_book() #changes the status of the book
        self._books.append(book) #records the book as borrowed inside user

    @classmethod
    def all_users(cls) -> set:
        return cls.all_usernames #returns the set of usernames 