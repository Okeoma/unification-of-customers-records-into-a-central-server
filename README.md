# Unification-of-customers-records-into-a-central-server
A Python program for combining multiple data sources (CSV, JSON, and XML) provided, and pushing these to a central organisational data store.
# APPLICATION DEVELOPMENT REQUIREMENTS AND PROCESSES
## IMPLEMENTATION AND FUTURE PLANS
The fictitious company (Laurel Technology Solutions Ltd.) is seeking to unify all its customers' records, which are currently stored in 
different formats (JSON, XML, and CSV) into a single database to expand its business. This will 
mark the first step towards moving forward with the plan to set up their operations in various
locations abroad. Thanks to the unification implementation, they will be able to analyze and exploit data. 
Finally, they will push all the data into a central database to 
expand from that point and scale out easily.

In light of their intentions to explore foreign markets starting in East Asia and taking advantage 
of the huge customer offerings that such a move brings, they are also concerned with the right 
technology and legal considerations that will ensure a smooth transition from manual 
operations to robust and automated systems that can scale well.

A console application is written in Python and a library for connecting to the central database 
server (ponyORM) was used to implement the ETL (Extract, Transform, and Load) procedure. 
The choice of using Python script over Jupyter Notebook was born from the fact that this 
application will act as a prototype for a more robust application. This will eventually require big data.
Due to the different data formats provided by the organization, the program should be 
able to carry out the following tasks:

• EXTRACT THE RECORDS WHICH ARE STORED IN VARIOUS FORMATS: The file formats 
and a description of what they contain are:
- JSON - Customers' Credit Card records
- XML - Customers Employment records
- CSV - Customers Vehicle records
The program was able to extract all three files using their various Python methods for 
reading into the application.

• TRANSFORM THE DATA INTO A UNIFIED FORMAT TO ENHANCE DATA WRANGLING: 
Since the data were extracted in different formats, the program was able to transform 
the JSON and XML files into CSV. With this process in place, it was easier to see clearly 
the values stored in each customer category. This helped the process of gaining insights 
into the nature of the data. It also helped in deciding on further investigations and 
exploration analysis that was carried out to further refine the data.

• DATA CLEANING: Prior to combining the three CSV files, the data had to be cleaned. The
program was written to automatically clean the anomalies in the records resulting from 
the original JSON file containing credit card records and some field names that had 
different naming conventions and inconsistent representations to generate a more 
consistent naming convention across all the files. In this application, field names are 
presented in Pascal notation.

• COMBINING THE THREE RECORD CATEGORIES AFTER CLEANING: Considerations were 
made about using identical field names that are common to each table as a unifying
factor to achieve coherent and consistent data unification. The program employed a 
Python Standard Library tool for Relational Database Management operations known as 
SQLite3, to perform the task of unifying the tables. (Python Documentation, Sqlite3-DB-API 2.0 interface for SQLite databases). 
Reasons why SQLite3 was introduced for this purpose are as follows:

- The SQL query language is bundled with a Python program that does not require a 
separate server or local application installation process. It simplifies the database 
management process and allows the program to be run on any computer.

- It is lightweight. With such a small size, it can easily be integrated into an application 
as internal data storage and used for database management.

- It is used for testing, creating prototypes, and running database applications without 
the internet. A select query was used to create a merged table from three 
independent tables without connecting to the internet or installing any software for 
the task at hand.

• EXPLORATION AND IMPLEMENTATION OF REQUIRED TASKS: A requirement for the 
application was to process a text file containing communications between staff of the 
organization generated through memos, emails, telegrams, and other electronic 
channels. To extract the tasks, the text file was read so the tasks could be understood. 
After breaking it down into four operations, the tasks were implemented 
programmatically. They were executed in the SQL table containing the unified records of 
the organization, from which the updated merged file was generated.

• LOAD THE DATA INTO THE CENTRAL DATABASE SERVER: The application was able to 
connect to the central data store with the help of the PonyORM library. This was 
achieved by first transforming the merged table in SQL back into CSV format before 
uploading it to the phpMyAdmin server programmatically.

:arrow_forward: &nbsp; **View Live Demo [here](https://youtu.be/5Q7hC-6v1Gk)**
