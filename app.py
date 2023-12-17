# Importing Libraries
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit.components.v1 import html
from streamlit_option_menu import option_menu
import warnings

# Importing Our Multipages
import home
import products
import locations


def run():
    st.set_page_config(
        page_title="Shopping Trends",
        page_icon="🛍️",
        layout="wide"
    )

    warnings.simplefilter(action='ignore', category=FutureWarning)

    # Function To Load Our Dataset
    @st.cache_data
    def load_data(the_file_path):
        df = pd.read_csv(the_file_path)
        df.columns = df.columns.str.replace(" ", "_")
        df.rename(
            columns={"Purchase_Amount_(USD)": "Price_in_USD"}, inplace=True)
        df.set_index("Customer_ID", inplace=True)
        return df

    df = load_data("shopping_trends_updated.csv")

    st.markdown(
        """
    <style>
         .main {
            text-align: center; 
         }

         div.block-containers{
            padding-top: 0.5rem
         }

         .st-emotion-cache-z5fcl4{
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 1.5rem;
            padding-right: 2.8rem;
            overflow-x: hidden;
         }

         .st-emotion-cache-16txtl3{
            padding: 2.7rem 0.6rem
         }
         div.st-emotion-cache-1r6slb0{
            padding: 15px 5px;
            background-color: #111;  
            border-radius: 5px;
            border: 3px solid #5E0303;
            opacity: 0.9;
         }
        div.st-emotion-cache-1r6slb0:hover{
            transition: all 0.5s ease-in-out;
            background-color: #000;  
            border: 3px solid red;
            opacity: 1;
         }

         .plot-container.plotly{
            border: 4px solid #333;
            border-radius: 7px;
         }

         div.st-emotion-cache-1r6slb0 span.st-emotion-cache-10trblm{
            font: bold 24px tahoma
         }
         div [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }


    </style>
    """,
        unsafe_allow_html=True
    )

    header = st.container()
    content = st.container()

    with st.sidebar:
        page = option_menu(
            menu_title='Sidebar',
            options=['Home', 'Products', "Locations"],
            icons=['house-fill', 'person-circle', "map-fill"],
            menu_icon='chat-text-fill',
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": '#000'},
                "icon": {"color": "white", "font-size": "20px"},
                "nav-link": {"color": "white", "font-size": "18px", "text-align": "left", "margin": "0px", },
                "nav-link-selected": {"background-color": "#5E0303"},

            }

        )

        st.write("***")

        # Get All Locations as a list
        location_options = sorted(df["Location"].unique().tolist())
        location_options.insert(0, "ALL")

        # Home Page
        if page == "Home":
            category_filter = st.multiselect("Select The Category 👕💎",
                                             options=sorted(
                                                 df["Category"].unique().tolist()),
                                             default=sorted(
                                                 df["Category"].unique().tolist()))

            size_filter = st.multiselect("Select The Size 👔",
                                         options=sorted(
                                             df["Size"].unique().tolist()),
                                         default=sorted(
                                             df["Size"].unique().tolist()))

            location_filter = st.selectbox("Select The Location 🌏",
                                           options=location_options,
                                           index=0)

            with header:
                home.home_header()

            with content:
                df_filtered = home.filter_data(df, category_filter,
                                               size_filter, location_filter)

                left_col, mid_col, right_col = st.columns(3)

                with left_col:
                    st.subheader("Total Customers")
                    st.subheader(home.total_customers(df_filtered))

                with mid_col:
                    st.subheader("Average Rating")
                    st.subheader(home.avergae_rating(df_filtered))

                with right_col:
                    st.subheader("Total Purchases")
                    st.subheader(home.total_purchases(df_filtered))

                st.markdown("---")

                left_chart, right_chart = st.columns(2)
                with left_chart:
                    st.plotly_chart(home.create_category_chart(
                        df_filtered), use_container_width=True)

                with right_chart:
                    st.plotly_chart(home.create_gender_chart(
                        df_filtered), use_container_width=True)

                st.markdown("---")
                st.plotly_chart(home.create_shipping_chart(
                    df_filtered), use_container_width=True)

        # Products Page
        if page == "Products":
            category_filter = st.multiselect("Select The Category 👕💎",
                                             options=sorted(
                                                 df["Category"].unique().tolist()),
                                             default=sorted(
                                                 df["Category"].unique().tolist()))

            size_filter = st.multiselect("Select The Size 👔",
                                         options=sorted(
                                             df["Size"].unique().tolist()),
                                         default=sorted(
                                             df["Size"].unique().tolist()))

            location_filter = st.selectbox("Select The Location 🌏",
                                           options=location_options,
                                           index=0)
            with header:
                products.products_header()

            with content:
                df_filtered = products.filter_data(df, category_filter,
                                                   size_filter, location_filter)

                left_col, mid_col, right_col = st.columns(3)

                with left_col:
                    st.image("imgs/dollar.png", caption="", width=70)
                    st.subheader("Total Sales")
                    st.subheader(products.total_sales(df_filtered))

                with mid_col:
                    st.image("imgs/clothes.png", width=70)
                    st.subheader("Categories")
                    st.subheader(products.number_of_category(df))

                with right_col:
                    st.image("imgs/online-shopping.png", width=70)
                    st.subheader("Products")
                    st.subheader(products.number_of_products(df_filtered))
                st.markdown("---")

                products_left_chart, products_right_chart = st.columns([7, 5])

                with products_left_chart:
                    st.plotly_chart(products.create_products_chart(df_filtered),
                                    use_container_width=True)

                with products_right_chart:
                    st.plotly_chart(products.create_size_chart(
                        df_filtered), use_container_width=True)

                st.plotly_chart(
                    products.category_via_season_chart(df_filtered),
                    use_container_width=True)

        # Locations Page
        if page == "Locations":

            category_filter = st.multiselect("Select The Category 👕💎",
                                             options=sorted(
                                                 df["Category"].unique().tolist()),
                                             default=sorted(
                                                 df["Category"].unique().tolist()))

            size_filter = st.multiselect("Select The Size 👔",
                                         options=sorted(
                                             df["Size"].unique().tolist()),
                                         default=sorted(
                                             df["Size"].unique().tolist()))

            season_filter = st.multiselect("Select The Season :snowflake::sunny:",
                                           options=sorted(
                                               df["Season"].unique().tolist()),
                                           default=sorted(
                                               df["Season"].unique().tolist()))
            with header:
                locations.sales_header()

            with content:
                df_filtered = locations.filter_data(df, category_filter,
                                                    size_filter, season_filter)

                st.plotly_chart(locations.create_map(df_filtered),
                                use_container_width=True)

                st.markdown("---")

                st.plotly_chart(locations.create_subscription_via_location(df_filtered),
                                use_container_width=True)

                st.markdown("---")

                l_c, r_c = st.columns([7, 5])
                with l_c:

                    st.plotly_chart(locations.create_location_category(df_filtered),
                                    use_container_width=True)

                with r_c:
                    st.plotly_chart(locations.create_top3_review(
                        df_filtered), use_container_width=True)


run()
