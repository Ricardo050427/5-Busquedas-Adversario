"""
Juego de othello

El estado se va a representar como una lista de 64 elementos, tal que

0  1   2   3   4   5   6   7
8  9  10  11  12  13  14  15
16 17 18  19  20  21  22  23
24 25 26  27  28  29  30  31
32 33 34  35  36  37  38  39
40 41 42  43  44  45  46  47
48 49 50  51  52  53  54  55
56 57 58  59  60  61  62  63

y cada elemento puede ser 0, 1 o -1, donde 0 es vacío, 1 es una ficha del
jugador 1 y -1 es una ficha del jugador 2.

Las acciones son poner una ficha en una casilla, que se representa como 1
o -1.

El estado terminal es cuando ningun jugadpr puede mover y gana quien en ese
momento tenga mas fichas en su tablero.
todo suma positiva o negativa para determinar quien gana?

La ganancia es 1 por cada ficha del jugador 1, -1 por cada ficha del jugador 2 y 0 si es un
empate.

"""

import juegos_simplificado as js
import minimax


class Othello(js.JuegoZT2):
    def inicializa(self):
        """
        fixme no inicializa en puros ceros
        """
        return tuple([0 for _ in range(8 * 8)])

    def jugadas_legales(self, s, j):
        return (pos for pos in range(8 * 8) if s[pos] == 0)

    def sucesor(self, s, a, j):
        s = list(s[:])
        for i in range(5, -1, -1):
            if s[a + 7 * i] == 0:
                s[a + 7 * i] = j
                break
        return tuple(s)

    def ganancia(self, s):
        # Verticales
        for i in range(7):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * (j + 1)] == s[i + 7 * (j + 2)] == s[i + 7 * (j + 3)] != 0):
                    return s[i + 7 * j]
        # Horizontales
        for i in range(6):
            for j in range(4):
                if (s[7 * i + j] == s[7 * i + j + 1] == s[7 * i + j + 2] == s[7 * i + j + 3] != 0):
                    return s[7 * i + j]
        # Diagonales
        for i in range(4):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * j + 8] == s[i + 7 * j + 16] == s[i + 7 * j + 24] != 0):
                    return s[i + 7 * j]
                if (s[i + 7 * j + 3] == s[i + 7 * j + 9] == s[i + 7 * j + 15] == s[i + 7 * j + 21] != 0):
                    return s[i + 7 * j + 3]
        return 0

    def terminal(self, s):
        if 0 not in s:
            return True
        return self.ganancia(s) != 0


class InterfaceOthello(js.JuegoInterface):
    def muestra_estado(self, s):
        """
        Muestra el estado del juego, se puede usar la función pprint_Othello
        para mostrar el estado de forma más amigable

        """
        simbolos = {1: 'X', -1: 'O', 0: ' '}
        print('\n  0   1   2   3   4   5   6 ')
        print('╔═══╦═══╦═══╦═══╦═══╦═══╦═══╗')
        for i in range(6):
            fila = [simbolos[x] for x in s[7 * i: 7 * (i + 1)]]
            print('║ ' + ' ║ '.join(fila) + ' ║')
            if i < 5:
                print('╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣')
        print('╚═══╩═══╩═══╩═══╩═══╩═══╩═══╝\n')

    def muestra_ganador(self, g):
        """
        Muestra el ganador del juego, se puede usar " XO"[g] para mostrar el
        ganador de forma más amigable

        """
        if g != 0:
            print("Gana el jugador " + " XO"[g])
        else:
            print("Un asqueroso empate")

    def jugador_humano(self, s, j):
        print("Jugador", " XO"[j])
        jugadas = list(self.juego.jugadas_legales(s, j))
        print("Jugadas legales:", jugadas)
        jugada = None
        while jugada not in jugadas:
            jugada = int(input("Jugada: "))
        return jugada


def ordena_centro(jugadas, jugador):
    """
    Ordena las jugadas de acuerdo a la distancia al centro
    """
    return sorted(jugadas, key=lambda x: abs(x - 3))


def evalua_ventana(ventana):
    """
    Recibe una lista de 4 casillas y
    devuelve un valor decimal basado en qué tan prometedora es.
    """
    score = 0
    fichas_p1 = ventana.count(1)  # Fichas del jugador 1
    fichas_p2 = ventana.count(-1)  # Fichas del jugador 2
    vacias = ventana.count(0)  # Casillas vacías

    # Evaluación para el jugador 1
    if fichas_p1 == 3 and vacias == 1:
        score += 0.1
    elif fichas_p1 == 2 and vacias == 2:
        score += 0.02

    # Penalización si el jugador 2 tiene amenaza
    if fichas_p2 == 3 and vacias == 1:
        score -= 0.1
    elif fichas_p2 == 2 and vacias == 2:
        score -= 0.02

    return score


def evalua_3con(s):
    """
    Evalua el estado s para el jugador 1.
    Extrae todas las combinaciones posibles de 4 casillas y las evalúa.
    """
    score = 0

    # Preferencia por la columna central (índices: 3, 10, 17, 24, 31, 38)
    columna_central = [s[3 + 7 * i] for i in range(6)]
    score += columna_central.count(1) * 0.05
    score -= columna_central.count(-1) * 0.05

    # Extraemos ventanas Horizontales (6 filas, 4 ventanas por fila)
    for i in range(6):
        for j in range(4):
            ventana = [s[7 * i + j + k] for k in range(4)]
            score += evalua_ventana(ventana)

    # Extraemos ventanas Verticales (7 columnas, 3 ventanas por col)
    for i in range(7):
        for j in range(3):
            ventana = [s[i + 7 * (j + k)] for k in range(4)]
            score += evalua_ventana(ventana)

    # Extraemos ventanas Diagonales hacia abajo (\)
    for i in range(4):
        for j in range(3):
            ventana = [s[i + 7 * j + 8 * k] for k in range(4)]
            score += evalua_ventana(ventana)

    # Extraemos ventanas Diagonales hacia arriba (/)
    for i in range(4):
        for j in range(3):
            ventana = [s[i + 7 * j + 3 + 6 * k] for k in range(4)]
            score += evalua_ventana(ventana)

    # Seguro contra desbordamiento (Mantenemos el score entre -0.99 y 0.99)
    # Dejamos el 1.0 y -1.0 exactos para cuando la función ganancia() detecte victoria real
    if score >= 1.0: return 0.99
    if score <= -1.0: return -0.99

    return score


if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Humano",  # Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Negamax",  # Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 5,
        "tiempo": 10,
        "ordena": ordena_centro,  # Puede ser None o una función f(jugadas, j) -> lista de jugadas ordenada
        "evalua": evalua_3con  # Puede ser None o una función f(estado) -> número entre -1 y 1
    }


    def jugador_cfg(cadena):
        if cadena == "Humano":
            return "Humano"
        elif cadena == "Aleatorio":
            return js.JugadorAleatorio()
        elif cadena == "Negamax":
            return minimax.JugadorNegamax(
                ordena=cfg["ordena"], d=cfg["profundidad máxima"], evalua=cfg["evalua"]
            )
        elif cadena == "Tiempo":
            return minimax.JugadorNegamaxIterativo(
                tiempo=cfg["tiempo"], ordena=cfg["ordena"], evalua=cfg["evalua"]
            )
        else:
            raise ValueError("Jugador no reconocido")


    interfaz = InterfaceOthello(
        Othello(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("El Juego del Conecta 4 ")
    print("Jugador 1:", cfg["Jugador 1"])
    print("Jugador 2:", cfg["Jugador 2"])
    print()

    interfaz.juega()
