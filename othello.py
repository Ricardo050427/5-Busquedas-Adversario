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

Las acciones son poner una ficha en una casilla que flanquee al menos una
ficha del rival que estara en una casilla del 0 al 63.

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
        s = [0] * 64
        s[27] = -1
        s[36] = -1
        s[28] = 1
        s[35] = 1
        return tuple(s)

    def jugadas_legales(self, s, j):
        jugadas = []
        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),  # Arriba-Izquierda, Arriba, Arriba-Derecha
            (0, -1), (0, 1),  # Izquierda, Derecha
            (1, -1), (1, 0), (1, 1)  # Abajo-Izquierda, Abajo, Abajo-Derecha
        ]

        for pos in range(64):
            if s[pos] == 0:
                fila_orig = pos // 8
                col_orig = pos % 8
                es_legal = False

                for df, dc in direcciones:
                    f = fila_orig + df
                    c = col_orig + dc
                    fichas_enemigas_vistas = 0
                    while 0 <= f < 8 and 0 <= c < 8 and s[f * 8 + c] == -j:
                        fichas_enemigas_vistas += 1
                        f += df
                        c += dc
                    if fichas_enemigas_vistas > 0 and 0 <= f < 8 and 0 <= c < 8 and s[f * 8 + c] == j:
                        es_legal = True
                        break

                if es_legal:
                    jugadas.append(pos)

        return jugadas if jugadas else [None]

    def sucesor(self, s, a, j):
        """
            Genera y devuelve el nuevo estado del tablero después de que el jugador 'j'
            realiza la acción 'a'.

            Esta función es pura (no modifica el tablero original). Crea un clon del
            estado actual, coloca la nueva ficha en el índice 'a' y lanza rayos en las
            8 direcciones para encontrar y voltear (cambiar de color) todas las fichas
            enemigas que hayan quedado atrapadas (flanqueadas) bajo las reglas del Othello.
        """
        if a is None:
            return s

        s_nuevo = list(s[:])
        s_nuevo[a] = j
        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        fila_orig = a // 8
        col_orig = a % 8

        for df, dc in direcciones:
            f = fila_orig + df
            c = col_orig + dc
            piezas_a_voltear = []

            while 0 <= f < 8 and 0 <= c < 8 and s[f * 8 + c] == -j:
                piezas_a_voltear.append(f * 8 + c)
                f += df
                c += dc

            if len(piezas_a_voltear) > 0 and 0 <= f < 8 and 0 <= c < 8 and s[f * 8 + c] == j:
                for pos_enemiga in piezas_a_voltear:
                    s_nuevo[pos_enemiga] = j

        return tuple(s_nuevo)

    def ganancia(self, s):
        """
        fixme posible ganancia
        """
        suma_total = sum(s)
        if suma_total > 0: return 1
        if suma_total < 0: return -1
        return 0

    def terminal(self, s):
        if 0 not in s:
            return True

        juego_negras = self.jugadas_legales(s, 1)
        juego_blancas = self.jugadas_legales(s, -1)

        if juego_blancas == [None] and juego_negras == [None]:
            return True

        return False


class InterfaceOthello(js.JuegoInterface):
    def muestra_estado(self, s):
        """
        Muestra el estado del juego, se puede usar la función pprint_Othello
        para mostrar el estado de forma más amigable

        """

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
