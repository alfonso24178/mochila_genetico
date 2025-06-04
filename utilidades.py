import csv
import statistics

def leer_datos_csv(ruta):
    productos = []
    with open(ruta, newline='') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            productos.append({
                'nombre': fila['nombre'],
                'peso': float(fila['peso']),
                'calorias': float(fila['calorias'])
            })
    return productos

def mostrar_resultados(resultados):
    promedios_peso = [r[1] for r in resultados]
    promedios_calorias = [r[2] for r in resultados]

    print("\nResumen de 30 ejecuciones:")
    print(f"Peso promedio: {statistics.mean(promedios_peso):.2f}")
    print(f"Calorías promedio: {statistics.mean(promedios_calorias):.2f}")

    mejor = max(resultados, key=lambda x: x[2])
    peor = min(resultados, key=lambda x: x[2])

    print("\nMejor mochila:")
    print(f"Genotipo: {mejor[0]}")
    print(f"Peso: {mejor[1]} | Calorías: {mejor[2]}")

    print("\nPeor mochila:")
    print(f"Genotipo: {peor[0]}")
    print(f"Peso: {peor[1]} | Calorías: {peor[2]}")

def guardar_en_csv(resultados, ruta="resultados/resumen.csv"):
    with open(ruta, mode='w', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["# Ejecucion", "Genotipo", "Peso", "Calorias"])
        for i, (genotipo, peso, calorias) in enumerate(resultados, 1):
            writer.writerow([i, "".join(map(str, genotipo)), peso, calorias])