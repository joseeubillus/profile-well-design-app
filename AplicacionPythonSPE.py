'''Cargamos las librerias a utilizar para el desarrollo de la aplicacion, es probable que se 
necesiten mas a medida que se desarrollan las lineas de codigo'''

#Importamos las librerias a utilizar
import pandas as pd 
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

#Configuraciones basicas de la pantalla de Streamlit
st.set_page_config(page_title='Well Trajectory Design',
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
st.image('BANNER (AMARILLO).jpg',use_column_width=True,)
st.header('WELL TRAJECTORY DESIGN TOOL')
st.text('''The equations used belong to the book Well Engineering and Construction by Rabia''')
st.subheader('Information Required')
st.text('Depends on the type of well to be build')
#Barra de contenido
st.sidebar.header('Well types')
tipo_pozo=st.sidebar.radio('Choose the type of well to design',('Type 1', 'Type 2'))
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("Developed by: Jose Eduardo Ubillus")


if tipo_pozo == 'Type 1':
    bur=st.number_input('Input BUR')
    v3=st.number_input('Input Target TVD')
    v1=st.number_input('Input KOP')
    d2=st.number_input('Input the Horizontal Displacement of the Target')
    st.subheader("Well Trajectory Results")
    check_resultados=st.checkbox('View results',value=False)
    if check_resultados == True:
        r=radio_curvatura(bur)
        alfa=alfa_max(r,d2,v3,v1)
        MD2=md2(bur,alfa)
        V2=v2(v1,r,alfa)
        D1=d1(r,alfa)
        MD3=md3(v3,V2,alfa)
        MDT=mdt(v1,MD2,MD3)

        st.text(f'The curvature radius is: {r} ft')
        st.text(f'The max inclination angle: {alfa} grados')
        st.text(f'The MD in the build up section is: {MD2} ft')
        st.text(f'The vertical section in the build up is: {V2} ft')
        st.text(f'The Horizontal Displacement at the end of the build up section is: {D1} ft')
        st.text(f'The MD in the tangential section is: {MD3} ft')
        st.text(f'The total MD is: {MDT} ft')

        #tabla de datos
        columnas=('X', 'Y')
        data=[(0,0),(0,v1),(D1,V2),(d2,v3)]
        tabla_coordenadas=pd.DataFrame(data=data,columns=columnas)
        col1, col2= st.beta_columns([1.5,1])
        with col1:
            st.subheader('Coordenates needed for the Type 1 Well')
        with col2:
            st.dataframe(tabla_coordenadas)
        
        #grafico de la trayectoria
        #Configuracion de las caracteristicas de la figura
        st.subheader('Type 1 Well Graph')
        fig, ax1= plt.subplots()
        ax1.set_title('Trajectory')
        ax1.set_ylabel('TVD (ft)')
        ax1.set_xlim(xmin=-100,xmax=v3+1000)
        ax1.set_xlabel('Horizontal Displacement (ft)')
        ax1.set_ylim(ymin=0,ymax=v3+1000)
        ax1.invert_yaxis()
        #Primera seccion
        ax1.plot((tabla_coordenadas['X'][0],tabla_coordenadas['X'][1]),(tabla_coordenadas['Y'][0],tabla_coordenadas['Y'][1]),label='KOP')
        #Seccion de construccion
        def arco (r,alfa):
            x=[]
            y=[]
            for theta in np.arange(0,np.round(alfa,1),0.1):
                x.append(r*(1-np.cos(np.deg2rad(theta))))
                y.append(v1+r*np.sin(np.deg2rad(theta)))
            
            return x,y
        
        x,y=arco(r,alfa)
        ax1.plot(x,y,label='Build Up Section')
        #Seccion tangencial
        ax1.plot((tabla_coordenadas['X'][2],tabla_coordenadas['X'][3]),(tabla_coordenadas['Y'][2],tabla_coordenadas['Y'][3]),label='Tangential Section')
        #Locacion del target
        ax1.plot(d2,v3,'bo',label='Target')
        #Labels
        ax1.legend()
        st.pyplot(fig)
if tipo_pozo == 'Type 2':
    st.subheader('Under Construction...')

    
    







