'''  
      RRS ( RAILWAY RESERVATION SYSTEM ) 
''' 
 
# --- Importing Built-in Modules/Functions ----# 
import mysql.connector 
import time 
from random import randint 
from datetime import datetime 
 
#---- CREATING DATABASE -----------------# 
 
 
def create_database(): 
    try: 
        # Connection to MySQL 
        conn = mysql.connector.connect( 
            host="localhost",       
            user="root",           # Your MySQL username 
            password="passwd"    # Your MySQL password 
        ) 
        cursor = conn.cursor() 
 
        # Create database if not exists 
        cursor.execute("CREATE DATABASE IF NOT EXISTS RailwayReservationSystem") 
        cursor.execute("USE RailwayReservationSystem") 
 
        # Create table if not exists 
        create_table = ''' 
        CREATE TABLE IF NOT EXISTS RESERVATIONS ( 
            PNR INT PRIMARY KEY, 
            USERNAME VARCHAR(50), 
            ORIGIN VARCHAR(50), 
            DESTINATION VARCHAR(50), 
            DATE DATE, 
            TRAIN VARCHAR(100), 
            CLASS VARCHAR(20), 
            SEATS VARCHAR(10), 
            NAME_OF_PASSENGERS TEXT, 
            FOOD VARCHAR(50), 
            TOTAL_COST DECIMAL(10, 2) 
        ) 
        ''' 
        cursor.execute(create_table) 
 
        # Commit the changes 
        conn.commit() 
 
    except mysql.connector.Error as err: 
        print(f"Error: {err}") 
    finally: 
        if conn.is_connected(): 
            cursor.close() 
            conn.close() 
 
create_database() 
 
 
 
# MAIN PYTHON PROGRAM ===================================================== 
 
print(''' 
               WELCOME TO RAILWAY RESERVATION SYSTEM (RRS) 
 
        You can book railway tickets in minutes with this program. 
 
Guidelines: 
1. While booking ticket, make sure you input the username and remember it! 
   Username will play an important role in operation of this program. 
2. Make sure you enter the information for booking the tickets very 
carefully. 
   If you enter invalid choices, then the program will terminate for 
   security concerns! 
 
''') 
 
# Database connection 
def connect_to_db(): 
    try: 
        connection = mysql.connector.connect( 
            host="localhost", 
            user="root",  # Replace with your MySQL username 
            password="Database",  # Replace with your MySQL password 
            database="RailwayReservationSystem" 
        ) 
        if connection.is_connected(): 
            return connection 
    except mysql.connector.Error as err: 
        print(f"Error: {err}") 
        return None 
 
# Close the database connection 
def close_connection(connection): 
    if connection.is_connected(): 
        connection.close() 
 
 
# Reserve a ticket function 
 
# Constants  
train_costs = { 
    "Rajdhani Express (12925)": 500, 
    "Double Decker Express (12420)": 250, 
    "Vande Bharat Express (12250)": 555, 
    "Duronto Express (12050)": 200, 
    "Gujarat Mail (12743)": 200, 
    "Humsafar Express (12697)": 150, 
    "Festival Special Express (01969)": 100 
} 
 
class_costs = { 
    "AC 1 Tier": 500, 
    "AC 2 Tier": 300, 
    "AC 3 Tier": 250, 
    "AC Chair Car": 200, 
    "Sleeper": 150 
} 
 
food_costs = { 
    "Veg Thali": 250, 
    "Non-Veg Thali": 300 
} 
 
 
 
def reserve_ticket(): 
    connection = connect_to_db() 
    if connection is None: 
        print("Failed to connect to the database. Exiting...") 
        return 
 
    cursor = connection.cursor() 
 
    # 1. Ask for Username 
    username = input("Enter your username: ") 
 
    # 2. Ask for Origin (20 stations) 
    stations = [ 
        " Mumbai", " Delhi", " Bangalore", " Hyderabad", " Ahmedabad", 
        " Surat", " Vadodara", " Rajkot", " Gandhinagar", " Pune", 
        "Chennai", "Kolkata", "Jaipur", "Lucknow", "Indore", 
        "Bhopal", "Chandigarh", "Nagpur", "Thane", "Vapi" 
    ] 
    print("Select Origin Station:") 
    for idx, station in enumerate(stations, start=1): 
        print(f"{idx}. {station}") 
    for i in range(5):   
        origin_choice = int(input("Enter the serial no. for origin (1 to 20): "))   
        if 1 <= origin_choice <= 20:   
            print("Valid choice!") 
            break   
        else: 
            print("Invalid choice! Please input the correct serial no. from the list (1 to 20)!") 
    else: 
        print("Too many invalid attempts!")  
 
         
    origin = stations[origin_choice - 1] 
 
    # 3. Ask for Destination (same list excluding origin) 
    print("Select Destination Station:") 
    available_destinations = [station for station in stations if station != origin] 
    for idx, station in enumerate(available_destinations, start=1): 
        print(f"{idx}. {station}") 
    destination_choice = int(input("Enter the number of your Destination Station: ")) 
    destination = available_destinations[destination_choice - 1] 
 
    # 4. Ask for Date 
 
    for i in range(5):   
        travel_date = input("Enter your travel date (YYYY-MM-DD): ") 
        try: 
            travel_date = datetime.strptime(travel_date, "%Y-%m-%d").date() 
            print("Valid date!") 
            break   
        except ValueError: 
            print("Invalid date format. Please enter in YYYY-MM-DD format.") 
    else: 
        print("Too many invalid attempts!")   
 
 
    # 5. Ask for Train
    trains = {
        "1": "Rajdhani Express (12925)",
        "2": "Double Decker Express (12420)",
        "3": "Vande Bharat Express (12250)",
        "4": "Duronto Express (12050)",
        "5": "Gujarat Mail (12743)",
        "6": "Humsafar Express (12697)",
        "7": "Festival Special Express (01969)"
    }
    print("Select Train:")
    for key, value in trains.items():
        print(f"{key}. {value}")
    train_choice = input("Enter the serial number of your preferred train: ")
    train = trains.get(train_choice, "Invalid choice")

    if train == "Invalid choice":
        print("Invalid train selection.")
        return

    # 6. Ask for Class
    classes = ["AC 1 Tier", "AC 2 Tier", "AC 3 Tier", "AC Chair Car", "Sleeper"]
    print("Select Class:")
    for idx, class_type in enumerate(classes, start=1):
        print(f"{idx}. {class_type}")
    class_choice = int(input("Enter the number of your preferred class :"))
    travel_class = classes[class_choice - 1]

    # 7. Display Seat Layout and Ask for Seat
    seat_layout = """
 ______________     
/              \ 
|========  ====|
|[ 1][ 2]  [ 5]| 
|[ 3][ 4]  [ 6]| 
|========  ====|
|[ 7][ 8]  [11]|
|[ 9][10]  [12]|
|========  ====|
|[13][14]  [17]|
|[15][16]  [18]|
|========  ====|      
|[19][20]  [23]| 
|[21][22]  [24]| 
|========  ====|
|[25][26]  [29]| 
|[27][28]  [30]| 
|========  ====|
|[31][32]  [35]| 
|[33][34]  [36]| 
|========  ====|
|[37][38]  [41]| 
|[39][40]  [42]| 
|========  ====|
|[43][44]  [47]| 
|[45][46]  [48]| 
|========  ====|
\______________/ 
"""
    print(seat_layout)
    selected_seat = input("Enter seat number to select (comma-separated):")
    num_commas = selected_seat.count(',')
    num_seats= num_commas+1
    
    # 8. Ask for Name of Passengers
    passenger_names = input("Enter passenger names (comma-separated):")

    # 9. Ask for Food Option
    food_options = ["Veg Thali", "Non-Veg Thali"]
    print("Select Food Option:")
    for idx, option in enumerate(food_options, start=1):
        print(f"{idx}. {option}") 
    food_choice = int(input("Enter the number of your food option :")) 
    food = food_options[food_choice - 1] 
 
    # calculating cost: 
    train_cost = train_costs[train] 
    class_cost = class_costs[travel_class] 
    food_cost = food_costs[food] 
    total_cost = (train_cost + class_cost + food_cost) * num_seats 
    gst = total_cost * 0.18  # 18% GST 
    total_cost_with_gst = total_cost + gst 
 
 
    # 10. Preview Ticket and Ask for Confirmation 
    print("\n=-=-=-=-=-= TICKET PREVIEW =-=-=-=-=-=-=-=-=") 
    print() 
    print(f"Username: {username}") 
    print(f"Origin: {origin}") 
    print(f"Destination: {destination}") 
    print(f"Date: {travel_date}") 
    print(f"Train: {train}") 
    print(f"Class: {travel_class}") 
    print(f"Seat: {selected_seat}") 
    print(f"Passengers: {passenger_names}") 
    print(f"Food: {food}") 
    total_cost = 1500.00  # Placeholder cost; you can calculate this based on class and food choices 
    print(f"Total Cost with GST: ₹{total_cost_with_gst:.2f}") 
 
    confirm = input("Do you want to confirm this reservation? (yes/no) :").lower() 
    if confirm != 'yes': 
        print("Reservation cancelled.") 
        return 
 
    # 11. Generate 5-digit PNR and Save to Database
    pnr = randint(10000, 99999)
    try:
        cursor.execute("""
            INSERT INTO RESERVATIONS (PNR, USERNAME, ORIGIN, DESTINATION, DATE, TRAIN, CLASS, SEATS, NAME_OF_PASSENGERS, FOOD, TOTAL_COST)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (pnr, username, origin, destination, travel_date, train, travel_class, selected_seat, passenger_names, food, total_cost))
        connection.commit()
        print("-------------------------------------------")
        print(f"Reservation successful! Your PNR is: {pnr}|")
        print("-------------------------------------------")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    cursor.close()
    close_connection(connection)






# FUNCTION TO VIEW RESERVATIONS FROM A USERNAME------------------
def view_all_reservations():
    connection = connect_to_db()
    if connection is None:
        print("Failed to connect to the database. Exiting...")
        return

    cursor = connection.cursor()

    # 1. Ask for Username
    username = input("Enter the username to view reservations :")

    # 2. Fetch Reservations for the Username
    try:
        cursor.execute("SELECT * FROM RESERVATIONS WHERE USERNAME = %s", (username,))
        reservations = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

    # 3. Display Reservations
    if not reservations:
        print(f"No reservations found for username '{username}'.")
    else:
        print("\n=-=-=-= RESERVATIONS =-=-=-=")
        for row in reservations:
            print(f"PNR: {row[0]}")
            print(f"Username: {row[1]}")
            print(f"Origin: {row[2]}")
            print(f"Destination: {row[3]}")
            print(f"Date: {row[4]}")
            print(f"Train: {row[5]}")
            print(f"Class: {row[6]}")
            print(f"Seats: {row[7]}")
            print(f"Passengers: {row[8]}")
            print(f"Food: {row[9]}")
            print(f"Total Cost: {row[10]}")
            print("==============================")
            print()
            time.sleep(2)

    cursor.close()
    close_connection(connection)


#FUNCTION TO CHECK PNR STATUS:
def check_pnr_status():
    connection = connect_to_db()
    if connection is None:
        print("Failed to connect to the database. Exiting...")
        return

    cursor = connection.cursor()

    # 1. Ask for PNR Number
    pnr = input("Enter your PNR number :")

    # 2. Fetch Reservation Details
    try:
        cursor.execute("SELECT * FROM RESERVATIONS WHERE PNR = %s", (pnr,))
        reservation = cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

    # 3. Display Reservation Details
    if reservation is None:
        print(f"No reservation found for PNR '{pnr}'.")
    else:
        print("\n=-=-=-= RESERVATION DETAILS =-=-=-=-=-=-=")
        print(f"PNR: {reservation[0]}")
        print(f"Username: {reservation[1]}")
        print(f"Origin: {reservation[2]}")
        print(f"Destination: {reservation[3]}")
        print(f"Date: {reservation[4]}")
        print(f"Train: {reservation[5]}")
        print(f"Class: {reservation[6]}")
        print(f"Seats: {reservation[7]}")
        print(f"Passengers: {reservation[8]}")
        print(f"Food: {reservation[9]}")
        print(f"Total Cost: {reservation[10]}")
        print("-------------------------------------------")

    cursor.close()
    close_connection(connection)


# FUNCTION TO CANCEL TICKET
def cancel_reservation():
    connection = connect_to_db()
    if connection is None:
        print("Failed to connect to the database. Exiting...")
        return

    cursor = connection.cursor()

    # 1. Input PNR Number
    pnr = input("Enter the PNR number of the ticket to be canceled :")

    # 2. Verify Username
    username = input("Enter the username associated with the PNR :")

    # 3. Check and Delete Reservation
    try:
        # Fetch the reservation details
        cursor.execute("SELECT * FROM RESERVATIONS WHERE PNR = %s", (pnr,))
        reservation = cursor.fetchone()

        if reservation is None:
            print(f"No reservation found for PNR '{pnr}'.")
            return

        if reservation[1] != username:
            print("Username does not match with this PNR. Cancellation denied.")
            return

        # Display the canceled ticket details
        print("\n=-=-=-=-= CANCELLED TICKET =-=-=-=-=-=-=")
        print()
        print(f"PNR: {reservation[0]}")
        print(f"Username: {reservation[1]}")
        print(f"Origin: {reservation[2]}")
        print(f"Destination: {reservation[3]}")
        print(f"Date: {reservation[4]}")
        print(f"Train: {reservation[5]}")
        print(f"Class: {reservation[6]}")
        print(f"Seats: {reservation[7]}")
        print(f"Passengers: {reservation[8]}")
        print(f"Food: {reservation[9]}")
        print(f"Total Cost: {reservation[10]}")
        print()
        print("------------------------------------------")

        # Proceed to delete the reservation
        cursor.execute("DELETE FROM RESERVATIONS WHERE PNR = %s", (pnr,))
        connection.commit()
        print("Reservation successfully canceled.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        close_connection(connection)




# --------------- MAIN MENU PROGRAM -----------------------#
def main_menu():
    loop=True
    while loop==True:
        print("\n====== Railway Reservation System ======")
        print()
        print(" 1. Reserve a Ticket")
        print("  2. View all Reservations")
        print("   3. Check PNR Status")
        print("    4. Cancel Reservation")
        print("     5. Exit the System") 
        print('')
        choice = input("Enter your choice (1-5) :")
        
        if choice == '1':
            print()
            reserve_ticket()
            print()
        elif choice == '2':
            print()
            view_all_reservations()
            print()
        elif choice == '3':
            print()
            check_pnr_status()
            print()
        elif choice == '4':
            print()
            cancel_reservation()
            print()
        elif choice == '5':
            loop=False
            print()
            print("THANK YOU FOR USING RAILWAY RESERVATION SYSTEM !!!")
            time.sleep(5)
            print()
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()


# ======= END OF PROGRAM =======
 
''' 
 THIS COMPLEX PROGRAM CONSITING 465 LINES OF CODE
 WAS MADE IN A EFFORT TO ADD ADDITIONAL FEATURES IN TRAIN 
 RESERVATIONS LIKE SEAT SELECTION AND EASIER TICKET BOOKING''' 
