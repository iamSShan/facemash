import math

class Elo:

    def calculate_probability(self, rating1, rating2):
        """
        Find winning probability
        P1: Probability of winning of player with rating2
        P1 = (1.0 / (1.0 + pow(10, ((rating1 - rating2) / 400))));
        """
        output = 1.0 / (1 + 1.0 * math.pow(10, ((rating1 - rating2) / 400)))
        return output

    def give_rating(self, rating1, rating2, winner):
        prob_1 = self.calculate_probability(rating1, rating2)
        prob_2 = self.calculate_probability(rating2, rating1)
        # K is taken as any constant value
        K = 28

        # Setting up the actual score
        # S(1) = 1 if player 1 wins / 0.5 if draw / 0 if player 2 wins
        # S(2) = 0 if player 1 wins / 0.5 if draw / 1 if player 2 wins

        #The rating of player is updated using the formula given below :-
        # rating1 = rating1 + K*(Actual Score - Expected score)
        if winner == 1:
            rating1 = rating1 + K * (1 - prob_1)
            rating2 = rating2 + K * (0 - prob_2)
        else:
            rating1 = rating1 + K * (0 - prob_1)
            rating2 = rating2 + K * (1 - prob_2)

        rating1 = round(rating1, 2)
        rating2 = round(rating2, 2)

        return rating1, rating2
