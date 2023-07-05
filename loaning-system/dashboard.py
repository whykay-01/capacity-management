from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
# Using flask to host the app
from flask import (
    Flask,
    render_template,
)

from app.utils import (load_dataframes, 
                       fill_dict_user_equipment)
from app.top5_bar_charts import (generate_top_5_bar_chart)
from app.pie_chart import (generate_fig_pie)
from app.daily_equipment_timeline import (generate_fig_time_cycle)
from app.monthly_equipment_timeline import (generate_fig_time_cycle_month)
from app.non_unique_user_usage import (generate_non_unique_user_equipment_bar)


# app = Dash(__name__)

app = Flask(__name__)

def dashboard():
    """
    This function is the main function that calls functions which generate the dashboard
    :param None
    :return: dictionary of the graphs
    """
    # loading the dataframes
    user_cycle_df, unique_user_equipment_df, non_unique_user_equipment_df, equipment_cycle_df = load_dataframes()
    
    # turning dictionary back into a dataframe and then sorting it
    equipment_usertype_df = fill_dict_user_equipment(unique_user_equipment_df, user_cycle_df, "Unique Users")

    # pie chart: GRAPHS
    fig_pie = generate_fig_pie(user_cycle_df)
    
    # top 5 and least 5 bar graph: GRAPHS
    fig_top_5_bar = generate_top_5_bar_chart("Most Used", equipment_usertype_df)
    fig_least_5_bar = generate_top_5_bar_chart("Least Used", equipment_usertype_df)
    
    # non-unique equipment bar graph: GRAPHS
    fig_non_unique_equipment_bar = generate_non_unique_user_equipment_bar(non_unique_user_equipment_df, user_cycle_df)

    # daily check out graph: GRAPHS
    fig_time_daily = generate_fig_time_cycle(equipment_cycle_df)

    # monthly check out graph: GRAPHS
    fig_time_monthly = generate_fig_time_cycle_month(equipment_cycle_df)

    print("Dashboard has been generated")

    return {"Non-Unique User Pie Chart": fig_pie,
            "5 Most Used Equipment (Unique)": fig_top_5_bar,
            "5 Least Used Equipment (Unique)": fig_least_5_bar,
            "Used Equipment by non-unique Users": fig_non_unique_equipment_bar,
            "Daily Equipment Timeline": fig_time_daily,
            "Monthly Equipment Timeline": fig_time_monthly}

@app.route("/")
def index():
    figures = dashboard()
    return render_template("index.html", figures=figures)

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
# app.run_server(host="0.0.0.0", port=8050, debug=True)
