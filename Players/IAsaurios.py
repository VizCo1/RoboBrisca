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
        self.heuristic = Heuristic()  # Mon was here!!//

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
        played_cards = observation.playing_cards.len()
        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        if played_cards == 0 or played_cards == 2:
            factor = -1
        else:
            factor = 1
        # AAAAAAAAAAAAAAAAAAAAAAAAAAAA

        # Antes de entrar al bucle, mirar en qué posición estoy
        playing_cards = observation.playing_cards
        trump = observation.trump_card
        first_card = observation.playing_cards.get_card(0)

        # Somos los ultimos -> jugar como humanos
        if (played_cards == 3):
            best_played_card_id = 0
            for x in range(1, 3):
                if (is_better_card(playing_cards.get_card(x), playing_cards.get_card(best_played_card_id), trump,
                                   first_card)):
                    best_played_card_id = x

            best_card_index = -1
            # Compañero va ganando
            if (best_played_card_id == 1):

                #mirar la más alta que no es triunfo
                for action_index in range(0, 3):
                    action_card = list_actions[action_index].getCard()

                    #mirar si no es triunfo
                    if action_card.getType() != trump.getType():
                        #es la primera carta NO triunfo
                        if best_card_index == -1:
                            best_card_index = action_index
                        #toca comparar cartas
                        else:
                            if action_card.getValue() > list_actions[best_card_index].getCard().getValue():
                                best_card_index = action_index

                #si todas son triunfos, coger la más baja
                if best_card_index == -1:
                    best_card_index = 0
                    for action_index in range(1, 3):

                        if list_actions[action_index].getCard().getValue() < list_actions[best_card_index].getCard().getValue():
                            best_card_index = action_index

            #somos los últimos pero equipo va perdiendo
            else:
                # Sacar la más baja?

            return list_actions[best_card_index]

        #no somos los ultimos -> IA
        else:
            # poner un while para evitar el fallo de tiempo
            while (time.time() - initial_time < time_difference):
                j = 0
                new_obs_rand = observation.get_randomized_clone()
                for action in list_actions:
                    new_obs = new_obs_rand.clone()
                    # Yo juego mi carta
                    value = self.forward_model.play(new_obs, action, self.heuristic)
                    played_cards = played_cards + 1
                    other = player_id + 1

                    # while iteraciones
                    # Recoger cartas, barajar y volver a repartir
                    while played_cards < 4:
                        if other == 4:
                            other = 0
                        # Seleccionar una carta al azar
                        ith = random.choice(range(new_obs.hands[other].len()))
                        c = new_obs.hands[other].get_card(ith)
                        # Otro jugador juega una carta
                        value = self.forward_model.play(new_obs, Action(c), self.heuristic)
                        played_cards += 1
                        other += 1

                    # Guarda el valor de nuestras cartas

                    values[j] += value * factor

                    j += 1

            # buscar el maximo en values una vez que hemos salido de los bucles
            # print(values)
            max = -math.inf
            index = -1
            for i in range(len(list_actions)):
                if values[i] > max:
                    max = values[i]
                    index = i
            # print(len(list_actions))
            # print(index)
            return list_actions[index]

# Soy 1,

# Soy 4, si gana mi compañero --> poner muchos puntos cuando merezca la pena, pero no triunfo

# class IAsuariosHeuristic:
#     def check_not_better_card(self, player_card, observation, others_card):
#         if is_better_card(player_card, observation.playing_cards.get_card(others_card),
#                           observation.trump_card, observation.playing_cards.get_card(0)):
#             return False
#         return True
#
#     # Returns the points that the player_id is going to win in the actual round.
#     # If the player is going to lose, then returns -points.
#     # player_id = gs.turn
#     def get_score(self, observation, player_id):
#
#         if observation.playing_cards.len() == 1:
#             return observation.playing_cards.get_card(0).get_value()
#
#         cards = observation.playing_cards.get_cards()
#         points = 0
#         #Palo de la primera carta
#         #Puntos de mi equipo
#         #Puntos del otro equipo
#         for card in cards:
#             points += card.get_value()
#
#         player_card = observation.playing_cards.get_last_card()
#
#         # Obtener el card.get_value() de tu equipo y el del otro equipo no se
#         # Tener en cuenta el palo de las cartas ?¿
#
#         # is_better = True
#
#         # Hay 1 carta, soy el segundo jugador
#         if observation.playing_cards.len() == 1:
#             if self.check_not_better_card(player_card, observation, 0):
#                 return -points
#
#         # Hay 2 cartas, soy el tercer jugador
#         elif observation.playing_cards.len() == 2:
#             if self.check_not_better_card(player_card, observation, 1):
#                 if self.check_not_better_card(observation.playing_cards.get_card(0), observation, 1):
#                     return -points
#
#         # Hay 3 cartas, soy el cuarto jugador
#         elif observation.playing_cards.len() == 3:
#             if self.check_not_better_card(player_card, observation, 2):
#                 if self.check_not_better_card(player_card, observation, 0):
#                     if self.check_not_better_card(observation.playing_cards.get_card(1), observation, 2):
#                         if self.check_not_better_card(observation.playing_cards.get_card(1), observation, 0):
#                             return -points
#
#         return points
#
#         # if is_better:
#         #    return points
#         # else:
#         #    return -points

class MyHeuristic:
    def get_score(self, observation, player_id):
        if observation.playing_cards.len() == 0:
            return 0

        # points of played cards
        cards = observation.playing_cards.get_cards()
        points = 0
        for card in cards:
            points += card.get_value()

        player_card = observation.playing_cards.get_last_card()
        first_card = observation.playing_cards.get_card(0)
        if observation.playing_cards.len() == 1:
            score = points
        elif observation.playing_cards.len() == 2:
            other_player_card = observation.playing_cards.get_card(0)
            if is_better_card(other_player_card, player_card, observation.trump_card, first_card):
                score = -points
            else:
                score = points
        elif observation.playing_cards.len() == 3:
            other_player_card = observation.playing_cards.get_card(1)
            my_mate_card = observation.playing_cards.get_card(0)
            if is_better_card(other_player_card, player_card, observation.trump_card, first_card) and \
                    is_better_card(other_player_card, my_mate_card, observation.trump_card, first_card):
                score = -points
            else:
                score = points
        else:
            other_player_card1 = observation.playing_cards.get_card(0)
            other_player_card2 = observation.playing_cards.get_card(2)
            my_mate_card = observation.playing_cards.get_card(1)
            if (is_better_card(other_player_card1, player_card, observation.trump_card, first_card) and
                    is_better_card(other_player_card1, my_mate_card, observation.trump_card, first_card)) or \
                (is_better_card(other_player_card2, player_card, observation.trump_card, first_card) and
                    is_better_card(other_player_card2, my_mate_card, observation.trump_card, first_card)):
                score = -points
            else:
                score = points

        return score
