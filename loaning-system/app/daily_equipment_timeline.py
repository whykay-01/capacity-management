"""
This file is used to generate the Daily Equipment Timeline Bar Graph, and it contains the following functions:
    
    * generate_equipment_cycle_dict_daily
    * generate_time_series
    * generate_fig_time_cycle
    
"""

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

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



def generate_fig_time_cycle(equipment_cycle_df):
    # creating a dictionary for daily timeline because the equipment cycle dataframe isn't in the correct format
    equipment_cycle_dict_daily = generate_equipment_cycle_dict_daily(equipment_cycle_df)

    # daily check out graph
    fig_daily_timeline_df = pd.DataFrame(equipment_cycle_dict_daily)
    fig_daily_timeline_total = fig_daily_timeline_df.groupby("Time").sum(numeric_only=True)
    fig_time_cycle = px.histogram(
        equipment_cycle_dict_daily,
        x="Time",
        y="Cycles",
        color="Equipment",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    # label for total number of cycles
    fig_time_cycle.add_trace(
        go.Scatter(
            x=fig_daily_timeline_total.index,
            y=fig_daily_timeline_total["Cycles"],
            text=fig_daily_timeline_total["Cycles"],
            mode="text",
            textposition="top center",
            textfont=dict(size=11),
            showlegend=False,
        )
    )
    time_series = generate_time_series(equipment_cycle_df)
    fig_time_cycle.update_xaxes(categoryorder="array", categoryarray=time_series)

    return fig_time_cycle
