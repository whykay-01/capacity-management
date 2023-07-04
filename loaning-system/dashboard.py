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
    
    # turning the dictionary back into a dataframe and then sorting it (for non-unique use equipment)
    non_unique_equipment_usertype_df = fill_dict_user_equipment(non_unique_user_equipment_df, user_cycle_df, "Users")
    
    dfg = (
        non_unique_equipment_usertype_df.groupby(["Equipment"])
        .size()
        .to_frame()
        .sort_values([0], ascending=False)
        .reset_index()
    )
    non_unique_final_df = non_unique_equipment_usertype_df.merge(dfg)

    # creating a dictionary for daily timeline because the equipment cycle dataframe isn't in the correct format
    equipment_cycle_dict_daily = generate_equipment_cycle_dict_daily(equipment_cycle_df)

    # creating a dictionary for monthly timeline because the equipment cycle dataframe isn't in the correct format
    equipment_cycle_dict_monthly = generate_equipment_cycle_dict_monthly(equipment_cycle_df)

    time_list = generate_time_series(equipment_cycle_df)
    
    # turning dictionary back into a dataframe and then sorting it
    equipment_usertype_df = fill_dict_user_equipment(unique_user_equipment_df, user_cycle_df, "Unique Users")

    # calculating top 5 and least 5 equipment used: DATAFRAMES
    final_top_df = top5_used_equipment(equipment_usertype_df)
    final_bottom_df = least5_used_equipment(equipment_usertype_df)

    # top 5 and least 5 bar graph: GRAPHS
    fig_top_5_bar = generate_top_5_bar_chart(final_top_df)
    fig_least_5_bar = generate_top_5_bar_chart(final_bottom_df)


    # creating the graphs from the dataframes -------------------------------------------------------------------------
    # pie chart 3668
    fig_pie_total = user_cycle_df.groupby("User Type").sum(numeric_only=True)
    fig_pie = px.pie(user_cycle_df, "User Type", "Cycles")
    fig_pie.update_layout(
        title_text="Total Cycles: " + str(fig_pie_total["Cycles"].sum())
    )

    # non-unique equipment bar graph
    non_unique_equipment_bar_total = non_unique_final_df.groupby("Equipment").sum(numeric_only=True)
    fig_non_unique_equipment_bar = px.histogram(
        non_unique_final_df,
        x="Equipment",
        y="Count",
        color="User Type",
        color_discrete_map={
            "Student": px.colors.qualitative.Plotly[0],
            "Staff": px.colors.qualitative.Plotly[1],
            "Others": px.colors.qualitative.Plotly[3],
            "Faculty": px.colors.qualitative.Plotly[2],
            "IT": px.colors.qualitative.Plotly[4],
        },
    )
    # label for total numer of cycles
    fig_non_unique_equipment_bar.add_trace(
        go.Scatter(
            x=non_unique_equipment_bar_total.index,
            y=non_unique_equipment_bar_total["Count"],
            text=non_unique_equipment_bar_total["Count"],
            mode="text",
            textposition="top center",
            textfont=dict(size=14),
            showlegend=False,
        )
    )
    fig_non_unique_equipment_bar.update_xaxes(categoryorder="total descending")

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
    fig_time_cycle.update_xaxes(categoryorder="array", categoryarray=time_list)

    # monthly check out graph
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

    # graph layouts
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
