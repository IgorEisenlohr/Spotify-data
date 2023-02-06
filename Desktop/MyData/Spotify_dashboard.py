import pandas as pd
import plotly.express as px
import streamlit

data1 = pd.read_json("StreamingHistory0.json")
data2 = pd.read_json("StreamingHistory1.json")