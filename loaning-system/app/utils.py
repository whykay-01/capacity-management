import os
from app.database import (equipment_cycle_database, 
                          user_cycle_database, 
                          unique_user_equipment_database, 
                          non_unique_user_equipment_database, 
                          generate_main_db)

from app.database_to_csv import (equipment_cycle_csv, 
                                 user_cycle_csv, 
                                 unique_user_equipment_csv, 
                                 non_unique_user_equipment_csv)
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def load_dataframes():
    """
    This function loads the dataframes from the CSV files.
    :return: List of loaded pandas dataframes
    """
    volume_mountpoint = "/data"
    valid_dfs = True

    dataframes = []

    # Define the file paths
    file_paths = [
        "user_cycle.csv",
        "unique_user_equipment.csv",
        "non_unique_user_equipment.csv",
        "equipment_cycle.csv"
    ]

    for file_name in file_paths:
        csv_path = os.path.join(volume_mountpoint, file_name)
        
        try:
            df = pd.read_csv(csv_path)
            dataframes.append(df)
        except FileNotFoundError:
            print(f"File '{file_name}' not found. Skipping...")
            valid_dfs = False
        except pd.errors.EmptyDataError:
            print(f"File '{file_name}' is empty. Skipping...")
            valid_dfs = False
        except pd.errors.ParserError:
            print(f"Error parsing file '{file_name}'. Skipping...")
            valid_dfs = False

    return [dataframes, valid_dfs]



def fill_dict_user_equipment(dataframe, user_cycle_df, user_type):
    """
    this function fills the dictionary with the equipment and the number of unique users that have used it
    :param df: dataframe of the user_equipment database
    :param user_cycle_df: dataframe of the user_cycle database
    :param user_type: string of the user type {'Unique Users', 'Users'}
    :return: dictionary of equipment and number of users
    """

    equipment_usertype_dict = {"Equipment": [], "User Type": [], "Count": []}

    for i in range(len(dataframe["Equipment"])):
        user_list = dataframe[user_type][i].split(", ")

        for j in user_list:
            if (user_cycle_df.loc[user_cycle_df["Unique Users"] == j, "User Type"].iloc[0]== "Staff"):

                equipment_usertype_dict["Equipment"].append(dataframe["Equipment"][i])
                equipment_usertype_dict["User Type"].append("Staff")
                equipment_usertype_dict["Count"].append(1)

            elif (user_cycle_df.loc[user_cycle_df["Unique Users"] == j, "User Type"].iloc[0]== "Student"):

                equipment_usertype_dict["Equipment"].append(dataframe["Equipment"][i])
                equipment_usertype_dict["User Type"].append("Student")
                equipment_usertype_dict["Count"].append(1)

            elif (user_cycle_df.loc[user_cycle_df["Unique Users"] == j, "User Type"].iloc[0] == "Faculty"):

                equipment_usertype_dict["Equipment"].append(dataframe["Equipment"][i])
                equipment_usertype_dict["User Type"].append("Faculty")
                equipment_usertype_dict["Count"].append(1)

            elif (user_cycle_df.loc[user_cycle_df["Unique Users"] == j, "User Type"].iloc[0] == "IT"):

                equipment_usertype_dict["Equipment"].append(dataframe["Equipment"][i])
                equipment_usertype_dict["User Type"].append("IT")
                equipment_usertype_dict["Count"].append(1)

            else:
                
                equipment_usertype_dict["Equipment"].append(dataframe["Equipment"][i])
                equipment_usertype_dict["User Type"].append("Other")
                equipment_usertype_dict["Count"].append(1)

    return pd.DataFrame(data=equipment_usertype_dict)


def test_generate_main_db(path, filename):
    try:
        main_database = generate_main_db(path, filename)

        # Generate the tables from the new source
        equipment_cycle = equipment_cycle_csv(
            equipment_cycle_database(main_database)
        )
        user_cycle = user_cycle_csv(
            user_cycle_database(main_database)
        )
        unique_user_equipment = unique_user_equipment_csv(
            unique_user_equipment_database(main_database)
        )
        non_unique_user_equipment = non_unique_user_equipment_csv(
            non_unique_user_equipment_database(main_database)
        )
        return [equipment_cycle, user_cycle, unique_user_equipment, non_unique_user_equipment]
    
    except Exception as e:
        return True