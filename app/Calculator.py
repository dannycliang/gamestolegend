from random import *
stars_by_rank = {4: 2, 3: 3, 2: 4, 1: 5, 0: 5}
floors = [20, 15, 10, 5]

class Player:
    current_rank = 25
    current_stars = 0
    winstreak_counter = 0


    def __init__(self, current_rank, current_stars = 0, winstreak_counter = 0):
        self.current_rank = current_rank
        self.current_stars = current_stars
        self.winstreak_counter = winstreak_counter

    def climb_simulation(self, goal_rank, winrate):
        simulate_player = Player(self.current_rank, self.current_stars, self.winstreak_counter)
        games = 0
        while simulate_player.current_rank != goal_rank:
            result = randint(1, 100)
            print(str(simulate_player.current_rank) + " " + str(simulate_player.current_stars))
            if winrate > result:
                simulate_player.win()
            else:
                simulate_player.lose()
            games += 1
        return games


    def win(self):
        rank = self.current_rank
        if self.winstreak_counter >= 2 and rank > 5:
            bonus = 1
        else:
            bonus = 0
        stars = self.current_stars + 1 + bonus
        necessary_stars = stars_by_rank[(self.current_rank - 1) // 5]
        if (stars > necessary_stars):
            self.promote(stars - necessary_stars)
        else:
            self.current_stars = stars
            self.winstreak_counter += 1

    def lose(self):
        rank = self.current_rank
        self.winstreak_counter = 0
        stars = self.current_stars - 1
        if stars < 0:
            self.demote()
        elif self.current_rank < 21:
            self.current_stars = stars

    def promote(self, stars):
        self.current_rank -= 1
        self.current_stars = stars

    def demote(self):
        if self.current_rank < 25 and self.current_rank not in floors:
            self.current_rank += 1
            self.current_stars = stars_by_rank[(self.current_rank - 1) // 5] - 1
