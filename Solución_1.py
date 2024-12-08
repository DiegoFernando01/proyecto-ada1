# Librerías necesarias

import subprocess # Se utiliza para abrir el archivo de salidas automatimente tras una ejecución de una entrada.

# Clases y estructuras de datos utilizadas

class nodo: # Representa un nodo de un árbol binario de búsqueda (BST).
  """
  Atributos:
    key: Clave utilizada para ordenar y buscar nodos en el árbol.
    value: Valor asociado al nodo (por defecto es None).
    left: Nodo hijo izquierdo (por defecto es None).
    right: Nodo hijo derecho (por defecto es None).
  """

  def __init__(self, key, value=None):
    self.key = key
    self.value = value
    self.left = None
    self.right = None

class arbol_binario: # Árbol binario de búsqueda (Binary Search Tree).
  """
  Atributos:
    root: Raíz del árbol (por defecto es None).
  Métodos:
    insert(key, value): Inserta un nodo con la clave y el valor proporcionados.
    inorder(): Devuelve una lista de los valores en el árbol en orden ascendente.
  """
  def __init__(self):
    self.root = None

  def insert(self, key, value=None): # Inserta un nodo en el árbol
    """
    Atributos:
      key: Clave para ordenar el nodo en el árbol.
      value: Valor asociado al nodo (por defecto es None).
    """
    if not self.root:
      self.root = nodo(key, value)
    else:
      self._insert(self.root, key, value)

  def _insert(self, node, key, value): # Inserta un nodo de manera recursiva en el árbol.
    """
    Atributos:
      node: Nodo actual del árbol.
      key: Clave del nodo a insertar.
      value: Valor asociado al nodo.
    """
    if key < node.key:
      if node.left:
        self._insert(node.left, key, value)
      else:
        node.left = nodo(key, value)
    else:
      if node.right:
        self._insert(node.right, key, value)
      else:
        node.right = nodo(key, value)

  def inorder(self): # Obtiene los valores del árbol en orden ascendente.
    """
    Returns:
      Lista de valores del árbol en orden ascendente.
    """
    result = []
    self._inorder(self.root, result)
    return result

  def _inorder(self, node, result): # Realiza un recorrido in-order recursivo.
    """
    Atributos:
      node: Nodo actual del árbol.
      result: Lista para almacenar los valores en orden.
    """
    if node:
      self._inorder(node.left, result)
      result.append(node.value)
      self._inorder(node.right, result)

class Encuestado: # Representa a un encuestado en el sistema.
  """
  Atributos:
    id: Identificador único del encuestado.
    nombre: Nombre del encuestado.
    experticia: Nivel de experticia del encuestado.
    opinion: Opinión del encuestado.
  """
  def __init__(self, id_, nombre, experticia, opinion):
    self.id = id_
    self.nombre = nombre
    self.experticia = experticia
    self.opinion = opinion

  def __repr__(self): 
    return f"({self.id}, Nombre: '{self.nombre}', Experticia: {self.experticia}, Opinión: {self.opinion})"

class Pregunta: # Representa una pregunta en el sistema.
  """
  Atributos:
    id: Identificador único de la pregunta.
    encuestados: Árbol binario que contiene a los encuestados que respondieron la pregunta.
    promedio_opinion: Promedio de las opiniones de los encuestados.
    promedio_experticia: Promedio de la experticia de los encuestados.
  """
  def __init__(self, id_):
    self.id = id_
    self.encuestados = arbol_binario()
    self.promedio_opinion = 0
    self.promedio_experticia = 0

  def agregar_encuestado(self, encuestado): # Agrega un encuestado a la pregunta.
    """
    Atributos:
      encuestado: Objeto de tipo Encuestado a agregar.
    """
    key = (-encuestado.opinion, -encuestado.experticia, -encuestado.id)
    self.encuestados.insert(key, encuestado)

  def calcular_promedios(self): # Calcula los promedios de opinión y experticia basados en los encuestados.
    encuestados = self.encuestados.inorder()
    self.promedio_opinion = round(sum(e.opinion for e in encuestados) / len(encuestados), 2)
    self.promedio_experticia = round(sum(e.experticia for e in encuestados) / len(encuestados), 2)

class Tema: # Representa un tema que contiene preguntas.
  """
  Atributos:
    nombre: Nombre del tema.
    preguntas: Árbol binario que contiene las preguntas asociadas al tema.
    promedio_opinion: Promedio de las opiniones de las preguntas del tema.
    promedio_experticia: Promedio de la experticia de las preguntas del tema.
    total_encuestados: Total de encuestados en todas las preguntas del tema.
  """
  def __init__(self, nombre):
    self.nombre = nombre
    self.preguntas = arbol_binario()
    self.promedio_opinion = 0
    self.promedio_experticia = 0

  def agregar_pregunta(self, pregunta): # Agrega una pregunta al tema.
    """
    Atributos:
      pregunta: Objeto de tipo Pregunta a agregar.
    """
    key = (-pregunta.promedio_opinion, -pregunta.promedio_experticia, -len(pregunta.encuestados.inorder()))
    self.preguntas.insert(key, pregunta)

  def calcular_promedios(self): # Calcula los promedios de opinión, experticia y total de encuestados en el tema.
    preguntas = self.preguntas.inorder()
    self.promedio_opinion = round(sum(p.promedio_opinion for p in preguntas) / len(preguntas), 2)
    self.promedio_experticia = round(sum(p.promedio_experticia for p in preguntas) / len(preguntas), 2)
    self.total_encuestados = sum(len(p.encuestados.inorder()) for p in preguntas)

# Definición de funciónes para la implementación de la solución #1

def leer_entradas(archivo): # Lee y procesa la entrada para crear objetos de tipo Encuestado, Pregunta y Tema. Calcula los promedios de opiniones y experticia.
  """
  Parámetros:
    archivo (str): Ruta del archivo de entrada.
  Retorna:
    tupla (encuestados, temas):
      - encuestados (dict): Diccionario con los encuestados indexados por ID.
      - temas (list): Lista de objetos Tema con preguntas y encuestados procesados.
  """
  with open(archivo, 'r', encoding='utf-8') as texto: # Lectura del archivo de entrada
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
    preguntas = [linea for linea in bloque.split('\n') if linea.strip()]
    for pregunta_idx, linea in enumerate(preguntas, start=1):
      pregunta = Pregunta(f"Pregunta {tema_idx}.{pregunta_idx}")
      ids = map(int, filter(None, linea.strip('{}').split(',')))
      for encuestado_id in ids:
        pregunta.agregar_encuestado(encuestados[encuestado_id])
      pregunta.calcular_promedios()
      tema.agregar_pregunta(pregunta)
    tema.calcular_promedios()
    temas.append(tema)

  return encuestados, temas

def merge_sort(arr, key=lambda x: x): # Implementación del algoritmo de ordenamiento Merge Sort.
  """
  Parámetros:
    arr (list): Lista de elementos a ordenar.
    key (función, opcional): Función que define el criterio de ordenación.
  Retorna:
    list: Lista ordenada según el criterio especificado.
  """
  if len(arr) <= 1:
    return arr

  mid = len(arr) // 2
  left = merge_sort(arr[:mid], key)
  right = merge_sort(arr[mid:], key)

  return merge(left, right, key)

def merge(left, right, key): # Combina dos listas ordenadas en una sola lista también ordenada.
  """
  Parámetros:
    left (list): Sublista izquierda ordenada.
    right (list): Sublista derecha ordenada.
    key (función): Función que define el criterio de comparación.
  Retorna:
    list: Lista combinada y ordenada.
  """
  result = []
  i = j = 0

  while i < len(left) and j < len(right):
    if key(left[i]) <= key(right[j]):
      result.append(left[i])
      i += 1
    else:
      result.append(right[j])
      j += 1

  result.extend(left[i:])
  result.extend(right[j:])

  return result

def maximo(iterable, key=lambda x: x): # Encuentra el elemento máximo en un iterable basado en un criterio.
  """
  Parámetros:
    iterable (iterable): Colección de elementos.
    key (función, opcional): Función que define el criterio de comparación.
  Retorna:
    object: Elemento máximo según el criterio.
  """
  max_element = None
  max_value = None

  for item in iterable:
    value = key(item)
    if max_value is None or value > max_value:
      max_value = value
      max_element = item

  return max_element

def minimo(iterable, key=lambda x: x): # Encuentra el elemento mínimo en un iterable basado en un criterio.
  """
  Parámetros:
    iterable (iterable): Colección de elementos.
    key (función, opcional): Función que define el criterio de comparación.
  Retorna:
    object: Elemento mínimo según el criterio.
  """
  min_element = None
  min_value = None

  for item in iterable:
    value = key(item)
    if min_value is None or value < min_value:
      min_value = value
      min_element = item

  return min_element

def calcular_metricas(temas, encuestados): # Calcula métricas como preguntas con mayor o menor promedio de opinión y experticia, y encuestados destacados.
  """
  Parámetros:
    temas (list): Lista de objetos Tema procesados.
    encuestados (dict): Diccionario de objetos Encuestado.
  Retorna:
    dict: Diccionario con las métricas calculadas, incluyendo preguntas, encuestados destacados y promedios generales.
  """
  pregunta_mayor_opinion = None
  pregunta_menor_opinion = None
  pregunta_mayor_experticia = None
  pregunta_menor_experticia = None
  mayor_opinion = float('-inf')
  menor_opinion = float('inf')
  mayor_experticia = float('-inf')
  menor_experticia = float('inf')

  for tema in temas:
    for pregunta in tema.preguntas.inorder():
      if pregunta.promedio_opinion > mayor_opinion:
        mayor_opinion = pregunta.promedio_opinion
        pregunta_mayor_opinion = pregunta
      if pregunta.promedio_opinion < menor_opinion:
        menor_opinion = pregunta.promedio_opinion
        pregunta_menor_opinion = pregunta
      if pregunta.promedio_experticia > mayor_experticia:
        mayor_experticia = pregunta.promedio_experticia
        pregunta_mayor_experticia = pregunta
      if pregunta.promedio_experticia < menor_experticia:
        menor_experticia = pregunta.promedio_experticia
        pregunta_menor_experticia = pregunta

  encuestado_mayor_opinion = maximo(encuestados.values(), key=lambda e: (e.opinion, e.id))
  encuestado_menor_opinion = minimo(encuestados.values(), key=lambda e: (e.opinion, e.id))
  encuestado_mayor_experticia = maximo(encuestados.values(), key=lambda e: (e.experticia, e.opinion, -e.id))
  encuestado_menor_experticia = minimo(encuestados.values(), key=lambda e: (e.experticia, e.opinion, e.id))
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

def escribir_salidas(archivo, temas, encuestados, metricas): # Escribe los resultados del análisis en el archivo de texto
  """
  Parámetros:
    archivo (str): Ruta del archivo de salida.
    temas (list): Lista de objetos Tema procesados.
    encuestados (dict): Diccionario de objetos Encuestado.
    metricas (dict): Diccionario con las métricas calculadas.
  Retorna:
    None: Escribe directamente en el archivo especificado.
  """
  with open(archivo, 'w', encoding='utf-8') as texto:
    texto.write("Resultados de la encuesta:\n\n") # Impresión resultados de la encuesta
    for tema in temas:
      texto.write(f"[{tema.promedio_opinion}] {tema.nombre}:\n")
      for pregunta in tema.preguntas.inorder():
        encuestados_ordenados = pregunta.encuestados.inorder()
        ids = ", ".join(str(e.id) for e in encuestados_ordenados)
        texto.write(f" [{pregunta.promedio_opinion}] {pregunta.id}: ({ids})\n")
      texto.write("\n")

    texto.write("Lista de encuestados:\n") # Impresión del listado de encuestados
    lista_encuestados = merge_sort(list(encuestados.values()), key=lambda e: (-e.experticia, -e.opinion, e.id))
    texto.write("\n".join(str(e) for e in lista_encuestados) + "\n\n")

    texto.write("Resultados:\n") # Impresión de métricas de la encuesta
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

  encuestados, temas = leer_entradas(archivo_entrada)
  temas = merge_sort(temas, key=lambda t: (-t.promedio_opinion, -t.promedio_experticia, -t.total_encuestados))
  metricas = calcular_metricas(temas, encuestados)

  escribir_salidas(archivo_salida, temas, encuestados, metricas)

  print("\033c", end="")
  print("\nResultados:\nPrueba ejecutada:", archivo_entrada)
  print("Ejecución exitosa, archivo de texto con la salida:", archivo_salida)
  subprocess.Popen(['notepad', archivo_salida]) # Apertura automática del archivo de salida

if __name__ == "__main__": # Método de ejecución
  main()
