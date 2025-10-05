

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="United Airlines Flight Difficulty Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    try:
        conn = sqlite3.connect('skyhack.db')
        query = )

if __name__ == "__main__":
    main()
