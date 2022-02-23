import math
from random import random

from Game.Action import Action
from Game.ForwardModel import ForwardModel
from Game.Heuristic import Heuristic
from Players.Player import Player

class OTLAPlayer(Player):
    def __init__(self):
        self.fm = ForwardModel()
        self.ht = Heuristic()

    def __str__(self):
        return "IAsauriosPlayer"

    def think(self, obs, budget):
        l = obs.get_list_actions()
        values = [0, 0, 0]

        player_id = obs.turn
        n = obs.playing_cards.len()
        if n == 0 or n == 2:
            factor = -1
        else:
            factor = 1

        # while iteraciones
        # Recoger cartas, barajar y volver a repatir
        j = 0

        #while tiempo < 850ms
        for action in l:
            new_obs = obs.clone()
            value = self.fm.play(new_obs, action, self.ht)
            n = n + 1
            other = player_id + 1
            while n < 4:
                if other == 4:
                    other = 0
                # Seleccionar una carta al azar
                ith = random.choice(range(3))
                c = new_obs.hands[other].get_card(ith)
                a = Action(c)
                # Jugarla
                value = self.fm.play(new_obs, a, self.ht)
                n += 1
                other += 1

            values[j] += value * factor
            j += 1

        # buscar el maximo en values una vez que hemos salido de los bucles
        max = -math.inf
        index = -1
        for i in range(len(values)):
            if values[i] > max:
                max = values[i]
                index = i

        return l[index]