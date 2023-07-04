import os

import pandas as pd


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
            if (
                user_cycle_df.loc[user_cycle_df["Unique Users"] == j, "User Type"].iloc[
                    0
                ]
                == "Staff"
            ):
                equipment_usertype_dict["Equipment"].append(dataframe["Equipment"][i])
                equipment_usertype_dict["User Type"].append("Staff")
                equipment_usertype_dict["Count"].append(1)

            elif (
                user_cycle_df.loc[user_cycle_df["Unique Users"] == j, "User Type"].iloc[
                    0
                ]
                == "Student"
            ):
                equipment_usertype_dict["Equipment"].append(dataframe["Equipment"][i])
                equipment_usertype_dict["User Type"].append("Student")
                equipment_usertype_dict["Count"].append(1)

            elif (
                user_cycle_df.loc[user_cycle_df["Unique Users"] == j, "User Type"].iloc[
                    0
                ]
                == "Faculty"
            ):
                equipment_usertype_dict["Equipment"].append(dataframe["Equipment"][i])
                equipment_usertype_dict["User Type"].append("Faculty")
                equipment_usertype_dict["Count"].append(1)

            elif (
                user_cycle_df.loc[user_cycle_df["Unique Users"] == j, "User Type"].iloc[
                    0
                ]
                == "IT"
            ):
                equipment_usertype_dict["Equipment"].append(dataframe["Equipment"][i])
                equipment_usertype_dict["User Type"].append("IT")
                equipment_usertype_dict["Count"].append(1)

            else:
                equipment_usertype_dict["Equipment"].append(dataframe["Equipment"][i])
                equipment_usertype_dict["User Type"].append("Other")
                equipment_usertype_dict["Count"].append(1)

    return equipment_usertype_dict


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

