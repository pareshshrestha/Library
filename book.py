from typing import Literal

class Book:
    '''
    Creates a book object with title, author and it's status in the library (available or borrowed).
    Has method to be returned or be borrowed which updates it's status respectively.
    Has str method which returns "{title of book} by {author}:{status}".
    Also has a equals to method which compares the title and author name regardless of case.
    '''

    def __init__(self, title:str, author:str, status:Literal["available","borrowed"]="available"):
        self.title = title
        self.author = author
        self._status = status #can be "available" or "borrowed"

    def __str__(self) -> str:
        '''
        Return format:
        "{title of book} by {author}:{status}"
        '''
        return f"{self._title} by {self.author}:{self.status}"
    
    def __eq__(self, other) -> bool:
        '''
        Compares the book title and author name and is not case sensitive.
        '''
        if other == None:
            return False
        else:
            return (self._title.lower() == other.title.lower() and self.author.lower() == other.author.lower())
    
    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
    
    @property
    def status(self):
        return self._status
    
    @title.setter
    def title(self, title):
        self._title = title.title()
    
    @author.setter
    def author(self, author):
        self._author = author.title()
    
    @status.setter
    def status(self, status):
        self._status = status
    
    def borrow_book(self):
        '''
        Checks if the book is available or not. 
        If it is available, changes the status to borrowed. 
        '''
        if self.status == "available":
            self.status = "borrowed"
            print(f"You have borrow {self.title} by {self.author}")
        else:
            print("The book is not available to be borrowed. Sorry.")

    def return_book(self):
        '''
        Checks if the book was borrowed previously. 
        If it was, changes the status to have been returned by marking it available.
        '''
        if self.status == "borrowed":
            self.status = "available"
            print(f"You have returned {self.title} by {self.author}")
        else:
            print("Are you sure this is the book you borrowed?")