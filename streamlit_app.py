# Required libraries
import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from datetime import timedelta

# App title
st.title("Task Organizer with Gantt Chart")

# Creating tasks data table in the app
st.markdown("### Enter your tasks:")
tasks = st.empty()
num_tasks = st.slider("Number of tasks:", 1, 10)
# Creating the structure of the DataFrame and updating the column names
task_cols = ["Task", "Start", "Finish", "Hours", "Priority"]
task_data = pd.DataFrame(columns=task_cols)
for i in range(num_tasks):
    task_name = st.text_input(f"Task name {i+1}", key=f"task_name_{i}")
    task_start = st.date_input(f"Start date task {i+1}", key=f"task_start_{i}")
    task_end = st.date_input(f"Finish date task {i+1}", key=f"task_end_{i}")
    task_hours = st.number_input(f"Estimated hours for task {i+1}", min_value=1, key=f"task_hours_{i}")
    task_priority = st.selectbox(f"Task priority {i+1}", ["High", "Medium", "Low"], key=f"task_priority_{i}")

    task_data.loc[i] = [task_name, task_start, task_end, task_hours, task_priority]

st.markdown("### Your tasks:")
st.write(task_data)

# Creating Gantt chart
st.markdown("### Gantt Chart:")
if st.button("Create Gantt Chart"):
    fig = make_subplots(rows=1, cols=1, specs=[[{"type": "xy"}]])
    fig = ff.create_gantt(task_data, colors=['#FF5733', '#37AA9C', '#FFC300'], index_col='Priority', show_colorbar=True,
                          bar_width=0.2, showgrid_x=True, showgrid_y=True, group_tasks=True)
    st.plotly_chart(fig)

# Daily planning
st.markdown("### Daily Planning:")

task_data["Duration"] = (task_data["Finish"] - task_data["Start"]).apply(lambda x: x.days + 1)
task_data["Allocation"] = task_data.apply(lambda row: row.Hours / row.Duration, axis=1)

date_set = set()
for i, row in task_data.iterrows():
    date_set.update(pd.date_range(row["Start"], row["Finish"]))

date_list = sorted(list(date_set))

for date in date_list:
    st.markdown(f"#### {date.strftime('%Y-%m-%d')}")
    tasks_on_date = task_data.loc[(task_data["Start"] <= date) & (task_data["Finish"] >= date)].sort_values(
        by="Priority", key=lambda col: col.map({"High": 0, "Medium": 1, "Low": 2}))
    tasks_on_date["Daily Hours"] = tasks_on_date["Allocation"]
    st.write(tasks_on_date[["Task", "Daily Hours", "Priority"]])
