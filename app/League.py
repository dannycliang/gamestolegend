from random import *

Ranks = {'V': 5, 'IV': 4, 'III': 3, 'II': 2, 'I': 1, '5': 5, '4': 4, '3': 3, '2': 2, '1': 1, 'v': 5, 'iv': 4, 'iii': 3, 'ii': 2, 'i': 1}
reverse_Ranks = {5: 'V', 4: 'IV', 3: 'III', 2: 'II', 1: 'I'}
tiers = {'bronze': 'Silver V', 'silver': 'Gold V', 'gold': 'Platinum V', 'platinum': 'Diamond V', 'diamond': 'Master I'}
reverse_tiers = {'silver': "Bronze I", 'gold': 'Silver I', 'platinum': 'Gold I', 'diamond': 'Platinum I', 'master': 'Diamond I'}
homogenize_divison = {'5': 'V', '4': 'IV', '3': 'III', '2': 'II', '1':'I', 'V': 'V', 'IV': 'IV', 'III': 'III', 'II': 'II', 'I':'I', 'v': 'V', 'iv': 'IV', 'iii': 'III', 'ii': 'II', 'i':'I'}


class Player:
    Current_Rank = ""
    Current_Ranking = ""
    Current_Gain = 0
    Current_Loss = 0
    Current_LP = 0
    Current_Tier = 0
    In_Series = False
    Series_Wins = 0
    Series_Losses = 0
    Buffer = 3
    Balance = 0

    def __init__(self, Rank, Base_Gain = 20, Base_Loss = 20, Current_LP = 0, In_Series = False, Series_Wins = 0, Series_Losses = 0):
        self.Current_Rank = Rank
        self.Current_Gain = Base_Gain
        self.Current_Loss = Base_Loss
        self.Current_LP = Current_LP
        self.Current_Ranking = Rank.split(' ')[0]
        self.Current_Tier = tier_interpreter(Rank.split(' ')[1])
        self.In_Series = In_Series
        self.Series_Wins = Series_Wins
        self.Series_Losses = Series_Losses
        if self.Current_Tier == 5:
            self.Buffer = 20

    def Ranked_calculate(self, Goal_Rank, Winrate):
        Simulate_Player = Player(self.Current_Rank, self.Current_Gain, self.Current_Loss, self.Current_LP, self.In_Series, self.Series_Wins, self.Series_Losses)
        winning = Winrate
        games = 0
        goal_rank = Goal_Rank.split()[0][:1].upper() + Goal_Rank.split()[0][1:].lower() + " " + homogenize_divison[Goal_Rank.split()[1].upper()]
        while Simulate_Player.Current_Rank != goal_rank and games < 1000:
            result = randint(1, 80)
            if (winning > result):
                Simulate_Player.win()
            else:
                winning = Simulate_Player.lose(winning)
            games += 1
            print(str(Simulate_Player.Current_Rank) + " " + str(Simulate_Player.Current_LP))
        return games

    def win(self):
        new_LP = self.Current_LP + self.Current_Gain + randint(-2, 2)
        self.modify_gain(True)
        if self.In_Series:
            self.series_win()
        elif new_LP >= 100 and "aster" not in self.Current_Rank:
            self.In_Series = True
            self.Current_LP = new_LP
        else:
            self.Current_LP = new_LP


    def series_win(self):
        if self.Current_Tier == 1:
            new_wins = (self.Series_Wins + 1) % 3
            if new_wins == 0:
                self.Current_LP = 0
                self.Series_Wins = 0
                self.In_Series = False
                self.Buffer += 20
                self.add_Rank()
            else:
                self.Series_Wins = new_wins
                self.Current_LP += self.Current_Gain
        else:
            new_wins = (self.Series_Wins + 1) % 2
            if new_wins == 0:
                self.Current_LP = 0
                self.Series_Wins = 0
                self.In_Series = False
                self.Buffer += 3
                self.add_Rank()
            else:
                self.Series_Wins = new_wins
                self.Current_LP += self.Current_Gain

    def series_loss(self):
        if self.Current_Tier == 1:
            new_losses = (self.Series_Losses + 1) % 3
            self.Current_LP -= (self.Current_Loss + randint(-2, 2))
            if new_losses == 0:
                self.In_Series = False
            else:
                self.Series_Losses = new_losses
        else:
            new_losses = (self.Series_Losses + 1) % 2
            self.Current_LP -= (self.Current_Loss + randint(-2, 2))
            if new_losses == 0:
                self.In_Series = False
            else:
                self.Series_Losses = new_losses


    def add_Rank(self):
        if self.Current_Tier == 1:
            self.Current_Tier = 5
            self.Current_Rank = tiers[self.Current_Ranking.lower()]
            self.Current_Ranking = self.Current_Rank.split(' ')[0]
        else:
            self.Current_Tier -= 1
            self.Buffer = 3
            self.Current_Rank = self.Current_Rank.split(' ')[0] + ' ' + reverse_Ranks[self.Current_Tier]


    def lose_Rank(self):
        if self.Current_Tier == 5:
            if "ronze" in self.Current_Rank:
                return
            self.Current_Tier = 1
            self.Current_LP = 75
            self.Current_Rank = reverse_tiers[self.Current_Ranking.lower()]
            self.Current_Ranking = self.Current_Rank.split(' ')[0]
        else:
            self.Current_Tier += 1
            if self.Current_Tier == 5:
                self.Buffer = 20
            self.Current_LP = 75
            self.Current_Rank = self.Current_Rank.split(' ')[0] + ' ' + reverse_Ranks[self.Current_Tier]


    def lose(self, winrate):
        new_LP = self.Current_LP - (self.Current_Loss + randint(-2, 2))
        self.modify_gain(False)
        if self.In_Series:
            self.series_loss()
        elif new_LP < 0:
            if self.Current_LP == 0:
                if self.Buffer == 0:
                    self.lose_Rank()
                    return winrate
                else:
                    self.Buffer -= 1
            else:
                self.Current_LP = 0
        else:
            self.Current_LP = new_LP
        return winrate

    def modify_gain(self, Win):
        if Win:
            new_balance = self.Balance + 1
            if new_balance > (self.Current_LP - 20):
                self.Balance = 0
                if self.Current_Gain < 30:
                    self.Current_Gain += 1
                    self.Current_Loss -= 1
            else:
                self.Balance = new_balance
        else:
            new_balance = self.Balance - 1
            if new_balance < (self.Current_LP - 20):
                self.Balance = 0
                if self.Current_Gain > 12:
                    self.Current_Gain -= 1
                    self.Current_Loss += 1
            else:
                self.Balance = new_balance



def tier_interpreter(name):
    return Ranks[name]
