import random
import os

def generar_entrada(nombre_archivo, num_encuestados, num_temas, max_preguntas):
  """
  Genera un archivo de entrada con datos simulados.

  Parámetros:
  - nombre_archivo (str): Nombre del archivo de salida.
  - num_encuestados (int): Número de encuestados.
  - num_temas (int): Número de temas.
  - max_preguntas (int): Número máximo de preguntas por tema.

  Retorno:
  - None
  """
  with open(nombre_archivo, "w", encoding="utf-8") as archivo:
    # Generar encuestados
    for i in range(1, num_encuestados + 1):
      nombre = f"Encuestado #{i}"
      experticia = random.randint(1, 10)
      opinion = random.randint(0, 10)
      archivo.write(f"{nombre}, Experticia:{experticia}, Opinión:{opinion}\n")

    archivo.write("\n")

    # Generar temas y preguntas
    for tema in range(1, num_temas + 1):
      archivo.write("\n")
      num_preguntas = random.randint(1, max_preguntas)
      for pregunta in range(1, num_preguntas + 1):
        encuestados_por_pregunta = random.sample(
          range(1, num_encuestados + 1), random.randint(1, min(10, num_encuestados))
        )
        archivo.write(f"{{{", ".join(map(str, encuestados_por_pregunta))}}}\n")
      archivo.write("\n")

# Parámetros para los archivos
configuraciones = [ # Cantidad encuestados, cantidad de temas, número máximo de preguntas por tema
  ("entrada_100.txt", 100, 5, 10), # 100 encuestados, 5 temas, 10 preguntas por tema máximo
  ("entrada_1000.txt", 1000, 20, 30), # 1000 encuestados, 20 temas, 30 preguntas por tema máximo
  ("entrada_10000.txt", 10000, 50, 100), # 10000 encuestados, 50 temas, 100 preguntas por tema máximo
  ("entrada_100000.txt", 100000, 100, 200), # 100000 encuestados, 100 temas, 200 preguntas por tema máximo
  ("entrada_1000000.txt", 1000000, 200, 400), # 1000000 encuestados, 200 temas, 400 preguntas por tema máximo
  #("entrada_10000000.txt", 10000000, 400, 800), # 10000000 encuestados, 400 temas, 800 preguntas por tema máximo - Pesa alrededor de 500 megabytes
]

# Crea el directorio para guardar las entradas
os.makedirs("entradas_generadas", exist_ok=True)

# Genera los archivos
for config in configuraciones:
  generar_entrada(os.path.join("entradas_generadas", config[0]), config[1], config[2], config[3])

print("\nArchivos de entrada generados guardados en el directorio 'entradas_generadas'.")