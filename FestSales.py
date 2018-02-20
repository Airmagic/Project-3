import sqlite3
import traceback

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
    elif choice == '6':
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
        3. Search for Date
        4. Update Date
        5. Delete Date
        q. Quit
    ''')

def festival_date():
    orderList = input("Would you like the list by Date(D) or Name(N)? ")

if orderList in ("Name", "N", "name", "n"):
    for row in cur.execute('select * from recordHolder ORDER BY personsName '):
        print(row)

def restart_festival_dates():
    # this is a hidden option to reset the db back to the beginning
    try:
        making sure they want to reset the database
        reset_record = input('Would you like to restart the record? Y or N ')

        # if statement to reset the db or not
        if reset_record in ('Y', 'y'):
            cur.execute('drop table recordHolder')# deleting table
            db.commit()

            #create table
            cur.execute('create table FestivalDates (placeOfFestival text, monthOfFestival int, dayofFestivel)')
            cur.execute('Insert into FestivalDates values ("Civic Center", 01 , 31) ')
            cur.execute('Insert into FestivalDates values ("Energy Center", 02, 28) ')
            cur.execute('Insert into FestivalDates values ("Time Square", 03, 04) ')



            #add some

            # cur.execute('insert into recordHolder values (?, ?, ?)', (personsName, country, catches))

            db.commit() #save changes


            for row in cur.execute('select * from FestivalDates'):
                print(row)

            main()
        else:
            print('Did not reset the db')
            main()

    # error handling if there is a problem and roll back the db
    except sqlite3.Error as e:

        print('rolling back changes because of error:', e)
        traceback.print_exe() #displays a stack trace, for debugging
        db.rollback()


# calling the main program
if __name__ == '__main__':
    main()
