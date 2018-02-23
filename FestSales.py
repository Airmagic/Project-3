import sqlite3
# import traceback

# pointing to the db file
db = sqlite3.connect('FestSales.db')# creates or opens db files

# making variable for accessing the db
cur = db.cursor() #need a cursor object to perform operations

# makes the database if one doesn't exist
cur.execute('create table If Not Exists FestivalDates (placeOfFestival text not null unique, monthOfFestival int, dayofFestivel int)')

# main Program
def main():
    # displaying the choice menu
    choice_menu()
    # getting input from user
    choice = input('Enter your selection: ')
    # 1. Showing the list of the records
    if choice == '1':
        festival_date()

    # 2. adding a new record to the table
    elif choice == '2':
        add_new_date()

    # 3. searching the record
    elif choice == '3':
        search_for_date()

    # 4. updating a record
    elif choice == '4':
        update_date()

    # 5. mechandise for the festial
    elif choice == '5':
        merchandise_for_festival()

    # 6. viewing the merch for a fest
    elif choice == '6':
        view_merch_for_fest()

    # 7 Deleting a record from the table
    elif choice == '7':
        delete_date()


    # 666. Restarting the record from basic
    elif choice == '666':
        restart_festival_dates()

    # q. Quit
    elif choice in ('q', "Q"):
        db.close()
        quit()

    # message to show if input is not in the menu
    else:
        print('Please enter a valid selection')
        main()

def choice_menu():
    '''Display choices for user, return users' selection'''

    print('''
        Sale for Festival Merchandise
        ---------------------------------------
        1. See Festival Dates
        2. Add New Date
        3. Search Date
        4. Update Festival Name and Date
        5. Add Merchandise for Festival
        6. View Merchandise for Festival
        7. Delete Festival
        q. Quit
    ''')

def festival_date():
    # making a variable to order the list
    orderList = input("Would you like the list by Date(D) or Name(N)? ")

    # printing the record for the user
    if orderList in ("Date", "D", "date", "d"):
        for row in cur.execute('select * from FestivalDates ORDER BY monthOfFestival, dayofFestivel '):
            print(row)

    # printing the record for the user
    elif orderList in ("Name", "N", "name", "n"):
        for row in cur.execute('select * from FestivalDates ORDER BY placeOfFestival '):
            print(row)

    # else statement if the user doesn't choose one of the options
    else:
        for row in cur.execute('select * from FestivalDates ORDER BY monthOfFestival, dayofFestivel '):
            print(row)
    # calling the main method after the printout
    main()

def add_new_date():
    try:
        # getting input for the festival name
        festivelName = input("Enter the Name of the Festival: ")
        # formating the input
        festivelName = toFormatInput(festivelName)
        # getting the month from the user
        whichMonth = int(input("What month is the festivel(1-12): "))
        # sending the month to a checker to make sure it's 1-12
        checkMonth = checkMonthInput(whichMonth)
        # if statment checking if the information cam back true
        if checkMonth == True:
            # getting the day from the user
            whichDay = int(input("What day is the festivel(1-31): "))
            # sending it to a day checker to see if it is between 1-12
            # doesn't check to make sure the day is real
            checkDay = checkDayInput(whichDay)
            # if statement to see if the check day is true
            if checkDay == True:
                # adding the festival to the db
                cur.execute('insert into FestivalDates values (?, ?, ?)', (festivelName, whichMonth, whichDay))
                # formating to making a table to insert items into
                festivelName = festivelName.replace(" ", "")
                # creating the table
                cur.execute("create table IF NOT EXISTS {} (nameOfItem text, howManyItems int, price int)".format(festivelName,))
                db.commit() #save changes
                # printing out what the user input so they know it was added
                print("Festival {} add to date {}, {}".format(festivelName, whichMonth, whichDay))
            # else staement if days are not in parameters
            else:
                print("Please have the days from 1-31")
                add_new_date()
        # else staement if months are not in parameters
        else:
            print("Please have the months from 1-12")
            add_new_date()
        main()

    # a catch for the in inputs
    except ValueError:
        print("Needs to be a number")
        add_new_date()


def search_for_date():
    try:
        # getting the month for the user
        dateMonthSearch = int(input("What Month are you searching for?(1-12) "))
        # getting the day from the user
        dateDaySearch = int(input("What Day are you searching for? (1-31) "))

        # getting the information for that day
        festivalDay = cur.execute("select * from FestivalDates where monthOfFestival = ? and dayofFestivel = ?" , (dateMonthSearch, dateDaySearch,))
        # printing the information about that day or none if nothing on it
        print(festivalDay.fetchone())
        # calling the main
        main()

    # a catch for int inputs
    except ValueError:
        print("Needs to be a number")
        search_for_date()

def update_date():
    try:
        # getting the festival from the user
        whichToUpdate = input('What Festival To update? ')
        # formatting the input
        whichToUpdate = toFormatInput(whichToUpdate)
        # retrieving the information from the db
        festivalDay = cur.execute("select * from FestivalDates where placeOfFestival = ?", (whichToUpdate,))
        # making a variable to test if it comes back none
        checkOutput = festivalDay.fetchone()
        # printing out what is retrieved from the db
        print(checkOutput)

        # if statement if data comes back from the db
        if checkOutput != None:
            # first line to tell the user what to do
            print("What would you like to change/update")
            # getting the input from the user
            whatToUpdate = input("Festival Name(N) or Date(D) ")

            # if statement to see if the user picks Name
            if whatToUpdate in ('Name', 'N', 'name', 'n'):
                # setting the what to update to place of the festival for db query
                whatToUpdate = "placeOfFestival"
                # getting the new information from user
                updatingInput = input('What would you like to Change the name to? ')
                # formation the information they are inserting
                updatingInput = toFormatInput(updatingInput)
                # asking if they are sure
                countinue = areYouSure()

            # elif statement for the date
            elif whatToUpdate in ('Date', 'D', 'date', 'd'):
                # asking for the day or month to change
                dayOrMonth = input("Do you want to change month(m) or day(d)? ")
                # if statement for month
                if dayOrMonth in ("Month", "month", "M", "m"):
                    # making the what to update to month
                    whatToUpdate = "monthOfFestival"
                    # getting the new month
                    updatingInput = int(input('What would you like to Change the month to(1-12)? '))
                    # checking the input
                    checkMonth = checkMonthInput(updatingInput)
                    # if input is good asking are you sure
                    if checkMonth == True:
                        goOn = areYouSure()
                    else:
                        # setting goOn to anything but yes
                        goOn = "No"
                        # print that user was incorrect
                        print("The Month has to be between 1-12")


                # else if statement for the day
                elif dayOrMonth in ("Day", "D", "day", "d"):
                    # change what to updat for the db
                    whatToUpdate = "dayofFestivel"
                    # getting the input from the user
                    updatingInput = int(input('What would you like to Change the month to(1-31)? '))
                    # Checking the input from the user
                    checkDay = checkDayInput(updatingInput)
                    # if statement after checking input
                    if checkDay == True:
                        # making sure they want to change the day
                        goOn = areYouSure()
                    else:
                        # setting goOn to no and telling the user their input was incorrect
                        goOn = "No"
                        print("The Day must be between 1-31")
                # iF user doesn't pick month or day
                else:
                    print("Please pick month or day")

            # if statement to commit the changes or not
            if goOn == "Yes":
                # sending the information to the db
                cur.execute("Update FestivalDates set {} = ?  where placeOfFestival = ?".format(whatToUpdate), (updatingInput, whichToUpdate))
                # printing out the results for the user
                print("{} what updated {} to {}".format(whichToUpdate, whatToUpdate, updatingInput,))
                # Saving it to the database
                db.commit()
            else:
                # telling the user it wasn't sent to the db
                print("{} was not updated".format(whichToUpdate),)
        else:
            # if the table returns a none this is printed for the user
            print('Festival is not in the record')


        main()

    except ValueError:
        print("Needs to be a number")
        update_date()

def merchandise_for_festival():
    whichToAddMerch = input("What Festival do you want to add mearchandise to? ")
    whichToAddMerch = toFormatInput(whichToAddMerch)
    festivalDay = cur.execute("select * from FestivalDates where placeOfFestival = ?", (whichToAddMerch,))
    checkOutput = festivalDay.fetchone()
    print(checkOutput)

    if checkOutput != None:


        howManyItems = int(input("How many items are going to be there? "))
        i = 0
        while i < howManyItems:
            nameOfItem = input("Name of Item? ")
            numberOfItems = int(input("Number of " + nameOfItem + " ? "))
            priceOfItem = float(input("Price for " + nameOfItem + " ? "))

            cur.execute('Insert into {} values (?, ? , ?) '.format(whichToAddMerch,),(nameOfItem,numberOfItems, priceOfItem,))
            i += 1

            db.commit()

        for row in cur.execute('select * from {}'.format(whichToAddMerch,)):
            print(row)

        main()



    else:
        print("Festivel not in the records")
        main()

def view_merch_for_fest():
    whichFestMerch = input("What Festival do you want to view merch for? ")
    whichFestMerch = toFormatInput(whichFestMerch)
    festivalDay = cur.execute("select * from FestivalDates where placeOfFestival = ?", (whichFestMerch,))
    checkOutput = festivalDay.fetchone()
    print(checkOutput)
    if checkOutput != None:
        whichFestMerch = whichFestMerch.replace(" ", "")
        for row in cur.execute('select * from {}'.format(whichFestMerch,)):
            print(row)
        main()
    else:
        print("There is no Festivel")
        main()

    # for row in cur.execute('select * from {}'.format(whichFestMerch,)):
    #     print(row)

def delete_date():
    whichToDelete = input('!!! What Festival To Delete? !!! ')
    whichToDelete = toFormatInput(whichToDelete)
    festivalDay = cur.execute("select * from FestivalDates where placeOfFestival = ?", (whichToDelete,))
    checkOutput = festivalDay.fetchone()
    print(checkOutput)

    if checkOutput != None:
        goOn = areYouSure()
        if goOn == "Yes":
            cur.execute('DELETE FROM FestivalDates WHERE placeOfFestival = ?', (whichToDelete,))
            print("Recorded deleted")
            main()

        else:
            print("record not deleted")
            main()

    else:
        print('Festival is not in the record')
        main()

def restart_festival_dates():
    # this is a hidden option to reset the db back to the beginning
    try:
        # making sure they want to reset the database
        reset_record = input('Would you like to restart the record? Y or N ')

        # if statement to reset the db or not
        if reset_record in ('Y', 'y'):
            # deleting all the tables made for each festivel
            for row in cur.execute('select placeOfFestival from FestivalDates'):
                # joining the truple
                table = "".join(row)
                # formating the string to what the tables are
                table = table.replace(",", "").replace(" ","")
                # dropping the table
                cur.execute('DROP TABLE IF EXISTS {}'.format(table),)

            cur.execute('DROP TABLE IF EXISTS FestivalDates')# deleting table

            # commiting to the db
            db.commit()

            #create table
            cur.execute('create table FestivalDates (placeOfFestival text not null unique, monthOfFestival int, dayofFestivel int)')
            cur.execute('Insert into FestivalDates values ("Civic Center", 1 , 31) ')
            cur.execute("create table IF NOT EXISTS 'CivicCenter' (nameOfItem text, howManyItems int, price int)")

            db.commit() #save changes

            # printing the record for the user
            for row in cur.execute('select * from FestivalDates'):
                print(row)

            main()

        else:
            print('Did not reset the db')
            main()

    # error handling if there is a problem and roll back the db
    except sqlite3.Error as e:

        print('rolling back changes because of error:', e)
        db.rollback()

def checkMonthInput(whichMonth):
    if whichMonth >= 1 and whichMonth <= 12:
        return True
    else:
        return False

def checkDayInput(whichDay):
    if whichDay >=1 and whichDay <= 31:
        return True
    else:
        return False


def toFormatInput(festival):
    festival =  festival.lower().title()
    return festival

def areYouSure():
    areYouSure = input('Are You Sure you want to continue?')
    if areYouSure in ('Y', 'y', 'Yes'):
        return "Yes"
    else:
        return "No"


# calling the main program
if __name__ == '__main__':
    main()
