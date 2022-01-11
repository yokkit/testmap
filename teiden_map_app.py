import folium
import json
import pandas as pd
# import numpy as np
# import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from streamlit_folium import folium_static

with open('chiba.geojson', encoding='utf-8') as fh:
    chiba_geojson = json.load(fh)
chiba_teiden_df = pd.read_csv('./chiba_teiden_2.csv', index_col=0)
hosp_df = pd.read_csv('./chiba_saigai_kyoten_hospitals.csv', index_col=0)
total_teiden_df = pd.read_csv('./total_teiden_df.csv', index_col=0)
chiba_total_teiden_suii = pd.read_csv('./chiba_total_teiden_suii.csv', index_col=0)

def show_hospital(m):
    """
    災害拠点病院のマッピングを足す関数です。
    """
    hosp_df.apply(lambda r: folium.Marker(location=[r['緯度'], r['経度']], 
                                                popup=r['機関名']+'　　　　　　　　　　　　　',
                                                icon=folium.Icon(icon="header"),
                                                ).add_to(m), axis=1)
def make_map_to_web(date_value, hospitals, m):
    """
    フォリウムでコロプレス（停電地域）とマッピング（災害拠点病院）を作成するための関数です。
    """
    min_teiden = chiba_teiden_df.iloc[:,4:].min().min()
    threshold = [min_teiden, 10000, 30000, 50000, 70000, 90000]

    choropleth = folium.Choropleth(
        geo_data=chiba_geojson,
        name='choropleth',
        key_on= 'feature.properties.N03_004',
        threshold_scale=threshold,
        data=chiba_teiden_df,
        columns=['市', date_value],
        fill_color='YlOrRd',
        legend_name="停電戸数（戸）",
        nan_fill_color = 'transparent',
    #     nan_fill_opacity = 0.1,
    ).add_to(m)

    # マウスオーバーで各市の停電戸数を表示します
    choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(fields=['N03_004', date_value],
                                   aliases=['市:', '停電戸数:'],
                                   labels=True,
                                   localize=True,
                                   sticky=False,
                                   style="""
                                   background-color: #F0EFEF;
                                   border: 2px solid black;
                                   border-radius: 3px;
                                   box-shadow: 3px;
                                   """,)
                                   )

    if hospitals=='する':
        show_hospital(m)

    folium.LayerControl().add_to(m)

def show_maps():
    """
    千葉県の停電エリアのコレオプレス図を時系列で示すページを表示する関数です。
    """

    add_select = st.sidebar.selectbox("地図のタイプを選択",("OpenStreetMap", "cartodbpositron","Stamen Terrain","Stamen Toner"))

    # chiba_city = [35.609985,140.118126]
    # ichihara_city=[35.497775,140.115700]
    mobara_city=[35.428528,140.28806]

    m = folium.Map(location=mobara_city, tiles=add_select, zoom_start=9)

    times = ['2019/9/9 1:09', '2019/9/9 22:38','2019/9/10 11:49', '2019/9/10 14:31', '2019/9/10 17:36']
    dict_date = dict(zip(times, times))
    select_data = st.sidebar.radio('閲覧したいデータを選んでください',tuple(times))
    hospitals = st.sidebar.radio('災害拠点病院を表示',('する','しない'))

    make_map_to_web(select_data, hospitals, m)

    st.subheader(f'千葉県内の停電エリアマップ {select_data}時点')

    total_teiden_number = total_teiden_df[total_teiden_df['日時']==select_data]['総停電数']
    diffs_teiden =total_teiden_df[total_teiden_df['日時']==select_data]['増減']
    st.metric(label="千葉県内の総停電戸数", 
            value=int(total_teiden_number), 
            delta=int(diffs_teiden))
    folium_static(m)

def show_linechart():
    '''
    千葉県内の停電世帯の推移をラインチャートで表示する関数です。
    '''
    st.subheader('千葉県内の停電世帯の推移')
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=chiba_total_teiden_suii['日時'], 
                y=chiba_total_teiden_suii['停電戸数'], 
                mode='lines+markers', 
                name='停電戸数',
                line=dict(color='firebrick', width=3)),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=chiba_total_teiden_suii['日時'], 
                y=chiba_total_teiden_suii['停電市町村数'], 
                name="停電市町村数",
                mode='lines+markers',
                line=dict(color='royalblue', width=2, dash='dot')),
        secondary_y=True,
    )

    # Set x-axis title
    fig.update_xaxes(title_text="日時")

    # Set y-axes titles
    fig.update_yaxes(title_text="戸数", secondary_y=False)
    fig.update_yaxes(title_text="市町村数", secondary_y=True)
    fig.update_xaxes(tickangle=45)

    st.plotly_chart(fig)

def main():
    st.header('令和元年房総半島台風（台風15号）')
    info_type = st.sidebar.radio('表示する内容を選択',
                ('停電世帯のマップ', '停電世帯数の推移チャート'))
    if info_type == '停電世帯数の推移チャート':
        show_linechart()
    else:
        show_maps()

if __name__ == "__main__":
    main()
