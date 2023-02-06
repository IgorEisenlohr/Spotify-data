import pandas as pd 
import numpy as np 
import streamlit as st
import plotly.express as px
from PIL import Image

data1 = pd.read_json("StreamingHistory0.json")
data2 = pd.read_json("StreamingHistory1.json")

data = pd.concat([data1, data2])

data['date'] = data.endTime.apply(lambda x: x.split(' ')[0])
data['hrPlayed'] = data.msPlayed.apply(lambda x: x/3.6e6)
data.drop(columns=['endTime'], inplace = True)
data.date = pd.to_datetime(data.date)

image = Image.open('logo@2x.png')
image.thumbnail((256,256))

def app_layout():
    st.set_page_config(layout='wide')

    col1, col2 = st.columns(2)
    with col1:
        st.image(image)
    with col2:
        st.header("Perfil de músicas do usuário (2022-2023)")
        st.write("Selecione o artista para saber informações detalhadas")

    artista = st.selectbox('Selecione o artista: ', options=data.artistName.unique())

    col1, col2 = st.columns(2)
    with col1:
        group_artist = data.groupby('artistName').hrPlayed.sum().reset_index().query(f'artistName == "{artista}"')
        horas_artista_plot = px.bar(group_artist, x='hrPlayed', y='artistName', color_discrete_sequence=["#1DB954"])
        horas_artista_plot.update_traces(textposition='inside')
        horas_artista_plot.update_layout(xaxis_title="Total de horas",
                                        yaxis_title="",
                                        xaxis=dict(showticklabels=False), 
                                        height=300)
        st.plotly_chart(horas_artista_plot)

    with col2:
        group_artista_track = data.groupby(['artistName', 'trackName']).hrPlayed.sum().reset_index()
        group_artista_track_filtered = group_artista_track.query(f'artistName == "{artista}"').sort_values(by='hrPlayed',ascending=True).query('hrPlayed > 1')
        group_artista_track_plot = px.bar(group_artista_track_filtered, y='trackName', x='hrPlayed', color_discrete_sequence=["#1DB954"])
        group_artista_track_plot.update_layout(xaxis_title="Total de horas",
                                                 yaxis_title="",
                                                 xaxis=dict(showticklabels=False),
                                                 height=400)
        st.plotly_chart(group_artista_track_plot)

    group_date = data.groupby([data.date.dt.month, 'artistName']).hrPlayed.sum().reset_index().query(f'artistName == "{artista}"')
    group_date_plot = px.line(group_date, x='date', y='hrPlayed', color_discrete_sequence=["#1DB954"])
    group_date_plot.update_layout(width=1920)
    st.plotly_chart(group_date_plot)

if __name__ == '__main__':
    app_layout()
