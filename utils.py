import pandas
import sqlite3
import requests

def get_countries_info():
    country = requests.get(
        "https://restcountries.com/v3.1/all",
        verify=False
    )

    if country.status_code == 200:
        return country.json()
    else:
        raise KeyError("The request to the Countries RESTApi failed.")

def save_data_sqlite(dataframe: pandas.DataFrame):
    conn = sqlite3.connect("mydb.db")
    dataframe.to_sql("countries_dataset", conn, if_exists="replace")
    conn.close()

def save_data_json(dataframe: pandas.DataFrame):
    dataframe.to_json("countries_dataset.json")