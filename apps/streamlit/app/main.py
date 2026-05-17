from pathlib import Path

import altair as alt
import duckdb
import pandas as pd
import streamlit as st


DB_PATH = Path("/workspace/storage/analytics.duckdb")


st.set_page_config(
    page_title="Data Lith Analytics",
    page_icon=None,
    layout="wide",
)


@st.cache_data(ttl=30)
def load_event_counts() -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame(
            columns=["event_date", "event_name", "event_count", "unique_users"]
        )

    with duckdb.connect(str(DB_PATH), read_only=True) as conn:
        return conn.execute(
            """
            select
                event_date,
                event_name,
                event_count,
                unique_users
            from curated.event_counts_by_day
            order by event_date, event_name
            """
        ).df()


st.title("Data Lith Analytics")

events = load_event_counts()

if events.empty:
    st.info("No curated data available yet. Run the dbt pipeline first.")
    st.code("docker compose --profile tools run --rm dbt run", language="powershell")
    st.stop()

event_names = sorted(events["event_name"].unique())
selected_events = st.multiselect(
    "Event types",
    event_names,
    default=event_names,
)

filtered = events[events["event_name"].isin(selected_events)]

total_events = int(filtered["event_count"].sum())
unique_users = int(filtered["unique_users"].sum())
active_days = int(filtered["event_date"].nunique())

metric_cols = st.columns(3)
metric_cols[0].metric("Events", f"{total_events:,}")
metric_cols[1].metric("Unique users", f"{unique_users:,}")
metric_cols[2].metric("Active days", f"{active_days:,}")

trend = (
    alt.Chart(filtered)
    .mark_bar()
    .encode(
        x=alt.X("event_date:T", title="Date"),
        y=alt.Y("event_count:Q", title="Events"),
        color=alt.Color("event_name:N", title="Event"),
        tooltip=[
            alt.Tooltip("event_date:T", title="Date"),
            alt.Tooltip("event_name:N", title="Event"),
            alt.Tooltip("event_count:Q", title="Events"),
            alt.Tooltip("unique_users:Q", title="Unique users"),
        ],
    )
    .properties(height=360)
)

st.altair_chart(trend, use_container_width=True)

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
)

