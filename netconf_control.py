# netconf_control.py
from ncclient import manager
import sys

# Parámetros de conexión al CSR1000v (Configurados con tu IP y contraseña real)
ROUTER_IP = "192.168.18.207"
NETCONF_PORT = 830
USUARIO = "cisco"
CONTRASENA = "cisco123!"

# 1. XML de configuración para cambiar el Hostname
xml_hostname = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>Valdes-DRY7122</hostname>
    </native>
</config>
"""

# 2. XML de configuración para crear y levantar la Loopback 11
xml_loopback = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback>
                <name>11</name>
                <description>Loopback 11 - Creada via NETCONF por Marcelo Valdes</description>
                <ip>
                    <address>
                        <primary>
                            <address>11.11.11.11</address>
                            <mask>255.255.255.255</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
    </native>
</config>
"""

def main():
    print(f"[i] Conectando via NETCONF a {ROUTER_IP}:{NETCONF_PORT}...")
    
    try:
        # Usamos unknown_host_cb para saltar la validación de firmas SSH de forma compatible
        with manager.connect(
            host=ROUTER_IP,
            port=NETCONF_PORT,
            username=USUARIO,
            password=CONTRASENA,
            device_params={'name': 'iosxe'},
            unknown_host_cb=lambda host, fingerprint: True
        ) as m:
            
            print("[+] ¡Conexión NETCONF establecida con éxito!")
            print("--------------------------------------------------")
            
            # Requerimiento 1: Cambiar el Hostname
            print("[i] Enviando solicitud RPC para modificar el Hostname...")
            respuesta_hostname = m.edit_config(target='running', config=xml_hostname)
            if "<ok/>" in str(respuesta_hostname):
                print("[+] Cambiado con éxito: El nuevo Hostname es 'Valdes-DRY7122'.")
            else:
                print("[-] Error o advertencia al cambiar el Hostname.")
                
            print("--------------------------------------------------")
            
            # Requerimiento 2: Crear la Loopback 11
            print("[i] Enviando solicitud RPC para aprovisionar Loopback 11...")
            respuesta_loopback = m.edit_config(target='running', config=xml_loopback)
            if "<ok/>" in str(respuesta_loopback):
                print("[+] ¡Interfaz Loopback 11 (11.11.11.11/32) configurada y activa!")
            else:
                print("[-] Error o advertencia al aprovisionar la interfaz.")
                
            print("--------------------------------------------------")
            print("[+] Operaciones NETCONF completadas de manera exitosa.")
            
    except Exception as e:
        print(f"\n[!] Error crítico de conexión o ejecución NETCONF:\n{e}")

if __name__ == "__main__":
    main()
