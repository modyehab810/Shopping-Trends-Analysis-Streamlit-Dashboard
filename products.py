# Importing Libraries
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit.components.v1 import html
import streamlit_option_menu
import warnings
import os
from PIL import Image
from time import sleep


def products_header():

    st.title("Products :shopping_bags:")


def filter_data(df, category_filter, size_filter, location_filter):
    if location_filter == "ALL":
        filt = (df["Category"].isin(category_filter)) &\
            (df["Size"].isin(size_filter))

    else:
        filt = (df["Category"].isin(category_filter)) &\
            (df["Size"].isin(size_filter)) &\
            (df["Location"] == location_filter)

    return df[filt]


def number_of_products(the_df):
    return the_df["Item_Purchased"].nunique()


def number_of_category(the_df):
    return the_df["Category"].nunique()


def total_sales(the_df):
    return f'{the_df["Price_in_USD"].sum():,.0f}'


def create_products_chart(the_df):
    # products_sales = the_df.groupby("Item_Purchased")["Price_in_USD"]\
    #     .sum().nlargest(15)

    top_10_products = the_df["Item_Purchased"].value_counts().nlargest(10)

    fig = px.bar(top_10_products,
                 x=top_10_products.index,
                 y=(top_10_products / sum(top_10_products)) * 100,
                 color=top_10_products.index,
                 color_discrete_sequence=["#E64848"],
                 template="plotly_dark",
                 text=top_10_products.apply(
                     lambda x: f"{ (x / sum(top_10_products)) * 100:0.0f}%"),
                 labels={"index": "Product",  "y": "Popularity (%)"},
                 title="\t\tTop 10 Products",
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
            "family": "consolas",
            "size": 17,
            "color": "#fff"
        },
        hovertemplate="Product: %{y}<br>Popularity (%): %{x:.0f}%",
    )

    return fig


def create_size_chart(the_df):
    size = the_df["Size"].value_counts()

    fig = px.pie(names=size.index,
                 values=size,
                 color_discrete_sequence=["#FF0060",
                                          "#00DFA2", "#0079FF", "#F6FA70"],
                 template="plotly_dark",
                 title="\t\tThe Popularity of Size",
                 )

    fig.update_traces(
        textinfo="label+percent",
        textfont={
            "family": "consolas",
            "size": 18,
            "color": "#000"
        },
        hovertemplate="Size: %{label}<br>Popularity (%): %{percent}",
        marker=dict(line=dict(color='#111', width=2))

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


def category_via_season_chart(the_df):
    category_season = the_df.groupby("Season")["Category"]\
        .value_counts().unstack()

    fig = px.line(category_season,
                  template="plotly_dark",
                  labels={"value": "Popularity", "index": "Season"},
                  color_discrete_sequence=[
                      "#ADA2FF", "#C0DEFF", "#FCDDB0", "#FF9F9F", "#EDD2F3"],
                  title="\t\tThe Frequency of Category Via Seasons",
                  height=565,
                  markers="o"

                  )

    fig.update_layout(title={
        "font": {
            "size": 26,
            "family": "tahoma"
        }
    }
    )
    fig.update_traces(
        hovertemplate="Category: %{x}<br>Popularity: %{y}",
        marker_size=10)

    return fig
