from time import sleep
from db_utils import mycursor


def print_ticket_on_console(myresult, pnr):
    print('-------------------------------------------------------------------------------------------------')
    print('pnr         TRAIN_NO       TRAIN_NAME     DATE JOURNEY       DEPARTURE     ARRIVAL       STATUS')
    print('-------------------------------------------------------------------------------------------------')
    for x in myresult:
        print(*x, sep='        ')
    print('-------------------------------------------------------------------------------------------------\n')

    sql_query = "SELECT pass_no,passenger_name,age,gender FROM ticket_details where pnr=" + pnr
    mycursor.execute(sql_query)
    myresult = mycursor.fetchall()

    print('PASSENGER No.     NAME     AGE     GENDER')
    for x in myresult:
        print(*x, sep='               ')
    print('-------------------------------------------------------------------------------------------------\n')


def is_correct_format(pnr):
    try:
        int(pnr)
    except Exception as ex:
        return False

    return True


def fetch_pnr_details(pnr):
    sql_query = """
    SELECT ticket_master.pnr,train_master.TRAIN_no,train_master.TRAIN_NAME,ticket_master.date_journey,train_master.DEPARTURE_STATION,train_master.SOURCE_STATION ,ticket_master.ticket_status 
    FROM ticket_master 
    INNER JOIN train_master ON ticket_master.TRAIN_NO=train_master.train_no 
    where pnr=""" + pnr
    mycursor.execute(sql_query)
    myresult = mycursor.fetchall()
    return myresult


def VIEW_TICKET(G_PNR):
    pnr = str(input('\nENTER pnr NO:'))

    # check format
    correct_pnr = is_correct_format(pnr)
    if not correct_pnr:
        print("Incorrect pnr FORMAT")
        VIEW_TICKET(G_PNR)
        return

    # check pnr present in db or not
    myresult = fetch_pnr_details(pnr)
    if len(myresult) == 0:
        print("No data present")
        VIEW_TICKET(G_PNR)
        return

    print_ticket_on_console(myresult, pnr)

    G_PNR = pnr
    sleep(2)

    return G_PNR
