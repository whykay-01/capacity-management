"""
This file is responsible for creating two bar charts (most and least 5 used equipment types), and it contains relevant functions to do so.
"""

import json
import os
import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from app.utils import load_dataframes

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



def generate_top_5_bar_chart(graph_type, equipment_usertype_df):
    """
    this function takes the final dataframe and generates the top 5 bar chart (most or least used equipment)
    :param final_df: dataframe of the final data
    :return: plotly figure of the top 5 bar chart
    """
    if graph_type == "Most Used":
        final_df = top5_used_equipment(equipment_usertype_df)
    
    elif graph_type == "Least Used":
        final_df = least5_used_equipment(equipment_usertype_df)

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

    fig_top_5_bar_final = json.dumps(fig_top_5_bar, cls=plotly.utils.PlotlyJSONEncoder)

    return fig_top_5_bar_final

