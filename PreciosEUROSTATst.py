import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

@st.cache()
def coger_datos():
    datos=pd.read_excel('Eurostat.xlsx')
    return datos
datos=coger_datos()
fechas=datos['Fecha'].unique()
paises=datos['País'].unique()
tasas=datos['Tasa'].unique()
productos=datos['Producto'].unique()

st.title('PRECIOS (€/MWh) ELÉCTRICOS Y DE GAS NATURAL EN EUROPA')
st.title("Comparativa entre países europeos")

producto=st.selectbox('Elegir producto',productos)
bandas=datos.loc[datos['Producto']==producto,'Banda'].unique()
banda=st.selectbox('Elegir banda',bandas)
fecha=st.selectbox('Elegir semestre',np.flipud(fechas))

filtro=(datos['Producto']==producto) & (datos['Banda']==banda) &(datos['Fecha']==fecha)
tab_graf=datos.loc[filtro,:].pivot_table(index='País',columns='Tasa',values='Precio (€/MWh)',fill_value=0,aggfunc=np.mean)
tab_graf=tab_graf[tab_graf['All taxes and levies included']!=0]
tab_graf.sort_values('All taxes and levies included',inplace=True)
x=tab_graf.index
y_todoIncluido=tab_graf['All taxes and levies included'].values
y_exclyendoIVA=tab_graf['Excluding VAT and other recoverable taxes and levies'].values
y_valorBase=tab_graf['Excluding taxes and levies'].values
colores1=['yellow' if pais=='Spain' else 'gold' for pais in x]
colores2=['aqua' if pais=='Spain' else 'skyblue' for pais in x]
colores3=['red' if pais=='Spain' else 'salmon' for pais in x]

fig,ax=plt.subplots(figsize=(16,8))
plt.bar(x,y_todoIncluido,label='Total',color=colores1)
plt.bar(x,y_exclyendoIVA,label='Sin IVA',color=colores2)
plt.bar(x,y_valorBase,label='Base',color=colores3)

contador=0
for _ in x:
    plt.text(x[contador], y_todoIncluido[contador]+0.5, str(round(y_todoIncluido[contador], 1)), horizontalalignment='center')
    contador+=1

plt.title(producto+' - '+fecha+'\n'+ banda)
plt.xticks(x,rotation='vertical')
plt.legend(loc='upper left')
plt.tight_layout()
st.pyplot(fig)

tab_graf_styler=tab_graf.style.format(na_rep='No disponible',formatter="{:.1f}")
st.table(tab_graf_styler)


import base64
def crear_link(df, archivo_nombre,etiqueta):
    object_to_download = df.to_csv()
    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{archivo_nombre}">{etiqueta}</a>'

link = crear_link(tab_graf, 'Descarga.csv','Descargar csv')
st.markdown(link, unsafe_allow_html=True)

st.title("Evolución por país, producto y banda")
producto_escog=st.selectbox('Elegir producto',np.concatenate((productos,['-']),axis=0))
bandas_escog=datos.loc[datos['Producto']==producto_escog,'Banda'].unique()
banda_escog=st.selectbox('Elegir banda',np.concatenate((bandas_escog,['-']),axis=0))
pais_escog=st.selectbox('Elegir país',np.concatenate((paises,['-']),axis=0))

filtro=(datos['Producto']==producto_escog) & (datos['Banda']==banda_escog) &(datos['País']==pais_escog)
tab_graf_2=datos.loc[filtro,:].pivot_table(index='Fecha',columns='Tasa',values='Precio (€/MWh)',fill_value=0,aggfunc=np.mean)
tab_graf_2=tab_graf_2[tab_graf_2['All taxes and levies included']!=0]
x=tab_graf_2.index
y_todoIncluido=tab_graf_2['All taxes and levies included'].values
y_exclyendoIVA=tab_graf_2['Excluding VAT and other recoverable taxes and levies'].values
y_valorBase=tab_graf_2['Excluding taxes and levies'].values

fig,ax=plt.subplots(figsize=(16,8))
plt.bar(x,y_todoIncluido,label='Total')
plt.bar(x,y_exclyendoIVA,label='Sin IVA')
plt.bar(x,y_valorBase,label='Base')

contador=0
for _ in x:
    plt.text(x[contador], y_todoIncluido[contador]+0.5, str(round(y_todoIncluido[contador], 1)), horizontalalignment='center')
    contador+=1

plt.title(producto_escog+' - '+pais_escog+'\n'+ banda_escog)
plt.xticks(x,rotation='vertical')
plt.legend(loc='upper left')
plt.tight_layout()
st.pyplot(fig)

tab_graf_2_styler=tab_graf_2.style.format(na_rep='No disponible',formatter="{:.1f}")
st.table(tab_graf_2_styler)

link_2 = crear_link(tab_graf_2, 'Descarga.csv','Descargar csv')
st.markdown(link_2, unsafe_allow_html=True)
