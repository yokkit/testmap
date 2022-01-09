import folium
import json
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_folium import folium_static

chiba_city = [35.609985,140.118126]
m = folium.Map(location=chiba_city, tiles='cartodbpositron', zoom_start=8)
st.header('テスト的にアップしたアプリです')
st.subheader('千葉県だけのマップです')
folium_static(m)