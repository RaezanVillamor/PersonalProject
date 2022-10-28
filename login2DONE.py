import searchartistDONE
import sys
import sqlite3

conn = sqlite3.connect("loginTest2Better.db")
# conn = sqlite3.connect(sys.argv[1])
#

c = conn.cursor()

# Menu Screen. Login, 
# Signup (only for users) artists are preassumed to be in the databse
# Logout Go back to menu screen

def login():
    '''
    Case 1: A user or artist tries to log in --> Find an id match in either artist or user --> prompt for password --> password is correct -->succesful sign in
    Case 2: A  userr tries to log in --> Find an id match in either artist or user --> prompt for password --> password is incorrect --> print "incorrect pass" --> takes you back to menu
    
    Case 3: An artist who is also a user tries to log in --> id match in artist and user --> prompt to log in as a user or id --> succesful sign in
    Case 4: An artist who is also a user tries to log in --> id match in artist and user --> prompt to log in as a user or id --> password incorrect. --> takes you back to menu
    
    Case 5: user tries to log in but is not in database --> print out "not in database. Signup?" --> after signing up as a USER (because artists are already presumed to be in the database) then go back to main menu and next time we try to 
    Maybe we can handle cas 5 in another function
    
    IMPORTANT NOTES:
    On ECLASS Davvod says that and I quote:
    Davood: The spec for neither Assignment 2 and the project says that uid should start with 'u' and aid with 'a'. What we say in the project description that the same id can appear in users and artists tables, for example when a user is also an artist.
    So therefore I assume that the user id and artist id get be the same number etc like 3 or 4. No need to have it start with 'u' or 'a'
    
    For signup cases I believe sqlite will automatically handle unique ID's but however I could be wrong. Talk to group members about this.
    
    # use the thing where we can pass the database as a comman line argument !!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!

    If in the thing we're supposed to find the ID's which do have a u and an a in the beginning then we must scrape the a and u in the beginning
    '''
    # Grab all users and artists id
    
    # handles user input so you cant have more than 4 characters
    while True:
        userInput = input("please login using your id: ")

        if len(userInput) > 4:
            print('Enter a maximum of 3 characters.')
            continue
        else:
            print(userInput)
            break
    
    # print(type(userInput))

    c.execute("SELECT  substr(uid, 2, length(uid)) as username,* FROM users WHERE username=?", (userInput,)) #Need a comma after userunput to make our parameters a tuple. Otherwise this will not work when suppled with big numbers
    rowForUsers = c.fetchone()
    c.execute("SELECT substr(aid, 2, length(aid)) as artistname ,* FROM artists WHERE artistname=?", (userInput,)) #Need a comma after userunput to make our parameters a tuple. Otherwise this will not work when suppled with big numbers
    rowForArtists = c.fetchone()
    print(rowForUsers)
    print(rowForArtists)

    
#   This if statement checks if the input given by the user is within the artists and users
    if rowForArtists != None and rowForUsers!= None and rowForUsers[0] == rowForArtists[0] :
        print("A login has been detected for both users and artists")
        loginChoose = input("Would you like to login as a user (1) or artist (2): ")
        # Choosing login type either as a user or artist
        if loginChoose == '1':
            loginForUsers(rowForUsers)
        if loginChoose == '2':
            loginForArtists(rowForArtists)
    elif rowForUsers:
        # If user is only a user login
        loginForUsers(rowForUsers)
    elif rowForArtists:
        # If person only has a artist account
        loginForArtists(rowForArtists)
    else:
        # Handles user creation
        print("No such user detected. Make an account?")
        createUser = input("yes (y) or no (n): ")
        if createUser == 'y':
            signup()
        elif createUser == 'n':
            print("mmkay bye u bum")
        else: 
            print("not a valid input exiting....")
    
    
            


def loginForUsers(rowForUsers):
    if rowForUsers:
        userPwd = input("please enter your password " + rowForUsers[1] + ": ")
        if rowForUsers[3] == userPwd:
            print("Succesful login "+ rowForUsers[1])
            # Call the function do the menus
            menuCheck()
        else:
            print("Incorrect login try again "+ rowForUsers[1])

def loginForArtists(rowForArtists):
    if rowForArtists:
        userPwd = input("please enter your password " + rowForArtists[1] + ": ")
        if rowForArtists[4] == userPwd:
            print("Succesful login "+ rowForArtists[1])
            # Call menu
            menuCheck()
        else:
            print("Incorrect login try again "+ rowForArtists[1])


def exitOrLogout():
    # Maybe this should only pop up if you succesfully signin or else whats the point
    request = input("would you like to exit? exit(e) or logout (l):")
    if request == 'e':
        # Create a new user
        print("bye")
    elif request == 'l':
        login()
    
def signup():
    '''
    Case 5: handling sigup if no id is in da thingy for either users or artists
    
    '''
    print("Thank you for deciding to signup!")
    userIdInput = input("Please enter a user id that is less than 4 characters: ")
    userNameInput = input("What's your name?: ")
    userPwdInput = input("Please enter a super secret password: ")
    c.execute('''
              INSERT INTO users(uid, name,pwd) VALUES(?,?,?)
              
              ''', (userIdInput, userNameInput, userPwdInput)
              )
    conn.commit() #Forgot to commit last time therefore it was making a separate database. Again be careful lol
    print("thank you for signing up! Taking you back now to the login page...")
    
    login() #this extra logout will stack. Be careful of this
    
def menuCheck():
    
    print("Press 1 to start a session")
    print("Press 2 to to search for a song")
    print("Press 3 to search for an artists")
    print("Press 4 to end the session")
    menuInput = input("What would you like to do today?: ")
    if menuInput == '2':
        searchartistDONE.searchArtists()
        
        


 
# if __name__ == "__main__":
#     login()

def main():
    login()
main()
# Afterwards we need to check if this ID is part of users and artists or stands alone
 