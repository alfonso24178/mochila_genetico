import random  # Importa el módulo random para generar números aleatorios

# Calcula el "fitness" o aptitud de un individuo
def fitness(individuo, productos, capacidad, min_calorias):
    # Calcula el peso total de los productos seleccionados
    peso = sum(productos[i]['peso'] for i in range(len(individuo)) if individuo[i])
    # Calcula las calorías totales de los productos seleccionados
    calorias = sum(productos[i]['calorias'] for i in range(len(individuo)) if individuo[i])
    # Si el peso excede la capacidad o no alcanza las calorías mínimas, el fitness es 0
    if peso > capacidad or calorias < min_calorias:
        return 0
    # Si es válido, retorna las calorías como valor de aptitud
    return calorias

# Crea un individuo aleatorio (una posible solución)
def crear_individuo(n):
    return [random.randint(0, 1) for _ in range(n)]  # 0 o 1 para cada producto (no llevar o llevar)

# Aplica mutación a un individuo
def mutar(individuo, prob_mutacion):
    return [
        1 - gen if random.random() < prob_mutacion else gen  # Invierte el gen con cierta probabilidad
        for gen in individuo
    ]

# Cruza dos individuos (padres) para generar dos hijos
def cruzar(a, b):
    punto = random.randint(1, len(a) - 1)  # Selecciona un punto de cruce aleatorio
    return a[:punto] + b[punto:], b[:punto] + a[punto:]  # Intercambia segmentos entre padres

# Selecciona un individuo de la población usando ruleta (selección probabilística)
def seleccionar(poblacion, fitnesses):
    total = sum(fitnesses)  # Suma total de los fitness
    if total == 0:
        return random.choice(poblacion)  # Si nadie tiene fitness, elige aleatorio
    probs = [f / total for f in fitnesses]  # Probabilidad proporcional al fitness
    return random.choices(poblacion, weights=probs, k=1)[0]  # Elige uno con esas probabilidades

# Función principal que ejecuta el algoritmo genético
def ejecutar_algoritmo(productos, capacidad, min_calorias, tam_poblacion, prob_mutacion, generaciones=500):
    # Genera la población inicial de forma aleatoria
    poblacion = [crear_individuo(len(productos)) for _ in range(tam_poblacion)]

    # Ciclo principal de evolución
    for _ in range(generaciones):
        # Evalúa el fitness de cada individuo en la población
        fitnesses = [fitness(ind, productos, capacidad, min_calorias) for ind in poblacion]
        nueva_poblacion = []
        # Genera nuevos individuos (hijos) a partir de cruces y mutaciones
        for _ in range(tam_poblacion // 2):
            padre1 = seleccionar(poblacion, fitnesses)  # Selecciona primer padre
            padre2 = seleccionar(poblacion, fitnesses)  # Selecciona segundo padre
            hijo1, hijo2 = cruzar(padre1, padre2)       # Cruza para obtener hijos
            nueva_poblacion.extend([mutar(hijo1, prob_mutacion), mutar(hijo2, prob_mutacion)])  # Aplica mutación
        poblacion = nueva_poblacion  # Reemplaza la población con la nueva generación

    # Al terminar todas las generaciones, se evalúa la mejor solución final
    fitnesses = [fitness(ind, productos, capacidad, min_calorias) for ind in poblacion]
    mejor = poblacion[fitnesses.index(max(fitnesses))]  # Encuentra el individuo con mayor fitness
    peso_total = sum(productos[i]['peso'] for i in range(len(mejor)) if mejor[i])  # Calcula su peso total
    calorias_total = sum(productos[i]['calorias'] for i in range(len(mejor)) if mejor[i])  # Y sus calorías totales
    return mejor, peso_total, calorias_total  # Retorna la mejor mochila y sus métricas
