import streamlit as st
import plotly_express as px 
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
    

st.caption("***Baul-Analytics - 2024***")
