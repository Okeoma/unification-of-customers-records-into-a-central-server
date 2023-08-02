# Please Note: Before you start running the program, all the four initial input files, 
# that is; userdata for JSON, XML, CSV and TXT files should remain in the data folder 
# and the data folder placed in a folder with this .py script. Thank you.
welcome_screen = ('''
==========================================================================================
                            LAUREL TECHNOLOGY SOLUTIONS LTD
==========================================================================================
An ETL program that extracts Laurel's customer data split across various systems, wrangles 
and transforms them to a singular format and finally pushes them into a central data store
------------------------------------------------------------------------------------------
The program will unify three major data formats and information areas:
    o   JSON    -   Customers Credit Card records
    o   XML     -   Customers Employment records
    o   CSV     -   Customers Vehicle records
------------------------------------------------------------------------------------------
The program also performs data investigation, exploitation and updating records based on
specified tasks in a TEXT file and finally pulls the data into a central database server    
==========================================================================================
Press ENTER to start the program: ''')

# Importing libraries 
from xml.etree import ElementTree
import sqlite3
import json
import csv
import os
# Libraries required for phpMyAdmin connection
from pony.orm import *
import webbrowser
db = Database() # Create database object

# Connection details
provider = 'mysql'
host = 'europa.ashley.work'
user = 'student_bi24yz'
password = 'iE93F2@8EhM@1zhD&u9M@K'
database = 'student_bi24yz'

# Regular used prompts and messages
go_back = "Press ENTER to go back to main menu: "
success = "========================== All operations completed successfully ========================="
failure = "(: Something went wrong along the line!"
csv_created = "==================================== CSV file created ===================================="
continue_program = "Press 'ENTER' to continue to the next operation or 'CTL+C and ENTER' to go back: "
line = "------------------------------------------------------------------------------------------"
operation_done = "==================================== Operation complete ===================================="

# Main menu function 
def menu_choice():
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    print(line)
    
    menu = int(input('''Select the option number (Please start from the top to the bottom):
    1 - Process Credit Card records (JSON)
    2 - Process Employment records (XML)
    3 - Process Vehicle records (CSV)
    4 - Convert all three CSV tables to SQL database
    5 - Merge all three tables in SQL
    6 - Convert merged SQL data to CSV
    7 - Perform operations on data and update
    8 - Convert updated merged SQL data to CSV
    9 - Connect to central database server
    0 - Exit
    : '''))
    print(line)
    return menu

# Function to check and create output file path
def output_path(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        except OSError as exc: # Guard against race condition
            print("There is a problem with the csv file. Please close file if open!")   
            exit()
    return file_path

# Function to read json file
def read_json(filename):
    return json.loads(open(filename).read())

# Function to write json to csv file
def write_json_to_csv(data, filename):
    with open(filename, 'w+', encoding='utf-8', newline='') as outf:
        writer = csv.writer(outf)
        writer.writerow(data[0].keys())
        for row in data:
            writer.writerow(row.values())            
    print(csv_created)

# Function to convert Json to CSV
def convert_json():    
    input_file = "data/user_data.json"          # json input file path
    output_file = "output/json/json_data.csv"   # csv file path after conversion 

    # Prepare output path
    output_file = output_path(output_file)
    # Converts input to csv and then saves the file
    write_json_to_csv(read_json(input_file), output_file)

# Function to check input file path and return it
def check_inputfile(file_path):
    try:
        return file_path
    except:
        print("Please create the input csv file first!")   
        exit()

# Function to clean csv file
def clean_csv(input_file, output_file):
    with open(input_file) as instream:
        # Setup the input
        reader = csv.DictReader(instream)
        rows = list(reader)
        # Setup the output fields
        output_fields = reader.fieldnames      
        

    with open(output_file, "w+", newline='') as outstream:
        # Setup the output
        writer = csv.DictWriter(
            outstream,        
            fieldnames=output_fields,
            extrasaction="ignore",  # Ignore extra dictionary keys/values
        )

        # Write to the output
        writer.writeheader()
        writer.writerows(rows)        
        print("==================================== CSV file cleaned ====================================")            

# Function to clean csv data
def clean_data(input_file, output_file):
    input_file = check_inputfile(input_file)
    try:
        clean_csv(input_file, output_file)
    except OSError as exc: # Guard against race condition
        print("There is a problem with the output file")   
        exit()

# Function to clean csv header
def clean_header(cleaned_input_file):
    with open(cleaned_input_file) as instream:
        # Setup the input
        reader = csv.DictReader(instream)         
        # Setup the output fields
        output_fields = reader.fieldnames
        new_fields = []             

        for field in output_fields:
            field = field.replace("_", " ")
            field = field.title()  
            if field == "First Name":
                field = "Firstname"          
            elif field == "Second Name":
                field = "Lastname"          
            elif field == "Age (Years)":
                field = "Age"
            field = field.replace(" ", "")
            new_fields.append(field)    
           
    print("=================================== CSV Header cleaned ===================================")
    return new_fields

# Function to process the cleaned header and combine with records 
def process_csv(header):
    with open(cleaned_input_file) as rf, open(temp_file, "w", newline ="") as wf:  
        write_header = csv.writer(wf)
        write_header.writerow(header)
        for i, line in enumerate(rf):
            if i != 0:    
                wf.write(line)
    os.replace(temp_file, cleaned_input_file)

# Funtion to tie all csv cleaning process together
def process_csvtable(cleaned_input_file):
    header = clean_header(cleaned_input_file)
    print(header)
    process_csv(header)

# Function to open csv in excel
def launch_csv(file_loc):
    try:
        # Get working directory 
        path = os.getcwd()
        # Only opens if run on windows
        if os.name == "nt":
            os.startfile(path + file_loc)
            print("...Opening CSV file in Excel ============>>>")
        else:
            subprocess.call(("open", path + file_loc))            
    except:
        print("Error: Unable to open file!")

# Function to parse xml file
def read_xml(filename):
    return ElementTree.parse(filename)

# Function that converts a parsed xml to csv
def write_xml_to_csv(data, filename):
    # create csv file
    with open(filename,'w+',encoding='utf-8', newline='') as outf:
        writer = csv.writer(outf)

        # Add the header to csv
        writer.writerow(["firstName", "lastName", "age",
                        "sex","retired", "dependants",
                        "marital_status", "salary" , "pension" ,
                        "company" ,"commute_distance" ,"address_postcode" ])

        # Looping through each user
        for user in data.findall("user"):
            
            # Extract employee details
            firstName = user.get("firstName")
            lastName = user.get("lastName")
            age = user.get("age")
            sex = user.get("sex")
            retired = user.get("retired")
            dependants = user.get("dependants")
            marital_status = user.get("marital_status")
            salary = user.get("salary")
            pension = user.get("pension")
            company = user.get("company")
            commute_distance = user.get("commute_distance")
            address_postcode = user.get("address_postcode")	  
            
            csv_line = [firstName, lastName, age,
                        sex, retired, dependants,
                        marital_status, salary, pension,
                        company, commute_distance, address_postcode]
            
            # Adds a new row to the csv file
            writer.writerow(csv_line)
        print(csv_created)

# Function to convert xml to csv
def convert_xml():    
    input_file = "data/user_data.xml"         # json input file path
    output_file = "output/xml/xml_data.csv"   # csv file path after conversion 

    # Prepare output path
    output_file = output_path(output_file)
    # Converts input to csv and then saves the file
    write_xml_to_csv(read_xml(input_file), output_file)

# Function to confirm the datatype of each column from an SQL table
def col_datatypes(fin):
    dr = csv.DictReader(fin) # Using comma as a default delimiter
    fieldTypes = {}
    for entry in dr:
        feildslLeft = [f for f in dr.fieldnames if f not in fieldTypes.keys()]        
        if not feildslLeft: break # Job completion
        for field in feildslLeft:
            data = entry[field]

            # Checking the length of data
            if len(data) == 0:
                continue

            if data.isdigit():
                fieldTypes[field] = "INTEGER"
            else:
                fieldTypes[field] = "TEXT"
       
    if len(feildslLeft) > 0:
        raise Exception("Failed to find all the data types for the columns!")
    return fieldTypes

# Function for storing the correct values by encoding and decoding table records
def escaping_generator(f):
    for line in f:
        yield line.encode("ascii", "xmlcharrefreplace").decode("ascii")

# Function for converting csv to sql database
def csv_sql(csvFile, dbFile, tablename):    
    try: 
        con = sqlite3.connect(dbFile)

        with open(csvFile,'r', encoding="ISO-8859-1") as fin:
            datatype = col_datatypes(fin)

            fin.seek(0)

            reader = csv.DictReader(fin)

            # Keep the order of the columns name just as in the CSV
            fields = reader.fieldnames
            cols = []

            # Set field and type
            for f in fields:
                cols.append("\"%s\" %s" % (f, datatype[f])) 

            # A statement to drop table if it exists to avoid duplicate records     
            drpt = "DROP TABLE IF EXISTS \"" + tablename + "\""
            # Generate create table statement:
            stmt = "CREATE TABLE \"" + tablename + "\" (%s)" % ",".join(cols)
            print(stmt)
            
            cur = con.cursor()
            cur.execute(drpt)
            cur.execute(stmt)

            fin.seek(0)

            reader = csv.reader(escaping_generator(fin))

            # Generate insert statement:
            stmt = "INSERT INTO \"" + tablename + "\" VALUES(%s);" % ','.join('?' * len(cols))

            cur.executemany(stmt, reader)
            # Removes the additional header row generated from reader
            cur.execute("DELETE FROM \"" + tablename + "\" WHERE rowid in (select rowid FROM \"" + tablename + "\" LIMIT 1)")       
            con.commit()
            con.close()
            
            print(f'============================= Table {tablename} generated ==============================')            
    except Exception as e:
        # Roll back any change if something goes wrong
        con.rollback()
        raise e
    finally:
        # Close the db connection
        con.close()

# Function to view an SQL table record (1 row)
def view_record(dbFile,tablename):
    try:        
        con = sqlite3.connect(dbFile)        
        cur = con.cursor()
        # Select and prints table record
        cur.execute("SELECT * FROM \"" + tablename + "\"")
        row1 = cur.fetchone()
        print(row1)       
        con.commit()        
    except Exception as e:
        # Roll back any change if something goes wrong
        con.rollback()
        raise e
    finally:
        # Close the db connection
        con.close()    

# Function to merge all three SQL tables together 
def merge_tables():
    try:
        # Creates or opens a db file with a SQLite3 connection
        con = sqlite3.connect('laurel_technology_db')
        # Get a cursor object
        cur = con.cursor()
        # Deletes and creates a table from select statement   
        cur.execute("DROP TABLE IF EXISTS complete_tb")
        cur.execute('''
            CREATE TABLE complete_tb AS
            SELECT DISTINCT E.*, V.VehicleMake, V.VehicleModel, V.VehicleYear, V.VehicleType,
            C.Iban, C.CreditCardNumber, C.CreditCardSecurityCode, C.CreditCardStartDate, 
            C.CreditCardEndDate, C.AddressMain, C.AddressCity
            FROM employment_tb E 
            INNER JOIN vehicle_tb V
                ON E.Firstname = V.Firstname
                AND E.Lastname = V.Lastname           
                AND E.Sex = V.Sex 
                AND E.Age = V.Age  
            INNER JOIN creditcard_tb C
                ON C.Firstname = E.Firstname
                AND C.Lastname = E.Lastname
                AND C.Age = E.Age
                AND C.AddressPostcode = E.AddressPostcode           
                   
            ''')         
        # Commit the change
        con.commit()       

        print("===================== All three tables merged to 'complete_tb' table =====================")
        # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        con.rollback()
        raise e
    finally:
        # Close the db connection
        con.close()

# Function to convert sql to csv
def sql_csv(csvFile, dbFile, tablename):
    try:
        con = sqlite3.connect(dbFile)
        cur = con.cursor()
        cur.execute("SELECT * FROM \"" + tablename + "\";")
        with open(csvFile, 'w',newline='') as csv_file:         
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cur.description]) 
            csv_writer.writerows(cur)  
            print(f"============================ CSV file - {csvFile} generated =============================") 
    except:
        print("Please check the CSV output file. Close it if it's open")
        exit() 
    finally:
        # Close the db connection
        con.close()

# Function that reads the data from a text file 'user_data.txt' and prints on the screen
def read_txt(txtFile):
    try:
        #Opening file in read-only mode
        with open(txtFile, "r", encoding='utf-8') as f:    
            text = f.read() # Reading the text in the user_data.txt file

            # Printing the text inside user_data.txt
            print("________________________________________Message body________________________________________")
            print(text)
    except:
        print("Please confirm the text file exists in the specified location")

# Function that displays all the tasks
def show_tasks():
    print("====================================== To do (Tasks) =======================================")
    print("1.\tChange Shane Chambers's credit card security code ('CreditCardSecurityCode') to 935")
    print("2,\tIncrease Joshua Lane's salary by 2100")
    print("3.\tChange Suzanne Wright's age ('Age') to 37")
    print("4.\tAdd to Kyle Dunn's pension a 0.15 percent of his current amount of 22358")
    print(line)

# Function for resolving task1  
def task1():
    try:        
        con = sqlite3.connect('laurel_technology_db')        
        cur = con.cursor()
        # Input data        
        Sec_code = 935
        FirstName = 'Shane'
        LastName = 'Chambers'   

        # Check the previous value
        print("=================================== Beginning of Task 1 ====================================")       
        print(f"Previous credit card security code for {FirstName} {LastName}")
        cur.execute('''
            SELECT Firstname, Lastname, CreditCardSecurityCode FROM complete_tb 
            WHERE Firstname = ?
            AND Lastname = ?  
            ''', (FirstName, LastName))
        result = cur.fetchone()
        print(result)
        # Execute the change        
        cur.execute('''
            UPDATE complete_tb SET CreditCardSecurityCode = ? 
            WHERE Firstname = ?
            AND Lastname = ?                 
            ''', (Sec_code, FirstName, LastName))
        print(operation_done)
        
        # Confirm the new value
        print(f"Confirm the new credit card security code for {FirstName} {LastName}")
        cur.execute('''
            SELECT Firstname, Lastname, CreditCardSecurityCode FROM complete_tb 
            WHERE Firstname = ?
            AND Lastname = ?  
            ''', (FirstName, LastName))
        result = cur.fetchone()
        print(result)
        con.commit()
        print("Task 1: Job done!")
        print(line)
        # Catch the exception
    except Exception as e:        
        con.rollback()
        raise e
    finally:        
        con.close()

# Function for resolving task2
def task2():
    try:        
        con = sqlite3.connect('laurel_technology_db')        
        cur = con.cursor()
        # Input data        
        SalaryIncrease = 2100
        FirstName = 'Joshua'
        LastName = 'Lane'   

        # Check the previous value
        print("=================================== Beginning of Task 2 ====================================")        
        print(f"Previous salary for {FirstName} {LastName}")
        cur.execute('''
            SELECT Firstname, Lastname, Salary FROM complete_tb 
            WHERE Firstname = ?
            AND Lastname = ?  
            ''', (FirstName, LastName))
        result = cur.fetchone()
        print(result)
        # Execute the change
        Salary = result[2]
        NewSalary = Salary + SalaryIncrease
        cur.execute('''
            UPDATE complete_tb SET Salary = ?
            WHERE Firstname = ?
            AND Lastname = ?                 
            ''', (NewSalary, FirstName, LastName))
        print(operation_done)
        
        # Confirm the new value
        print(f"Confirm the new salary for {FirstName} {LastName}")
        cur.execute('''
            SELECT Firstname, Lastname, Salary FROM complete_tb 
            WHERE Firstname = ?
            AND Lastname = ?  
            ''', (FirstName, LastName))
        result = cur.fetchone()
        print(result)
        con.commit()
        print("Task 2: Job done!")
        print(line)
        # Catch the exception
    except Exception as e:        
        con.rollback()
        raise e
    finally:        
        con.close()

# Function for resolving task3 
def task3():
    try:        
        con = sqlite3.connect('laurel_technology_db')        
        cur = con.cursor()
        # Input data        
        Age = 37
        FirstName = 'Suzanne'
        LastName = 'Wright'   

        # Check the previous value
        print("=================================== Beginning of Task 3 ====================================")        
        print(f"Previous age for {FirstName} {LastName}")
        cur.execute('''
            SELECT Firstname, Lastname, Age FROM complete_tb 
            WHERE Firstname = ?
            AND Lastname = ?  
            ''', (FirstName, LastName))
        result = cur.fetchone()
        print(result)
        # Execute the change        
        cur.execute('''
            UPDATE complete_tb SET Age = ? 
            WHERE Firstname = ?
            AND Lastname = ?                 
            ''', (Age, FirstName, LastName))
        print(operation_done)
        
        # Confirm the new value
        print(f"Confirm the new age for {FirstName} {LastName}")
        cur.execute('''
            SELECT Firstname, Lastname, Age FROM complete_tb 
            WHERE Firstname = ?
            AND Lastname = ?  
            ''', (FirstName, LastName))
        result = cur.fetchone()
        print(result)
        con.commit()
        print("Task 3: Job done!")
        print(line)
        # Catch the exception
    except Exception as e:        
        con.rollback()
        raise e
    finally:        
        con.close()

# Function for resolving task4
def task4():
    try:        
        con = sqlite3.connect('laurel_technology_db')        
        cur = con.cursor()
        # Input data        
        PercentValue = 0.15
        FirstName = 'Kyle'
        LastName = 'Dunn'   

        # Check the previous value
        print("=================================== Beginning of Task 4 ====================================")               
        print(f"Previous pension for {FirstName} {LastName}")
        cur.execute('''
            SELECT Firstname, Lastname, Pension FROM complete_tb 
            WHERE Firstname = ?
            AND Lastname = ?  
            ''', (FirstName, LastName))
        result = cur.fetchone()
        print(result)
        # Execute the change
        Pension = result[2]
        rate = Pension * (PercentValue/100)
        NewPension = round((Pension + rate),2)
        cur.execute('''
            UPDATE complete_tb SET Pension = ?
            WHERE Firstname = ?
            AND Lastname = ?                 
            ''', (NewPension, FirstName, LastName))
        print(operation_done)
        
        # Confirm the new value
        print(f"Confirm the new pension for {FirstName} {LastName}")
        cur.execute('''
            SELECT Firstname, Lastname, Pension FROM complete_tb 
            WHERE Firstname = ?
            AND Lastname = ?  
            ''', (FirstName, LastName))
        result = cur.fetchone()
        print(result)
        con.commit()
        print("Task 4: Job done!")
        print(line)
        # Catch the exception
    except Exception as e:        
        con.rollback()
        raise e
    finally:        
        con.close()

# Strings for displaying steps for connecting to central server
first_steps = ('''Please read the following before pressing 'Enter' key:

o   UPLOAD Laurel Technology Solutions ltd. csv file to the central database store

    Please Note: This step should be done once after carrying out the complete ETL
    process and there must be an internet access to connect to central server.

    * You must ensure that the table does not exist in the server before progressing.
    * If present, DROP (Delete) the table (laurel_technology_tb) in the central server first.
    * Restart the app then come back here to upload the table if you have fulfilled all of 
      the above requirements. 
    ''') 

sub_steps = ('''
o   QUERY database to perform required tasks after uploading table to the server

    Subsequently, you can perform various tasks on the central data store by running queries
    directly from this app after setting up the table inside the organisational database.    
    ''')

# Function to store counts of number of bindings to database
def binding_count():
    if hasattr(binding_count, "num"):
        binding_count.num += 1        # increment if not first call
    else:
        binding_count.num = 0         # initialize on first call
    return binding_count.num

# Function for binding connection parameters to database
def db_binding():  
    bound = binding_count()  # Calls the binding count function
    if bound == 0:           # Binds to the database for the first time
        # Database binding    
        db.bind(provider = provider,
            host = host,
            user = user,
            passwd = password,
            db = database)
        # Mapping entities to database table
        db.generate_mapping(create_tables=True)        
    
# Function for connecting to central server
def server_connection():
    print("======================= Welcome to Leural Technology Central Server ========================")        
    while True:
        try:    
            option = input('''Enter: 
            'U' to Upload table to server,     
            'Q' to Query database,
            'L' to Login to server (phpMyAdmin) or 
            'E' to Go back:_''').lower()
            # Option to upload table to server
            if option == 'u':        
                print(line)    
                    
                # Creating the table in the central server             
                class Laurel_Technology_tb(db.Entity):
                    id = PrimaryKey(int, auto=True)            
                    Firstname = Required(str)
                    Lastname = Required(str)
                    Age = Required(int)
                    Sex = Required(str)
                    Retired = Optional(str)
                    Dependants = Optional(str)
                    MaritalStatus = Optional(str)
                    Salary = Optional(float)
                    Pension = Optional(float)
                    Company = Optional(str)                
                    CommuteDistance = Optional(float)
                    AddressPostcode = Required(str)
                    VehicleMake = Optional(str)
                    VehicleModel = Optional(str)
                    VehicleYear = Optional(int)
                    VehicleType = Optional(str)
                    Iban = Optional(str)
                    CreditCardNumber = Optional(float)
                    CreditCardSecurityCode = Optional(int)
                    CreditCardStartDate = Optional(str)
                    CreditCardEndDate = Optional(str)
                    AddressMain = Optional(str)
                    AddressCity = Optional(str) 

                print("'Laurel_Technology_tb' TABLE CREATED")            
                # Reading the merged csv file
                reader = csv.DictReader(open('Laurel_Tech_updated.csv'))

                # Initializing an empty dictionary for iterating the table records
                csv_data = []

                # Appending the dictionary to a list (Dictionary List)
                for row in reader:
                    csv_data.append(dict(row))  
                
                db_binding() # bind database object                
                print(line)
                print("Uploading records to central datastore...")
                with db_session:
                    # Iterating through the rows of the table and populating the table
                    for i in csv_data:
                        Laurel_Technology_tb(Firstname = i['Firstname'], Lastname = i['Lastname'], Age = i['Age'], Sex = i['Sex'], Retired = i['Retired'],
                        Dependants = i['Dependants'], MaritalStatus = i['MaritalStatus'], Salary = i['Salary'], Pension = i['Pension'], Company = i['Company'],
                        CommuteDistance = i['CommuteDistance'], AddressPostcode = i['AddressPostcode'], VehicleMake = i['VehicleMake'],
                        VehicleModel = i['VehicleModel'], VehicleYear = i['VehicleYear'], VehicleType = i['VehicleType'], Iban = i['Iban'], 
                        CreditCardNumber = i['CreditCardNumber'], CreditCardSecurityCode = i['CreditCardSecurityCode'], CreditCardStartDate = i['CreditCardStartDate'],
                        CreditCardEndDate = i['CreditCardEndDate'], AddressMain = i['AddressMain'], AddressCity = i['AddressCity']
                        )    
                        commit()                                    
                db.disconnect()   # Close the database connection for the current thread

                print()
                print("All records uploaded successfully!")
                print(operation_done)           
                input("Press ENTER to go back: ")                     
                print(line)  
            # Connecting to the server with pony and querying database
            elif option == 'q':
                print(line)              
                db_binding() # bind database object
                    
                # Creating a new session to allow database querying
                with db_session:
                    # Querying the table records using the id of customers
                    id_ = int(input("Please enter the ID of the customer you'd like to search for: "))    
                    my_query = db.select(f"SELECT * FROM laurel_technology_tb WHERE id={id_};")
                    print(line)
                    if my_query == []:                
                        print('The ID does not exist in the table!')
                        continue
                    else:                    
                        print(my_query)
                    print(line)
                db.disconnect()   # Close the database connection for the current thread                             
            # Option to log into phpMyAdmin server
            elif option == 'l':
                print(line)
                webbrowser. open('https://europa.ashley.work/phpmyadmin/')
                print("Log-in to central server with previleged credentials")
                input("Press ENTER to go back: ")                     
                print(line)
            # Option to exist the server connection section
            elif option == 'e':                       
                break    
            else:
                print("You have entered a wrong value. Please try again!")        
        except:        
            print("There is a problem with the connection. Please check that the table exists!")

# Implementation
input(welcome_screen)
menu = 11 # Initialize menu option

while True:    
    try:    
        menu = menu_choice()
        if menu == 1:
            try:            
                input_file = "output/json/json_data.csv"   # csv file path after conversion
                output_file = "cleanjson_data.csv" 
                cleaned_input_file = 'cleanjson_data.csv' # inputs and re-saves cleaned csv here
                temp_file = 'temp.csv' # stores the csv headers temporarily here
                file_loc = '\cleanjson_data.csv' # Get the file location

                # Calls function to convert json to csv
                convert_json()            
                # Calls function to clean csv (converted json file)
                clean_data(input_file, output_file)
                # Calls function to clean header and re-attach to records           
                process_csvtable(cleaned_input_file)
                # Lunch cleaned - json converted (credit cards records) csv file            
                launch_csv(file_loc)
                # Prints success message
                print(success)
                # Prompts user to continue to main menu        
                input(go_back)            
            except:
                # prints error message
                print(failure)        
        elif menu == 2:
            try:
                input_file = "output/xml/xml_data.csv"   # csv file path after conversion
                output_file = "cleanxml_data.csv"
                cleaned_input_file = 'cleanxml_data.csv' # inputs and re-saves cleaned csv here
                temp_file = 'temp.csv' # stores the csv headers temporarily here
                file_loc = '\cleanxml_data.csv' # Get the file location

                # Calls function to convert xml to csv
                convert_xml()        
                # Calls function to clean csv (converted xml file)
                clean_data(input_file, output_file)        
                # Calls function to clean header and re-attach to records
                process_csvtable(cleaned_input_file)        
                # Lunch cleaned - xml converted (employment records) csv file            
                launch_csv(file_loc)            
                print(success)                 
                input(go_back)       
            except:            
                print(failure)      
        elif menu == 3:
            try:
                input_file = "data/user_data.csv"   # csv file path
                output_file = "cleancsv_data.csv"
                cleaned_input_file = 'cleancsv_data.csv' # inputs and re-saves cleaned csv here
                temp_file = 'temp.csv' # stores the csv headers temporarily here
                file_loc = '\cleancsv_data.csv' # Get the file location
                    
                # Calls function to clean csv
                clean_data(input_file, output_file)        
                # Calls function to clean header and re-attach to records
                process_csvtable(cleaned_input_file)        
                # Lunch cleaned csv file (vehicle records)           
                launch_csv(file_loc)           
                print(success)                   
                input(go_back)
            except:            
                print(failure)
        elif menu == 4:
            try:
                # Convert csv file to SQL database for credit card table            
                csv_sql('cleanjson_data.csv','laurel_technology_db','creditcard_tb')            
                input(continue_program) # Prompts user to continue to next stage

                # Convert csv file to SQL database for employment table            
                csv_sql('cleanxml_data.csv','laurel_technology_db','employment_tb')            
                input(continue_program)

                # Convert csv file to SQL database for employment table            
                csv_sql('cleancsv_data.csv','laurel_technology_db','vehicle_tb')           
                print(success)                  
                input(go_back)
            except:            
                print(failure)        
        elif menu == 5:
            try:
                # Calls function to merge all three tables
                merge_tables()
                # Calls function to view first record of the merged table
                view_record('laurel_technology_db','complete_tb')            
                print(success)                   
                input(go_back)
            except:           
                print(failure)
        elif menu == 6:
            try:
                file_loc = '\merged.csv'
                # Function file that generates merged csv file from SQLite
                sql_csv('merged.csv', 'laurel_technology_db', 'complete_tb')
                # Opens merged csv file by lunching excel            
                launch_csv(file_loc)            
                print(success)                    
                input(go_back)
            except:            
                print(failure)
        elif menu == 7:
            try:
                txt_input = 'data/user_data.txt'
                # Calls function that reads in message containing tasks from text file
                read_txt(txt_input)
                input(continue_program)         
                print()
                # Calls function that outlines each task
                show_tasks()
                input(continue_program)
                # Calls functions that performs each task
                task1()
                input(continue_program)
                task2()
                input(continue_program)
                task3()
                input(continue_program)
                task4()            
                print(success)            
                input(go_back)
            except:
                print(failure)
        elif menu == 8:
            try:
                file_loc = '\Laurel_Tech_updated.csv'
                # Function file that generates merged csv file from SQLite
                sql_csv('Laurel_Tech_updated.csv', 'laurel_technology_db', 'complete_tb')
                # Opens merged csv file by lunching excel            
                launch_csv(file_loc)            
                print(success)                    
                input(go_back)
            except:            
                print(failure)
        elif menu == 9:
            print("First time access? select the first option:")
            print(line)
            print(first_steps)
            print(line)
            print(sub_steps)
            print(line)        
            # Calls function to try connecting to database server        
            server_connection()
        elif menu == 0:
            print('Goodbye!!!')
            raise SystemExit()
        else:
            print("You have made a wrong choice, Please Enter a number (0-9)!")
    except:
        if menu == 0:
            exit()
        else:
            print('Wrong input. Access denied!')   