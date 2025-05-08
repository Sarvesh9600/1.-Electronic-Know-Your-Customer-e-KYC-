import mysql.connector
import streamlit as st
import pandas as pd
from datetime import datetime



# Establish a connection to MySQL Server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SarveshJ@1212",
    database="ekyc"
)

mycursor = mydb.cursor()
print("Connection Established")


def insert_records(text_info):
    sql = "INSERT INTO users(id, name, father_name, dob, id_type, embedding) VALUES (%s, %s, %s, %s, %s, %s)"

    # Parse and validate DOB
    dob_str = text_info.get('DOB', '')
    dob = None
    if dob_str:
        try:
            text_info['DOB'] = text_info['DOB'].strftime('%Y-%m-%d')
            #dob = datetime.strptime(dob_str, "%Y-%m-%d")          
            
        except ValueError:
            st.error("DOB format must be YYYY-MM-DD")
            return

    value = (
        text_info['ID'],
        text_info['Name'],
        text_info["Father's Name"],
        dob,
        text_info['ID Type'],
        str(text_info['Embedding'])
    )
    mycursor.execute(sql, value)
    mydb.commit()

def fetch_records(text_info):
    try:
        # Ensure we have at least an ID to search for
        if 'ID' not in text_info or not text_info['ID']:
            return pd.DataFrame()  # Return empty dataframe if no ID
        
        query = f"""
        SELECT id, create_time, name, father_name, dob, id_type, embedding
        FROM users
        WHERE id = '{text_info['ID']}'
        """
        records = pd.read_sql(query, mydb)
        
        # Fill None values with empty strings for display
        records.fillna('', inplace=True)
        return records
        
    except Exception as e:
        print(f"Error fetching records: {e}")
        return pd.DataFrame()  # Return empty dataframe on error
# def fetch_records(text_info):
#     sql = "SELECT * FROM users WHERE id = %s"
#     value = (text_info['ID'],)
#     mycursor.execute(sql, value)
#     result = mycursor.fetchall()
#     if result:
#         df = pd.DataFrame(result, columns=[desc[0] for desc in mycursor.description])
#         return df
#     else:
#         return pd.DataFrame()


def check_duplicacy(text_info):
    try:
        if 'ID' not in text_info or not text_info['ID']:
            return False  # No ID provided, can't be duplicate
        
        query = f"SELECT 1 FROM users WHERE id = '{text_info['ID']}' LIMIT 1"
        mycursor.execute(query)
        return mycursor.fetchone() is not None
        
    except Exception as e:
        print(f"Error checking duplicate: {e}")
        return False
# def check_duplicacy(text_info):
#     df = fetch_records(text_info)
#     return df.shape[0] > 0







# CREATE TABLE users(  
#     id VARCHAR(255) NOT NULL PRIMARY KEY,
#     create_time DATETIME COMMENT 'Create Time',
#     name VARCHAR(255),
#     father_name VARCHAR(255),
#     dob DATETIME,
#     id_type VARCHAR(255) NOT NULL,
#     embedding BLOB
# )