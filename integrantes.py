

def mostrar_integrantes():

    integrantes = [
        "Marcelo Nicolás Valdés Maureira"
    ]

    print("\n=======================================")
    print("  Examen Transversal DRY7122 - Repositorio")
    print("=======================================")
    for i, integrante in enumerate(integrantes, start=1):
        print(f"{i}. {integrante}")
    print("=======================================\n")

if __name__ == "__main__":
    mostrar_integrantes()
