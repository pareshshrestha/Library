from pathlib import Path
import csv
import re
import sys
import typing
from book import Book
from user import User
from librarian import Librarian
from library_file import Library 

def database_exists():
    #checks if library database file exists or not and is hardcoded for it
    file_path = Path("library_database.csv")
    return file_path.exists()

def load_data()-> typing.Tuple[str, list,list, list]:
    '''
    Reads the library_database.csv file. 
    Loops through the rows and prompts user to choose one of the libraries.
    When correct is chosen, returns the library name and list of dictionaries of books, users and librarians.
    If user chooses to make a new library, returns name and 3 empty lists.
    '''
    #file check exists before this
    with open("library_database.csv", "r") as file:
            reader = list(csv.DictReader(file)) #turns it into a list so we can loop over it many times
    #looping to make sure the user has a valid choice 
    while True:
        for row in reader:
            prompt = "Would you like to load the data of "+row["name"]+" ? (Y/N)"
            if is_yes(prompt):
                return row["name"], row["books"], row["users"], row["librarians"]              
            #case if the user does not choose any library in this loop
        #new library 
        if is_yes("Would you like to create a new library? (Y/N)"):
            name = input("Enter the name of the library: ")
            return name.title(),[],[],[]
        else:
            print("Let's do this again.")

def save_all(name:str, books:list[dict], users:list[dict], librarians:list[dict]):
    '''
    Takes in unpacked data or list of dictionaries made from objects in the library object. 
    Creates a list by reading the file. 
    Replaces old library data with library data if the name matches, else appends the data to the list. 
    Writes in the old file all the old and the updated data.
    '''
    updated_data = { #creating a dictionary for the library datacase from modified data
        "name": name,
        "books": books,
        "users": users,
        "librarians":librarians
    }
    
    found = False
    with open("library_database.csv", "r") as file:
        reader = list(csv.DictReader(file))
        for row in reader:
            if name == row["name"]: #checking for the library for the updated data 
                #if name matches, replace the old with the updated data
                row["books"] = updated_data["books"]
                row["users"] = updated_data["users"]
                row["librarians"] = updated_data["librarians"]
                found = True
                break
    if not found:
        reader.append(updated_data) #new library and it's data

    with open("library_database.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "books", "users", "librarians"])
        writer.writeheader() #write column titles
        writer.writerows(reader) #write data for each library

#standard yes-or-no sorter
#returns True if the answer is yes and False if no
def is_yes(prompt:str) -> bool:
    while True:
        user_input = input(prompt)
        user_input = user_input.strip().lower()
        if user_input.startswith("y"):
            return True
        elif user_input.startswith("n"):
            return False
        else:
            print("Please enter Y or N only.")

#does the user want to login as regular user or librarian
def find_user_type(library_name:str)-> typing.Literal["user","librarian"]:
    print(f"Welcome to {library_name}.\nLet's sign you in.")
    while True:
        user_input = input("Are you a user or librarian? ").lower()
        match = re.search(r"(user|librarian)", user_input) #search for user or librarian
        if match:
            return match.group(1)
        else:
            print("Please choose one or the other.\nIf you did and you're still getting this message, please check your spelling.")

#promts the user to choose and returns either "login" or "signup"
def login_or_signup() -> typing.Literal["login", "signup", "sign up"]:
    while True:
        user_input = input("Do you want to login or signup?: ").lower()
        match = re.search(r"(login|sign ?up)", user_input)
        if match:
            return match.group(1)
        else:
            print("Please enter either login or signup.\n(Hint:try no spaces between signup.)")

#new user, makes sure that no overlapping username takes place, and returns valid username and password
def new_user(name_set : set)->tuple[str, str]:
    '''
    Takes the user chosen username and checks if it is unique to the library. 
    If it is unique, it accepts the password for the user and returns them.
    '''
    while True:
        username = input("Please enter your username: ")
        if username not in name_set:
            break
        else:
            print("The username is taken. Please choose something else.")
    
    password = input("Please enter your password: ")
    return username, password

#checks if the username and password are valid 
#returns 
def login(userlist:list[User]) -> User:
    '''
    Takes username and password as user input and compares it to the user. 
    Returns the User object that matches the entered values. 
    Exits the entire program if there are more than 3 failed attempts.
    '''
    attemp_count = 0 #tracks failed attempts
    while True:
        username = input("Please enter your user name: ")
        password = input("Please enter your password: ")
        for user in userlist:
            if username == user.name and password == user.password:
                return user
        
        print("Wrong username or password.")
        attemp_count += 1 
        if attemp_count > 3: #too many login attemps
            print("Too many failed login attemps!")
            sys.exit() #not allowing the user to brute force the system

def display_menu(is_librarian:bool) -> int:
    '''
    Displays the main menu to the user according to their access level. 
    Takes the userchoice and returns the integer value. 
    '''
    print (
        "Here are your menu options:",
        "0. End the program.",
        "1. Search for a book.",
        "2. Return book.", 
        "3. Borrow book.",
        sep="\n"
    )
    if is_librarian:
        print(
            "4. Add a book.",
            "5. Remove a book.",
            "6. Remove user.", 
            sep="\n"
        )
    
    while True:
        try:
            userchoice = int(input(("Please enter the integer corresponding to the menu option you would like to select: ")))
            if (0 <= userchoice <= 3) or (is_librarian and 4 <= userchoice <= 6): #because only librarian can use the last 2 options
                return userchoice
        except ValueError:
            print("Please choose an integer value only.")

def unpack_data(library:Library) -> tuple[str, list[dict],list[dict],list[dict]]:
    '''
    Takes in a library object. 
    Then it turns all the book, user and librarian objects back into list of dictionaries and returns them. 
    This is for the sole purpose of saving the data back into the csv database. 
    '''
    #name 
    name = library.name

    #unpack books 
    books = []
    for book in library.books:
        books.append({
            "title": book.title,
            "author": book.author,
            "status":book.status
        })
    
    #unpack users
    users = []
    for user in library.users:
        booklist = [] 
        for book in user.books:
            booklist.append({
                "name":book.name,
                "author":book.author
            })
        users.appen({
            "name": user.name,
            "password": user.password,
            "books":booklist
        })
    
    #unpack librarians
    librarians = []
    for librarian in library.librarians:
        booklist = []
        for book in librarian.books:
            booklist.appen({
                "name":book.name,
                "author":book.author
            })
        librarians.append({
            "name": librarian.name,
            "password": librarian.password,
            "books":booklist
        })
    
    return name, books, users, librarians
