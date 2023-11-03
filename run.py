# Programa para levantar automaticamente el proyecto en dev y produccion
import os
import subprocess

# Establecer códigos de escape ANSI para los colores
rojo = "\033[91m"
verde = "\033[92m"
azul = "\033[94m"
amarillo = "\033[93m"
morado = "\033[95m"
resetear = "\033[0m"  # Para restablecer al color por defecto

# Establecer códigos de escape ANSI para los colores
rojo = "\033[91m"
verde = "\033[92m"
azul = "\033[94m"
amarillo = "\033[93m"
morado = "\033[95m"
resetear = "\033[0m"  # Para restablecer al color por defecto


def main():
    os.system("clear")
    print(morado + "PROGRAMA DE SET UP CMS IS2 - 2023 - GRUPO 2"+ resetear)
    print(morado + "TheLittleSwine.com"+resetear)

    while True:
        print("\nOpciones:")
        print("1. Ejecutar en Desarrollo")
        print("2. Ejecutar en Producción")
        print("3. Crear y ejecutar documentación")
        print("4. Salir")

        opcion = input("Seleccione una opción (1/2/3): ")

        if opcion == "1":
            ejecutar_en_desarrollo()
            break
        elif opcion == "2":
            ejecutar_en_produccion()
            break
        elif opcion == "3":
            crear_documentacion()
            break
        else:
            print("Opción no válida. Por favor, seleccione 1, 2 o 3.")

def crear_documentacion():
    print(azul+"[INFO] "+resetear+"Inicia el proceso de creacion de documentacion")

def ejecutar_en_desarrollo():
    os.system("clear")
    mostrar_opciones()
    tag = input("Ingrese el tag específico: ")
    cadena = "iteracion_" + str(tag)
    print(azul+"[INFO] "+resetear+"Ejecutando en el entorno de " + azul + "DESARROLLO" + resetear + " con el tag" + azul + f" {cadena} " + resetear)
    checkout_to_tag(cadena)
    eliminar_migraciones()
    ejecutar_docker_dev("docker-compose-dev.yaml")
    print(verde + "[SUCCESS] " + resetear + "Ejecucion exitosa de DESARROLLO")


def ejecutar_docker_dev(compose_file):
    print(azul + "[INFO] " + resetear + "Inicia el proceso para crear para levantar los contenedores")
    print(azul + "[INFO] " + resetear + "Se ejecuta el archivo"+morado + f"[{compose_file}] " + resetear)

    try:
        # Construye el comando docker-compose
        comando = ["docker-compose", "-f", compose_file, "up", "--build", "-d"]
        # Ejecuta el comando
        subprocess.run(comando, check=True)
        print(amarillo + "[WARN] " + resetear +"Ejecutando en segundo plano")
    except subprocess.CalledProcessError:
        print(rojo + "[ERROR] " + resetear + f"Error al ejecutar el archivo"+morado + f"[{compose_file}] " + resetear)

    print(azul + "[INFO] " + resetear + "Finaliza el proceso para levantar los contenedores")

def eliminar_migraciones():
    print(amarillo + "[WARN] " + resetear + "Se ejecuta el comando para eliminar migraciones y base de datos ")
    comando = "./delete-migrations.sh"
    try:
        subprocess.run(comando, shell=True, check=True)
    except subprocess.CalledProcessError:
        comando_sudo = f"sudo {comando}"
        subprocess.run(comando_sudo, shell=True, check=True)

    print(azul + "[INFO] " + resetear + "Se elimino los archivos de migraciones")

def checkout_to_tag(tag):
    print(azul + "[INFO] " + resetear + "Inicia el proceso de cambio de tag")
    try:
        # Realiza un checkout al tag específico
        subprocess.run(["git", "checkout", tag], check=True)

        print(verde + "[SUCCESS] " + resetear +f"Checkout al tag '{tag}' exitoso.")
    except subprocess.CalledProcessError:
        print(rojo + "[ERROR] " + resetear + f"Error al realizar el checkout al tag '{tag}'.")

    print(azul + "[INFO] " + resetear + "Finaliza la rutina de cambio de tag")




def ejecutar_en_produccion():
    os.system("clear")
    mostrar_opciones()
    tag = input("Ingrese el tag específico: ")
    cadena = "iteracion_" + str(tag)
    print(azul+"[INFO] "+resetear+"Ejecutando en el entorno de "+azul+"PRODUCCION"+resetear+" con el tag"+azul+f" {cadena}"+resetear)
    checkout_to_tag(cadena)
    print(morado+"EN EL CASO DE PROD, NO EJECUTAMOS POBLACION DE BASE DE DATOS PORQUE SE MONTA EN UNA BASE DE DATOS EXTERNA"+resetear)
    ejecutar_docker_dev("docker-compose-prod.yaml")
    print(verde + "[SUCCESS] " + resetear + "Ejecucion exitosa de PRODUCCION")


def mostrar_opciones():
    print(morado+f"\nTAGS DISPONIBLES:"+resetear)
    opciones_validas = ["iteracion_1", "iteracion_2", "iteracion_3", "iteracion_4", "iteracion_5"]
    for i, opcion in enumerate(opciones_validas, 1):
        print(f"{i}. {opcion}")


if __name__ == "__main__":
    main()
