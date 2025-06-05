# Importa librerías necesarias para la interfaz
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Importa funciones personalizadas
from algoritmo_genetico import ejecutar_algoritmo  # Función principal del algoritmo genético
from utilidades import leer_datos_csv  # Función para leer productos desde archivo CSV

# Importa módulo para cálculos estadísticos
import statistics

# === Parámetros del problema ===
NUM_EJECUCIONES = 30               # Número de veces que se ejecuta el algoritmo
CAPACIDAD_MOCHILA = 0.7           # Peso máximo permitido
MIN_CALORIAS = 400                 # Calorías mínimas requeridas
TAM_POBLACION = 1000               # Tamaño de la población
PORCENTAJE_MUTACION = 0.1          # Probabilidad de mutación por gen

productos = []     # Lista de productos cargados
resultados = []    # Resultados de las ejecuciones

# === Configuración de la ventana principal ===
ventana = tk.Tk()
ventana.title("Algoritmo Genético - Problema de la Mochila")
ventana.geometry('900x600')

# Barra de progreso para mostrar avance
progress = ttk.Progressbar(ventana, orient='horizontal', length=800, mode='determinate')
progress.pack(pady=10)

# Área de texto para mostrar resultados
text_area = tk.Text(ventana, width=110, height=25)
text_area.pack(padx=10, pady=10)

# Contenedor para botones
btn_frame = tk.Frame(ventana)
btn_frame.pack(pady=10)

# === Función para cargar productos desde archivo CSV ===
def cargar_archivo():
    global productos
    # Abre diálogo para seleccionar archivo
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de productos", filetypes=[("CSV Files", "*.csv")])
    if archivo:
        productos = leer_datos_csv(archivo)  # Lee los productos desde archivo
        messagebox.showinfo("Carga Exitosa", f"Se cargaron {len(productos)} productos.")  # Muestra mensaje al usuario

# === Función principal que ejecuta el algoritmo múltiples veces ===
def correr_algoritmo():
    if not productos:
        messagebox.showwarning("Advertencia", "Primero carga un archivo de productos.")
        return

    resultados.clear()  # Limpia resultados anteriores
    text_area.config(state=tk.NORMAL)
    text_area.delete('1.0', tk.END)  # Limpia área de texto
    progress['maximum'] = NUM_EJECUCIONES  # Configura el máximo de la barra de progreso

    # Función recursiva para ejecutar cada corrida con delay visual
    def ejecutar_cada_corrida(i=0):
        if i < NUM_EJECUCIONES:
            # Ejecuta una corrida del algoritmo genético
            mejor, peso, calorias = ejecutar_algoritmo(
                productos,
                capacidad=CAPACIDAD_MOCHILA,
                min_calorias=MIN_CALORIAS,
                tam_poblacion=TAM_POBLACION,
                prob_mutacion=PORCENTAJE_MUTACION
            )
            # Obtiene nombres de productos seleccionados
            seleccionados = [p['nombre'] for idx, p in enumerate(productos) if mejor[idx]]
            resultados.append((i + 1, seleccionados, peso, calorias))  # Guarda resultados

            # Muestra resultados parciales en pantalla
            text_area.insert(tk.END, f"Ejecución {i + 1}: Peso={peso:.2f}, Calorías={calorias}, Productos={', '.join(seleccionados)}\n")
            text_area.see(tk.END)
            progress['value'] = i + 1  # Actualiza barra de progreso
            ventana.after(100, ejecutar_cada_corrida, i + 1)  # Espera 100ms y repite
        else:
            mostrar_resumen_final()  # Muestra resumen al final

    ejecutar_cada_corrida()  # Inicia ejecuciones

# === Muestra resumen con mejor y peor ejecución, y promedios ===
def mostrar_resumen_final():
    if not resultados:
        messagebox.showwarning("Advertencia", "No hay resultados para mostrar.")
        return

    # Calcula promedios, mejor y peor ejecución
    pesos = [r[2] for r in resultados]
    calorias = [r[3] for r in resultados]
    mejor = max(resultados, key=lambda x: x[3])
    peor = min(resultados, key=lambda x: x[3])

    # Muestra resumen en el área de texto
    resumen_texto = f"\n✅ Ejecuciones completas.\nResumen de {NUM_EJECUCIONES} ejecuciones:\n"
    resumen_texto += f"Peso promedio: {statistics.mean(pesos):.2f}\n"
    resumen_texto += f"Calorías promedio: {statistics.mean(calorias):.2f}\n"
    resumen_texto += f"\n Mejor mochila (Ejecución {mejor[0]}): {', '.join(mejor[1])} | Peso={mejor[2]:.2f}, Calorías={mejor[3]}\n"
    resumen_texto += f" Peor mochila (Ejecución {peor[0]}): {', '.join(peor[1])} | Peso={peor[2]:.2f}, Calorías={peor[3]}\n"

    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, resumen_texto)
    text_area.config(state=tk.DISABLED)

# === Botones ===
btn_cargar = tk.Button(btn_frame, text="📂 Cargar Productos", command=cargar_archivo)
btn_cargar.grid(row=0, column=0, padx=10)

btn_correr = tk.Button(btn_frame, text="▶ Ejecutar Algoritmo", command=correr_algoritmo)
btn_correr.grid(row=0, column=1, padx=10)

# === Inicia la aplicación ===
ventana.mainloop()
