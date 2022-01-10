import folium
import json
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_folium import folium_static

times = ['2019/09/09 1:09', '2019/09/09 22:38','2019/09/10 11:49', '2019/09/10 14:31', '2019/09/10 17:36']

dict_date = dict(zip(times, times))
select_data = st.sidebar.radio('閲覧したいデータを選んでください',tuple(times))
hospitals = st.sidebar.radio('災害拠点病院を表示',('する','しない'))

chiba_city = [35.609985,140.118126]
m = folium.Map(location=chiba_city, tiles='cartodbpositron', zoom_start=8)

st.header('テストデータのアップロードです')
st.subheader('千葉県のマップだけ載せてます。今は動きません')
folium_static(m)