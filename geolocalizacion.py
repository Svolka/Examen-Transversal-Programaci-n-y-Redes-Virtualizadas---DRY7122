
import requests


API_KEY = "default"

def obtener_coordenadas(ciudad, pais):
    """Busca las coordenadas de una ciudad usando la API de Geocoding."""
    url = f"https://graphhopper.com/api/1/geocode?q={ciudad},{pais}&locale=es&key={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        datos = response.json()
        if datos.get("hits"):

            primer_resultado = datos["hits"][0]
            lat = primer_resultado["point"]["lat"]
            lng = primer_resultado["point"]["lng"]
            nombre_completo = primer_resultado["name"]
            return lat, lng, nombre_completo
    except Exception as e:
        print(f"Error al conectar con el servicio de mapas: {e}")
    return None

def calcular_ruta(lat_origen, lng_origen, lat_destino, lng_destino, perfil_transporte):
    """Calcula la distancia y duración de la ruta entre dos puntos."""
    url = f"https://graphhopper.com/api/1/route?point={lat_origen},{lng_origen}&point={lat_destino},{lng_destino}&profile={perfil_transporte}&locale=es&calc_points=false&key={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        datos = response.json()
        if "paths" in datos:
            return datos["paths"][0]
    except Exception as e:
        print(f"Error al calcular el trayecto: {e}")
    return None

def main():
    while True:
        print("\n" + "="*50)
        print("   SISTEMA DE GEOLOCALIZACIÓN CHILE - ARGENTINA")
        print("="*50)
        print("Nota: Ingrese 's' en cualquier momento para salir del programa.\n")
        
        # 1. Solicitar Ciudad de Origen (Chile)
        ciudad_origen = input("Ingrese Ciudad de Origen (Chile): ").strip()
        if ciudad_origen.lower() == 's':
            print("Saliendo del programa... ¡Hasta luego, Marcelo!")
            break
            
        # 2. Solicitar Ciudad de Destino (Argentina)
        ciudad_destino = input("Ingrese Ciudad de Destino (Argentina): ").strip()
        if ciudad_destino.lower() == 's':
            print("Saliendo del programa... ¡Hasta luego, Marcelo!")
            break
            
        if not ciudad_origen or not ciudad_destino:
            print("Error: Los nombres de las ciudades no pueden estar vacíos.")
            continue

        # 3. Selección del medio de transporte
        print("\nSeleccione su medio de transporte:")
        print("1) Automóvil (Car)")
        print("2) Bicicleta (Bike)")
        print("3) Caminando (Foot)")
        opcion = input("Seleccione una opción (1-3): ").strip()
        
        if opcion.lower() == 's':
            break
            
        # Mapeo de perfiles aceptados nativamente por GraphHopper
        if opcion == "1":
            perfil = "car"
            transporte_txt = "Automóvil"
        elif opcion == "2":
            perfil = "bike"
            transporte_txt = "Bicicleta"
        elif opcion == "3":
            perfil = "foot"
            transporte_txt = "Caminata"
        else:
            print("Opción inválida. Se seleccionará Automóvil por defecto.")
            perfil = "car"
            transporte_txt = "Automóvil"

        print("\n[i] Buscando coordenadas geográficas en la API...")
        coord_origen = obtener_coordenadas(ciudad_origen, "Chile")
        coord_destino = obtener_coordenadas(ciudad_destino, "Argentina")
        
        if not coord_origen:
            print(f"No se pudo localizar la ciudad de origen: '{ciudad_origen}' en Chile. Intente de nuevo.")
            continue
        if not coord_destino:
            print(f"No se pudo localizar la ciudad de destino: '{ciudad_destino}' en Argentina. Intente de nuevo.")
            continue
            
        print(f" -> Origen confirmado: {coord_origen[2]}")
        print(f" -> Destino confirmado: {coord_destino[2]}")
        
        print("[i] Trazando ruta internacional y calculando métricas...")
        ruta = calcular_ruta(coord_origen[0], coord_origen[1], coord_destino[0], coord_destino[1], perfil)
        
        if ruta:
            # GraphHopper entrega la distancia en metros y el tiempo en milisegundos
            distancia_km = ruta["distance"] / 1000
            distancia_millas = distancia_km * 0.621371
            
            tiempo_minutos = ruta["time"] / 60000
            horas = int(tiempo_minutos // 60)
            minutos = int(tiempo_minutos % 60)
            
            print("\n" + "-"*45)
            print("          RESULTADOS DEL VIAJE")
            print("-"*45)
            print(f"Distancia total: {distancia_km:.2f} Kilómetros")
            print(f"Distancia total: {distancia_millas:.2f} Millas")
            print(f"Duración estimada: {horas} horas con {minutos} minutos")
            print(f"Medio utilizado: {transporte_txt}")
            print("-"*45)
            print("\nNARRATIVA DEL VIAJE:")
            print(f"El viaje comienza en la ciudad de {coord_origen[2]} (Chile). Iniciando el trayecto en")
            print(f"{transporte_txt}, se avanza cruzando los complejos fronterizos de la Cordillera de los Andes")
            print(f"para finalmente adentrarse en territorio argentino, concluyendo de manera exitosa el recorrido")
            print(f"en el destino planificado: {coord_destino[2]}.")
            print("-" * 45)
        else:
            print("\n[!] No se pudo estructurar una ruta transfronteriza válida para el medio de transporte seleccionado.")

if __name__ == "__main__":
    main()
