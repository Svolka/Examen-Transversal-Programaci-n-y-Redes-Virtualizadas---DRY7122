# vlan_validator.py

def validar_vlan():
    print("=== Validador de Rangos de VLAN ===")
    try:
        vlan = int(input("Ingrese el número de VLAN a validar: "))

        if vlan == 1:
            print(f"La VLAN {vlan} es la VLAN por defecto (Rango Normal).")
        elif 2 <= vlan <= 1001:
            print(f"La VLAN {vlan} corresponde al Rango Normal (Uso general).")
        elif 1002 <= vlan <= 1005:
            print(f"La VLAN {vlan} corresponde al Rango Normal (Reservadas para Token Ring/FDDI).")
        elif 1006 <= vlan <= 4094:
            print(f"La VLAN {vlan} corresponde al Rango Extendido (Proveedores / SD-WAN).")
        else:
            print("Número de VLAN inválido. El rango correcto en switches Cisco es de 1 a 4094.")

    except ValueError:
        print("Error: Por favor, ingrese un número entero válido.")

if __name__ == "__main__":
    validar_vlan()
