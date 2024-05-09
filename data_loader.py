import pandas as pd
import mysql.connector

#Database connection for local editing

host = "sql5.freesqldatabase.com" 
user = "sql5680691" 
password = "g4fgFKv83C" 
database = "sql5680691" 
port = 3306 

#Database connection for production
'''host = "jtmcdermott9.mysql.pythonanywhere-services.com"
user = "jtmcdermott9"
password = "Ihatemysql123"
database = "jtmcdermott9$capstone"
port = 3306'''

connection = mysql.connector.connect(
                                    host=host,     
                                    user=user,     
                                    password=password,     
                                    database=database,     
                                    port=port ) 

mycursor = connection.cursor()


#Put database read in try/except block for safety

try:
    mycursor.execute("SELECT * FROM blightdata")
    rows = mycursor.fetchall()
    columns = [desc[0] for desc in mycursor.description]

    df = pd.DataFrame(rows, columns=columns)
    

except:
    print("Error loading data")
else:
    print("Data loaded successfully into dataframe")
finally:
    print("End of try/except")

#print(df.columns)
#print(df["stage"])
#Reorder column names
data_cols = ['final_address',
             'data_source',
             'request_status',
             'stage',
             'objectid',
             'casefiled',
             #'o_c',
             'zipcode',
             'latitude',
             'longitude']


#Set data to our df from server
data = df[data_cols]

#Dictionary mapping to rename columns to more readable format 
new_column_names = {
    'final_address':'Address',
    'data_source': 'Source',
    'request_status':'Request Status',
    'objectid':'Object ID',
    'casefiled':'Case Filed Date',
    #'o_c':'Open/Closed',
    'latitude':'Latitude',
    'longitude':'Longitude',
    'stage':'Stage',
    'zipcode':'ZIP'
}

data = data.rename(columns=new_column_names)
data = data.fillna('n/a')

#Repeat for USPS data
try:
    mycursor.execute("SELECT * FROM dfusps")
    rows = mycursor.fetchall()
    columns = [desc[0] for desc in mycursor.description]

    df_usps = pd.DataFrame(rows, columns=columns)
    

except:
    print("Error loading data")
else:
    print("USPS Data loaded successfully into dataframe")
finally:
    print("End of try/except (USPS)")

#(df_usps.columns)
