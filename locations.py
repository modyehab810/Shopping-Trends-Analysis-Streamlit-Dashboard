import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit.components.v1 import html


def sales_header():

    st.title('Locations :earth_americas:')


def filter_data(df, category_filter, size_filter, season_filter):

    filt = (df["Category"].isin(category_filter)) &\
        (df["Size"].isin(size_filter)) &\
        (df["Season"].isin(season_filter))

    return df[filt]


# Function To Get The latitude and longitude for each Location
@st.cache_data
def load__locations_data():
    positions = pd.read_csv(
        "https://raw.githubusercontent.com/jasperdebie/VisInfo/master/us-state-capitals.csv")

    return positions


def create_map(the_df):
    pos = load__locations_data()

    alt_df = the_df.merge(pos, left_on="Location", right_on="name", how="left")
    alt_df = alt_df.groupby(["Location", "latitude", "longitude"], as_index=False)[
        "Price_in_USD"].sum()

    fig = px.scatter_mapbox(alt_df, lat="latitude",
                            lon="longitude", hover_name="Location",
                                hover_data=["Price_in_USD"],
                                color="Price_in_USD",
                            size="Price_in_USD",
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            zoom=3,
                            height=650,
                            title="\t\tLocations Via Sales"
                            )

    fig.update_layout(
        mapbox_style="open-street-map",
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

    return fig


def get_top_n(the_df, n):
    top_n_location = the_df.groupby("Location")["Price_in_USD"]\
        .sum().nlargest(n)
    top_n_location = top_n_location.index.tolist()

    filt = the_df["Location"].isin(top_n_location)
    return the_df[filt]


def create_subscription_via_location(the_df):
    dff = get_top_n(the_df, 10)

    subscription_via_loc = dff.groupby("Location")["Subscription_Status"]\
        .value_counts().unstack()

    total = subscription_via_loc["No"] + subscription_via_loc["Yes"]

    subscription_via_loc["No"] = round(
        subscription_via_loc["No"] / total * 100)

    subscription_via_loc["Yes"] = round(
        subscription_via_loc["Yes"] / total * 100)

    fig = px.bar(subscription_via_loc,

                 color_discrete_sequence=["#FF0060",
                                          "#00DFA2", "#0079FF", "#F6FA70"],
                 barmode="group",
                 template="plotly_dark",
                 text_auto=True,
                 labels={
                     "value": "Popularity (%)", "Subscription_Status": "Subscription Status"},
                 title="\t\tSubscription Status Via 10 State",
                 )

    fig.update_layout(
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
        hovertemplate="State: %{x}<br>Popularity (%): %{y:.0f}%",
    )

    return fig


def create_location_category(the_df):
    dff = get_top_n(the_df, 5)
    category_via_loc = dff.groupby("Location", as_index=False)["Category"]\
        .value_counts()

    fig = px.sunburst(category_via_loc, path=['Location', 'Category'],
                      values='count',
                      color_discrete_sequence=[
                          "#FF0060", "#00DFA2", "#0079FF", "#F6FA70", "#EDD2F3"],
                      title="\t\tThe Popularity of Category Via Top 5 State"

                      )

    fig.update_layout(margin=dict(t=50, l=0, r=0, b=10))
    fig.update_layout(
        title={
            "font": {
                "size": 18,
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
            "size": 13,
        },
        hovertemplate="State: %{label}<br>Popularity (%): %{value:.0f}%",
    )

    return fig


def create_top3_review(the_df):
    loc_review = the_df.groupby("Location")["Review_Rating"].mean().nlargest(3)
    fig = px.bar(loc_review,
                 color_discrete_sequence=["#FF0060",
                                          "#00DFA2", "#0079FF", "#F6FA70"],
                 template="plotly_dark",
                 text_auto="0.1f",
                 labels={
                     "value": "Popularity (%)", "Subscription_Status": "Subscription Status"},
                 title="\t\tTop 3 States By Review Rating",
                 )

    fig.update_layout(
        showlegend=False,
        title={
            "font": {
                "size": 16,
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
            "size": 14,
        },
        hovertemplate="State: %{x}<br>AVG Review: %{y:.1f}",
    )

    return fig
