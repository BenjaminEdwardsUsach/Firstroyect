# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 23:19:44 2024

#r"C:/Users/benja/OneDrive/Documentos/python/locator_server_KMZISY.txt"

@author: benja
"""
import math
import matplotlib.pyplot as plt  # Se importan las librerías necesarias

def leerArchivo(nombre):
    """
    Lee un archivo de datos de satélite y convierte las coordenadas a metros.

    Parameters
    ----------
    nombre : string
        Nombre del archivo a leer.

    Returns
    -------
    fecha : list of str
        Lista de fechas en formato 'AA:MM:DD'.
    hora : list of str
        Lista de horas en formato 'HH:MM:SS'.
    x : list of float
        Coordenadas X convertidas a metros (radios terrestres * 6378000).
    y : list of float
        Coordenadas Y convertidas a metros (radios terrestres * 6378000).3
    z : list of float
        Coordenadas Z convertidas a metros (radios terrestres * 6378000).
    """
    with open(nombre, "r") as file:
        # Se leen las líneas desde un punto especificado, ignorando metadatos
        contenido = file.readlines()[inicio:final]
    
    # Inicialización de listas para almacenar los datos leídos
    fecha, hora, x, y, z = [], [], [], [], []
    
    # Se procesa cada línea del archivo
    for linea in contenido:
        # Se dividen los datos de cada línea
        info = linea.strip().split()  
        fecha.append(info[0])         # Guardar fecha
        hora.append(info[1])          # Guardar hora
        # Conversión de las coordenadas de radios terrestres a metros
        x.append(float(info[2]) * 6378000)
        y.append(float(info[3]) * 6378000)
        z.append(float(info[4]) * 6378000)
    
    return fecha, hora, x, y, z

def graficar(x, y, variable_x, variable_y, unidad_x="m", unidad_y="m"):
    """
    Grafica dos variables en función del tiempo con la posibilidad de especificar unidades.

    Parameters
    ----------
    x : list of float
        Valores para la primera variable a graficar.
    y : list of float
        Valores para la segunda variable a graficar.
    variable_x : str
        Etiqueta para la primera variable.
    variable_y : str
        Etiqueta para la segunda variable.
    unidad_x : str, opcional
        Unidad de la primera variable (por defecto 'm').
    unidad_y : str, opcional
        Unidad de la segunda variable (por defecto 'm').
    
    Returns
    -------
    None
    """
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    # Graficar las variables en función del tiempo, con etiquetas y unidades
    ax.plot(segundos_t, x, color="blue", label=f"{variable_x} ({unidad_x})")
    ax.plot(segundos_t, y, color="green", label=f"{variable_y} ({unidad_y})")
    ax.set_title(f"{variable_x} y {variable_y}")  # Título del gráfico
    ax.set_xlabel(f"Tiempo (s)")  # Etiqueta del eje X
    ax.set_ylabel(f"{variable_x} / {variable_y}")  # Etiqueta del eje Y
    ax.legend()  # Mostrar la leyenda
    plt.show()

def graficar2(x, y, variable_x, variable_y, unidad_x="m", unidad_y="m"):
    """
    Grafica dos variables una contra la otra (x vs y) con posibilidad de especificar unidades.

    Parameters
    ----------
    x : list of float
        Valores para la primera variable (eje X).
    y : list of float
        Valores para la segunda variable (eje Y).
    variable_x : str
        Etiqueta para la primera variable (eje X).
    variable_y : str
        Etiqueta para la segunda variable (eje Y).
    unidad_x : str, opcional
        Unidad de la primera variable (por defecto 'm').
    unidad_y : str, opcional
        Unidad de la segunda variable (por defecto 'm').
    
    Returns
    -------
    None
    """
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    # Graficar x contra y
    ax.plot(x, y, color="blue")
    # Configurar el título, etiquetas y mostrar el gráfico
    ax.set_title(f"{variable_x} ({unidad_x}) y {variable_y} ({unidad_y})")
    ax.set_xlabel(f"{variable_x} ({unidad_x})")
    ax.set_ylabel(f"{variable_y} ({unidad_y})")
    plt.show()

# Solicitar al usuario el rango de líneas donde se encuentran los datos
inicio = int(input("Ingrese desde dónde parten sus datos: "))
final = int(input("Ingrese hasta dónde llegan sus datos: "))
# Leer archivo de datos y extraer las coordenadas y tiempos
fecha, hora, x, y, z = leerArchivo(input("Ingrese la localización de su archivo: "))

# Conversión de tiempo a segundos
segundos_t = []
for i in range(len(hora)):
    # Extraer horas, minutos y segundos de cada registro de tiempo
    horas = (int(hora[i][0]) * 10 + int(hora[i][1])) * 3600  # Horas a segundos
    minutos = (int(hora[i][3]) * 10 + int(hora[i][4])) * 60  # Minutos a segundos
    segundos = int(hora[i][6]) * 10 + int(hora[i][7])  # Segundos
    segundos_t.append(horas + minutos + segundos)  # Almacenar el total en segundos

# Buscar los índices del valor máximo y mínimo de la coordenada X
intento, intento2 = 0, 0
for elem in x:
    if elem == max(x):
        break
    else:
        intento += 1

for elem in x:
    if elem == min(x):
        break
    else:
        intento2 += 1

# Calcular el radio orbital aproximado
radio_o = (((max(x)-min(x))**2 + (y[intento]-y[intento2])**2 + (z[intento]-z[intento2])**2)**(1/2)) / 2

# Cálculos orbitales (período, velocidad angular, lineal y aceleración centrípeta)
periodo = 2 * math.pi * ((((radio_o)**3) / ((5.972 * (10**24)) * (6.674 * (10**-11))))**(1/2))
frec = 1 / periodo  # Frecuencia orbital
velocidad_w = (2 * math.pi) / periodo  # Velocidad angular
velocidad_l = velocidad_w * radio_o  # Velocidad lineal
aceleración_n = (velocidad_w**2) * radio_o  # Aceleración centrípeta

# Calcular vectores de posición, velocidad y aceleración en función del tiempo
posicion, velocidad, aceleración = [], [], []
for elem in segundos_t:
    # Cálculo de la posición
    posicion.append(radio_o * (math.cos(velocidad_w * elem) + math.sin(velocidad_w * elem)))
    # Cálculo de la velocidad
    velocidad.append(-radio_o * velocidad_w * math.sin(velocidad_w * elem) + radio_o * velocidad_w * math.cos(velocidad_w * elem))
    # Cálculo de la aceleración
    aceleración.append(-radio_o * (velocidad_w**2) * math.cos(velocidad_w * elem) - radio_o * (velocidad_w**2) * math.sin(velocidad_w * elem))

# Gráfico 3D de la trayectoria
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
# Graficar la trayectoria en el espacio
ax.plot(x, y, z, label="Trayectoria 3D", marker="o")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
plt.legend()
plt.show()

# Gráfico 3D de los vectores de posición, velocidad y aceleración
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
# Graficar los vectores de posición, velocidad y aceleración
ax.plot(posicion, velocidad, aceleración, label="Vectores", marker="x")
ax.set_xlabel("Posición (m)")
ax.set_ylabel("Velocidad (m/s)")
ax.set_zlabel("Aceleración (m/s²)")
plt.legend()
plt.show()

# Graficar combinaciones de las variables usando graficar y graficar2
graficar(x, y, "Posición X", "Posición Y", unidad_x="m", unidad_y="m")
graficar(x, z, "Posición X", "Posición Z", unidad_x="m", unidad_y="m")
graficar(y, z, "Posición Y", "Posición Z", unidad_x="m", unidad_y="m")
graficar(velocidad, aceleración, "Velocidad", "Aceleración", unidad_x="m/s", unidad_y="m/s²")
graficar(velocidad, posicion, "Velocidad", "Posición", unidad_x="m/s", unidad_y="m")
graficar(aceleración, posicion, "Aceleración", "Posición", unidad_x="m/s²", unidad_y="m")

# Graficar en 2D con graficar2
graficar2(x, y, "Posición X", "Posición Y", unidad_x="m", unidad_y="m")
graficar2(x, z, "Posición X", "Posición Z", unidad_x="m", unidad_y="m")
graficar2(y, z, "Posición Y", "Posición Z", unidad_x="m", unidad_y="m")
graficar2(velocidad, aceleración, "Velocidad", "Aceleración", unidad_x="m/s", unidad_y="m/s²")
graficar2(velocidad, posicion, "Velocidad", "Posición", unidad_x="m/s", unidad_y="m")
graficar2(aceleración, posicion, "Aceleración", "Posición", unidad_x="m/s²", unidad_y="m")