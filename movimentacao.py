import serial
import time


# CONFIGURAÇÕES
PORTA_GRBL = 'COM3'
PORTA_NANO = 'COM4'

cnc = None
garra = None

FATOR_CORRECAO = 1/6


# POSIÇÕES
POSICOES = {
    "Nicho 1": (175, 50, 95),
    "Nicho 2": (174, 133, 95),
    "Nicho 3": (3, 43, 95),
    "Nicho 4": (3, 123, 95),
    "Nicho 5": (3, 206, 95)
}

RETIRADA = (190, 270, 95)

Z_SEGURO = 0


# CONEXÃO
def conectar():
    global cnc, garra

    try:
        cnc = serial.Serial(PORTA_GRBL, 115200, timeout=0.1)
        time.sleep(2)

        # RESET GRBL
        cnc.write(b"\x18")
        time.sleep(1)
        cnc.write(b"$X\n")
        cnc.write(b"G90\n")
        cnc.write(b"G21\n")

        garra = serial.Serial(PORTA_NANO, 9600, timeout=1)

        time.sleep(2)
        print("Conectado GRBL + Garra")

    except Exception as e:
        print(f"Erro: {e}")


# ESPERAR IDLE
def esperar_idle(timeout=15):
    start = time.time()

    while True:
        cnc.write(b"?\n")
        time.sleep(0.05)
        resp = cnc.read_all().decode(errors="ignore")

        if "<Idle" in resp:
            return

        if time.time() - start > timeout:
            print("Timeout esperando Idle")
            return


# MOVIMENTO
def mover(x=None, y=None, z=None, feed=3000):
    cmd = "G90 G0"

    if x is not None:
        cmd += f" X{x * FATOR_CORRECAO:.2f}"

    if y is not None:
        cmd += f" Y{y * FATOR_CORRECAO:.2f}"

    if z is not None:
        cmd += f" Z{z * FATOR_CORRECAO:.2f}"

    cmd += f" F{feed}\n"

    print(cmd.strip())
    cnc.write(cmd.encode())
    esperar_idle()


# GARRA
def esperar_resposta(timeout=2):
    start = time.time()

    while True:
        if garra.in_waiting:
            resp = garra.readline().decode().strip()
            print("Garra:", resp)

            if resp == "OK":
                return

        if time.time() - start > timeout:
            print("Timeout garra")
            return


# ABRIR GARRA
def abrir_garra():
    esperar_idle()
    garra.write(b"OPEN\n")
    esperar_resposta()


# FECHAR GARRA
def fechar_garra():
    esperar_idle()
    garra.write(b"CLOSE\n")
    esperar_resposta()


# CICLO UNITÁRIO
def executar_ciclo(nicho):

    if nicho not in POSICOES:
        print("Nicho inválido")
        return

    x, y, z = POSICOES[nicho]
    xr, yr, zr = RETIRADA
    print(f"\nIniciando ciclo → {nicho}")

   
    # 1. ABRE GARRA
    abrir_garra()

    # 2. Z SOBE PARA POSIÇÃO SEGURA
    mover(z=Z_SEGURO)

    # 3. XY VÃO JUNTOS PARA O NICHO
    mover(x=x, y=y)

    # 4. Z DESCE
    mover(z=z)

    # 5. FECHA GARRA
    fechar_garra()

    # ESPERA GARRA FECHAR
    time.sleep(0.8)

    # 6. Z SOBE
    mover(z=Z_SEGURO)

    # 7. Y VAI PARA ENTREGA
    mover(y=yr)

    # 8. X VAI PARA ENTREGA
    mover(x=xr)

    # 9. Z DESCE
    mover(z=zr)

    # 10. ABRE GARRA
    abrir_garra()

    # ESPERA GARRA ABRIR
    time.sleep(0.8)

    # 11. Z SOBE
    mover(z=Z_SEGURO)

    # 12. VOLTA ORIGEM
    mover(x=0, y=0)

    print("Ciclo finalizado\n")


# EXECUTAR SEPARAÇÃO
def executar_separacao(nicho, quantidade):
    nome_nicho = f"Nicho {nicho}"

    for i in range(quantidade):
        print(f"Item {i+1}/{quantidade}")
        executar_ciclo(nome_nicho)


# MAIN
if __name__ == "__main__":
    conectar()

    # TESTE
    executar_separacao(1, 1)