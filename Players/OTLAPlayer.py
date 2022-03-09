import math
import time
import random

from Game.Common import is_better_card
from Game.Action import Action
from Game.ForwardModel import ForwardModel
from Game.Heuristic import Heuristic
from Players.Player import Player


class IAsauriosPlayer(Player):
    def __init__(self):
        self.forward_model = ForwardModel()
        self.heuristic = Heuristic()

    def __str__(self):
        return "IAsauriosPlayer"

    def think(self, observation, budget):
        initial_time = time.time()
        time_difference = budget * 0.9  # para tener tiempo de margen

        # Lista de acciones del turno
        list_actions = observation.get_list_actions()
        if len(list_actions) == 1:
            return list_actions[0]

        values = [0, 0, 0]

        player_id = observation.turn
        n = observation.playing_cards.len()
        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        if n == 0 or n == 2:
            factor = -1
        else:
            factor = 1
        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

        # while iteraciones
        # Recoger cartas, barajar y volver a repartir

        j = 0
        # poner un while para evitar el fallo de tiempo
        while (time.time() - initial_time < time_difference):
            j = 0
            new_obs_rand = observation.get_randomized_clone()
            for action in list_actions:
                new_obs = new_obs_rand.clone()
                # Yo juego mi carta
                value = self.forward_model.play(new_obs, action, self.heuristic)
                n = n + 1
                other = player_id + 1
                while n < 4:
                    if other == 4:
                        other = 0
                    # Seleccionar una carta al azar
                    ith = random.choice(range(new_obs.hands[other].len()))
                    c = new_obs.hands[other].get_card(ith)
                    a = Action(c)
                    # Otro jugador juega una carta
                    value = self.forward_model.play(new_obs, a, self.heuristic)
                    n += 1
                    other += 1

                # Guarda el valor de nuestras cartas
                # print(j)
                values[j] += value * factor

                j += 1

        # buscar el maximo en values una vez que hemos salido de los bucles
        max = -math.inf
        index = -1
        for i in range(len(list_actions)):
            if values[i] > max:
                max = values[i]
                index = i
        print(len(list_actions))
        return list_actions[index]

class IAsuariosHeuristic:
    # Returns the points that the player_id is going to win in the actual round.
    # If the player is going to lose, then returns -points.
    # player_id = gs.turn
    def check_not_better_card(self, player_card, observation, previous_card):
        if not is_better_card(player_card, observation.playing_cards.get_card(previous_card),
                              observation.trump_card, observation.playing_cards.get_card(0)):
            return True
        return False

    def get_score(self, observation, player_id):

        if observation.playing_cards.len() == 1:
            return observation.playing_cards.get_card(0).get_value()

        cards = observation.playing_cards.get_cards()
        points = 0
        for card in cards:
            points += card.get_value()

        player_card = observation.playing_cards.get_last_card()

        # Player_id es el id del jugador que llama a la funcion
        # Si player_id == 0 --> pana_id == 2
        # Si player_id == 1 --> pana_id == 3
        # Si eres 0 no se pone nada esta arriba ya hecho
        # Si eres 2 --> si mi carta es peor que la del player_id_1 --> miro si carta de player_id_0 es mejor o peor que la de player_id_1

        is_better = True

        # Hay 1 carta, soy el segundo jugador
        if observation.playing_cards.len() == 1:
            is_better = not self.check_not_better_card(player_card, observation, 0)

        # Hay 2 cartas, soy el tercer jugador
        elif observation.playing_cards.len() == 2:
            if self.check_not_better_card(player_card, observation, 1):
                is_better = not self.check_not_better_card(0, observation, 1)

        # Hay 3 cartas, soy el cuarto jugador
        # Comparar mi carta con el tercer jugador
        elif observation.playing_cards.len() == 3:
            is_better = not self.check_not_better_card(player_card, observation)

        for i in range(observation.playing_cards.len() - 1):
            if not is_better_card(player_card, observation.playing_cards.get_card(i),
                                  observation.trump_card, observation.playing_cards.get_card(0)):
                is_better = False
                break

        if is_better:
            return points
        else:
            return -points