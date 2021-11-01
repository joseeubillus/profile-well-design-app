'''Cargamos las librerias a utilizar para el desarrollo de la aplicacion, es probable que se 
necesiten mas a medida que se desarrollan las lineas de codigo'''

#Importamos las librerias a utilizar
import pandas as pd 
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

#Configuraciones basicas de la pantalla de Streamlit
st.set_page_config(page_title='Diseño de Trayectorias de Pozos de Hidrocarburos',
                   page_icon='♣',
                   layout='centered',
                   initial_sidebar_state='collapsed')

#Definir funciones y metodos para elaborar la trayectoria 

def radio_curvatura(bur):
    r=(360*100)/(2*np.pi*bur)
    return r
def alfa_max(r,d2, v3,v1):
    if r>d2:
        alfa=np.degrees(np.arctan((v3-v1)/(r-d2)))-np.degrees(np.arccos((r/(v3-v1)*np.sin(np.arctan((v3-v1)/(r-d2))))))
    else:
        alfa=180-np.degrees(np.arctan((v3-v1)/(d2-r)))-np.degrees(np.arccos((r/(v3-v1)*np.sin(np.arctan((v3-v1)/(d2-r))))))

    return alfa
        
def md2(bur,alfa):
    md2=(alfa*100)/bur
    return md2

def v2(v1,r,alfa):
    v2=v1+r*np.sin(np.deg2rad(alfa))
    return v2

def d1 (r,alfa):
    d1=r*(1-np.cos(np.deg2rad(alfa)))
    return d1

def md3 (v3,v2,alfa):
    md3=(v3-v2)/np.cos(np.deg2rad(alfa))
    return md3

def mdt (md1,md2,md3):
    tmd=md1+md2+md3
    return tmd

#Estructuramos la pagina a nuestro gusto
#Principal
st.image('perforacion.jpg',use_column_width=True,)
st.header('HERRAMIENTA DE DISEÑO DE TRAYECTORIA DE POZOS')
st.subheader("Society of Petroleum Engineering - Escuela Politecnica Nacional Student Chapter")
st.text('''Las ecuaciones utilizadas para elaborar la trayectoria de un pozo pertenecen 
al libro Well Engineering and Construction - Rabia''')
st.subheader('Informacion de la trayectoria')
st.text('Esta informacion dependera del tipo de pozo seleccionado')
#Barra de contenido
st.sidebar.header('Tipos de Pozos')
tipo_pozo=st.sidebar.radio('Seleccione el tipo de pozo a diseñar',('Tipo 1', 'Tipo 2'))
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("Elaborado por: Jose Eduardo Ubillus")
st.sidebar.image("spe_logo.png")


if tipo_pozo == 'Tipo 1':
    bur=st.number_input('Ingrese el BUR')
    v3=st.number_input('Ingrese el TVD del target')
    v1=st.number_input('Ingrese el KOP')
    d2=st.number_input('Ingrese la distancia horizontal del target')
    st.subheader("Resultados del diseño de la trayectoria del pozo")
    check_resultados=st.checkbox('Visualizar resultados de la trayectoria',value=False)
    if check_resultados == True:
        r=radio_curvatura(bur)
        alfa=alfa_max(r,d2,v3,v1)
        MD2=md2(bur,alfa)
        V2=v2(v1,r,alfa)
        D1=d1(r,alfa)
        MD3=md3(v3,V2,alfa)
        MDT=mdt(v1,MD2,MD3)

        st.text(f'El radio de curvatura es: {r} ft')
        st.text(f'El angulo maximo de inclinacion es: {alfa} grados')
        st.text(f'El MD en seccion de construccion es: {MD2} ft')
        st.text(f'La distancia vertical en seccion de construccion es: {V2} ft')
        st.text(f'La distancia horizontal al final de la seccion de construccion es: {D1} ft')
        st.text(f'El MD en seccion tangente es: {MD3} ft')
        st.text(f'El MD total es: {MDT} ft')

        #tabla de datos
        columnas=('Coordenada X', 'Coordenada Y')
        data=[(0,0),(0,v1),(D1,V2),(d2,v3)]
        tabla_coordenadas=pd.DataFrame(data=data,columns=columnas)
        col1, col2= st.beta_columns([1.5,1])
        with col1:
            st.subheader('Coordenadas necesarias en pozo TIPO I')
        with col2:
            st.dataframe(tabla_coordenadas)
        
        #grafico de la trayectoria
        #Configuracion de las caracteristicas de la figura
        st.subheader('Grafica de la trayectoria del pozo TIPO I')
        fig, ax1= plt.subplots()
        ax1.set_title('TRAYECTORIA POZO TIPO 1')
        ax1.set_ylabel('TVD (ft)')
        ax1.set_xlim(xmin=-100,xmax=d2+1000)
        ax1.set_xlabel('Distancia horizontal (ft)')
        ax1.set_ylim(ymin=0,ymax=v3+1000)
        ax1.invert_yaxis()
        #Primera seccion
        ax1.plot((tabla_coordenadas['Coordenada X'][0],tabla_coordenadas['Coordenada X'][1]),(tabla_coordenadas['Coordenada Y'][0],tabla_coordenadas['Coordenada Y'][1]),label='KOP')
        #Seccion de construccion
        def arco (r,alfa):
            x=[]
            y=[]
            for theta in range(0,int(alfa),1):
                x.append(r*(1-np.cos(np.deg2rad(theta))))
                y.append(v1+r*np.sin(np.deg2rad(theta)))
            
            return x,y
        
        x,y=arco(r,alfa)
        ax1.plot(x,y,label='Seccion de Construccion')
        #Seccion tangencial
        ax1.plot((tabla_coordenadas['Coordenada X'][2],tabla_coordenadas['Coordenada X'][3]),(tabla_coordenadas['Coordenada Y'][2],tabla_coordenadas['Coordenada Y'][3]),label='Seccion tangencial')
        #Locacion del target
        ax1.plot(d2,v3,'bo',label='Target')
        #Labels
        ax1.legend()
        st.pyplot(fig)
if tipo_pozo == 'Tipo 2':
    st.subheader('En construccion...')

    
    







