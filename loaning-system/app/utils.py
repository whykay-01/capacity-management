import os
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


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


def load_dataframes():
    # Get the mountpoint of the volume inside the container
    volume_mountpoint = "/data"

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


def generate_top_5_bar_chart(final_df):
    """
    this function takes the final dataframe and generates the top 5 bar chart (most or least used equipment)
    :param final_df: dataframe of the final data
    :return: plotly figure of the top 5 bar chart
    """
    fig_top_5_bar = px.histogram(
        final_df,
        x="Equipment",
        y="Count",
        color="User Type",
        color_discrete_map={
            "Student": px.colors.qualitative.Plotly[0],
            "Staff": px.colors.qualitative.Plotly[1],
            "Other": px.colors.qualitative.Plotly[3],
            "Faculty": px.colors.qualitative.Plotly[2],
            "IT": px.colors.qualitative.Plotly[4],
        }
    )

    fig_top_5_bar_total = final_df.groupby("Equipment").sum(numeric_only=True)

    # label for total number of cycles
    fig_top_5_bar.add_trace(
        go.Scatter(
            x=fig_top_5_bar_total.index,
            y=fig_top_5_bar_total["Count"],
            text=fig_top_5_bar_total["Count"],
            mode="text",
            textposition="top center",
            textfont=dict(size=14),
            showlegend=False,
        )
    )
    fig_top_5_bar.update_xaxes(categoryorder="total descending")

    return fig_top_5_bar



def top5_used_equipment(equipment_usertype_df):
    """
    this function returns the top 5 used equipment given the dataframe with user types and the equipment they use
    """
    intermediate_val = equipment_usertype_df.groupby(["Equipment"]).size().to_frame().sort_values([0], ascending=False).head(5).reset_index()
    return equipment_usertype_df.merge(intermediate_val)



def least5_used_equipment(equipment_usertype_df):
    """
    this function returns the least 5 used equipment given the dataframe with user types and the equipment they use
    """
    intermediate_val = equipment_usertype_df.groupby(["Equipment"]).size().to_frame().sort_values([0], ascending=True).head(5).reset_index()
    return equipment_usertype_df.merge(intermediate_val).sort_values(by=0).reset_index()


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


def generate_equipment_cycle_dict_daily(equipment_cycle_df):
    """
    this function is used to generate the equipment cycle dictionary for the daily cycle bar chart
    :param equipment_cycle_df: dataframe of the equipment cycle
    :return: equipment cycle dictionary
    """
    equipment_cycle_dict = {"Time": [], "Cycles": [], "Equipment": []}
    
    for i in range(len(equipment_cycle_df["Equipment"])):
        
        check_out_time_list = equipment_cycle_df["Check Out Times"][i].split(", ")
        
        for j in check_out_time_list:
            
            try:
                index = equipment_cycle_dict["Time"].index(j, len(equipment_cycle_dict["Time"]) - 1)
                
                if (equipment_cycle_dict["Equipment"][index]!= equipment_cycle_df["Equipment"][i]):

                    equipment_cycle_dict["Time"].append(j)
                    count = 0
                    for k in range(int(equipment_cycle_df["Cycles"][i])):
                        if check_out_time_list[k] == j:
                            count += 1
                    equipment_cycle_dict["Cycles"].append(count)
                    equipment_cycle_dict["Equipment"].append(
                        equipment_cycle_df["Equipment"][i]
                    )
            
            except ValueError:
                
                equipment_cycle_dict["Time"].append(j)
                count = 0
                
                for k in range(int(equipment_cycle_df["Cycles"][i])):
                    test = check_out_time_list[k]
                    
                    if test == j:
                        count += 1

                equipment_cycle_dict["Cycles"].append(count)
                equipment_cycle_dict["Equipment"].append(equipment_cycle_df["Equipment"][i])
    
    return equipment_cycle_dict


def generate_time_series(equipment_cycle_df):
    """
    this function is generating the time series for the equipment cycles
    :param equipment_cycle_df: dataframe with equipment cycles
    :return: time series
    """
    time_list = []
    
    for i in range(len(equipment_cycle_df["Equipment"])):
        
        check_out_time_list = equipment_cycle_df["Check Out Times"][i].split(", ")
        # check_out_list = ['01/09/2021', '01/09/2021', '01/09/2021', ...]
        
        for check_out_time in check_out_time_list:
            
            if check_out_time not in time_list:
                
                if len(time_list) == 0:
                    time_list.append(check_out_time)
                
                else:
                    added = False
                    for j in range(len(time_list) - 1, -1, -1):
                        
                        if (
                            pd.to_datetime(
                                time_list[j], dayfirst=True, format="%d/%m/%Y"
                            ).isoformat()[0:10]
                            < pd.to_datetime(
                                check_out_time, dayfirst=True, format="%d/%m/%Y"
                            ).isoformat()[0:10]
                        ):
                            time_list.insert(j + 1, check_out_time)
                            added = True
                            break

                    if not added:
                        time_list.insert(0, check_out_time)
    
    return time_list


def generate_equipment_cycle_dict_monthly(equipment_cycle_df):
    """
    this function takes the equipment cycle dataframe and generates a dictionary of the equipment cycles
    :param equipment_cycle_df: dataframe of the equipment cycles
    :return: dictionary of the equipment cycles
    """
    equipment_cycle_dict2 = {"Time": [], "Cycles": [], "Equipment": []}
    
    for i in range(len(equipment_cycle_df["Equipment"])):
        check_out_time_list = equipment_cycle_df["Check Out Times"][i].split(", ")
        for j in check_out_time_list:
            try:
                index = equipment_cycle_dict2["Time"].index(
                    j[3:10], len(equipment_cycle_dict2["Time"]) - 1
                )
                if (
                    equipment_cycle_dict2["Equipment"][index]
                    != equipment_cycle_df["Equipment"][i]
                ):
                    equipment_cycle_dict2["Time"].append(j[3:10])
                    count = 0
                    for k in range(int(equipment_cycle_df["Cycles"][i])):
                        if check_out_time_list[k] == j[3:10]:
                            count += 1
                    equipment_cycle_dict2["Cycles"].append(count)
                    equipment_cycle_dict2["Equipment"].append(
                        equipment_cycle_df["Equipment"][i]
                    )
            except ValueError:
                equipment_cycle_dict2["Time"].append(j[3:10])
                count = 0
                for k in range(int(equipment_cycle_df["Cycles"][i])):
                    test = check_out_time_list[k][3:10]
                    if test == j[3:10]:
                        count += 1
                equipment_cycle_dict2["Cycles"].append(count)
                equipment_cycle_dict2["Equipment"].append(
                    equipment_cycle_df["Equipment"][i]
                )
    
    return equipment_cycle_dict2