#CSC221
#m3hw

"""
Author: Reagan
A video rental program, yo
"""

import csv
import random

def main():
    #Variable for recieving user answer
    answer = 0

    #Variable for containing the list of movies
    movies = []

    #Variable for containing the list of customers
    customers = []

    #Here are our filenames
    filename1 = 'customerdatabase.csv'
    filename2 = 'moviedatabase.csv'

    #A while statement that makes main run until exit is chosen
    while(answer != 7):
        print("1. Load customers database.")
        print("2. Load movies database.")
        print("3. Display currently renting customers.")
        print("4. Display overdue customers.")
        print("5. Display one customer's invoice.")
        print("6. Rent a movie to a customer.")
        print("7. Exit")
        answer = int(input("Please make a selection  "))

        #lists the choices for the user
        if(answer==1):
            loadCust(filename1, customers)
        elif(answer==2):
            loadMovie(filename2, movies)
        elif(answer==3):
            showRenters(customers,movies)
        elif(answer==4):
            showOverdue(customers,movies)
        elif(answer==5):
            printInvoice(customers,movies)
        elif(answer==6):
            rentFilm(customers, movies)
        elif(answer==7):
            exit
        else:
            print("Please choose a valid answer")


""" This loads the customers into the program.  Option 1"""
def loadCust(filename, customers):
    firstName = ""
    lastName = ""
    custID = ""
    # Checks if customer is currently renting anything
    renting = ""

    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            firstName = row[0]
            lastName = row[1]
            custID = row[2]
            renting = row[3]
            customer = Customer(firstName, lastName, custID, renting)
            customers.append(customer)

    print("\nCustomer file has been loaded\n")
    



"""loads in the movie file into a list.  Option 2 """
def loadMovie(filename, movies):
    title = ""
    ID = ""
    genre = ""
    # Checks to see if a movie is in or out.
    out = ""
    rentedBy = ""
    # Days a movie has been rented out
    daysOut = 0
    # Days a movie is over the rental limit
    daysOver = 0

    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            title = row[0]
            ID = row[1]
            genre = row[2]
            out = row[3]
            rentedBy = row[4]
            daysOut = int(row[5])
            daysOver = int(row[6])
            movie = Movie(title, ID, genre, out, rentedBy, daysOut, daysOver)
            movies.append(movie)
            
    print("\nMovie file has been loaded\n")



    
""" Shows the list of customers currently renting movies. Option 3"""
def showRenters(customers,movies):
    #check and see if the customers and movies lists are loaded
    if len(customers) == 0:
        print("\nCustomer file has not been loaded!\n")
    if len(movies) == 0:
        print("\nCustomer file has not been loaded!\n")

    #print all customers who have stuff rented out
    print("\nThese are the people currently renting from us: ")
    for customer in customers:
        if(customer.renting =="yes"):
            print("\t",customer.firstName,customer.lastName,)
    print("\n")





""" Shows any customers who haven't turned in movies during rental period.
    Option 4"""
def showOverdue(customers, movies):
    #check and see if the customers and movies lists are loaded
    if len(customers) == 0:
        print("\nCustomer file has not been loaded!\n")
    if len(movies) == 0:
        print("\nCustomer file has not been loaded!\n")
    print("\n", "These customers are overdue:")

    #search movie list for overdue movies
    for movie in movies:
        if(movie.daysOver != 0):
            #after finding an overdue movie, search customer database for renter
            for customer in customers:
                if(movie.rentedBy == customer.custID):
                    #print the name of the person who is overdue and why
                    print(customer.firstName, customer.lastName, "is", movie.daysOver,
                          "days overdue with movie:", movie.title)
    print('\n')







""" Prints out information for one specific customer.  Option 5 """
def printInvoice(customers, movies):
    #check and see if the customers and movies lists are loaded
    if len(customers) == 0:
        print("\nCustomer file has not been loaded!\n")
    if len(movies) == 0:
        print("\nCustomer file has not been loaded!\n")

    # Enter the name of the customer you are looking for
    custFname = input("Enter the customer's first name: ")
    custLname = input("Enter the customer's last name: ")
    print("\n")

    #variables to determine late fees
    allDaysOver = 0
    lateFee = 2.0
    totalFees = 0.0

    #search customer database to see if customer match exists
    for customer in customers:
        if(custFname == customer.firstName) and (custLname == customer.lastName):
            #if a match, searches database for movie rented 
            for movie in movies:
                #if customer code matches movie code, print customer and days overdue
                if(customer.custID == movie.rentedBy):
                    print(movie.title, "is", movie.daysOver, "days overdue.")
                    #The days overdue for each movie are summed together
                    allDaysOver += movie.daysOver
            break
        
       # Late fees are determined by multiplying days by the daily late fee
    totalFees = allDaysOver * lateFee

    # If there are no fees, only this fact is printed
    if(totalFees == 0):
        print("\n",custFname, custLname, "has no late fees.\n")
    else:
        print(customer.firstName, customer.lastName, "owes", totalFees,
              "in late fees.\n")
                    
         



""" Helps customer rent a movie.  Option 6 """
def rentFilm(customers, movies):
    #check and see if the customers and movies lists are loaded
    if len(customers) == 0:
        print("\nCustomer file has not been loaded!\n")
    if len(movies) == 0:
        print("\nCustomer file has not been loaded!\n")
        

    # Enter the name of the customer you are looking for
    custFname = input("Enter the customer's first name: ")
    custLname = input("Enter the customer's last name: ")

    # Variables in case one needs to add a new customer
    firstName = ""
    lastName = ""
    custID = ""
    # Checks if customer is currently renting anything
    renting = "yes"

    # This saves me trouble by not asking for new customer information for every line in the customer database
    check = 0

    #searches customer database for customer
    for customer in customers:
        if(custFname == customer.firstName) and (custLname == customer.lastName):
            print("Customer in database.\n")
            check = 1
            break

    # If the customer is not in the database, they have to be entered in
    if(check == 0):
        print("New customer.  Generating data now.")
        firstName = custFname
        lastName = custLname
        # Each customer ID is their initials and four random numbers
        custID = custFname[1] + custLname[1] + str(random.randint(1,10)) + str(random.randint(1,10)) + str(random.randint(1,10)) + str(random.randint(1,10))
        #renting is already set to "yes", because you're not going to enter someone in a database if they aren't renting a movie.
        customer = Customer(firstName, lastName, custID, renting)
        customers.append(customer)
        print("Customer data entered.\n")
        

    # Resetting the check variable for reuse
    check = 0
    # variables for asking for a movie to rent
    film = ""
    rentfilm = 'y'
    # variables if a new movie needs to be added
    title = ""
    ID = ""
    genre = ""
    # Checks to see if a movie is in or out.
    out = ""
    rentedBy = ""
    # Days a movie has been rented out
    daysOut = 0
    # Days a movie is over the rental limit
    daysOver = 0
    asking = 0

    while (rentfilm !='n') and (rentfilm != 'N'):
        film = input("What movie is the customer renting?  ")
        print("\n")
        for movie in movies:
            if(film == movie.title):
                if(movie.out == "yes"):
                    print("This movie is being rented already.\n")
                    check = 2
                    break
                movie.out = "yes"
                movie.rentedBy = customer.custID
                check = 2
                break

#if the movie isn't in the database, it's added in
        if(check == 0):
            print("That movie is not in the database.  Preparing entry.")
            title = film
            # A movie id is its first three characters and five random numbers
            ID = film[1:3] + str(random.randint(1,10)) + str(random.randint(1,10)) + str(random.randint(1,10)) + str(random.randint(1,10)) + str(random.randint(1,10))
            asking = int(input("Is this film a 1. New Release, 2. Children's Film, or 3. General? \nEnter 1, 2, or 3.  "))
            if(asking == 1):
                genre = "New Release"
            elif(asking == 2):
                genre = "Children's"
            elif(asking == 3):
                genre = "General"
            else:
                print("Invalid input.  Assuming General.")
                genre = "General"
            rentedBy = customer.custID
            #Other details unnecessary to change as they can be assumed.
            movie = Movie(title, ID, genre, out, rentedBy, daysOut, daysOver)
            movies.append(movie)
            print("Film has been entered.")

        rentfilm = input("Would you like to rent another movie? (y or n)") 
       
        


   
    
    

""" Customer class to create customer objects """
class Customer:
    def __init__(self, firstName, lastName, custID, renting):
        self.firstName = firstName
        self.lastName = lastName
        self.custID = custID
        self.renting = renting

    def setFirst(self, firstName):
        self.firstName = firstName
    def setLast(self, lastName):
        self.lastName = lastName
    def setID(self, custID):
        self.custID = custID
    def setRenting(self, renting):
        self.renting = renting

    def getFirst(self):
        return self.firstName
    def getLast(self):
        return self.lastName
    def getID(self):
        return self.custID
    def getRenting(self):
        return renting


""" Movie class to create movie objects """
class Movie:
    def __init__(self, title, ID, genre, out, rentedBy, daysOut, daysOver):
        self.title = title
        self.ID = ID
        self.genre = genre
        self.out = out
        self.rentedBy = rentedBy
        self.daysOut = daysOut
        self.daysOver = daysOver

    def setTitle(self, title):
        self.title = title
    def setID(self, ID):
        self.ID = ID
    def setGenre(self, genre):
        self.genre = genre
    def setOut(self, out):
        self.out = out
    def setRentedBy(self, rentedBy):
        self.rentedBy = rentedBy
    def setDaysOut(self, daysOut):
        self.daysOut = daysOut
    def setDaysOver(self, daysOver):
        self.daysOver = daysOver

    def getTitle(self):
        return self.title
    def getID(self):
        return self.ID
    def getGenre(self):
        return self.genre
    def getOut(self):
        return self.out
    def getRentedBy(self):
        return self.rentedBy
    def getDaysOut(self):
        return self.daysOut
    def getDaysOver(self):
        return self.daysOver
        
    



if __name__ == "__main__":
    main()
