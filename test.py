import streamlit as st
import pandas as pd
import altair as alt

df = pd.read_csv("covid_impact_on_airport_traffic.csv")

countries = ["United States of America (the)", "Chile"]
# df_plot = pd.DataFrame(columns=countries)
# for c in countries:
#     dfc = df[df["Country"] == c]
#     df_plot[c] = dfc.groupby("Date")["PercentOfBaseline"].mean().rolling(30).mean()
# st.write(df_plot.tail())

st.write("Airport Traffic in 2020 during COVID-19")

window_size = st.sidebar.slider("Moving Average Window Size", 1, 120, 7)
all_countries = df["Country"].unique()
selected_countries = st.sidebar.multiselect("Countries", all_countries, all_countries)
df = df[df["Country"].isin(selected_countries)]


dfs = []
for c in selected_countries:
    dfc = df[df["Country"] == c].groupby(['Country', 'Date'])["PercentOfBaseline"].mean().rolling(window_size, min_periods=1).mean().reset_index()
    dfs.append(dfc)
if len(dfs) > 0:
    df_plot = pd.concat(dfs)
else:
    df_plot = df[df["Country"] == "Unknown"]

chart = alt.Chart(df_plot).mark_line().encode(  
    x="Date:T",
    y="PercentOfBaseline:Q",
    color="Country:N",
    tooltip=["Country:N", "Date:T", "PercentOfBaseline:Q"]
)
st.altair_chart(chart, use_container_width=True)
