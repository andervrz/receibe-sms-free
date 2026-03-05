import receive_sms
import time
import os
from datetime import datetime

# ─────────────────────────────────────────
#  Números públicos disponibles (gratuitos)
#  Puedes buscar más en: https://receive-smss.com
# ─────────────────────────────────────────
NUMEROS_DISPONIBLES = [
    "12018577757",   # USA
    "14155552671",   # USA (ejemplo)
    "447700900077",  # UK (ejemplo)
]

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_mensajes(numero: str):
    """Obtiene y muestra los mensajes de un número virtual."""
    print(f"\n📡 Consultando mensajes para: +{numero}")
    print("─" * 50)

    try:
        mensajes = receive_sms.get_messages(phone_number=numero)

        if not mensajes:
            print("📭 No hay mensajes en este número.")
            return

        print(f"📬 {len(mensajes)} mensaje(s) encontrado(s):\n")

        for i, msg in enumerate(mensajes, 1):
            print(f"  [{i}] De:      +{msg.from_number}")
            print(f"       Texto:   {msg.text}")
            try:
                fecha = msg.date.strftime("%d/%m/%Y %H:%M")
            except Exception:
                fecha = str(msg.date)
            print(f"       Fecha:   {fecha}")
            print("  " + "·" * 40)

    except Exception as e:
        print(f"❌ Error al obtener mensajes: {e}")
        print("   Verifica tu conexión o prueba otro número.")

def monitoreo_continuo(numero: str, intervalo: int = 30):
    """Monitorea un número cada X segundos y muestra nuevos mensajes."""
    print(f"\n🔄 Modo monitoreo activo — Revisando cada {intervalo}s")
    print("   Presiona Ctrl+C para detener.\n")

    mensajes_vistos = set()

    while True:
        try:
            mensajes = receive_sms.get_messages(phone_number=numero)
            nuevos = [m for m in mensajes if m.text not in mensajes_vistos]

            if nuevos:
                hora = datetime.now().strftime("%H:%M:%S")
                print(f"\n🔔 [{hora}] {len(nuevos)} nuevo(s) mensaje(s):")
                for msg in nuevos:
                    print(f"   De +{msg.from_number}: {msg.text}")
                    mensajes_vistos.add(msg.text)
            else:
                hora = datetime.now().strftime("%H:%M:%S")
                print(f"   [{hora}] Sin mensajes nuevos...", end="\r")

            time.sleep(intervalo)

        except KeyboardInterrupt:
            print("\n\n⛔ Monitoreo detenido.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            time.sleep(intervalo)

def menu():
    limpiar_pantalla()
    print("=" * 50)
    print("   📱 SMS RECEIVER — Números Virtuales Gratuitos")
    print("=" * 50)
    print("\n¿Qué deseas hacer?\n")
    print("  [1] Ver mensajes de un número predefinido")
    print("  [2] Ingresar un número personalizado")
    print("  [3] Modo monitoreo continuo")
    print("  [4] Salir")
    print()

    opcion = input("👉 Elige una opción: ").strip()

    if opcion == "1":
        print("\nNúmeros disponibles:")
        for i, num in enumerate(NUMEROS_DISPONIBLES, 1):
            print(f"  [{i}] +{num}")
        idx = input("\nElige número (1-3): ").strip()
        try:
            numero = NUMEROS_DISPONIBLES[int(idx) - 1]
            mostrar_mensajes(numero)
        except (IndexError, ValueError):
            print("❌ Opción inválida.")

    elif opcion == "2":
        numero = input("\nIngresa el número (solo dígitos, sin +): ").strip()
        mostrar_mensajes(numero)

    elif opcion == "3":
        numero = input("\nNúmero a monitorear (sin +): ").strip()
        intervalo = input("Intervalo en segundos (default 30): ").strip()
        intervalo = int(intervalo) if intervalo.isdigit() else 30
        monitoreo_continuo(numero, intervalo)

    elif opcion == "4":
        print("\n👋 ¡Hasta luego!\n")
        return

    else:
        print("❌ Opción no válida.")

    input("\nPresiona Enter para continuar...")
    menu()

if __name__ == "__main__":
    menu()
