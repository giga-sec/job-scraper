import streamlit as st
import plotly.express as px
import plotly.io as pio
import pandas as pd
from streamlit_plotly_events import plotly_events

# Sample data
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 11, 12, 13, 14]
})

# Set a theme
pio.templates.default = "plotly_dark"  # You can choose from "plotly", "plotly_white", "ggplot2", "seaborn", etc.

# Create Plotly figure with the chosen theme
fig = px.bar(df, x='x', y='y', title='Click on Points', orientation='h')

# Streamlit app
st.title('Interactive Plotly with Click Events and Theming in Streamlit')

# Use plotly_events to capture click events
selected_points = plotly_events(fig, click_event=True, hover_event=False, select_event=False)

# Display click event data
if selected_points:
    st.write('You clicked on point:', selected_points)
else:
    st.write('Click on a point in the plot.')
