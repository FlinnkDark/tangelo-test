import time
import pandas
from hashlib import sha1
from utils import get_countries_info, save_data_sqlite, save_data_json

def country_data_inframe():
    try:
        # Generate a mark in the moment of the execution's start
        start_time = time.time()

        # Declaring the frame
        dataframe = pandas.DataFrame(columns = ["Region" , "Country Name", "Language", "Time"])

        # First, getting the country sended by the request
        all_countries_data = get_countries_info()

        # Appending country data to the dataframe
        for country_data in all_countries_data:
            dataframe = pandas.concat([dataframe, pandas.DataFrame({
                "Region" : [country_data["region"]],
                "Country Name": [country_data["name"]["common"]],
                "Language": [sha1(
                    bytes(list(country_data["languages"].values())[0], "utf-8")
                ).hexdigest() if country_data.get("languages", {}) else "None"],
                "Time": [(start_time - time.time()) * -1]
            })], ignore_index=True, axis=0)
            
        # Printing the result
        print(
f""" 
            ========= DATAFRAME ==========
{dataframe}
            ========= DATA =========
Total time: {dataframe["Time"].sum()}
Time mean: {dataframe["Time"].mean()}
Time min: {dataframe["Time"].min()}
Time max: {dataframe["Time"].max()}
""")
        
        # Now saving the result in a sqlite database
        save_data_sqlite(dataframe)

        # And saving the result in a json file
        save_data_json(dataframe)
        
    except (KeyError, Exception) as e:
        print(e)
        print(type(e).__name__)

country_data_inframe()