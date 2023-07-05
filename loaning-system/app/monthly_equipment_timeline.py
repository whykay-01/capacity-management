"""
This file is used to generate the Monthly Equipment Timeline Bar Graph, and it contains the following functions:
    
    * generate_equipment_cycle_dict_monthly
    * generate_fig_time_cycle_month
    
"""


import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


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



def generate_fig_time_cycle_month(equipment_cycle_df):
    
    # creating a dictionary for monthly timeline because the equipment cycle dataframe isn't in the correct format
    equipment_cycle_dict_monthly = generate_equipment_cycle_dict_monthly(equipment_cycle_df)

    fig_monthly_timeline_df = pd.DataFrame(equipment_cycle_dict_monthly)
    fig_monthly_timeline_total = fig_monthly_timeline_df.groupby("Time").sum(numeric_only=True)
    fig_time_cycle2 = px.histogram(
        equipment_cycle_dict_monthly,
        x="Time",
        y="Cycles",
        color="Equipment",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    # label for total number of cycles
    fig_time_cycle2.add_trace(
        go.Scatter(
            x=fig_monthly_timeline_total.index,
            y=fig_monthly_timeline_total["Cycles"],
            text=fig_monthly_timeline_total["Cycles"],
            mode="text",
            textposition="top center",
            textfont=dict(size=14),
            showlegend=False,
        )
    )

    return fig_time_cycle2
