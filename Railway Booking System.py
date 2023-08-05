import mysql.connector
import datetime
from time import sleep

from view_ticket import VIEW_TICKET
# os.system('clear')

from db_utils import mycursor, close_connection

G_PNR = 0
# print(myconn)
print('✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰')

# mycursor.execute("CREATE TABLE passengers (name VARCHAR(255),age VARCHAR(3),gender CHAR(1), phone_number char(10), train_no varchar(6),class varchar(10)")
print(
    '\n✰                                            !!!!  Welcome to Railway services!!!!                                                                                              ✰')
print('\n✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰✰')


def menu():
    #    print('-------------------------------------------------------------------------------------------------')
    print('\n\n#1. Book a Ticket')
    print('#2. View a Ticket')
    print('#3. Train Details')
    print('#4. Cancel a Ticket')
    print('#5. Print a Ticket')
    print('#6. Exit')


def TRAIN_DETAILS():
    sql_query = "select * from train_master "

    mycursor.execute(sql_query)

    myresult = mycursor.fetchall()

    print('-------------------------------------------------------------------------------------------------')
    print('TRAIN_NO      TRAIN_NAME   SOURCE_STATION   DEPARTURE_STATION')
    print('-------------------------------------------------------------------------------------------------')
    for x in myresult:
        print(*x, sep='          ')
    print('-------------------------------------------------------------------------------------------------\n')

    sleep(2)


def reservation():
    print("\n------------PLEASE ENTER THE TICKET DETAILS--------------------")

    checkpoint = 'FALSE'

    while checkpoint == 'FALSE':

        train_no = str(input('Enter your Train Number[Refer list]:'))
        sql_query1 = "Select * from train_master where TRAIN_no=" + train_no
        mycursor.execute(sql_query1)
        mycursor.fetchall()
        if mycursor.rowcount <= 0:
            print('Sorry, incorrect Train Number')

        else:
            checkpoint = 'TRUE'
            continue

    class_ = input('Enter Class(1.AC/2.NON AC)[Enter 1 or 2]:')
    while class_ != '1' and class_ != '2':
        print('Invalid input')
        print('Try again later(This ticket will not be booked')
        class_ = input('Enter Class(1.AC/2.NON AC)[Enter 1 or 2]:')

    phone_no = int(input('Enter your Phone Number:'))
    length_ = len(str(phone_no))
    if length_ != 10:
        print('Invalid Phone number')
        phone_no = int(input('Enter your Phone Number:'))

    x = datetime.datetime.now()
    Date_booking = (x.strftime("%x"))

    JOURNEY_DATE = input('Enter the date of journey(YYYY-MM-DD):')

    x1 = datetime.datetime.now()
    booking_time = (x.strftime("%X"))

    amount = input('Enter your amount:')

    email = input('Enter your E-mail address:')

    sql = "select max(pnr)+1 from ticket_master"
    mycursor.execute(sql)
    myresult1 = mycursor.fetchall()
    for x in myresult1:
        print(x)
        #        pnr=*x
        try:
            sql = "INSERT INTO ticket_master (pnr,phone_number, train_no,class,date_booking,date_journey,booking_time,amount,email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (*x, phone_no, train_no, class_, Date_booking, JOURNEY_DATE, booking_time, amount, email)
            mycursor.execute(sql, val)
            myconn.commit()
            print(mycursor.rowcount, "record inserted.")

        except mysql.connector.Error as e:
            print('DB exception: %s' % e)
            return

    print("------------PLEASE ENTER THE PASSENGER DETAILS--------------------")

    tickets = int(input('\nEnter no. of passengers:'))
    for i in range(tickets):

        if tickets > 6:
            print(
                'Sorry, you have exceeded the maximum booking limit of 6.To book more tickets, please try in the next slot')
            break

        else:
            pass_no = i + 1
            name = str(input('Enter your Full Name:'))
            #            name_l.append(name)
            age = int(input('Enter your Age:'))
            #            age_l.append(age)

            gender = str(input('Enter your Gender(1.Male/2.Female)[Enter M or F]:'))
            if gender != 'M' and gender != 'F':
                print('Invalid Input')
                print('Please try again later(This ticket will not be booked)')
                i = i - 1

        sql = "INSERT INTO ticket_details (pnr,pass_no,passenger_name,age,gender) VALUES (%s, %s, %s, %s, %s)"
        val = (*x, pass_no, name, age, gender)
        mycursor.execute(sql, val)
        myconn.commit()
        print(mycursor.rowcount, "record inserted.")
        continue


def cancelltaion():
    l_PNR = VIEW_TICKET(G_PNR)

    ans = str(input("Do You Cancel The Ticket Y/N)"))
    print(ans)
    if ans != 'Y' and ans != 'N':
        print('Invalid inpt')
        print('Try again later(This ticket will not be booked')
    if ans == 'N':
        print("OK")
        master()
    ans1 = str(input("Do You Want To Cancel For all passengers?(Y/N) )"))
    if ans1 == 'Y':
        t_PNR = str(l_PNR)
        sql = "UPDATE ticket_details SET ticket_status = 'C' WHERE pnr =" + t_PNR
        mycursor.execute(sql)
        sql = "UPDATE ticket_master SET ticket_status = 'C' WHERE pnr =" + t_PNR
        mycursor.execute(sql)
        myconn.commit()
        myresult1 = mycursor.fetchall()
        for x in myresult1:
            print(x)
    if ans1 == 'N':
        ans2 = int(input("For how many passenger you want to cancel to ticket"))
        for i in range(ans2):
            ans3 = int(input('enter the pass_no for you want to delete the ticket'))
            t_PNR = str(l_PNR)

            sql = "UPDATE ticket_details SET ticket_status = 'C' WHERE pnr = " + t_PNR + " and pass_no = " + str(ans3)
            mycursor.execute(sql)
            myconn.commit()
            print("TICKET CANCELLED")
        master()


'''def PRINT_TICKET():
    from win32 import win32print
    print('PRINTING DONE')
    p = win32print.OpenPrinter(EPSON_L3150_SERIES)
    job = win32print.StartDocPrinter(p,1,("test of raw data", None, "RAW"))
    win32print.StartPagePrinter(p)
    win32print.WritePrinter(p,"data to print")
    win32print.EndPagePrinter(p)'''


def master():
    menu()
    inp = input('\nEnter your choice(Only numbers from the choice above): ')
    a = str(inp)
    if a == '1':
        reservation()
        master()
    elif a == '2':
        VIEW_TICKET(G_PNR)
        master()
    elif a == '3':
        TRAIN_DETAILS()
        master()
    elif a == '4':
        cancelltaion()
    elif a == '5':
        pass
        # PRINT_TICKET()
    elif a == '6':
        print('Thank You')
        close_connection()
    else:
        print('Invalid Choice')
        master()


master()

"""
if __name__ == "__main__":
    master()
"""
