import io
import os
import time
from flask import *
import base64
import codecs
import csv

import pandas as pd
from app.utils import (load_dataframes, 
                       fill_dict_user_equipment)
from app.top5_bar_charts import (generate_top_5_bar_chart)
from app.pie_chart import (generate_fig_pie)
from app.daily_equipment_timeline import (generate_fig_time_cycle)
from app.monthly_equipment_timeline import (generate_fig_time_cycle_month)
from app.non_unique_user_usage import (generate_non_unique_user_equipment_bar)
import csv

app = Flask(__name__)

# creating the variable for the static folder path
# TODO: use this path
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "data")
print("Destination folder: ", app.config["UPLOAD_FOLDER"])

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


@app.route("/upload-files")
def upload_files():
    return render_template("upload-files.html")


@app.route("/confirmation-page", methods=["POST"])
def confirmation_page():
    file = request.files['database_snippet']
    
    csv_data = pd.read_csv(file)
    more_than_10 = len(csv_data) > 10

    csv_data_display = []

    if more_than_10:
        csv_data_display = csv_data[:11].values.tolist()
    else:
        csv_data_display = csv_data.values.tolist()

    session['csv_data'] = csv_data.to_csv(index=False)
    
    return render_template('confirmation-page.html', 
                            uploaded_file=file.filename, 
                            file_content=csv_data_display, 
                            more_than_10=more_than_10, 
                            csv_data=csv_data)


@app.route("/confirm-upload", methods=["POST"])
def confirm_upload():
    csv_data = session['csv_data']

    csv_data.to_csv(os.path.join("data", "test.csv"), index=False)

    success = "Your file has been uploaded successfully!"
    flash(success, 'success')

    return redirect(url_for('index'))

@app.route("/cancel-upload")
def cancel_upload():
    temp_file_path = session['csv_file']
    os.remove(temp_file_path)

    message = "You have aborted the file upload."
    flash(message, 'error')

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = 'my_secret_key'
    app.run('127.0.0.1', 5000, debug=True)
