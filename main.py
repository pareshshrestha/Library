'''
This project was created for the sole purpose of understanding classes and OOP.
It is a simple library which will allow users to login and borrow/return books. 
There will also be a librarian, only who can add or remove books but also users. 

Project maker: Paresh Shrestha
Project start date: 02/18/2025
Project finish date: 02/22/2025
'''
from library.library_file import Library
import utils as action
from library.user import User

def main():

    #Create a library object.
    #See if a database for the library already exists. 
    if action.database_exists():
        '''
        action.load_data() reads through the database csv file and allows user to choose a library or create a new one.
        Once chosen, returns the name, dictionary of books, dictionary of users. 
        Pass those values to create a library object of class Library.
        '''
        lib_name, lib_books, lib_users,lib_librarians = action.load_data() #get the data of the correct library
        library = Library(lib_name, lib_books, lib_users, lib_librarians) #instantiate a library with the given data
    else:
        #a file does not exist so create a library to save for later    
        print("Let's create the database for your library.")
        user_input = input("Please enter the name of your library: ")
        library = Library(user_input.title)
    
    #allows the user to login as user or librarian or make a new account
    user_type = action.find_user_type(library.name) #will return "user" or "librarian"
    
    #checking if new user or old user; signup or login
    type_login = action.login_or_signup()

    #if it's a signup, make a new user object and append to the list inside library object
    if type_login == "signup" or type_login == "sign up":
        name, password = action.new_user(User.all_users())
        current_user = library.add_user(name, password)
    
    #if it's login, make sure the username and password match
    else:
        if user_type == "user":
            current_user = action.login(library.users)
            authorised = False
        elif user_type=="librarian":
            current_user = action.login(library.librarians)
            authorised = True

    while True:
        #printing and finding the user's menu choice
        menu_choice = action.display_menu(authorised)

        #perform the action associated with the menu choice
        if menu_choice == 0: #exit from the database
            break

        elif menu_choice == 1: #search for a book
            keyword = input("Please enter either the name of the book or author you want to search: ")
            search_results = library.search_book(keyword)
            for book in search_results:
                print(book)

        elif menu_choice == 2: #return a book
            print("You have currently borrowed the following books: ")
            for book in current_user.books:
                print(book)
            keyword = input("Please enter the book you want to return: ")
            library.return_book(current_user, keyword)

        elif menu_choice == 3: #borrow a book
            keyword = input("Please enter either the name of the book or author you want to search: ")
            library.borrow_book(current_user, keyword)
            
        elif menu_choice == 4 and authorised: #add a book
            library.add_book(current_user)
            
        elif menu_choice == 5 and authorised: #remove a book
            library.remove_book(current_user)
            
        elif menu_choice == 6 and authorised: #remove a user
            library.remove_user(current_user)
    
    #user has exited main menu 
    print("Thank you for using the library today!")

    #autosave function
    name, books, users, librarians = action.unpack_data(library)
    action.save_all(name, books, users, librarians)

if __name__=="__main__":
    main()