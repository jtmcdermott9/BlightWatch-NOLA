import pandas as pd
import mysql.connector
import json
import MySQLdb

#Open config file
# Read configuration from JSON file
with open('config.json') as f:
    config = json.load(f)

#Database connection for local editing

host = config["host"] 
user = config["username"] 
password = config["password"] 
database = config["database"] 
port = config["port"]

#close config.json
f.close()

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
    

except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
    
else:
    print("Data loaded successfully into dataframe")
finally:
    print("End of try/except")

#print(df.columns)
#print(df["stage"])
#Reorder column names
data_cols = ['final_address',
             'Data Source',
             'request_status',
             'stage',
             'objectid',
             'casefiled',
             #'o_c',
             'zip_code',
             'latitude',
             'longitude']

print(f'df:{df}')
#Set data to our df from server
data = df[data_cols]

#Dictionary mapping to rename columns to more readable format 
new_column_names = {
    'final_address':'Address',
    'Data Source': 'Source',
    'request_status':'Request Status',
    'objectid':'Object ID',
    'casefiled':'Case Filed Date',
    #'o_c':'Open/Closed',
    'latitude':'Latitude',
    'longitude':'Longitude',
    'stage':'Stage',
    'zip_code':'ZIP'
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
