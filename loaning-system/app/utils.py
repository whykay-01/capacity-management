import os
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def load_dataframes(volume_mountpoint = '/data'):
    """
    this function loads the dataframes from the csv files
    :param volume_mountpoint: the path to the volume mountpoint (OPTIONAL)
    :return: list of loaded pandas dataframes
    """
    
    # TODO: Change this to the correct path
    # volume_mountpoint = "/data"
    volume_mountpoint = os.getcwd() + '/data'


    # Set the path to the CSV files relative to the volume mountpoint
    user_cycle_csv_path = os.path.join(volume_mountpoint, "user_cycle.csv")
    unique_user_equipment_csv_path = os.path.join(volume_mountpoint, "unique_user_equipment.csv")
    non_unique_user_equipment_csv_path = os.path.join(volume_mountpoint, "non_unique_user_equipment.csv")
    equipment_cycle_csv_path = os.path.join(volume_mountpoint, "equipment_cycle.csv")

    # Read the CSV files using the updated paths
    user_cycle_df = pd.read_csv(user_cycle_csv_path)
    unique_user_equipment_df = pd.read_csv(unique_user_equipment_csv_path).sort_values(by="Unique Users", ascending=False)
    non_unique_user_equipment_df = pd.read_csv(non_unique_user_equipment_csv_path).sort_values(by="Users", ascending=False)
    equipment_cycle_df = pd.read_csv(equipment_cycle_csv_path).sort_values(by="Equipment", ascending=False)

    return [user_cycle_df, unique_user_equipment_df, non_unique_user_equipment_df, equipment_cycle_df]



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


def update_graph_layouts(fig_pie, 
                         fig_top_5_bar, 
                         fig_least_5_bar, 
                         fig_non_unique_equipment_bar, 
                         fig_time_cycle, 
                         fig_time_cycle2,
                         colors =  {"background": "#ADD8E6", "text": "#111111"}):
    
    """
    this function takes the plotly figures and updates the layout for them
    :param fig_pie: plotly figure of the pie chart
    :param fig_top_5_bar: plotly figure of the top 5 bar chart
    :param fig_least_5_bar: plotly figure of the least 5 bar chart
    :param fig_non_unique_equipment_bar: plotly figure of the non unique user equipment bar chart
    :param fig_time_cycle: plotly figure of the time cycle bar chart
    :param fig_time_cycle2: plotly figure of the time cycle bar chart
    :return: None
    """
    
    fig_pie.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )

    fig_top_5_bar.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )

    fig_least_5_bar.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )

    fig_non_unique_equipment_bar.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )

    fig_time_cycle.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )

    fig_time_cycle2.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )

    return