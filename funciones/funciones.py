import pandas as pd
import matplotlib.pyplot as plt
import requests
import io

# Función para cargar CSV desde GitHub 
def cargar_csv_desde_github(url):
    try:
        response = requests.get(url) # descarga el archivo y realiza una solicitud GET a la URL y la guarda en response
        response.raise_for_status() # verifica si la carga fue exitosa y en caso contrario larga una excepción
        csv_temporal = io.StringIO(response.text) # crea un archivo temporal en memoria
        df = pd.read_csv(csv_temporal, sep=";") # carga el archivo al dataframe
        return df # Devuelve e dataframe
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None

def grafico_barras_plt(datos,datosx,datosy,titulo):
        
    x= datos[datosx] # capturamos los datos dle eje x
    y = datos[datosy] # capturamos los datos del eje y
    total= sum(y) # Sumar todas las cantidades para calcular el porcentaje
    
    fig, ax = plt.subplots(figsize=(10, 5))
     # Personalizar fondo del gráfico
    ax.set_facecolor("#c2c2c2")  # Fondo del área del gráfico
    fig.patch.set_facecolor("#7c7c7c")  # Fondo de la figura completa
    
    # Crear barras con colores personalizados
    colores_barras = ["#adc15e","#97a952","#829147","#6c793b","#56612f","#414823","#2b3018","#16180c"] # Lista de colores
    ax.set_title(titulo) # titulo del gráfico 
    ax.set_xlabel(datosx) # etiqueta eje x
    ax.set_ylabel(datosy) # etiqueta eje y
    fig.subplots_adjust(top=1)
    
    barras = ax.bar(x, y, 
                    color=colores_barras[:len(x)],  # Asignar colores
                    edgecolor='black',  # Color del borde
                    linewidth=1)        # Grosor del borde
    
    for barra in barras:
        altura = barra.get_height()  # Obtener la altura de la barra
        centro_x = barra.get_x() + barra.get_width() / 2  # Coordenada horizontal central
        porcentaje = (altura / total) * 100      # Calcular porcentaje        
        # Etiqueta con cantidad y porcentaje
        ax.annotate(f'{int(altura)} ({porcentaje:.1f}%)',
                    xy=(centro_x, altura + 15),  # Coordenadas centradas en la barra
                    ha='center', va='bottom',    # Alineación horizontal y vertical
                    color='black',               # Opcional: texto en blanco para contraste
                    fontsize=10)                 # Tamaño de la fuente
                    #weight='bold')              # Opcional: texto en negrita
    plt.show()
    
# creación de diccionario para los tipos de colesterol LDL segun su valor
clasificacion_colesterol_LDL = {
    "optimo":(0,100),
    "mejor que optimo":(100,129),
    "limite alto":(130,159),
    "alto":(160,189),
    "muy alto":(190,float("inf"))
}
# creación de diccionario para los tipos de trigliceridos segun su valor
clasificacion_trigliceridos = {
    "saludables":(0,150),
    "ligeramente altos":(150,190),
    "altos":(200,499),
    "muy altos":(500,float("inf"))
}
# funcion que retorna el tipo de colesterol 
def categorizar_colesterol(valor):
    for categoria, (inferior,superior) in clasificacion_colesterol_LDL.items():
        if inferior <= valor <= superior:
            return categoria 
        
# funcion que retorna el tipo de presión
def categorizar_presion(sis,dia):
    if sis <120 and dia <80:
        return "normal"
    elif 120 <= sis <=129 and dia < 80:
        return "elevada"
    elif (130 <= sis <=139) or (80 <= dia <= 89):
        return "hipertension grado 1"
    elif (140 <= sis <= 179) or (90 <= dia <=119):
        return "hipertension grado 2"
    elif sis >=180 or dia >=120:
        return "crisis hipertensiva"
    else:
        return "no clasificado"
    
def categorizar_trigliceridos(valor):
    for categoria, (inferior, superior) in clasificacion_trigliceridos.items():
        if inferior <= valor <=superior:
            return categoria

        
def limpiar_datos_IQR(columna,considerar):
    print("\n\t---- {} ----".format(columna))
    
    q1 = considerar[columna].quantile(0.25) #Calculamos el 1 quartil
    q3 = considerar[columna].quantile(0.75) # calculamos el 3 cuartil
    iqr = q3 - q1 # calculamosel IQR
    print("Q1 = {:,.4f}\nQ3 = {:,.4f} \nIQR = {:,.4f}".format(q1,q3,iqr))
    
    # Definición de los límites superior e inferior
    limite_inferior = q1 - (iqr * 1.5)
    limite_superior = q3 + (iqr * 1.5)
    print("IQR x 1.5 = {:,.4f}\nLímite inferior = {:,.4f}\nLímite superior = {:,.4f}".format((iqr*1.5), limite_inferior, limite_superior))
    return considerar [(considerar[columna]>limite_inferior) & (considerar[columna]<limite_superior)]

def dibujar_boxplot(datos,columna,limpio="con limpieza de datos"):    

    fig, ax = plt.subplots(figsize = (10, 5))
    fig.patch.set_facecolor("#c7c7c7")  # Color de fondo de la figura
    ax.set_facecolor("#c2c2c2")  # Color de fondo del gráfico
    ax.boxplot(datos[columna],
            vert=False,
        patch_artist=True,  # Permite rellenar las cajas con color
        
        # Personalización de las cajas
        boxprops=dict(
            facecolor="#829147",  # Color de relleno de la caja
            color="#adc15e",      # Color del borde de la caja
            alpha=0.6             # Transparencia
        ),
            flierprops=dict(markerfacecolor= "red")
            )
    plt.title("Columna {} {}".format(columna,limpio))
