import sqlite3
# import traceback

# pointing to the db file
db = sqlite3.connect('FestSales.db')# creates or opens db files

# making variable for accessing the db
cur = db.cursor() #need a cursor object to perform operations

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

    # 5. Deleting a record from the table
    elif choice == '5':
        delete_date()

    # 6. Restarting the record from basic
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
        4. Update Festival Info
        5. Delete Festival Info
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
        festivelName = input("Enter the Name of the Festival: ")
        festivelName = toFormatInput(festivelName)
        whichMonth = int(input("What month is the festivel(1-12): "))
        checkMonth = checkMonthInput(whichMonth)
        whichDay = int(input("What day is the festivel(1-31): "))
        checkDay = checkDayInput(whichDay)

        if checkMonth == True:
            if checkDay == True:
                cur.execute('insert into FestivalDates values (?, ?, ?)', (festivelName, whichMonth, whichDay))
                db.commit() #save changes
            else:
                print("Please have the days from 1-31")
                add_new_date()
        else:
            print("Please have the months from 1-12")
            add_new_date()
        main()

    except ValueError:
        print("Needs to be a number")
        add_new_date()

def search_for_date():
    try:
        dateMonthSearch = int(input("What Month are you searching for?(1-12) "))
        dateDaySearch = int(input("What Day are you searching for? (1-31) "))

        festivalDay = cur.execute("select * from FestivalDates where monthOfFestival = ? and dayofFestivel = ?" , (dateMonthSearch, dateDaySearch,))
        print(festivalDay.fetchone())
        # calling the main
        main()
    except ValueError:
        print("Needs to be a number")
        search_for_date()

def update_date():
    try:
        whichToUpdate = input('What Festival To update? ')
        whichToUpdate = toFormatInput(whichToUpdate)
        festivalDay = cur.execute("select * from FestivalDates where placeOfFestival = ?", (whichToUpdate,))
        checkOutput = festivalDay.fetchone()
        print(checkOutput)

        if checkOutput != None:
            print("What would you like to change/update")
            whatToUpdate = input("Festival Name(N) or Date(D) ")

            if whatToUpdate in ('Name', 'N', 'name', 'n'):
                whatToUpdate = "placeOfFestival"
                updatingInput = input('What would you like to Change the name to? ')
                updatingInput = toFormatInput(updatingInput)
                countinue = areYouSure()


            if whatToUpdate in ('Date', 'D', 'date', 'd'):
                dayOrMonth = input("Do you want to change month(m) or day(d)? ")
                if dayOrMonth in ("Month", "month", "M", "m"):
                    whatToUpdate = "monthOfFestival"
                    updatingInput = int(input('What would you like to Change the month to(1-12)? '))
                    checkMonth = checkMonthInput(updatingInput)
                    if checkMonth == True:
                        countinue = areYouSure()
                    else:
                        countinue = "No"
                        print("The Month has to be between 1-12")

                elif dayOrMonth in ("Day", "D", "day", "d"):
                    whatToUpdate = "dayofFestivel"
                    updatingInput = int(input('What would you like to Change the month to(1-31)? '))
                    checkDay = checkDayInput(updatingInput)
                    if checkDay == True:
                        countinue = areYouSure()
                    else:
                        countinue = "No"
                        print("The Day must be between 1-31")

                else:
                    print("Please pick month or day")

            if countinue == "Yes":
                cur.execute("Update FestivalDates set {} = ?  where placeOfFestival = ?".format(whatToUpdate), (updatingInput, whichToUpdate))
                print("{} what updated {} to {}".format(whichToUpdate, whatToUpdate, updatingInput,))
            else:
                print("{} was not updated".format(whichToUpdate),)
        else:
            print('Festival is not in the record')


        main()

    except ValueError:
        print("Needs to be a number")
        update_date()

def restart_festival_dates():
    # this is a hidden option to reset the db back to the beginning
    try:
        # making sure they want to reset the database
        reset_record = input('Would you like to restart the record? Y or N ')

        # if statement to reset the db or not
        if reset_record in ('Y', 'y'):
            cur.execute('DROP TABLE IF EXISTS FestivalDates')# deleting table
            db.commit()

            #create table
            cur.execute('create table FestivalDates (placeOfFestival text, monthOfFestival int, dayofFestivel int)')
            cur.execute('Insert into FestivalDates values ("Civic Center", 1 , 31) ')
            cur.execute('Insert into FestivalDates values ("Energy Center", 2, 28) ')
            cur.execute('Insert into FestivalDates values ("Time Square", 3, 4) ')



            #add some

            # cur.execute('insert into recordHolder values (?, ?, ?)', (personsName, country, catches))

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
        # traceback.print_exe() #displays a stack trace, for debugging
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
    areYouSure = input('Are You Sure you want to commit these changes?')
    if areYouSure in ('Y', 'y', 'Yes'):
        return "Yes"
    else:
        return "No"


# calling the main program
if __name__ == '__main__':
    main()
