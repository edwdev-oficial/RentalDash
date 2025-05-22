import pandas as pd
import streamlit as st

def adjust_coluns(df):
    df = df.astype(str)
    # st.write(df.dtypes)
    columns = df.columns
    if df.iloc[0, 0] == 'Customer(sv)':
        # today = pd.Timestamp.today()
        for column in range(6, 8):
            df.iloc[0, column] = columns[column]
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
        df['Total number of repairs'] = df['Total number of repairs'].replace("", "0" )
        df['Total number of repairs'] = df['Total number of repairs'].astype(int)
        df['Total billed amount'] = df['Total billed amount'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        df['Total billed amount'] = df['Total billed amount'].astype(float)
        df['Total billed amount'] = df['Total billed amount'] * 1.4
        df['Equip - at Cust date'] = pd.to_datetime(df['Equip - at Cust date'], dayfirst=True)
        df['Equip - Serv. Ex. Dt'] = pd.to_datetime(df['Equip - Serv. Ex. Dt'], dayfirst=True)   

    elif df.iloc[0, 0] == '(n) Serial Number':
        for column in range(4, 7):
            df.iloc[0, column] = columns[column]
        df.columns = df.iloc[0]
        df = df[2:].reset_index(drop=True)
        df['Tool Age in months (Delivery)'] = df['Tool Age in months (Delivery)'].astype(int)

        df['# of completed repairs'] = df['# of completed repairs'].replace("", "0")
        df['# of completed repairs'] = df['# of completed repairs'].astype(float)
        df['Covered by Customer'] = df['Covered by Customer'].replace("", "0")
        df["Covered by Customer"] = df["Covered by Customer"].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        df['Covered by Customer'] = df['Covered by Customer'].astype(float)
        df['Covered by Hilti'] = df['Covered by Hilti'].replace("", "0")
        df["Covered by Hilti"] = df["Covered by Hilti"].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        df['Covered by Hilti'] = df['Covered by Hilti'].astype(float)
        df['Covered by Customer'] = df['Covered by Customer'].fillna(0)
        df['Covered by Customer'] = df['Covered by Customer'] * 1.4
        df['Covered by Hilti'] = df['Covered by Hilti'].fillna(0)
        df['Covered by Hilti'] = df['Covered by Hilti'] * 1.4
        df['Notif. Completion Date'] = pd.to_datetime(df['Notif. Completion Date'], dayfirst=True)
        df['Total Cust'] = df['Covered by Customer'] + df['Covered by Hilti']

    return df