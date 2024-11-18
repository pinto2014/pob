import streamlit as st
import plotly.express as px 
import pandas as pd
import numpy as np


st.set_page_config(page_title="Poblacion 2020", layout="wide", page_icon=":luggage:")
st.title("Peru: Poblacion al :red[2020]")
st.markdown("---")
#to create Tabs:    
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Map", "Poblacion", "PBI", "Empleo", "Agricultura", "Mineria", "Pesca", "Turismo", "Social"  ])

st.subheader("Hola! :wave:, :coffee: ")
st.text("Segun el INEI, La poblacion del Peru al 2020 fue de 32,625,948 habitantes.")

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

perupob = pd.read_csv('pobdata.csv')

#peru_pbi1

perupob_df=perupob.sort_values(by=('Total'), ascending=False)


#to make a sidebar for interactivity:
st.sidebar.header("Para filtrar la data seleccione:" )
departamento=st.sidebar.multiselect("Departamento:", options=perupob_df["DEPARTAMENTO"].unique())



#TO CAPTURE THE FILTERS IN THE SIDEBAR WE USE QUERY METHOD:
df_selection1 = perupob_df.query("DEPARTAMENTO == @departamento")



col1, col2, col3, col4 = st.columns(4)
col1.metric("**Poblacion_Total**", value=f"{perupob_df["Total"].sum():,.0f}")
col2.metric("**Departamentos**", perupob_df["DEPARTAMENTO"].nunique())
col3.metric("**Provincias**", perupob_df["PROVINCIA"].nunique())
col4.metric("**Distritos**", value=f"{perupob_df["DISTRITO"].nunique():,.0f}")

st.markdown("---")

#barchart by All departamentos:
departamento_total=perupob_df.groupby('DEPARTAMENTO')['Total'].sum()
departamento_total=departamento_total.sort_values(ascending=False)
barchart1=px.bar(departamento_total, y='Total',  title='Poblacion por Departamento')
barchart1
st.markdown("---")

st.markdown("Seleccione un Departamento")
col5, col6, col7, col8 = st.columns(4)
col5.metric("**Poblacion_Departamental**", value=f"{df_selection1["Total"].sum():,.0f}")
col6.metric("**Departamentos**", df_selection1["DEPARTAMENTO"].nunique())
col7.metric("**Provincias**", df_selection1["PROVINCIA"].nunique())
col8.metric("**Distritos**", value=f"{df_selection1["DISTRITO"].nunique():,.0f}")



#TO CAPTURE THE FILTERS IN THE SIDEBAR WE USE QUERY METHOD:
#df_selection1 = perupob_df.query("DEPARTAMENTO == @departamento")
#st.dataframe(df_selection1.loc[:,["DEPARTAMENTO", "PROVINCIA", "DISTRITO", "Total"]])

#Formultipe filters:
#df_selection = perupob_df.query("DEPARTAMENTO == @departamento & PROVINCIA == @provincia")


#Mostrar un solo Departamento:
undepartamento_total=df_selection1.groupby('DEPARTAMENTO')['Total'].sum()
undepartamento_total=undepartamento_total.sort_values(ascending=True)
barchart2=px.bar(undepartamento_total, y='Total',  title='Departamento')
barchart2.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
#st.plotly_chart(barchart2)

# to show two charts in same row:
div1, div2=st.columns(spec=[0.5, 0.2])
with div1:
    st.dataframe(df_selection1.loc[:,["DEPARTAMENTO", "PROVINCIA", "DISTRITO", "Total"]])
with div2:
    barchart2

#barchart by PROVINCIA:
provincia_total=df_selection1.groupby('PROVINCIA')['Total'].sum()
provincia_total=provincia_total.sort_values(ascending=True)
barchart3=px.bar(provincia_total, x='Total',  title='Provincias')

#barchart by DISTRITO:
distrito_total=df_selection1.groupby('DISTRITO')['Total'].sum()
distrito_total=distrito_total.sort_values(ascending=True)
barchart4=px.bar(distrito_total, x='Total',  title='Distritos')

# to place the bar charts in one row:
div3, div4=st.columns(2)
with div3:
    barchart3
with div4:
    barchart4
    
#to create Tabs:    
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Map", "Poblacion", "PBI", "Empleo", "Agricultura", "Mineria", "Pesca", "Turismo", "Social"  ])
with tab1: #Map
    map=px.scatter_mapbox(df_selection1, lat=df_selection1['Lat'], lon=df_selection1['Lon'], zoom=8, color=df_selection1['DISTRITO'], 
                 size=df_selection1['Total'], width=1200, height=800, title="Mapa Distrital")
    map.update_layout(mapbox_style="open-street-map")
    map.update_layout(margin={"r":0, "t":100, "l":0, "b":10})
    #map.show()
    st.plotly_chart(map, use_container_width=True)

with tab3: #PBI
    peru_pbi = pd.read_excel('pbi_peru.xlsx', sheet_name='cuadro4', usecols='A:R', header=6)
    peru_pbi1 = peru_pbi.melt(id_vars='DEPARTAMENTO', value_vars=['2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', 
               '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'], var_name='Year', value_name='PBI')
    peru_pbi1_df =peru_pbi1.sort_values(by=('PBI'), ascending=False)

    st.sidebar.header("Para filtrar PBI por departamento, seleccione:" )
    departamento=st.sidebar.multiselect("Departamento:", 
                                    options=peru_pbi1_df["DEPARTAMENTO"].unique())
   
    df_selection2 = peru_pbi1.query("DEPARTAMENTO == @departamento")

    st.text("PBI por Departamento.  Valores a Precios Corrientes (Miles de soles). Fuente: INEI.")
    #st.dataframe(peru_pbi1)
    #st.dataframe(df_selection2.loc[:,["DEPARTAMENTO", "Year", "PBI"]])

    #GRAPH
    #undepartamento_pbi=df_selection2.groupby('DEPARTAMENTO')['PBI'].sum()
    undepartamento_pbi=pd.DataFrame (df_selection2.loc[:,["DEPARTAMENTO", "Year", "PBI"]])
    chart_pbi=px.line(undepartamento_pbi, x='Year', y=['PBI'])
    chart_pbi.update_layout(title= 'PBI Departamental Anual -  Valores a Precios Corrientes (Miles de soles). Fuente: INEI.', 
                            width=800, height=400,  yaxis_title='PBI- miles de Soles', xaxis_title='Año') 
    chart_pbi

    chart2_pbi=px.line(peru_pbi1, x='Year', y='PBI', color='DEPARTAMENTO', template='ggplot2', facet_col= 'DEPARTAMENTO', facet_col_wrap=6, title='pbi DEPARTAMENTAL', markers=True)
    chart2_pbi.update_layout(title= 'PBI Anual por Departamento -  Valores a Precios Corrientes (Miles de soles).', 
                            width=1600, height=2000)
    chart2_pbi.update_yaxes (matches=None)
   
    
    chart2_pbi

st.caption("***Baul-Analytics - 2024***")
