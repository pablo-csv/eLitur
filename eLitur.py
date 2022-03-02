# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 15:35:00 2022

@author: pablo
"""

import requests
from bs4 import BeautifulSoup
import streamlit as st
from pprint import pprint
from datetime import date

def get_data(url):  # webscrapping
    data = {}
    result = requests.get(url)
    web = result.content
    soup = BeautifulSoup(web)
    ano = soup.find('td', {'class':'t'}).text   # obtenemos el año
    tabla = soup.find('table', {'class':'tb'})  # obtenemos la tabla
    rows = tabla.find_all('tr')
    cod = '0000'         # ejemplos para saber qué
    mes = 'Diciembre'    # almacena cada variable
    dia_num = '25'
    dia_sem = 'Viernes'  # por ejemplo
    tiempo = 'Adviento'  
    for row in rows:
        if len(row.attrs) == 1:     # para actualizar el código de día
            cod = row.attrs['id']
            #print(cod)  # comentar
        if len(row.attrs) == 2:     # para actualizar el mes
            mes = row.text
            #print(mes)  # comentar
        if row.find('span', {'class':'zdate'}) is not None:   # para actualizar el día numérico y nominal
            dia_info = row.find_all('span', {'class':'zdate'})
            dia_num = dia_info[0].text
            dia_sem = dia_info[1].text
            #print(dia_num, dia_sem)  # comentar
        # cuando no hay atributos:
        if row.find('div', {'class':'season'}) is not None:   # para actualizar el tiempo
            tiempo = row.find('div', {'class':'season'}).text
            #print(tiempo)  # comentar
        if row.find('p', {'class':'indent'}) is not None:     # para actualizar fiesta, tipo y color
            if len(row.find_all('a')) != 0:
                tipo = row.find_all('a')[0]['title']
                if tipo == 'Conmemoración facoltativa':    # corrección
                    tipo = 'Conmemoración facultativa'
            else:
                tipo = 'Feria'
            fiesta_color = row.find('p', {'class':'indent'})
            fiesta = fiesta_color.text.strip()
            color = fiesta_color.find_all('span')[0].attrs['class'][0]
            if color == 'feastg': color = 'limegreen'      # verde
            elif color == 'feastw': color = 'white'        # blanco
            elif color == 'feastv': color = 'darkviolet'   # morado
            elif color == 'feastr': color = 'red'          # rojo
            elif color == 'feastp': color = 'hotpink'      # rosa
            elif color == 'feastb': color = 'deepskyblue'  # azul
            #print(fiesta, color, tipo)  # comentar
            if cod not in data:
                data[cod] = {'dia_sem':dia_sem,
                             'dia_num':dia_num,
                             'mes':mes,
                             'año':ano,
                             'tiempo':tiempo,
                             'fiestas':{fiesta:{'tipo':tipo, 'color':color}}}
            else:
                data[cod]['fiestas'][fiesta] = {'tipo':tipo, 'color':color}
    return data

def change2green():
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url('https://ae01.alicdn.com/kf/HTB1jQ_hKFXXXXccXXXXq6xXFXXXN/Priest-Costumes-Clothes-Male-Catholic-Church-Clergy-Chasuble-Celebrant-Green-Vestment-traje-de-padre.jpg')
        }
        </style>
        """,    
        unsafe_allow_html=True
    )

def change2white():
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url('https://psanjuancrisostomo.arquibogota.org.co/sites/default/files/noticias/2021-04/bjbqajbjktmme_br7i_umowkv__0mnvyu3stz1vnt66jyouz6f5sxzpovkxwc9lnlxy2x3xp2xre65zcpxixpznm3ks.jpg')
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def change2violet():
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url('')
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def change2red():
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url('')
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def change2pink():
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url('')
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def change2blue():
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url('')
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# CONFIGURACIÓN DE LA WEB
st.set_page_config(layout="wide", page_title="eLitur")

st.markdown(   # imagen de fondo
    """
    <style>
    .reportview-container {
        background: url("https://lh6.googleusercontent.com/-vZQUyXCsISw/Tm_At3p_3WI/AAAAAAAAHuY/nMyHpa3KKPY/s800/t1337_gif.jpg")
    }
    </style>
    """,
    unsafe_allow_html=True
)

#st.title('eLitur')

fecha = str(date.today()).split('-')
ano_hoy, mes_hoy, dia_hoy = fecha[0], fecha[1], fecha[2]

diocesis = {'Cuenca':f'http://www.gcatholic.org/calendar/{ano_hoy}/ES-cuen1-es.htm',
            'Madrid':f'http://www.gcatholic.org/calendar/{ano_hoy}/ES-madr1-es.htm',
            'Valencia':f'http://www.gcatholic.org/calendar/{ano_hoy}/ES-vale0-es.htm'}

col1, col2 = st.columns(2)
with col1:
    st.title('Diócesis')
with col2:
    option = st.selectbox('', sorted(diocesis))

if st.button('Ver calendario'):
    data = get_data(diocesis[option])
    st.write(data[mes_hoy+dia_hoy]['fiestas'])
    color = 'limegreen'
    if color == 'limegreen': change2green()
    elif color == 'white': change2white()
    elif color == 'darkviolet': change2violet()
    elif color == 'red': change2red()
    elif color == 'hotpink': change2pink()
    elif color == 'deepskyblue': change2blue()



















