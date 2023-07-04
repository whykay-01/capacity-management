from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import os
from dash.dependencies import Input, Output, State

from app.utils import (fill_dict_user_equipment, 
                       load_dataframes,
                       update_graph_layouts,
                    #    generate_equipment_cycle_dict_daily,
                    #    generate_time_series,
                    #    generate_equipment_cycle_dict_monthly,
                       generate_non_unique_user_df,
                       generate_non_unique_user_equipment_bar,
                       
                       generate_fig_time_cycle,
                       generate_fig_time_cycle_month)

from app.top5_bar_charts import (top5_used_equipment, 
                                 least5_used_equipment, 
                                 generate_top_5_bar_chart)

from app.pie_chart import generate_fig_pie


app = Dash(__name__)


def dashboard():

    # loading the dataframes
    user_cycle_df, unique_user_equipment_df, non_unique_user_equipment_df, equipment_cycle_df = load_dataframes()
    
    # turning dictionary back into a dataframe and then sorting it
    equipment_usertype_df = fill_dict_user_equipment(unique_user_equipment_df, user_cycle_df, "Unique Users")

    # calculating top 5 and least 5 equipment used: DATAFRAMES
    final_top_df = top5_used_equipment(equipment_usertype_df)
    final_bottom_df = least5_used_equipment(equipment_usertype_df)

    # top 5 and least 5 bar graph: GRAPHS
    fig_top_5_bar = generate_top_5_bar_chart(final_top_df)
    fig_least_5_bar = generate_top_5_bar_chart(final_bottom_df)


    # creating the graphs from the dataframes -------------------------------------------------------------------------
    
    # pie chart: GRAPHS
    fig_pie = generate_fig_pie(user_cycle_df)

    # non-unique equipment bar graph: DATAFRAMES
    non_unique_final_df = generate_non_unique_user_df(non_unique_user_equipment_df, user_cycle_df)
    # non-unique equipment bar graph: GRAPHS
    fig_non_unique_equipment_bar = generate_non_unique_user_equipment_bar(non_unique_final_df)

    # daily check out graph: GRAPHS
    fig_time_cycle = generate_fig_time_cycle(equipment_cycle_df)

    # monthly check out graph: GRAPHS
    fig_time_cycle2 = generate_fig_time_cycle_month(equipment_cycle_df)

    # graph layouts and their background features
    colors = {"background": "#ADD8E6", "text": "#111111"}
    update_graph_layouts(fig_pie, fig_top_5_bar, fig_least_5_bar, fig_non_unique_equipment_bar, fig_time_cycle, fig_time_cycle2, colors)

    # webpage layout
    app.layout = html.Div(
        style={"backgroundColor": colors["background"]},
        children=[
            html.H1(
                children="Loaning Dashboard",
                style={"textAlign": "center", "color": colors["text"]},
            ),
            html.H4(
                children="Add new CSV files to the system: ",
                style={"textAlign": "left", "color": colors["text"]},
            ),
            dcc.Upload(
                id="upload-data",
                children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                style={
                    "width": "50%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "2px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "left",
                    "margin": "10px",
                },
                multiple=True,
            ),
            html.H3(
                children="Non-Unique User Pie Chart",
                style={"textAlign": "center", "color": colors["text"]},
            ),
            dcc.Graph(id="pie-graph", figure=fig_pie),
            html.H3(
                children="5 Most Used Equipment (Unique)",
                style={"textAlign": "center", "color": colors["text"]},
            ),
            dcc.Graph(id="top-5-graph", figure=fig_top_5_bar),
            html.H3(
                children="5 Least Used Equipment (Unique)",
                style={"textAlign": "center", "color": colors["text"]},
            ),
            dcc.Graph(id="least-5-graph", figure=fig_least_5_bar),
            html.H3(
                children="Used Equipment by non-unique Users",
                style={"textAlign": "center", "color": colors["text"]},
            ),
            dcc.Graph(
                id="non_unique_equipment_bar", figure=fig_non_unique_equipment_bar
            ),
            html.H3(
                children="Daily Equipment Timeline",
                style={"textAlign": "center", "color": colors["text"]},
            ),
            dcc.Graph(id="-cycle-timeline-graph", figure=fig_time_cycle),
            html.H3(
                children="Monthly Equipment Timeline",
                style={"textAlign": "center", "color": colors["text"]},
            ),
            dcc.Graph(id="monthly-timeline-graph", figure=fig_time_cycle2),
        ],
    )

    app.run_server(host="0.0.0.0", port=8050, debug=True)


if __name__ == "__main__":
    dashboard()
