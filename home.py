import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit.components.v1 import html


def home_header():

    st.title('Shopping Trends Dashboard :bar_chart:')


def filter_data(df, category_filter, size_filter, location_filter):
    if location_filter == "ALL":
        filt = (df["Category"].isin(category_filter)) &\
            (df["Size"].isin(size_filter))

    else:
        filt = (df["Category"].isin(category_filter)) &\
            (df["Size"].isin(size_filter)) &\
            (df["Location"] == location_filter)

    return df[filt]


def total_customers(the_df):
    return f"{len(the_df):,.0f}"


def avergae_rating(the_df):
    return round(the_df["Review_Rating"].mean(), 1)


def total_purchases(the_df):
    return f"{the_df['Previous_Purchases'].sum():,.0f}"


def create_category_chart(the_df):
    category = the_df["Category"].value_counts()

    fig = px.bar(category,
                 x=category.index,
                 y=(category / sum(category)) * 100,
                 color=category.index,
                 color_discrete_sequence=["#FF0060",
                                          "#00DFA2", "#0079FF", "#F6FA70"],
                 template="plotly_dark",
                 text=category.apply(
                     lambda x: f"{ (x / sum(category)) * 100:0.0f}%"),
                 labels={"index": "Category",  "y": "Popularity (%)"},
                 title="\t\tThe Popularity of Each Category",
                 width=500
                 )

    fig.update_layout(
        showlegend=False,
        title={
            "font": {
                "size": 20,
                "family": "tahoma"
            }
        },
        hoverlabel={
            "bgcolor": "#222",
            "font_size": 14,
            "font_family": "tahoma"
        }
    )

    fig.update_traces(
        textfont={
            "family": "tahoma",
            "size": 15,
        },
        hovertemplate="Category: %{x}<br>Popularity (%): %{y:.0f}%",
    )

    return fig


def create_gender_chart(the_df):
    gender = the_df["Gender"].value_counts()
    fig = px.pie(names=gender.index,
                 values=gender,
                 color_discrete_sequence=["#FF6969", "#03C988"],
                 template="plotly_dark",
                 title="\t\tThe Freuqency of Gender",
                 hole=0.4,
                 width=480

                 )

    fig.update_traces(
        textinfo="label+percent",
        textfont={
            "family": "tahoma",
            "size": 16,
            "color": "#fff"
        },
        hovertemplate="Category: %{label}<br>Popularity (%): %{percent}",
        marker=dict(line=dict(color='#000', width=2))

    )
    fig.update_layout(
        showlegend=False,
        title={
            "font": {
                "size": 20,
                "family": "tahoma"
            }
        },
        hoverlabel={
            "bgcolor": "#222",
            "font_size": 14,
            "font_family": "tahoma"
        }
    )

    return fig


def create_shipping_chart(the_df):
    dfshipping_type = the_df["Shipping_Type"].value_counts()
    fig = px.scatter(dfshipping_type,
                     size=dfshipping_type,
                     color=dfshipping_type.index,
                     template="plotly_dark",
                     labels={"value": "Frequency", "index": "Shipping Type"},
                     color_discrete_sequence=[
                         "#ADA2FF", "#C0DEFF", "#FCDDB0", "#FF9F9F", "#EDD2F3"],
                     title="\t\tThe Popularity Shipping Type🛒",
                     opacity=0.87)

    fig.update_layout(
        showlegend=False,
        title={
            "font": {
                "size": 20,
                "family": "tahoma"
            }
        },
        hoverlabel={
            "bgcolor": "#222",
            "font_size": 15,
            "font_family": "tahoma"
        }
    )
    fig.update_traces(
        hovertemplate="Shipping Type: %{x}<br>Popularity: %{y}"
    )
    return fig
