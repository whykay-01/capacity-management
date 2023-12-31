import os
from flask import *
import pandas as pd
from flask_httpauth import HTTPBasicAuth

# importing helpers
from app.utils import load_dataframes, fill_dict_user_equipment, test_generate_main_db

# importing functions which generate the figures
from app.top5_bar_charts import generate_top_5_bar_chart
from app.pie_chart import generate_fig_pie
from app.daily_equipment_timeline import generate_fig_time_cycle
from app.monthly_equipment_timeline import generate_fig_time_cycle_month
from app.non_unique_user_usage import generate_non_unique_user_equipment_bar
import hashlib
from dotenv import load_dotenv


# importing functions which generate the DB inputs
from app.database import (
    generate_main_db,
    equipment_cycle_database,
    user_cycle_database,
    unique_user_equipment_database,
    non_unique_user_equipment_database,
)

# importing functions which transform DB into CSV
from app.database_to_csv import (
    equipment_cycle_csv,
    user_cycle_csv,
    unique_user_equipment_csv,
    non_unique_user_equipment_csv,
)


app = Flask(__name__)
auth = HTTPBasicAuth()

load_dotenv()
ADMIN_ACCESS_TOKEN = os.getenv("ADMIN_ACCESS_TOKEN")

users = {"admin": ADMIN_ACCESS_TOKEN}


def calculate_md5_hash(data):
    md5_hash = hashlib.md5()
    md5_hash.update(data.encode("utf-8"))
    return md5_hash.hexdigest()


@auth.verify_password
def verify_password(username, password):
    if username in users and calculate_md5_hash(password) == users.get(username):
        return username


# creating constants for the static folder path
VOLUME_MOUNTPOINT = "/data"

# check if the folder temp/ exists, if not, create it
if not os.path.exists(VOLUME_MOUNTPOINT + "/temp"):
    os.makedirs(VOLUME_MOUNTPOINT + "/temp")

TEMPORARY_MOUNTPOINT = "/data/temp"


def dashboard():
    """
    This function is the main function that calls functions which generate the dashboard
    :param None
    :return: dictionary of the graphs
    """
    # loading the dataframes
    (
        user_cycle_df,
        unique_user_equipment_df,
        non_unique_user_equipment_df,
        equipment_cycle_df,
    ) = load_dataframes()[0]

    # turning dictionary back into a dataframe and then sorting it
    equipment_usertype_df = fill_dict_user_equipment(
        unique_user_equipment_df, user_cycle_df, "Unique Users"
    )

    # pie chart: GRAPHS
    fig_pie = generate_fig_pie(user_cycle_df)

    # top 5 and least 5 bar graph: GRAPHS
    fig_top_5_bar = generate_top_5_bar_chart("Most Used", equipment_usertype_df)
    fig_least_5_bar = generate_top_5_bar_chart("Least Used", equipment_usertype_df)

    # non-unique equipment bar graph: GRAPHS
    fig_non_unique_equipment_bar = generate_non_unique_user_equipment_bar(
        non_unique_user_equipment_df, user_cycle_df
    )

    # daily check out graph: GRAPHS
    fig_time_daily = generate_fig_time_cycle(equipment_cycle_df)

    # monthly check out graph: GRAPHS
    fig_time_monthly = generate_fig_time_cycle_month(equipment_cycle_df)

    print("Dashboard has been generated")

    return {
        "Non-Unique User Pie Chart": fig_pie,
        "5 Most Used Equipment (Unique)": fig_top_5_bar,
        "5 Least Used Equipment (Unique)": fig_least_5_bar,
        "Used Equipment by non-unique Users": fig_non_unique_equipment_bar,
        "Daily Equipment Timeline": fig_time_daily,
        "Monthly Equipment Timeline": fig_time_monthly,
    }


@app.route("/")
@auth.login_required
def index():
    valid_dfs = load_dataframes()[1]
    try:
        figures = dashboard()
    except:
        figures = None
    return render_template("index.html", figures=figures, valid_dfs=valid_dfs)


@app.route("/upload-files")
@auth.login_required
def upload_files():
    return render_template("upload-files.html")


@app.route("/confirmation-page", methods=["POST"])
@auth.login_required
def confirmation_page():
    file = request.files["database_snippet"]
    filename = file.filename

    csv_data = pd.read_csv(file)
    more_than_10 = len(csv_data) > 10

    csv_data_display = []

    # Show the first ten rows of the CSV file in case the file is large
    if more_than_10:
        csv_data_display = csv_data[:11].values.tolist()
    else:
        csv_data_display = csv_data.values.tolist()

    # Reset the file pointer to the beginning
    file.seek(0)

    # Save the uploaded file to a temporary location
    temp_file_path = os.path.join(TEMPORARY_MOUNTPOINT, "fresh_upload.csv")
    file.save(temp_file_path)
    session["csv_file"] = temp_file_path

    return render_template(
        "confirmation-page.html",
        uploaded_file=filename,
        file_content=csv_data_display,
        more_than_10=more_than_10,
        csv_data=csv_data,
    )


@app.route("/confirm-upload", methods=["POST"])
@auth.login_required
def confirm_upload():
    file_path = session.get("csv_file")

    temp_check = test_generate_main_db(
        path=TEMPORARY_MOUNTPOINT, filename="/fresh_upload.csv"
    )

    if isinstance(temp_check, list):
        csv_data = pd.read_csv(file_path)
        csv_data.to_csv(os.path.join(VOLUME_MOUNTPOINT, "test.csv"), index=False)

        # Remove the temporary file after processing
        os.remove(file_path)
        del session["csv_file"]

        # this is generating csv from the uploaded file
        main_database = generate_main_db()

        # Generate the tables from the new source
        equipment_cycle = equipment_cycle_csv(equipment_cycle_database(main_database))
        user_cycle = user_cycle_csv(user_cycle_database(main_database))
        unique_user_equipment = unique_user_equipment_csv(
            unique_user_equipment_database(main_database)
        )
        non_unique_user_equipment = non_unique_user_equipment_csv(
            non_unique_user_equipment_database(main_database)
        )

        if (
            len(equipment_cycle) == 0
            or len(user_cycle) == 0
            or len(unique_user_equipment) == 0
            or len(non_unique_user_equipment) == 0
        ):
            error = "The file you uploaded generated empty dataframes. Please try again and upload the correct file."
            flash(error, "error")
            return redirect(url_for("upload_files"))

        # Upload new CSVs
        equipment_cycle.to_csv(
            os.path.join(VOLUME_MOUNTPOINT, "equipment_cycle.csv"), index=False
        )
        user_cycle.to_csv(
            os.path.join(VOLUME_MOUNTPOINT, "user_cycle.csv"), index=False
        )
        unique_user_equipment.to_csv(
            os.path.join(VOLUME_MOUNTPOINT, "unique_user_equipment.csv"), index=False
        )
        non_unique_user_equipment.to_csv(
            os.path.join(VOLUME_MOUNTPOINT, "non_unique_user_equipment.csv"),
            index=False,
        )

        success = "Your file has been uploaded successfully! Reload the page if you cannot see the update yet."
        flash(success, "success")
        return redirect(url_for("index"))

    else:
        temp_file_path = session["csv_file"]
        os.remove(temp_file_path)
        error = "An error occurred during file processing. Please try again and upload the file in the correct format!"
        flash(error, "error")
        return redirect(url_for("upload_files"))


@app.route("/cancel-upload")
@auth.login_required
def cancel_upload():
    temp_file_path = session["csv_file"]
    os.remove(temp_file_path)

    message = "You have aborted the file upload."
    flash(message, "error")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.secret_key = "my_secret_key"
    app.run("0.0.0.0", 8050, debug=True)
