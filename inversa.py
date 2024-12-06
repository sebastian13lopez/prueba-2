

# --- JAIRO RAMOS MENDEZ 192041 ---
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
import sympy as sp

# --- Funciones de la calculadora ---
def crear_entradas_matriz(tam):
    # Crea las entradas de la matriz en la interfaz gráfica según el tamaño especificado.
    global entradas_matriz
    for widget in frame_matriz.winfo_children():
        widget.destroy()  # Limpiar el contenido actual
    
    entradas_matriz = []   # Inicializar la lista de entradas
    for i in range(tam):
        fila = []
        for j in range(tam):
            entrada = ttk.Entry(frame_matriz, width=5, justify='center', font=('Arial', 12))
            entrada.grid(row=i, column=j, padx=3, pady=3, ipadx=3, ipady=3)  # Márgenes reducidos
            fila.append(entrada)
        entradas_matriz.append(fila)
        
def obtener_matriz_desde_entradas():
    # Obtiene los valores de la matriz desde las entradas de texto y los convierte a una matriz de SymPy.
    try:
        matriz = []
        for fila in entradas_matriz:
            matriz_fila = []
            for entrada in fila:
                valor = entrada.get()
                if not valor:
                    raise ValueError("Todas las entradas deben tener un valor numérico.")
                matriz_fila.append(sp.sympify(valor))   # Convierte el valor ingresado a un formato simbólico
            matriz.append(matriz_fila)
        return matriz
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return None
    except Exception as e:
        messagebox.showerror("Error", "Entrada inválida. Asegúrate de que los valores son numéricos, fracciones o raíces.")

def mostrar_matriz_inversa(inversa, tam):
    # Limpiar solo las etiquetas de resultados, sin borrar el título
    for widget in frame_resultado.winfo_children():
        if widget != lbl_resultado:
            widget.destroy()
  # Mostrar cada elemento de la matriz inversa en su respectiva etiqueta
    for i, fila in enumerate(inversa.tolist()):
        for j, valor in enumerate(fila):
            etiqueta = ttk.Label(frame_resultado, text=f"{valor:.4f}", relief="solid", borderwidth=1, font=('Arial', 12), width=8, anchor="center", background="#bce0fd")
            etiqueta.grid(row=i+1, column=j, padx=5, pady=5)  # Márgenes reducidos para ajustar más contenido

def calcular_inversa():
    # Calcula la matriz inversa utilizando el método de Gauss-Jordan y muestra el proceso.
    try:
        tam = int(combo_tam.get()[0])  # Obtener el tamaño de la matriz
        matriz_inicial = obtener_matriz_desde_entradas()  # Obtener la matriz desde las entradas
        
        # Validar si la matriz es cuadrada
        if len(matriz_inicial) != tam or any(len(fila) != tam for fila in matriz_inicial):
            messagebox.showerror("Error", "La matriz no es cuadrada. Por favor ingresa una matriz válida.")
            return
        
        if matriz_inicial:
            a = sp.Matrix(matriz_inicial)  # Crear una matriz de SymPy
            determinante = a.det()  # Calcular el determinante

            # Mostrar el determinante en el área de texto
            txt_proceso.config(state=tk.NORMAL)  # Habilitar la edición para agregar texto
            txt_proceso.delete("1.0", tk.END)
            txt_proceso.insert(tk.END, f"Determinante de la matriz: {determinante}\n", "titulo")

            # Verificar si el determinante es cero
            if determinante == 0:
                txt_proceso.insert(tk.END, "La matriz no es inversible, ya que su determinante es cero.\n", "error")
                txt_proceso.config(state=tk.DISABLED)
                messagebox.showerror("Error", "La matriz no tiene inversa, su determinante es cero.")
                return

            # Continuar con el método de Gauss-Jordan si el determinante no es cero
            identidad = sp.eye(tam)  # Matriz identidad del mismo tamaño
            aumentada = a.row_join(identidad)  # Crear la matriz aumentada
            
            # Mostrar la matriz aumentada con la separación
            txt_proceso.insert(tk.END, "\nMatriz aumentada inicial:\n", "titulo")
            matriz_con_separacion = sp.pretty(aumentada).replace('] [', '] | [')  # Añadir la línea de separación
            txt_proceso.insert(tk.END, f"{matriz_con_separacion}\n\n", "matriz")

            # Proceder con el método de Gauss-Jordan paso a paso
            paso = 1
            for i in range(tam):
                # Paso 1: Verificar si el pivote es cero y realizar intercambio de filas si es necesario
                if aumentada[i, i] == 0:
                    # Buscar una fila abajo que tenga un valor diferente de cero en la columna i
                    for k in range(i + 1, tam):
                        if aumentada[k, i] != 0:
                            aumentada.row_swap(i, k)  # Intercambiar filas
                            txt_proceso.insert(tk.END, f"Intercambiar fila {i+1} con fila {k+1} porque el pivote era cero.\n", "paso")
                            break
                    else:
                        # Si no se encuentra fila para intercambiar, el pivote sigue siendo cero
                        messagebox.showerror("Error", "El pivote es cero y no hay más filas para intercambiar. No se puede continuar.")
                        txt_proceso.config(state=tk.DISABLED)
                        return

                # Continuar con el método de Gauss-Jordan
                pivote = aumentada[i, i]
                aumentada[i, :] = aumentada[i, :] / pivote  # Hacer el pivote 1
                txt_proceso.insert(tk.END, f"Paso {paso}: Dividir la fila {i+1} entre {sp.pretty(pivote)} para hacer el pivote 1:\n", "paso")
                
                matriz_con_separacion = sp.pretty(aumentada).replace('] [', '] | [')  # Actualizar la matriz con la línea de separación
                txt_proceso.insert(tk.END, f"{matriz_con_separacion}\n\n", "matriz")
                paso += 1

                # Paso 2: Hacer ceros en la columna i para las otras filas
                for j in range(tam):
                    if j != i:
                        factor = aumentada[j, i]
                        aumentada[j, :] = aumentada[j, :] - factor * aumentada[i, :]
                        txt_proceso.insert(tk.END, f"Paso {paso}: Restar {sp.pretty(factor)} veces la fila {i+1} de la fila {j+1}:\n", "paso")
                        
                        matriz_con_separacion = sp.pretty(aumentada).replace('] [', '] | [')  # Actualizar la matriz con la línea de separación
                        txt_proceso.insert(tk.END, f"{matriz_con_separacion}\n\n", "matriz")
                        paso += 1

            # Extraer la parte derecha de la matriz aumentada, que es la inversa de la original
            inversa = aumentada[:, tam:]

            # Mostrar la matriz inversa
            mostrar_matriz_inversa(inversa, tam)
            txt_proceso.insert(tk.END, "Inversa calculada con éxito.\n", "exito")
            txt_proceso.config(state=tk.DISABLED)  # Hacer el área de texto de solo lectura nuevamente

    except ValueError:
        messagebox.showerror("Error", "Tamaño de la matriz inválido.")
    except Exception as e:
        messagebox.showerror("Error", str(e))



def limpiar_entradas():
    for fila in entradas_matriz:
        for entrada in fila:
            entrada.delete(0, tk.END) # Limpiar cada entrada
    
    # Limpiar solo las etiquetas de resultados, sin borrar el título
    for widget in frame_resultado.winfo_children():
        if widget != lbl_resultado:
            widget.config(text="")

    txt_proceso.config(state=tk.NORMAL)  # Habilitar para limpiar
    txt_proceso.delete("1.0", tk.END) # Limpiar el área de texto de proceso
    txt_proceso.config(state=tk.DISABLED)  # Deshabilitar nuevamente

def actualizar_matriz(event=None):
    tam = int(combo_tam.get()[0])  # Obtener el nuevo tamaño
    crear_entradas_matriz(tam) # Crear nuevas entradas
    actualizar_labels_resultado(tam) # Actualizar etiquetas de resultado

def actualizar_labels_resultado(tam):
    # Actualiza las etiquetas de resultado en función del tamaño de la matriz.
    # Limpiar solo las etiquetas de resultados, sin borrar el título
    for widget in frame_resultado.winfo_children():
        if widget != lbl_resultado:
            widget.destroy()

    # Re-crear etiquetas de resultado según el tamaño de la matriz
    for i in range(tam):
        for j in range(tam):
            etiqueta = ttk.Label(frame_resultado, text="", relief="solid", borderwidth=1, font=('Arial', 12), width=8, anchor="center", background="#bce0fd")
            etiqueta.grid(row=i+1, column=j, padx=5, pady=5)

# --- Función para mostrar el manual ---
def mostrar_manual():
    # Muestra una ventana con el manual de usuario de la aplicación.
    manual_window = tk.Toplevel(ventana)
    manual_window.title("Manual de Usuario")
    manual_window.geometry("1000x600")
    
    # Cambiar el tipo y tamaño de fuente para el contenido del manual
    font_style = ("Helvetica", 12)  # Cambia el tipo y tamaño de fuente del manual

    # Crear una barra de desplazamiento vertical para el texto
    y_scrollbar = ttk.Scrollbar(manual_window, orient="vertical")
    y_scrollbar.pack(side="right", fill="y")

    # Crear un widget de texto para mostrar el contenido del manual
    manual_text = tk.Text(manual_window, wrap=tk.WORD, yscrollcommand=y_scrollbar.set, bg="#f0f4c3", fg="#3e2723", font=("Arial", 12))
    manual_text.pack(fill="both", expand=True)

    # Configurar las barras de desplazamiento para interactuar con el widget Text
    y_scrollbar.config(command=manual_text.yview)

    # Cambiar el estilo de fuente del widget Text
    manual_text.config(font=font_style)

    # Contenido del manual
    manual_content = """\
Manual de Usuario

Aplicación de Cálculo de Matriz Inversa
Esta interfaz permite calcular la matriz inversa mediante el método de Gauss-Jordan,
ideal para sistemas de ecuaciones lineales y matrices cuadradas.

Instrucciones:
Seleccionar el tamaño:
Escoge el tamaño de la matriz (3x3 o 4x4) en el menú desplegable.

Ingresar valores:
Introduce los valores numéricos en las casillas 
(acepta enteros, fracciones y expresiones como raíces).

Calcular inversa:
Haz clic en "Calcular Inversa". Si la matriz es inversible (determinante ≠ 0),
se calculará su inversa.

Ver resultados:
La matriz inversa aparecerá debajo de la matriz original, 
junto con un desglose paso a paso.

Limpiar:
Haz clic en "Limpiar" para empezar un nuevo cálculo.

Errores comunes:
Determinante cero: Si el determinante es cero, la matriz no tiene inversa.
Entradas no válidas: Asegúrate de completar todas las casillas con números válidos.

Funciones avanzadas:
Paso a paso: Explicación detallada del proceso de Gauss-Jordan.
Soporte para fracciones: Puedes ingresar fracciones y expresiones matemáticas.

"""

    # Insertar el contenido del manual en el widget de texto
    manual_text.insert(tk.END, manual_content)  # Añade el texto del manual al widget de texto para que el usuario pueda leerlo

# --- Inicialización de la ventana principal ---

# Crear la ventana principal con un tema visual específico
ventana = ThemedTk(theme="arc")  # Usa el tema "arc" para darle un estilo moderno a la interfaz
ventana.title("Calculadora de Matriz Inversa")  # Título de la ventana principal
ventana.geometry("800x600")  # Tamaño inicial de la ventana
ventana.configure(bg="#f0f8ff")  # Color de fondo de la ventana para un aspecto más suave

# Crear el título principal de la aplicación
lbl_titulo = ttk.Label(ventana, text="Calculadora de Matriz Inversa - Método de Gauss-Jordan", font=('Arial', 16), background="#f0f8ff")
lbl_titulo.pack(pady=10)  # Coloca el título en la ventana con un margen vertical


# Selección del tamaño de la matriz
lbl_tam = ttk.Label(ventana, text="Selecciona el tamaño de la matriz:", background="#f0f8ff")
lbl_tam.pack()

# Combo box para seleccionar el tamaño de la matriz (ahora con opción 2x2)
combo_tam = ttk.Combobox(ventana, values=["2x2", "3x3", "4x4"], state="readonly")
combo_tam.pack(pady=5)
combo_tam.current(0)  # Selecciona 2x2 como predeterminado
combo_tam.bind("<<ComboboxSelected>>", actualizar_matriz)

# Marco para las entradas de la matriz
frame_matriz = ttk.Frame(ventana)
frame_matriz.pack(pady=10)

# Marco para los resultados
frame_resultado = ttk.Frame(ventana)  # Crea un marco que contendrá los resultados de la matriz inversa
frame_resultado.pack(pady=10)  # Coloca el marco en la ventana con un margen vertical

# Etiqueta para mostrar los resultados
lbl_resultado = ttk.Label(frame_resultado, text="Matriz Inversa", font=('Arial', 14), relief="solid", borderwidth=1, background="#bce0fd")
lbl_resultado.grid(row=0, column=0, columnspan=4, padx=5, pady=5)  # Configura la etiqueta en una cuadrícula para alineación

# Marco para los botones de acción
frame_botones = ttk.Frame(ventana)  # Crea un marco que contendrá los botones de acción
frame_botones.pack(pady=10)  # Coloca el marco en la ventana con un margen vertical

# Botón para calcular la inversa de la matriz
btn_calcular = ttk.Button(frame_botones, text="Calcular Inversa", command=calcular_inversa)
btn_calcular.grid(row=0, column=0, padx=5)  # Coloca el botón en la cuadrícula del marco

# Botón para limpiar las entradas y los resultados
btn_limpiar = ttk.Button(frame_botones, text="Limpiar", command=limpiar_entradas)
btn_limpiar.grid(row=0, column=1, padx=5)  # Coloca el botón junto al botón de cálculo

# Botón para mostrar el manual de usuario
btn_manual = ttk.Button(frame_botones, text="Manual de Usuario", command=mostrar_manual)
btn_manual.grid(row=0, column=2, padx=5)  # Coloca el botón junto al resto de botones

# --- Configuración del área de texto para mostrar el proceso ---

# Marco para mostrar el proceso de cálculo paso a paso
frame_proceso = ttk.Frame(ventana)  # Crea un marco que contendrá el área de texto para mostrar el proceso
frame_proceso.pack(pady=10)  # Coloca el marco en la ventana con un margen vertical

# Área de texto para mostrar el proceso de cálculo
txt_proceso = tk.Text(frame_proceso, height=15, width=60, font=('Arial', 12), wrap=tk.WORD, background="#eaf5fa")
txt_proceso.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Coloca el área de texto dentro del marco y la expande para llenar el espacio disponible

# --- Estilo para el área de texto ---
txt_proceso.tag_config("titulo", font=('Arial', 14, 'bold'), foreground="#004080")
txt_proceso.tag_config("paso", font=('Arial', 12, 'italic'), foreground="#0000cd")
txt_proceso.tag_config("matriz", font=('Courier New', 12), foreground="#2f4f4f")
txt_proceso.tag_config("exito", font=('Arial', 12, 'bold'), foreground="#228b22")

# Crear una barra de desplazamiento vertical para el área de texto
scrollbar = ttk.Scrollbar(frame_proceso, command=txt_proceso.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Coloca la barra de desplazamiento a la derecha del área de texto
txt_proceso.config(yscrollcommand=scrollbar.set)  # Asocia la barra de desplazamiento al área de texto

# --- Inicializar la matriz con entradas predeterminadas ---

# Crear las casillas de entrada para una matriz 3x3 al iniciar la aplicación
crear_entradas_matriz(2)

# Ejecutar el bucle principal de la interfaz
ventana.mainloop()  # Inicia la ejecución de la interfaz gráfica 