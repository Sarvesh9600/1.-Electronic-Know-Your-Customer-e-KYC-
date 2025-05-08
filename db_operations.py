from sqlalchemy import text
import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize connection.
conn = st.connection('mysql', type='mysql')

def insert_records(text_info):
    # Convert DOB string to date if needed
    dob_str = text_info.get('DOB', '')
    dob = None
    if dob_str:
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            st.error("DOB format must be YYYY-MM-DD")
            return

    with conn.session as s:
        s.execute(
            text('INSERT INTO users (id, name, father_name, dob, id_type, embedding) VALUES (:id, :name, :father_name, :dob, :id_type, :embedding);'),
            {
                'id': text_info['ID'],
                'name': text_info['Name'],
                'father_name': text_info["Father's Name"],
                'dob': dob,
                'id_type': text_info['ID Type'],
                'embedding': str(text_info['Embedding'])
            }
        )
        s.commit()


def fetch_record(text_info):
    id_value = text_info['ID']
    with conn.session as s:
        result = s.execute(text("SELECT * FROM users WHERE id = :id;"), {"id": id_value})
        rows = result.fetchall()
        df = pd.DataFrame(rows, columns=result.keys())
    return df


def check_duplicacy(text_info):
    df = fetch_record(text_info)
    return df.shape[0] > 0



