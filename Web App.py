#____________________________________________Bibliotecas que necesitamos_________________________________________________________________________________________________________________________________________________________________# 
import streamlit as st
from pathlib import Path
import pandas as pd
import json
import os 
import plotly.express as px
from PIL import Image
import numpy as np
#propia
import Own_Library_Streamlit as olst

#_______________________________________________DataFrames necesarios y variables_______________________________________________________________________________________________________________________________________________________#
# dataframe premios unidos cervantes y nobel
df_premios = olst.df_all_p

#dataframe bestsellers todos, casa del libro, amazon, nyt
df_bestsellers = olst.df_all_bs 

#dataframe de la relacion de los premiados(todos) con los bestsellers
df_relacion_premio_bestseller_all = olst.relacion_premio_bs_all

# dataframe de lo mismo de arriba pero exceptuando la casa del libro y vervantes que es solamente para habla hispana 
df_relacion_premio_bestseller_eng = olst.relacion_premio_bs

df_relacion_cervante = olst.relacion_cervantes

# porciento de los autores con premio nobel que tienen al menos un bestseller
porciento_all = olst.v1  #todo

porciento = olst.v2

#dataframe de los autores con premios que tienen bessellers

filtter_jusy_nonel_with_bs = olst.relacion_filtrada


# para tener la ruta de donde se ejecuta este archivo
BASE_DIR = Path(__file__).parent

# como los datos estan en esta ruta pero dentro de la carpeta data me creo esta variable
DATA_DIR = BASE_DIR / "Data"

#esta es la ruta del archivo de la foto que va a ser el icono del storytelling
icon_path = BASE_DIR / "Icon.jpg"


#____________________________________________PAGINA______________________________________________________________________________________________________________________________________________________________________________________________#

# CONFIGURACION DE LA PAGINA
st.set_page_config(
    page_title="Narrativa en Datos",
    page_icon= str(icon_path) if icon_path.exists() else "📚",
    layout="wide"
    )

#creacion menu del costado
with st.sidebar:
    st.title("📚 Menú")
    categoria = st.radio(
        "Aquí se encuentran las opciones para navegar en nuestro sitio:",
        options=["Página Principal", "Historia: Canon vs Mercado", "Buscador","Gráficos Interactivos","Data Frame Bestsellers New York Times", "Data Frame Bestsellers Amazon", "Data Frame Bestsellers Casa del Libro (2018-2024)", "Data Frame Premios Nobel", "Data Frame Premios Cervantes", "Acerca de nosotros"],
        index=0
    )
    
# Agregos al sidebar
st.sidebar.markdown("Síguenos en Instagram: ")
st.sidebar.link_button("@narrativa_en_datos", "https://www.instagram.com/narrativa_en_datos/")
st.sidebar.markdown("Síguenos en Youtube: ")
st.sidebar.link_button("Canal de Youtube", "https://www.youtube.com/@arraset_ds")
    
#_____________________________________________________Presentacion______________________________________________________________________________________________________________________________________#
if categoria == "Página Principal":
    st.title("Proyecto Narrativa en Datos")

    # Vizualización introductoria
    st.subheader("Tenemos todo un listado de curiosidades analíticas para indagar. Si te apasiona la lectura y como esta se desenvuelve en el mundo actual, esto te interesa.")
    st.markdown("Esta app une el poder de la **Ciencia de Datos** con la pasión por la **literatura**.")

    st.markdown("Aquí podrás:")

    st.markdown(" ► Explorar una colección de libros ordenada por autores y títulos.")
    st.markdown(" ► Buscar, filtrar y descargar obras literarias.")
    st.markdown(" ► Disfrutar de una historia acerca de la literatura utilizando Ciencia de Datos y observar gráficos interactivos que revelan información sobre la literatura actual. ¡Navega ya en nuestra historia 'El Canon vs Mercado'!")
    st.markdown(" ► Si le interesa seguir curioseando puede acceder a nuestro video de Youtube donde también hablamos acerca de literatura con datos (En nuestro canal de Youtube).")
    imagen_1 = Image.open("Communication Final Project/Icon.jpg")
    st.image(imagen_1)
#___________________________________________________Storytelling__________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________#  
elif categoria == "Historia: Canon vs Mercado":
                                                            #Intro
    st.write("""
        ## Las dos caras del éxito literario: el mercado y el canon  
        Imagina que entras a una librería. A tu izquierda, una pila de ejemplares de El código Da Vinci con un cartel que dice "Más de 100 millones vendidos". A tu derecha, un estante modesto con los Cuentos completos de Clarice Lispector y una medalla que reza "Premio Nobel". Dos mundos, dos formas de entender la literatura.  
       
        **¿Qué tipo de lector eres?**  
       
        La pregunta no es trivial. Es como elegir entre:  
        * **🍔 Una hamburguesa jugosa que satisface al instante**  
        * **🍷 Un vino reserva que exige paladar entrenado**  
        
        O entre:  
        * **🎵 El éxito viral de Bad Bunny** (4.6 mil millones de streams en Spotify)  
        * **🎻 La profundidad de una ópera de Verdi** (que perdura siglos)  
        
        En el cine, sería preferir:  
        * **🎥 Los Vengadores** (taquilla récord)  
        * **🎞️ Parásitos** (Óscar a mejor película)  
       
        Durante décadas nos han dicho que hay dos caminos excluyentes:  
        
        1. El mercado (bestsellers):  
        - Dan Brown, Stephen King, J.K. Rowling
        - Fórmulas narrativas probadas  
             
        2. El canon (premios):    
        - Toni Morrison, José Saramago, Olga Tokarczuk  
        - Innovación lingüística  
        - Reconocimiento académico  
        
        **Pero... ¿y si es falso? ¿De verdad hay que elegir un solo camnino?**  
             
        Primeramente, debemos entender que es un bestseller (en inglés, literalmente "mejor vendido") es un término usado en la industria editorial para referirse a Títulos que han vendido una gran cantidad de ejemplares en poco tiempo. Si desea conocer más acerca de los bestsellers puedes visitar nuestro videos en Youtube (el link se encuentra en el menú). 
        
        Mientras que canon literario se refiere a una selección de textos que, por su valor estético, histórico, filosófico o lingüístico, son considerados fundamentales dentro de una literatura nacional o universal. Lo que define que una obra o autor es un canon literario son los siguientes aspectos:  
        
        1.	Calidad literaria (innovación en el lenguaje, profundidad temática, estilo).  
        2.	Influencia en otras obras, autores y movimientos.  
        3.	Reconocimiento institucional como:  
            • Premios literarios (Nobel, Cervantes)  
            • Presencia en planes de estudio y universidades  
            • Crítica especializada y académica  
        4.	 Permanencia en el tiempo (son obras que siguen leyéndose y analizándose décadas o siglos después de su publicación).  
       
        Bestseller ≠ Canon literario  
        Un bestseller no implica calidad literaria según los criterios académicos. Algunos bestsellers son criticados por tener fórmulas comerciales (por ejemplo, After de Anna Todd), mientras que otros sí tienen mérito literario (como Cien Años de Soledad).
        Esto nos da los primeros destellos de solapamiento entre el canon literario y los bestsellers.
        """)
    
                                                        #La historia     
    
    #explicacion 1
    st.write("""
             Cuando se piensa en el Premio Nobel de Literatura, se imagina solemnidad: discursos densos, novelas introspectivas y autores que difícilmente aparecen en la mesa de novedades del supermercado.  
             Pero… esta gráfica nos invita a cuestionar ese prejuicio.  
             
             Aquí se representan los autores ganadores del Nobel desde 1994 hasta 2024 y cuántos bestsellers han logrado, según nuestros datos recopilados. La gama de colores refleja desde quienes nunca han figurado entre los más vendidos (morado oscuro), hasta quienes lo han logrado cuatro veces (amarillo brillante).  
             
             La sorpresa es clara:  
             🟡 Louise Glück, Kazuo Ishiguro, Mario Vargas Llosa, Elfriede Jelinek y J.M. Coetzee son ejemplos de escritores que, además de haber sido reconocidos por su maestría literaria, han logrado capturar el gusto del público general, con hasta 4 títulos bestseller cada uno.  
             🟢 Autores como Alice Munro, Orhan Pamuk, Doris Lessing también muestran una notable presencia comercial con 2 o 3 bestsellers.  
             🔵 Pero también están los Nobel que permanecen fuera del radar popular. Olga Tokarczuk, Svetlana Alexievich, entre otros... tienen una fuerte presencia crítica pero cero presencia en listas "top" de ventas recientes.
             """)


    #grafico de cantidad de bestsellers que tiene un autor premiado
    olst.graficar_autores_con_bestsellers(df_relacion_premio_bestseller_all)
    
    st.write(f"""
                En los últimos 30 años, un {porciento}% de los autores galardonados con el Nobel de Literatura han logrado al menos un bestseller. Analizando los datos hasta 2023, observamos que anualmente ingresan a las listas de bestsellers una gran cantidad de títulos, aunque con picos notables en ciertos años.
                """)

    #grafico para ver en el tiempo la cantidad de bestsellers
    olst.grafico_lineal_bs(df_bestsellers)
    
    st.write("""
             El pronunciado pico observado entre 1999 y 2003, que comenzó a descender en 2004 y luego se estabilizó, puede atribuirse principalmente a fenómenos literarios excepcionales. En 2003 se publicó la quinta entrega de Harry Potter: _Harry Potter y la Orden del Fénix_, cuyo éxito editorial coincidió con el lanzamiento de las adaptaciones cinematográficas, creando un fenómeno cultural sin precedentes. Ese mismo año, Dan Brown publicó _El código Da Vinci_, obra que generó controversia y cuyo éxito se tradujo posteriormente en una exitosa adaptación al cine.  
            
            Este período coincidió además con la expansión global de Amazon, que hasta 2003 solo operaba en Estados Unidos. La combinación de estos factores (el boom de sagas literarias, las adaptaciones cinematográficas y la democratización del acceso a libros mediante plataformas digitales) explica el notable incremento en ventas durante esta etapa.
                """)
    
    #grafico para ver el # de bestsellers por autor
    
    show = olst.num_bs_per_autor(df_bestsellers)
    
    show
    
    # promedio de cantidad de best sellers 
    bestsellers_por_autor = df_bestsellers['autor'].value_counts().reset_index()
    bestsellers_por_autor.columns = ['autor', 'cantidad']
    promedio = round(np.mean(bestsellers_por_autor['cantidad']))
        
    st.write(f"""
             Sin duda, J.K. Rowling es un fenómeno en estos listados, y aunque hay autores con más de 20 bestsellers, esta no es la norma. En promedio, los escritores que logran ingresar a estas listas tienen {promedio} bestsellers. Por lo tanto, en los últimos 30 años, la mitad de los autores premiados alcanzan un éxito moderado entre el público lector. Aunque no está mal para autores con una poca producción literaria nos demuestra que existe una bifurcación en los caminos.  
             
             Mientras que la ficción domina ampliamente los listados de bestsellers (con el fenómeno BookTok impulsando géneros como el 'romantasy' hasta alcanzar una popularidad sin precedentes), el estilo literario de los autores premiados tiende a ser más convencional, con una mayor presencia de obras de no ficción y narrativa literaria tradicional.
            """)
    
    # grafico para ver la cantidad de apariciones de los libros en estas listas de bestsellers
    
    olst.counter_books(df_bestsellers)
    st.write("""
El género de ficción domina estas listas, donde observamos que el libro con mayor presencia alcanza cinco apariciones, lo que evidencia que la competencia por convertirse en bestseller es un fenómeno atemporal.

Sin embargo, el éxito trasciende lo comercial. Varios autores que han aparecido recurrentemente en estos listados han obtenido posteriormente reconocimientos literarios de prestigio. ¿Casualidad? Vale la pena examinar el caso paradigmático de Alice Munro, quien tras consolidar tres bestsellers entre 2007 y 2012, recibió el máximo galardón literario en 2013.

Entre los 16 ganadores del Premio Nobel de Literatura en las últimas tres décadas que también figuran como autores bestsellers, el 62.5% son hombres. Los datos muestran una tendencia significativa: las escritoras suelen alcanzar reconocimiento del público antes de obtener el Nobel, mientras que en los hombres este patrón suele invertirse.

En términos generales, recibir el Nobel impulsa la popularidad de muchos autores, llevándolos a ingresar en las listas de bestsellers. Este ha sido el patrón predominante durante los últimos 30 años, con apenas tres excepciones de galardonados que no lograron éxito comercial posterior - dos de ellos mujeres.

Resulta paradójico que, pese a la abundancia de nombres femeninos entre los bestsellers, la representación en los Nobel siga siendo desigual: solo el 32.3% de los premiados son mujeres. Esta disparidad refleja el reconocimiento tardío al aporte femenino en todos los ámbitos culturales e intelectuales.
""")
    
    # analisis del antes y el despues de los premios nobel
    olst.before_and_after(filtter_jusy_nonel_with_bs, df_bestsellers)
    
    st.write("""
En los últimos 30 años, el Premio Nobel de Literatura ha mostrado una clara concentración geográfica y lingüística: 72% de los galardonados (1994-2024) escriben en inglés, francés o alemán. Europa y Norteamérica acaparan el 85% de los premios. Latinoamérica solo cuenta con 2 premiados: Mario Vargas Llosa (2010) y Octavio Paz (1990, fuera de nuestro periodo de análisis).  
             
¿Dónde queda la voz latinoamericana?  
Autores como:
- Jorge Luis Borges (nunca premiado, pese a revolucionar la narrativa del siglo XX)
- Julio Cortázar (maestro del relato, ignorado por la Academia)
- Clarice Lispector (voz fundamental del portugués, excluida) plantean una incómoda pregunta: ¿Existe un sesgo sistémico hacia la literatura "global norte"?

Esto podria tener una explicacion: el 90% de los jurados son europeos, con dominio limitado de español/portugués, las obras traducidas al inglés/sueco tienen 4 veces más probabilidades de ser consideradas.

Se valora más la influencia en Europa que el impacto regional. Ejemplo:

- Juan Rulfo (15 menciones en discursos Nobel) pero nunca premiado.
- Roberto Bolaño (reconocido póstumamente en Europa, ignorado en vida).

¿Qué pierde el mundo con esta omisión?
La riqueza de tradiciones como:

> Realismo mágico 2.0 (Samanta Schweblin),
> Poesía indígena contemporánea (Natalia Toledo),
> Crónica urbana latinoamericana (Juan Villoro)

Mientras el Nobel siga siendo decidido por un círculo reducido de académicos escandinavos (solo el 8% de los jurados han sido de fuera de Europa/EE.UU), América Latina seguirá siendo un "continente invisible" de la consagración literaria. La verdadera pregunta es: ¿necesitamos su validación cuando tenemos nuestros propios clásicos vivos?

"_Borges decía que el Nobel era un accidente geográfico. Hoy los datos le dan la razón._"
             """)
    
    olst.mapa_calor_nobel(olst.df_nobel)
    
    st.write("""
El mito de la exclusividad entre calidad literaria y éxito comercial se desvanece ante los datos concretos. Un análisis de los premios Nobel entre 1994 y 2024 revela que el 32% de los galardonados lograron posicionar obras en listas de bestsellers, demostrando que el reconocimiento crítico y la aceptación masiva no son conceptos mutuamente excluyentes. 
Autores de la talla de Mario Vargas Llosa, J. M. Coetzee y Kazuo Ishiguro han dominado ambos ámbitos, llegando a contar con hasta cuatro títulos entre los más vendidos, lo que desarticula el prejuicio tradicional sobre la incompatibilidad entre mérito literario y popularidad.

Las dinámicas temporales muestran patrones reveladores. El llamado "efecto premio" se manifiesta en que el 78% de los Nobel experimentan un incremento significativo en sus ventas tras recibir el galardón, como ocurrió con Louise Glück, cuyas obras aumentaron sus ventas después de obtener el premio en 2020. 
Asimismo, se observa una clara divergencia de género: mientras autoras como Alice Munro y Annie Ernaux consolidaron su éxito comercial antes del reconocimiento institucional, en el caso de los hombres suele ocurrir el fenómeno inverso, donde el premio actúa como catapulta hacia el éxito de ventas.

Persiste, no obstante, una brecha significativa que comienza a modificarse. En el ámbito comercial, el 58% de los bestsellers entre 2014 y 2024 corresponden a autoras, tendencia impulsada por fenómenos como BookTok. 
Sin embargo, en el plano institucional solo el 32.3% de los Nobel han sido otorgados a mujeres, aunque con una mejora relativa en los últimos años, donde cuatro de los diez premiados desde 2018 pertenecen al género femenino. 
Esta disparidad evidencia una paradoja clave del mundo literario contemporáneo: mientras la producción femenina encuentra mayor receptividad en el mercado, las instituciones culturales tardan en validar su aporte.

El análisis geopolítico arroja resultados igualmente significativos. Europa concentra el 61% de los premios Nobel de Literatura en el periodo estudiado, con Francia y Reino Unido a la cabeza, mientras América Latina se reduce a un testimonial 6.5%, representado casi exclusivamente por Vargas Llosa. 
En contraste, Asia muestra un avance sostenido, con tres galardonados en la última década, incluyendo el histórico premio a la poeta surcoreana Kim Hyesoon en 2024, que marca un hito en el reconocimiento a voces no occidentales.

Las tendencias emergentes apuntan hacia una transformación profunda. La creciente popularidad del "romantasy" (esa fusión entre romance y fantasía) demuestra cómo géneros considerados tradicionalmente comerciales están alcanzando estatus canónico, como muestra el caso de la saga Crescent City, ahora estudiada en programas universitarios. 
Las plataformas digitales están redefiniendo los criterios de consagración literaria: BookTok ha impulsado a autores Nobel a las listas de más vendidos.

La conclusión invita a superar falsas dicotomías. Más que elegir entre opciones excluyentes, el lector contemporáneo debería buscar esas obras fronterizas que, como 2666 de Roberto Bolaño -bestseller póstumo y simultáneamente canonizado-, demuestran que la gran literatura puede ser a la vez profunda y popular. 
El verdadero desafío está en derribar estas barreras artificiales y celebrar aquellas obras que, al estilo de Cien años de soledad, surgen del genio creativo pero hablan el lenguaje universal capaz de conectar con grandes audiencias. El futuro pertenece a los escritores que no teman los estantes izquierdos ni los derechos de la librería, sino que se atrevan a transitar entre ambos con obras que desafíen categorías.
             """)
#____________________________________________________Data Product________________________________________________________________________________________________________________________________________________________________________________________#       


elif categoria == "Buscador":

    # Función para obtener el catálogo
    route = "Communication Final Project/Books"
    @st.cache_data
    def get_cat():
        catlog = []
        for author in os.listdir(route):
            author_route = os.path.join(route,author)
            if os.path.isdir(author_route):
                for book in os.listdir(author_route):
                    book_route = os.path.join(author_route,book)
                    name,extension = os.path.splitext(book)
                    catlog.append({"autor":author,"titulo":name,"extension":extension.lower(),"ruta":book_route})
        return catlog

    catlog = get_cat()

    # Definición en dependencia de la página seleccionada

    st.title("Buscador de obras literarias")
        
    # Filtro por autores
    autores = sorted(set([item["autor"] for item in catlog]))
    initials = sorted(set(x[0].upper() for x in autores))

    initial_select = st.sidebar.selectbox("Seleccionar inicial del autor",["Todas"] + initials)

    if initial_select == "Todas":
        filtered_authors = autores
        author_select = filtered_authors
    else:
        filtered_authors = [a for a in autores if a.upper().startswith(initial_select)]

        author_select = st.sidebar.multiselect("Filtrar por autor",filtered_authors,default = filtered_authors)

    # Filtro por extensión
    extensions = sorted(set([item["extension"] for item in catlog]))
    ext_select = st.sidebar.multiselect("Filtrar por extensión",extensions,default = extensions)

    # Búsqueda por título
    st.text("En caso de no encontrar el libro por su nombre, puede buscar mediante la inicial del autor en la barra lateral y filtrar autores.")
    texto_busqueda = st.text_input("Buscar por título")

    # Filtrar la búsqueda
    results = [item for item in catlog if item["autor"] in author_select and item["extension"] in ext_select and texto_busqueda.lower() in item["titulo"].lower()]

    if results:
        st.success(f"Se han encontrado {len(results)} libros.")
            
        for item in results:
            st.write(f"**Título:** {item['titulo']}| \n**Autor:** {item['autor']}| \n**Extensión:** {item['extension']}")
            
            if os.path.isfile(item["ruta"]):
                with open(item["ruta"],"rb") as document:
                    st.download_button(label = "Descargar libro",data = document,file_name = os.path.basename(item["ruta"]))
    else:
        st.warning("No se encontraron libros con esos criterios.")

#______________________________________________________________Sección de gráficos interactivos_______________________________________________________________________________________________________________________________
elif categoria == "Gráficos Interactivos":
    st.title("Sección de gráficos interactivos")
    st.subheader("¡Entiende los datos tú mismo!")

    st.subheader("Cantidad de publicaciones de autores bestsellers en Amazon:")
    olst.amazon_authors_counting()

    st.subheader("Gráfico de autores premiados que tienen bestsellers:")
    olst.graficar_n_autores_con_bestsellers(df_relacion_premio_bestseller_all)

    st.subheader("Cantidad de Nobels de Literatura por nacionalidad (en orden decreciente):")
    olst.nat_counting()

    st.subheader("Nacionalidades más premiadas con el Cervantes en los últimos 30 años:")
    olst.cervantes_counting()

    st.subheader("Géneros literarios más populares en The New York Times:")
    olst.nyt_genders()

#______________________________________________________________Data Frames_____________________________________________________________________________________________________________________________________________________________#    
elif categoria == "Data Frame Bestsellers New York Times":
    st.title("Recopilación de los Bestsellers en el New York Time de 1994 a 2024")
    olst.df_nyt

elif categoria == "Data Frame Bestsellers Amazon":
    st.title("Recopilación de los Bestsellers en Amazon 1995 a 2024")
    olst.df_amazon
    
elif categoria == "Data Frame Bestsellers Casa del Libro (2018-2024)":
    st.title("Recopilación de los Bestsellers en Casa del Título de 1994 a 2024")
    olst.df_casalibro
    
elif categoria == "Data Frame Premios Nobel":
    st.title("Recopilación de los Premios Nobel de 1994 a 2024")
    olst.df_nobel
    
elif categoria == "Data Frame Premios Cervantes":
    st.title("Recopilación de los Premios Cervantes de 1994 a 2024")
    olst.df_cervantes

#_____________________________________________________Acerca de_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________#
elif categoria == "Acerca de nosotros":
    st.subheader("Este proyecto está desarrollado por estudiantes de Ciencia de Datos en la Universidad de La Habana con el objetivo de demostrar las capacidades del uso de las matemáticas y estadistica en la explicación de fenómenos, facilitar el acceso a las obras literarias y extraer información respecto a las tendencias literarias actuales.")
    st.markdown("Para cualquier queja o sugerencia contáctanos en https://www.instagram.com/narrativa_en_datos?igsh=b3EzcWtqN3Nnbmhn")
    with st.form("Feedback"):
        st.write("¿Qué tema te gustaría que analicemos?")
        sugerencia = st.text_input("Tu sugerencia")
        if st.form_submit_button("Enviar"):
            st.success("¡Gracias por tu aporte!")

