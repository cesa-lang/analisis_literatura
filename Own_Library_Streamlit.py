## biblioteca para el storytelling
import json
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import os
import pycountry

#rutas de los datos
amazon_path = "Communication Final Project/Data/amazonoficial1995-2024.json"
casa_del_libro_path = "Communication Final Project/Data/casa_del_libro_manual.json"
nobel_path = "Communication Final Project/Data/nobel_literature_1994_2024.json"
nyt_path = "Communication Final Project/Data/notable_books_nyt.json"
premios_cervantes_path = "Communication Final Project/Data/premios_cervantes.json"


#_______________________________________funcion para cargar los json_________________________________________________________________________#
def load_data(path):
    with open(path, 'r', encoding = 'utf-8') as f:
        json_data = json.load(f)
    return json_data

#DataFrames creados 
df_amazon = pd.DataFrame(load_data(amazon_path))
df_casalibro = pd.DataFrame(load_data(casa_del_libro_path))
df_nobel = pd.DataFrame(load_data(nobel_path))
df_nyt = pd.DataFrame(load_data(nyt_path))
df_cervantes = pd.DataFrame(load_data(premios_cervantes_path))

#___________________________________________funcion para normalizar los dataframe________________________________________________________________#

def normalize_df_bs(df):
    mapeo = {
        'titulo': 'titulo',
        'title': 'titulo',
        'Título': 'titulo',
        'nombre': 'titulo',
        'autor': 'autor',
        'author': 'autor',
        'escritor': 'autor',
        'name' : 'autor',
        'Autor': 'autor',
        'año': 'año',
        'year': 'año',
        'anio': 'año',
        'fecha': 'año',
        'Año': 'año',
        'publication_year': 'año'
    }
    df = df.rename(columns={k: v for k, v in mapeo.items() if k in df.columns})
    for col in ['titulo', 'autor', 'año']:
        if col not in df.columns:
            df[col] = None
    for col in ['titulo', 'autor']:
        df[col] = df[col].astype(str).str.lower().str.strip()
    return df

#DataFrame Normalizado
df_amazon = normalize_df_bs(df_amazon)
df_casalibro = normalize_df_bs(df_casalibro)
df_nobel = normalize_df_bs(df_nobel)
df_nyt = normalize_df_bs(df_nyt)
df_cervantes = normalize_df_bs(df_cervantes)

#_________________________________________________________funcion para mezclar los dataframe(2 o 3)________________________________________________________________#

def mix_df_3(amazon_df, nyt_df, casalibro_df):
    bestsellers_unidos = pd.concat(
        [amazon_df, nyt_df, casalibro_df],
        ignore_index=True
        )
    bestsellers_unidos = bestsellers_unidos.sort_values('año', ascending=False)
    return bestsellers_unidos

# funcion para mezclar los dataframe 2
def mix_df_2(amazon_df, nyt_df):
    bestsellers_unidos = pd.concat(
        [amazon_df, nyt_df],
        ignore_index=True
        )
    bestsellers_unidos = bestsellers_unidos.sort_values('año', ascending=False)
    return bestsellers_unidos

df_all_bs = mix_df_3(df_amazon, df_nyt, df_casalibro)
df_eng_bs = mix_df_2(df_amazon, df_nyt)
df_all_p = mix_df_2(df_nobel, df_cervantes)


#______________________________________funcion para ver cuantos bestsellers tiene cada autor________________________________________________________#
def new_df_number_bs(df_bs):
    conteo_bestsellers = (
        df_bs['autor']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'autor', 'autor': 'autor'})
    )
    return conteo_bestsellers

#DataFrame de los autores con su cantidad de bestsellers
count_all = new_df_number_bs(df_all_bs)

count_eng = new_df_number_bs(df_eng_bs)

count_sp = new_df_number_bs(df_casalibro)

#___________________________________________funcion para mezclar los dataframe__________________________________________________________________________________________________________________________________#

def mix_df(df_all_p, count_all):
    df_merged = df_all_p.merge(
        count_all.rename(columns={'autor': 'autor', 'count': 'count'}),
        on='autor',
        how='left'
    )
    df_merged['count'] = df_merged['count'].fillna(0).astype(int)
    return df_merged

#DataFrame de los premiados con su cantidad de bestsellers

relacion_premio_bs_all = mix_df(df_all_p, count_all)

relacion_premio_bs = mix_df(df_nobel, count_eng)

relacion_cervantes = mix_df(df_cervantes, count_all)

#______________________________________funcion por ciento de ganadores de bestsellers en ganadores nobel_______________________________________________________________________________________#

def average_premios_bs(df_premios):
    total = len(df_premios)
    autores_con_bs = df_premios[df_premios['count'] > 0].shape[0]
    
    porcentaje = (autores_con_bs / total) * 100
    return round(porcentaje, 2)

v1 = average_premios_bs(relacion_premio_bs_all)

v2 = average_premios_bs(relacion_premio_bs)


#__________________________________________________________funcion para filtar el data frame de las relaciones por lo que tienen bestsellers_______________________________________________________________________________________________________________________________________________________#

def filtter_bs(df):
    return df[df['count'] > 0].copy()

relacion_filtrada = filtter_bs(relacion_premio_bs)


#___________________________________________________________grafica para autores premiados y su cantidad de bestsellers________________________________________________________________________#

def graficar_autores_con_bestsellers(df_relacion):
        
    df = df_relacion.copy()
    df['año'] = df['año'].astype(int)  #asegurar q sea un entero
    df['count'] = df['count'].fillna(0).astype(int)

    df['barra'] = df['count'].apply(lambda x: x if x > 0 else 0.0001)
    df = df.sort_values('año')

    autores_ordenados = df.drop_duplicates('autor', keep='first')['autor'].tolist()

    df['autor'] = pd.Categorical(df['autor'], categories=autores_ordenados, ordered=True)
        
    fig = px.bar(
        df,
        x='barra',
        y='autor',
        orientation='h',
        color='count',
        color_continuous_scale='Viridis',
        hover_data={'año': True, 'nationality': True, 'language': True, 'count': True, 'barra': False},
        labels={
            'barra': 'Número de Bestsellers',
            'autor': 'Autor',
            'año': 'Año del Premio',
            'count': 'Bestsellers'
            },
        height=700,
        )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>" +
        "Bestsellers: %{customdata[3]}<br>" +
        "Premio: %{customdata[0]}<br>" +
        "Nacionalidad: %{customdata[1]}<br>" +
        "Idioma: %{customdata[2]}<extra></extra>"
        )
    fig.update_layout(
        coloraxis_colorbar=dict(title="Nº Bestsellers"),
        yaxis_title="Autor (ordenado por año del premio)",
        xaxis_title="Número de Bestsellers"
    )

    st.plotly_chart(fig, use_container_width=True)
        
    
#________________________________________________________________funcion de evolucion en el tiempo de la cantidad de bestsellers_________________________________________________________________#
def grafico_lineal_bs(df_bestsellers):
    df = df_bestsellers.copy()
    df = df[~df['año'].isin([2024, 2025])]
    count_by_year = df['año'].value_counts().reset_index()
    count_by_year.columns = ['año', 'cantidad']
    count_by_year = count_by_year.sort_values('año')

    fig = px.line(
        count_by_year,
        x='año',
        y='cantidad',
        title='<b>Tendencia Anual de Bestsellers</b>',
        labels={'año': 'Año', 'cantidad': 'Número de Bestsellers'},
        markers=True,
        line_shape='spline',
        template='plotly_white',
        height=500
        )

    fig.update_layout(
        hovermode='x unified',
        xaxis=dict(tickmode='linear', dtick=1),
        yaxis_title='Número de libros',
        title_x=0.3
    )
    max_year = count_by_year.loc[count_by_year['cantidad'].idxmax()]
    fig.add_annotation(
        x=max_year['año'],
        y=max_year['cantidad'],
        text=f"Máximo: {max_year['cantidad']} en {max_year['año']}",
        showarrow=True,
        arrowhead=1
    )
    st.plotly_chart(fig, use_container_width=True)
        
#________________________________________________________funcion para ver la cantidad de bestsellers que tienen cada autor bestseller_____________________________________________________________________#
def num_bs_per_autor(df_bestsellers):
    bestsellers_por_autor = df_bestsellers['autor'].value_counts().reset_index()
    bestsellers_por_autor.columns = ['autor', 'cantidad']
    bestsellers_por_autor = bestsellers_por_autor.sort_values('cantidad', ascending=False)
    bestsellers_por_autor = bestsellers_por_autor[bestsellers_por_autor["autor"] != "j. k. rowling"]

    col1, col2 = st.columns(2)
    with col1:
        top_n = st.slider(
            "Mostrar top N autores",
            min_value=5,
            max_value=50,
            value=15,
            help="Selecciona cuántos autores quieres visualizar"
        )
    with col2:
        min_bestsellers = st.slider(
            "Mínimo de bestsellers por autor",
            min_value=1,
            max_value=int(bestsellers_por_autor['cantidad'].max()),
            value=2,
            help="Filtrar autores con al menos X bestsellers"
        )

    df_filtrado = bestsellers_por_autor[
        (bestsellers_por_autor['cantidad'] >= min_bestsellers)
        ].head(top_n)

    fig = px.bar(
        df_filtrado,
        x='cantidad',
        y='autor',
        orientation='h',
        title=f'<b>Top {top_n} Autores con más Bestsellers</b>',
        labels={'autor': 'Autor', 'cantidad': 'Número de Bestsellers'},
        color='cantidad',
        color_continuous_scale='Bluered',
        height=600 + (top_n * 10)  # Ajuste dinámico de altura
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title="Número de libros en listas de bestsellers",
        title_x=0.3,
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)
    
#________________________________________funcion para grafico que dice los libros que mas aparecen en los listados de los bestsellers______________________________________________________________________________________________#    
def counter_books(df_bestsellers):
    libros_populares = df_bestsellers.groupby(['titulo', 'autor', 'Género']).size().reset_index(name='apariciones')
    libros_populares = libros_populares.sort_values('apariciones', ascending=False)

    # 2. Gráfico de los top N libros
    top_n_libros = st.slider("Selecciona cuántos libros mostrar:", 5, 20, 10)

    fig_libros = px.bar(
        libros_populares.head(top_n_libros),
        x='apariciones',
        y='titulo',
        orientation='h',
        color='autor',
        title=f'<b>Top {top_n_libros} Libros con más apariciones en listas</b>',
        labels={'Título': '', 'Apariciones': 'Veces en listas de bestsellers'},
        hover_data=['Género'],
        height=500 + (top_n_libros * 15)  # Ajuste dinámico de altura
    )

    fig_libros.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(fig_libros, use_container_width=True)
    
    
#_____________________________________funcion para ver los autores cuantos bestsellers tienen antes y despues de su premio nobel_______________________________________________________________________________________#

def before_and_after(filtter_jusy_nonel_with_bs, df_bestsellers):
    autores_nobel = filtter_jusy_nonel_with_bs['autor'].unique()
    
    # Widget de selección con search
    autor_seleccionado = st.selectbox(
        "Selecciona un autor Nobel:",
        options=sorted(autores_nobel),
        format_func=lambda x: f"{x} ({filtter_jusy_nonel_with_bs[filtter_jusy_nonel_with_bs['autor']==x]['año'].values[0]})"
    )
    
    # Datos del autor seleccionado
    datos_autor = filtter_jusy_nonel_with_bs[filtter_jusy_nonel_with_bs['autor'] == autor_seleccionado].iloc[0]
    año_nobel = datos_autor['año']
    
    # Mostrar imagen del autor
    ruta_imagen = None
    # Buscar imagen en diferentes formatos
    for ext in ['.jpg', '.jpeg', '.png']:
        ruta_prueba = f"Communication Final Project/Autores/{autor_seleccionado} ({año_nobel}){ext}"
        if os.path.exists(ruta_prueba):
            ruta_imagen = ruta_prueba
            break
    
    if ruta_imagen:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(ruta_imagen, width=150, caption=autor_seleccionado)
        with col2:
            st.write(f"### {autor_seleccionado}")
            st.write(f"**Premio Nobel:** {año_nobel}")
    else:
        st.write(f"## {autor_seleccionado} (Premio Nobel {año_nobel})")
        st.warning("No se encontró imagen del autor")
    
    # Filtrar bestsellers del autor (insensible a mayúsculas/minúsculas)
    libros_autor = df_bestsellers[
        (df_bestsellers['autor'].str.lower() == autor_seleccionado.lower())
    ].sort_values('año')
    
    # Gráfico de evolución
    if not libros_autor.empty:
        evolucion = libros_autor['año'].value_counts().reset_index()
        evolucion.columns = ['año', 'cantidad']
        evolucion = evolucion.sort_values('año')
        
    
        fig = px.area(
            evolucion,
            x='año',
            y='cantidad',
            title=f'<b>Bestsellers antes/después del Nobel {año_nobel}</b>',
            labels={'año': 'Año', 'cantidad': 'N° Bestsellers'},
            markers=True,
            line_shape='spline'
        )
        
        fig.add_vline(
            x=año_nobel,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Nobel {año_nobel}",
            annotation_position="top right"
        )
    
        fig.add_vrect(
            x0=año_nobel-5,
            x1=año_nobel+5,
            fillcolor="lightgray",
            opacity=0.2,
            annotation_text="Ventana de análisis",
            annotation_position="top left"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # metrics
        col1, col2, col3 = st.columns(3)
        antes = libros_autor[libros_autor['año'] < año_nobel]
        despues = libros_autor[libros_autor['año'] >= año_nobel]
        
        with col1:
            st.metric("Total bestsellers", len(libros_autor))
        with col2:
            st.metric("Antes del Nobel", len(antes))
        with col3:
            cambio = len(despues) - len(antes)
            st.metric("Después del Nobel", len(despues), delta=f"{'+' if cambio>=0 else ''}{cambio}")
        
        # Tabla de libros expandible
        with st.expander(f"📚 Ver todos los bestsellers de {autor_seleccionado}"):
            columnas_disponibles = ['Título', 'titulo', 'title', 'año', 'year', 'Género']
            columnas_a_mostrar = [col for col in columnas_disponibles if col in libros_autor.columns]
            
            st.dataframe(
                libros_autor[columnas_a_mostrar],
                column_config={
                    "año": st.column_config.NumberColumn("Año", format="%d"),
                    "year": st.column_config.NumberColumn("Año", format="%d")
                },
                hide_index=True,
                use_container_width=True
            )
            
    else:
        st.warning(f"No se encontraron bestsellers para {autor_seleccionado} en los datos")


#____________________________________________funcion para ver si el idioma esta presente en estas relaciones_______________________________________________#

def mapa_calor_nobel(df_nobel):
    df_nobel['pais_clean'] = df_nobel['nationality'].str.split('(').str[0].str.strip()
    
    # Correcciones manuales para coincidencia con pycountry
    replacements = {
        'France/China': 'China',
        'United Kingdom/Trinidad and Tobago': 'United Kingdom',
        'France/Mauritius': 'France',
        'Tanzania/United Kingdom': 'Tanzania',
        'South Korea': 'Korea, Republic of',
        'Congo': 'Congo, Republic of the'
    }
    df_nobel['pais_clean'] = df_nobel['pais_clean'].replace(replacements)
    
    # Contar premios por país
    conteo_paises = df_nobel['pais_clean'].value_counts().reset_index()
    conteo_paises.columns = ['country', 'premios']
    
    # Generar códigos de país ISO Alpha-3
    def get_iso3(country_name):
        try:
            return pycountry.countries.search_fuzzy(country_name)[0].alpha_3
        except:
            return None
    
    conteo_paises['iso_alpha'] = conteo_paises['country'].apply(get_iso3)
    
    # Crear mapa de calor
    fig = px.choropleth(conteo_paises,
                        locations="iso_alpha",
                        color="premios",
                        hover_name="country",
                        hover_data=["premios"],
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title="Concentración de Premios Nobel de Literatura por País (1994-2024)",
                        projection="natural earth")
    
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    
    st.plotly_chart(fig,use_container_width = True)

# Funciones de sección de gráficos interactivos:
#______________________________________________________Graficar conteo de autores en Amazon_______________________________________________
def amazon_authors_counting(amazon_df = df_amazon):
    
    author_count = {}
    for author in amazon_df["autor"]:
        if author not in author_count:
            counter = 0
            for name in amazon_df["autor"]:
                if name == author:
                    counter += 1
            author_count[author] = counter

    authors_count_df = pd.DataFrame(author_count.keys(),columns = ["Autores"])
    authors_count_df["Apariciones"] = author_count.values()
    authors_count_df = authors_count_df.sort_values(by = "Apariciones",ascending = False)
    authors_count_df = authors_count_df[authors_count_df['Autores'] != "j. k. rowling"]

    selection = st.slider(label = "Selecciona cuántos autores con más libros en Amazon quieres ver:",min_value = 1,max_value = 20,value = 5)

    fig = px.bar(data_frame = authors_count_df.head(selection),
                 x = authors_count_df['Apariciones'].head(selection),
                 y = authors_count_df["Autores"].head(selection),
                 orientation = "h",
                 title = "Libros en Amazon por n primeros autores",
                 hover_data = ["Autores","Apariciones"])
    
    st.plotly_chart(fig,use_container_width = True)
    
#_____________________________________________Graficar intersección de los n primeros autores premiados con sus bestsellers___________________________________________________________

def graficar_n_autores_con_bestsellers(df_relacion):
        
    df = df_relacion.copy()
    df['año'] = df['año'].astype(int)  #asegurar q sea un entero
    df['count'] = df['count'].fillna(0).astype(int)

    df['barra'] = df['count'].apply(lambda x: x if x > 0 else 0.0001)

    autores_ordenados = df.drop_duplicates('autor', keep='first')['autor'].tolist()

    df['autor'] = pd.Categorical(df['autor'], categories=autores_ordenados, ordered=True)
    df = df.sort_values(by = "count",ascending = False)
    df.loc[df["autor"] == "mario vargas llosa","count"] = 8
    selection = st.slider(label = "Elige la cantidad de autores a revisar:",min_value = 1,max_value = 30,value = 8)
    
    fig = px.bar(
        df.head(selection),
        x='barra',
        y='autor',
        orientation='h',
        color='count',
        color_continuous_scale='Viridis',
        hover_data={'año': True, 'nationality': True, 'language': True, 'count': True, 'barra': False},
        labels={
            'barra': 'Número de Bestsellers',
            'autor': 'Autor',
            'año': 'Año del Premio',
            'count': 'Bestsellers'
            },
        height=700,
        )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>" +
        "Bestsellers: %{customdata[3]}<br>" +
        "Premio: %{customdata[0]}<br>" +
        "Nacionalidad: %{customdata[1]}<br>" +
        "Idioma: %{customdata[2]}<extra></extra>"
        )
    fig.update_layout(
        coloraxis_colorbar=dict(title="Nº Bestsellers"),
        yaxis_title="Autor (ordenado por cantidad de bestsellers)",
        xaxis_title="Número de Bestsellers"
    )

    st.plotly_chart(fig, use_container_width=True)

#__________________________________________________Conteo de Nobels para N nacionalidades en orden_______________________________________________________

def nat_counting(df = df_nobel):

    nationalities_count = {"Nacionalidad":[],"Conteo":[]}
    
    for i in df["nationality"]:
        for nation in i.split("/"):
            if nation in nationalities_count["Nacionalidad"]:
                nationalities_count["Conteo"][nationalities_count["Nacionalidad"].index(nation)] += 1
            else:
                nationalities_count["Nacionalidad"].append(nation)
                nationalities_count["Conteo"].append(1)

    traduced = pd.DataFrame({"Nacionalidad":["Reino Unido","Francia","China","Polonia","Alemania","Estados Unidos","Austria","Japón","Portugal","Italia","Irlanda","Hungría","Trinidad y Tobago","Turquía","Mauricio"]})
    traduced.index = [i for i in range(15)]
    nationalities_count = pd.DataFrame(nationalities_count).sort_values(by = "Conteo",ascending = False)
    nationalities_count.index = [i for i in range(25)]
    new_nat_count = pd.concat([nationalities_count['Conteo'],traduced],axis = 1)
    selection = st.slider("Escoge un número de nacionalidades a visualizar",min_value = 1,max_value = 15,value = 5)

    fig = px.bar(data_frame = new_nat_count.head(selection),
                  x = "Nacionalidad",
                  y = "Conteo",
                  color = "Conteo",
                  hover_data = {"Conteo":True,"Nacionalidad":False})
    
    st.plotly_chart(fig,use_container_width = True)

#_______________________________________________Generos literarios más populares en The New York Times_________________________________________________________

def nyt_genders(df = df_nyt):
    
    genders_count = {"Estilo":[],"Conteo":[]}
    for gender in df["Género"]:
        if gender in genders_count["Estilo"]:
            genders_count["Conteo"][genders_count["Estilo"].index(gender)] += 1
        else:
            genders_count["Estilo"].append(gender)
            genders_count["Conteo"].append(1)
    
    count_df = pd.DataFrame(genders_count)
    count_df = count_df[count_df["Estilo"] != "nonfiction"].sort_values(by = "Conteo",ascending = False).head(5)
    count_df.index = [x for x in range(5)]
    traduced = pd.DataFrame({"Sector":["Ficción","Biografía","Historia","Memorias","Historias cortas"]})
    new_df = pd.concat([traduced,count_df["Conteo"]],axis = 1)

    fig = px.bar(data_frame = new_df,
                 x = new_df["Sector"],
                 y = new_df["Conteo"],
                 hover_data = {"Sector":False,"Conteo":True},
                 color_continuous_scale = "Viridis")
    
    st.plotly_chart(fig,use_container_width = True)

#__________________________________________________Conteo de los premios Cervantes por nacionalidad______________________________________________________

def cervantes_counting(df = df_cervantes):

    nat_count = {"País":[],"Conteo":[]}
    for nacionalidad in df["nationality"]:
        if nacionalidad in nat_count["País"]:
            nat_count["Conteo"][nat_count["País"].index(nacionalidad)] += 1
        else:
            nat_count["País"].append(nacionalidad)
            nat_count["Conteo"].append(1)

    nat_count
    data = pd.DataFrame(nat_count).sort_values(by = "Conteo",ascending = False).head(5)
    data = data[data['País'] != "Perú"]
    data = pd.concat([data,pd.DataFrame({"País":["Otros"],"Conteo":[4]})],axis = 0)
    data.index = [x for x in range(5)]

    fig = px.pie(data,
                 values = data["Conteo"],
                 names = data['País'],
                 hover_data = ["Conteo"])

    st.plotly_chart(fig,use_container_width = True)