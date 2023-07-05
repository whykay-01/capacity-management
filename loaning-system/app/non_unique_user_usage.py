from app.utils import fill_dict_user_equipment
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def generate_non_unique_user_df(non_unique_user_equipment_df, user_cycle_df):
    """
    This function is used to generate the non-unique user dataframe.
    :param non_unique_user_equipment_df: dataframe of non-unique user equipment
    :param user_cycle_df: dataframe of user cycle
    :return: dataframe of non-unique user equipment
    """

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
    
    return non_unique_final_df


def generate_non_unique_user_equipment_bar(non_unique_user_equipment_df, user_cycle_df):
    """
    This function generates the non-unique user equipment bar graph.
    :param non_unique_user_equipment_df: dataframe of non-unique user equipment
    :param user_cycle_df: dataframe of user cycle
    :return: bar graph of non-unique user equipment
    """
    non_unique_final_df = generate_non_unique_user_df(non_unique_user_equipment_df, user_cycle_df)
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

    return fig_non_unique_equipment_bar