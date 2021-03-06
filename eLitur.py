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
            fiesta_colores = row.find('p', {'class':'indent'})
            fiesta = fiesta_colores.text.strip()
            spans = fiesta_colores.find_all('span')
            colores = []  # lista con todos los colores posibles para una fiesta (no para un día)
            for span in spans:
                if span.attrs['class'][0][-1] in ['g', 'w', 'v', 'r', 'p', 'u', 'b']:
                    colores.append(span.attrs['class'][0])
            for i, color in enumerate(colores):
                if color == 'feastg': colores[i] = 'limegreen'      # verde
                elif color == 'feastw': colores[i] = 'white'
                elif color == 'feastv': colores[i] = 'darkviolet'   # morado
                elif color == 'feastr': colores[i] = 'red'
                elif color == 'feastp': colores[i] = 'hotpink'      # rosa
                elif color == 'feastu': colores[i] = 'deepskyblue'  # azul
                elif color == 'feastb': colores[i] = 'black'
            # corrección (sólo en castellano):
            if tiempo == 'Triduo Pascual' or fiesta == 'Domingo de Pascua de la Resurrección del Señor':
                tipo = 'Solemnidad'
            # se añade al diccionario
            if cod not in data:
                data[cod] = {'dia_sem':dia_sem,
                             'dia_num':dia_num,
                             'mes':mes,
                             'año':ano,
                             'tiempo':tiempo,
                             'fiestas':{fiesta:{'nombre':fiesta, 'tipo':tipo, 'colores':colores}}}
            else:
                data[cod]['fiestas'][fiesta] = {'nombre':fiesta, 'tipo':tipo, 'colores':colores}
    return data

def normalcolor(original):  # pasa del color exacto al general (en castellano)
    if original == 'limegreen': nuevo = 'verde'
    elif original == 'white': nuevo = 'blanco'
    elif original == 'darkviolet': nuevo = 'morado'
    elif original == 'red': nuevo = 'rojo'
    elif original == 'hotpink': nuevo = 'rosa'
    elif original == 'deepskyblue': nuevo = 'azul'
    elif original == 'black': nuevo = 'negro'
    return nuevo


# CONFIGURACIÓN DE LA WEB
st.set_page_config(layout="wide", page_title="eLitur")

diocesis = ['Barcelona', 'Cuenca', 'Madrid', 'Valencia', 'Santiago de Compostela']

col1, col2, col3 = st.columns(3)
with col1:
    st.image('logo.png')  # puede que en PC quede mejor otra distribución
with col2:
    option = st.selectbox('Diócesis', sorted(diocesis), index=1)  # index depende de la ciudad
with col3:
    min_date, max_date = date(2020, 1, 1), date(2027, 12, 31)  # límite webscrapping
    fecha = st.date_input('Día', value=date.today(), min_value=min_date, max_value=max_date)

fecha_sep = str(fecha).split('-')
ano_hoy, mes_hoy, dia_hoy = fecha_sep[0], fecha_sep[1], fecha_sep[2]

# ya teniendo el año:
diocesis_url = {'Barcelona':'http://www.gcatholic.org/calendar/2022/ES-barc0-es.htm',
                'Cuenca':f'http://www.gcatholic.org/calendar/{ano_hoy}/ES-cuen1-es.htm',
                'Madrid':f'http://www.gcatholic.org/calendar/{ano_hoy}/ES-madr1-es.htm',
                'Valencia':f'http://www.gcatholic.org/calendar/{ano_hoy}/ES-vale0-es.htm',
                'Santiago de Compostela':f'http://www.gcatholic.org/calendar/{ano_hoy}/ES-ztia0-es.htm'
                }

data = get_data(diocesis_url[option])
cod = mes_hoy + dia_hoy

for fiesta, dic in data[cod]['fiestas'].items():
    colores = dic['colores']
    with st.container():
        st.subheader(dic['nombre'])
        st.write(f"{data[cod]['dia_sem']}, {data[cod]['dia_num']} de {data[cod]['mes'].lower()} de {data[cod]['año']}")
        st.write(f"{dic['tipo']}. {data[cod]['tiempo']}.")
        for color in colores:
            color = normalcolor(color)
            st.image(f"{color}.png", caption=color.upper(), output_format="png")
        # aquí iría posible separación
# FIN
