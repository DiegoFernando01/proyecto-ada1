# Librerías necesarias

import subprocess # Se utiliza para abrir el archivo de salidas automatimente tras una ejecución de una entrada.

# Clases y estructuras de datos utilizadas

class Encuestado: # Representa a un encuestado en el sistema.
  """
  Atributos:
    id: Identificador único del encuestado.
    nombre: Nombre del encuestado.
    experticia: Nivel de experticia del encuestado.
    opinion: Opinión del encuestado.
  """
  def __init__(self, id_, nombre, experticia, opinion): # Constructor de la clase Encuestado.
    self.id = id_
    self.nombre = nombre
    self.experticia = experticia
    self.opinion = opinion

  def __repr__(self): # Representación textual de un objeto Encuestado.
    return f"({self.id}, Nombre: '{self.nombre}', Experticia: {self.experticia}, Opinión: {self.opinion})"

class Pregunta: # Representa una pregunta en el sistema.
  """
  Atributos:
    id_ (int): Identificador único de la pregunta.
    encuestados: Lista de encuestados que respondieron esta pregunta.
    promedio_opinion: Promedio de las opiniones de los encuestados.
    promedio_experticia: Promedio de la experticia de los encuestados.
  """
  def __init__(self, id_): # Constructor de la clase Pregunta.
    self.id = id_
    self.encuestados = []
    self.promedio_opinion = 0
    self.promedio_experticia = 0

  def agregar_encuestado(self, encuestado): # Agrega un encuestado a la pregunta.
    """
    Atributos:
      encuestado: Objeto de tipo Encuestado a agregar.
    """
    self.encuestados.append(encuestado)

  def calcular_promedios(self): # Calcula los promedios de opinión y experticia basados en los encuestados.
    self.promedio_opinion = round(sum(e.opinion for e in self.encuestados) / len(self.encuestados), 2)
    self.promedio_experticia = round(sum(e.experticia for e in self.encuestados) / len(self.encuestados), 2)

class Tema: # Representa un tema que contiene preguntas.
  """
  Atributos:
    nombre: Nombre del tema.
    preguntas: Lista de preguntas asociadas al tema.
    promedio_opinion: Promedio de las opiniones de las preguntas del tema.
    promedio_experticia: Promedio de la experticia de las preguntas del tema.
    total_encuestados: Total de encuestados en todas las preguntas del tema.
  """
  def __init__(self, nombre): # Constructor de la clase Tema.
    self.nombre = nombre
    self.preguntas = []
    self.promedio_opinion = 0
    self.promedio_experticia = 0
    self.total_encuestados = 0

  def agregar_pregunta(self, pregunta): # Agrega una pregunta al tema.
    """
    Atributos:
      pregunta: Objeto de tipo Pregunta a agregar.
    """
    self.preguntas.append(pregunta)

  def calcular_promedios(self): # Calcula los promedios de opinión, experticia y total de encuestados en el tema.
    self.total_encuestados = sum(len(p.encuestados) for p in self.preguntas)
    self.promedio_opinion = round(sum(p.promedio_opinion for p in self.preguntas) / len(self.preguntas), 2)
    self.promedio_experticia = round(sum(p.promedio_experticia for p in self.preguntas) / len(self.preguntas), 2)

# Algoritmos de ordenamiento

def quick_sort(arr, low, high, key=lambda x: x):
  """
  Implementación de Quick Sort para ordenar una lista.

  Parámetros:
    arr (list): Lista de elementos a ordenar.
    low (int): Índice inferior del rango a ordenar.
    high (int): Índice superior del rango a ordenar.
    key (function): Función clave para determinar el criterio de ordenamiento.

  Retorna:
    None: El ordenamiento es realizado in-place.
  """
  if low < high:
    pi = particion_quick_sort(arr, low, high, key)
    quick_sort(arr, low, pi - 1, key)
    quick_sort(arr, pi + 1, high, key)

def particion_quick_sort(arr, low, high, key):
  """
  Función auxiliar de Quick Sort que particiona el arreglo en torno a un pivote.

  Parámetros:
    arr (list): Lista de elementos.
    low (int): Índice inferior del rango.
    high (int): Índice superior del rango.
    key (function): Función clave para determinar el criterio de ordenamiento.

  Retorna:
    int: Índice del pivote después de la partición.
  """
  pivot = key(arr[high])
  i = low - 1
  for j in range(low, high):
    if key(arr[j]) <= pivot:
      i += 1
      arr[i], arr[j] = arr[j], arr[i]
  arr[i + 1], arr[high] = arr[high], arr[i + 1]
  return i + 1

def ordenar_encuestados(encuestados):
  """
  Ordena una lista de encuestados.

  Parámetros:
    encuestados (list): Lista de objetos Encuestado a ordenar.

  Retorna:
    None: El ordenamiento es realizado in-place.
  """
  quick_sort(encuestados, 0, len(encuestados) - 1, key=lambda e: (-e.experticia, -e.opinion, e.id))

def ordenar_preguntas(preguntas):
  """
  Ordena una lista de preguntas.

  Parámetros:
    preguntas (list): Lista de objetos Pregunta a ordenar.

  Retorna:
    None: El ordenamiento es realizado in-place.
  """
  quick_sort(preguntas, 0, len(preguntas) - 1, key=lambda p: (-p.promedio_opinion, -p.promedio_experticia, -len(p.encuestados)))

def ordenar_temas(temas):
  """
  Ordena una lista de temas.

  Parámetros:
    temas (list): Lista de objetos Tema a ordenar.

  Retorna:
    None: El ordenamiento es realizado in-place.
  """
  quick_sort(temas, 0, len(temas) - 1, key=lambda t: (-t.promedio_opinion, -t.promedio_experticia, -t.total_encuestados))

# Funciones principales

def leer_entrada(archivo):
  """
  Lee los datos desde el archivo de entrada y construye los objetos correspondientes a encuestados, preguntas y temas.

  Parámetros:
    archivo (str): Ruta al archivo de entrada.

  Retorna:
    tuple: Un diccionario de encuestados y una lista de temas.
  """
  with open(archivo, 'r', encoding='utf-8') as texto:
    contenido = texto.read().strip()

  bloques = contenido.split('\n\n')
  bloque_encuestados = bloques[0]
  bloque_temas = bloques[1:]

  encuestados = {}
  for idx, linea in enumerate(bloque_encuestados.split('\n'), start=1):
    if linea.strip():
      nombre, atributos = linea.split(', Experticia:')
      experticia, opinion = map(int, atributos.split(', Opinión:'))
      encuestados[idx] = Encuestado(idx, nombre.strip(), experticia, opinion)

  temas = []
  for tema_idx, bloque in enumerate(bloque_temas, start=1):
    tema = Tema(f"Tema {tema_idx}")
    for pregunta_idx, linea in enumerate(bloque.split('\n'), start=0): # 
      if linea.strip():
        pregunta = Pregunta(f"Pregunta {tema_idx}.{pregunta_idx}")
        ids = map(int, filter(None, linea.strip('{}').split(',')))
        for encuestado_id in ids:
          pregunta.agregar_encuestado(encuestados[encuestado_id])
        pregunta.calcular_promedios()
        ordenar_encuestados(pregunta.encuestados)
        tema.agregar_pregunta(pregunta)
    tema.calcular_promedios()
    ordenar_preguntas(tema.preguntas)
    temas.append(tema)

  return encuestados, temas


def calcular_metricas(temas, encuestados):
  """
  Calcula las métricas principales basadas en los datos de las preguntas y los encuestados.

  Parámetros:
    temas (list): Lista de objetos Tema.
    encuestados (dict): Diccionario de objetos Encuestado.

  Retorna:
    dict: Diccionario con las métricas calculadas, incluyendo máximos, mínimos y promedios.
  """
  preguntas = [pregunta for tema in temas for pregunta in tema.preguntas]

  pregunta_mayor_opinion = max(preguntas, key=lambda p: p.promedio_opinion)
  pregunta_menor_opinion = min(preguntas, key=lambda p: p.promedio_opinion)
  pregunta_mayor_experticia = max(preguntas, key=lambda p: p.promedio_experticia)
  pregunta_menor_experticia = min(preguntas, key=lambda p: p.promedio_experticia)
  encuestado_mayor_opinion = max(encuestados.values(), key=lambda e: e.opinion)
  encuestado_menor_opinion = min(encuestados.values(), key=lambda e: e.opinion)
  encuestado_mayor_experticia = max(encuestados.values(), key=lambda e: e.experticia)
  encuestado_menor_experticia = min(encuestados.values(), key=lambda e: e.experticia)
  promedio_experticia = round(sum(e.experticia for e in encuestados.values()) / len(encuestados), 2)
  promedio_opinion = round(sum(e.opinion for e in encuestados.values()) / len(encuestados), 2)

  return {
    "pregunta_mayor_opinion": pregunta_mayor_opinion,
    "pregunta_menor_opinion": pregunta_menor_opinion,
    "pregunta_mayor_experticia": pregunta_mayor_experticia,
    "pregunta_menor_experticia": pregunta_menor_experticia,
    "encuestado_mayor_opinion": encuestado_mayor_opinion,
    "encuestado_menor_opinion": encuestado_menor_opinion,
    "encuestado_mayor_experticia": encuestado_mayor_experticia,
    "encuestado_menor_experticia": encuestado_menor_experticia,
    "promedio_experticia": promedio_experticia,
    "promedio_opinion": promedio_opinion,
  }


def escribir_salida(archivo, temas, encuestados, metricas):
  """
  Escribe los resultados de la encuesta, los datos de los encuestados y las métricas calculadas en el archivo de salida.

  Parámetros:
    archivo (str): Ruta al archivo de salida.
    temas (list): Lista de objetos Tema.
    encuestados (dict): Diccionario de objetos Encuestado.
    metricas (dict): Diccionario con las métricas calculadas.

  Retorna:
    None
  """
  with open(archivo, 'w', encoding='utf-8') as texto:
    texto.write("Resultados de la encuesta:\n\n")
    for tema in temas:
      texto.write(f"[{tema.promedio_opinion}] {tema.nombre}:\n")
      for pregunta in tema.preguntas:
        ids = ", ".join(str(e.id) for e in pregunta.encuestados)
        texto.write(f" [{pregunta.promedio_opinion}] {pregunta.id}: ({ids})\n")
      texto.write("\n")

    texto.write("Lista de encuestados:\n")
    lista_encuestados = list(encuestados.values())
    ordenar_encuestados(lista_encuestados)
    texto.write("\n".join(str(e) for e in lista_encuestados) + "\n\n")

    texto.write("Resultados:\n")
    texto.write(f"  Pregunta con mayor promedio de opinión: [{metricas['pregunta_mayor_opinion'].promedio_opinion}] {metricas['pregunta_mayor_opinion'].id}\n")
    texto.write(f"  Pregunta con menor promedio de opinión: [{metricas['pregunta_menor_opinion'].promedio_opinion}] {metricas['pregunta_menor_opinion'].id}\n")
    texto.write(f"  Pregunta con mayor promedio de experticia: [{metricas['pregunta_mayor_experticia'].promedio_experticia}] {metricas['pregunta_mayor_experticia'].id}\n")
    texto.write(f"  Pregunta con menor promedio de experticia: [{metricas['pregunta_menor_experticia'].promedio_experticia}] {metricas['pregunta_menor_experticia'].id}\n")
    texto.write(f"  Encuestado con mayor opinión: {metricas['encuestado_mayor_opinion']}\n")
    texto.write(f"  Encuestado con menor opinión: {metricas['encuestado_menor_opinion']}\n")
    texto.write(f"  Encuestado con mayor experticia: {metricas['encuestado_mayor_experticia']}\n")
    texto.write(f"  Encuestado con menor experticia: {metricas['encuestado_menor_experticia']}\n")
    texto.write(f"  Promedio de experticia de los encuestados: {metricas['promedio_experticia']}\n")
    texto.write(f"  Promedio de opinión de los encuestados: {metricas['promedio_opinion']}\n")

def main(): # Función principal
  """
  Parámetros:
    Ninguno.

  Retorna:
    None: Ejecuta todo el flujo de trabajo y escribe los resultados en un archivo.
  """

  # Nombre (si están en el mismo directorio del código) o ruta del archivo de texto con la entrada y la salida incluyendo la extensión .txt
  # Si no se define un archivo de salida, por defecto se creará uno de nombre "salida_Victoria_Salas_Córdoba_Ramirez.txt"
  archivo_entrada = "archivos_de_entrada\\entrada_prueba_1.txt"
  archivo_salida = "salida_Victoria_Salas_Córdoba_Ramirez.txt"

  encuestados, temas = leer_entrada(archivo_entrada)
  ordenar_temas(temas)
  metricas = calcular_metricas(temas, encuestados)

  escribir_salida(archivo_salida, temas, encuestados, metricas)

  print("\033c", end="")
  print("\nResultados solución #2:\nPrueba ejecutada:", archivo_entrada)
  print("Ejecución exitosa, archivo de texto con la salida:", archivo_salida)
  subprocess.Popen(['notepad', archivo_salida]) # Apertura automática del archivo de salida

if __name__ == "__main__": # Método de ejecución
  main()