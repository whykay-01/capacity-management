"""
This file is responsible for creating the pie chart, and it contains relevant functions to do so.
"""

import os
import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import json

from app.utils import load_dataframes


def generate_fig_pie(user_cycle_df):
    
    fig_pie_total = user_cycle_df.groupby("User Type").sum(numeric_only=True)
    
    fig_pie = px.pie(user_cycle_df, "User Type", "Cycles")
    fig_pie.update_layout(title_text="Total Cycles: " + str(fig_pie_total["Cycles"].sum()))

    fig_pie_final = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)

    return fig_pie_final