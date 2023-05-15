from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Funcion que se ejecuta al presionar el boton de procesar
def process_image():
    # Abre el archivo
    archivo_1 = filedialog.askopenfilename(initialdir='.', title='Selecciona imagen a procesar', filetypes=(('JPEG', '*.jpg;*.jpeg'), ('PNG', '*.png'), ('Todos los archivos', '*.*')))
    archivo_2 = filedialog.askopenfilename(initialdir='.', title='Selecciona imagen a transponer sobre la original', filetypes=(('JPEG', '*.jpg;*.jpeg'), ('PNG', '*.png'), ('Todos los archivos', '*.*')))
    
    if archivo_2: # Si se selecciono dos imagenes 
        # Abre imagen 1
        imagen_1 = Image.open(archivo_1)
        # Convierte imagen 1
        matriz_imagen_1 = np.array(imagen_1)
        
        # Abre imagen 2
        imagen_2 = Image.open(archivo_2)
        # Convierte imagen 2
        matriz_imagen_2 = np.array(imagen_2)

        # Convierte matrices a tipo uint16 para evitar desbordamiento
        matriz_imagen_1 = matriz_imagen_1.astype(np.uint16)
        matriz_imagen_2 = matriz_imagen_2.astype(np.uint16)

        ##### Tranposicion de imagenes (suma de matrices)
        # Crea la matriz, limita los valores a 255, y los convierte a uint8
        # *Se dividen la matrices a sumar a la mitad para que el resultado final no afecte su brillo final
        matriz_imagen_1 = np.clip((matriz_imagen_1 * 0.5) + (matriz_imagen_2 * 0.5), 0, 255).astype(np.uint8)
        #####
    else: # Si solo se selecciono una imagen
        # Abre imagen 1
        imagen_1 = Image.open(archivo_1)
        # Convierte imagen 1
        matriz_imagen_1 = np.array(imagen_1)

        # Convierte la matriz a tipo uint16 para evitar desbordamiento
        matriz_imagen_1 = matriz_imagen_1.astype(np.uint16)

    # Obtiene los valores de la interfaz
    escalar = int(escalar_entry.get())
    red_escalar = float(red_slider.get())
    green_escalar = float(green_slider.get())
    blue_escalar = float(blue_slider.get())

    ##### Aumento de brillo
    # Obtiene al ancho y alto de la imagen/matriz
    alto_imagen_1, ancho_imagen_1 = imagen_1.size
    # Se crea el vector como elemento de la matriz a sumar
    vector_suma = (escalar,escalar,escalar)
    # Genera la matriz a sumar con todos sus elementos iguales
    matriz_suma = np.tile(vector_suma, (ancho_imagen_1 * alto_imagen_1, 1))
    # Necesario para asignar los vectores como elementos de la matriz
    matriz_suma = matriz_suma.reshape((ancho_imagen_1, alto_imagen_1, 3))
    # Suma las matrices
    matriz_imagen_1 = matriz_imagen_1 + matriz_suma
    #####

    ##### Aumenta los canales de color
    matriz_imagen_1_resultado = matriz_imagen_1.copy()
    matriz_imagen_1_resultado[..., 0] = np.clip(matriz_imagen_1[..., 0] * red_escalar, a_min=0, a_max=255)
    matriz_imagen_1_resultado[..., 1] = np.clip(matriz_imagen_1[..., 1] * green_escalar, a_min=0, a_max=255)
    matriz_imagen_1_resultado[..., 2] = np.clip(matriz_imagen_1[..., 2] * blue_escalar, a_min=0, a_max=255)
    #####

    # Convierte la matriz resultante a tipo uint8 para mostrar la imagen
    matriz_imagen_1_resultado = matriz_imagen_1_resultado.astype(np.uint8)

    # Crea una nueva imagen a partir de la matriz resultante
    imagen_resultado = Image.fromarray(matriz_imagen_1_resultado)

    # Muestra la imagen resultante
    imagen_resultado.save('resultado.png')

    #print ("Terminado")

# Crea la ventana principal
root = tk.Tk()
root.title('Seminario de Solucion de problemas de Metodos Matematicos II')

# Crea el cuadro de texto para ingresar el escalar
label_brillo = tk.Label(root, text="Brillo (x,x,x)+(R,G,B)")
label_brillo.pack(side=tk.LEFT, padx=10, pady=10)
escalar_entry = tk.Entry(root, width=10)
escalar_entry.pack(side=tk.LEFT)
escalar_entry.insert(0, '0')

# Crea el boton de procesar
process_button = tk.Button(root, text=" Procesar ", command=process_image)
process_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Crea los sliders de los canales de color
red_slider = tk.Scale(root, from_=0.0, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, label='Rojo (R*x,G,B)')
red_slider.set(1.0)
red_slider.pack(side=tk.LEFT, padx=10, pady=10)

green_slider = tk.Scale(root, from_=0.0, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, label='Verde (R,G*x,B)')
green_slider.set(1.0)
green_slider.pack(side=tk.LEFT, padx=10, pady=10)

blue_slider = tk.Scale(root, from_=0.0, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, label='Azul (R,G,B*x)')
blue_slider.set(1.0)
blue_slider.pack(side=tk.LEFT, padx=10, pady=10)

# Ejecuta ventana
root.mainloop()
