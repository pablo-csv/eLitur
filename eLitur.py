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

#@st.cache
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
            elif color == 'feastu': color = 'deepskyblue'  # azul
            # corrección:
            if tiempo == 'Triduo Pascual' or fiesta == 'Domingo de Pascua de la Resurrección del Señor':
                tipo = 'Solemnidad'
            # se añade al diccionario
            if cod not in data:
                data[cod] = {'dia_sem':dia_sem,
                             'dia_num':dia_num,
                             'mes':mes,
                             'año':ano,
                             'tiempo':tiempo,
                             'fiestas':{fiesta:{'nombre':fiesta, 'tipo':tipo, 'color':color}}}
            else:
                data[cod]['fiestas'][fiesta] = {'nombre':fiesta, 'tipo':tipo, 'color':color}
    return data

def normalcolor(original):  # pasa del color exacto al general
    if original == 'limegreen': nuevo = 'verde'
    elif original == 'white': nuevo = 'blanco'
    elif original == 'darkviolet': nuevo = 'morado'
    elif original == 'red': nuevo = 'rojo'
    elif original == 'hotpink': nuevo = 'rosa'
    elif original == 'deepskyblue': nuevo = 'azul'
    return nuevo


# CONFIGURACIÓN DE LA WEB
st.set_page_config(layout="wide", page_title="eLitur")

diocesis = ['Barcelona', 'Cuenca', 'Madrid', 'Valencia']

col1, col2, col3 = st.columns(3)
with col1:
    st.title('eLitur')  # puede que en PC quede mejor otra distribución
with col2:
    option = st.selectbox('Diócesis', sorted(diocesis), index=1)  # index depende de la ciudad
with col3:
    fecha = st.date_input('Día', value=date.today())

fecha_sep = str(fecha).split('-')
ano_hoy, mes_hoy, dia_hoy = fecha_sep[0], fecha_sep[1], fecha_sep[2]

# ya teniendo el año:
diocesis_url = {'Barcelona':'http://www.gcatholic.org/calendar/2022/ES-barc0-es.htm',
                'Cuenca':f'http://www.gcatholic.org/calendar/{ano_hoy}/ES-cuen1-es.htm',
                'Madrid':f'http://www.gcatholic.org/calendar/{ano_hoy}/ES-madr1-es.htm',
                'Valencia':f'http://www.gcatholic.org/calendar/{ano_hoy}/ES-vale0-es.htm'}

data = get_data(diocesis_url[option])
cod = mes_hoy + dia_hoy
#st.write(data[mes_hoy+dia_hoy]['fiestas'])

for fiesta, dic in data[cod]['fiestas'].items():
    color = normalcolor(dic['color'])
    with st.container():
        st.subheader(dic['nombre'])
        st.write(f"{dic['tipo']}")
        st.write(f"{data[cod]['tiempo']}. Color {color.upper()}.")
        st.image(f"{color}.png", output_format="png")
# FIN
