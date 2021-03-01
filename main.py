from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

stat_own_touchdown_yards = np.array([10, 30, 55, 70, 99])
stat_own_touchdown_chances = np.array([0.01, 0.1, 0.25, 0.4, 0.99])
# df = pd.read_excel('own_touchdown_stat.xlsx', header=None)
# stat_own_touchdown_yards = df[df.columns[0]].values
# stat_own_touchdown_chances = df[df.columns[1]].values

stat_own_touchdown_yards = np.insert(stat_own_touchdown_yards, 0, 0)
stat_own_touchdown_chances = np.insert(stat_own_touchdown_chances, 0, 0)
stat_own_touchdown_yards = np.append(stat_own_touchdown_yards, 100)
stat_own_touchdown_chances = np.append(stat_own_touchdown_chances, 1)


stat_opponent_touchdown_yards = np.array([10, 30, 55, 70, 99])
stat_opponent_touchdown_chances = np.array([0.9, 0.6, 0.3, 0.2, 0.01])
# df = pd.read_excel('opponent_touchdown_stat.xlsx', header=None)
# stat_opponent_touchdown_yards = df[df.columns[0]].values
# stat_opponent_touchdown_chances = df[df.columns[1]].values

stat_opponent_touchdown_yards = np.insert(stat_opponent_touchdown_yards, 0, 0)
stat_opponent_touchdown_chances = np.insert(stat_opponent_touchdown_chances, 0, 1)
stat_opponent_touchdown_yards = np.append(stat_opponent_touchdown_yards, 100)
stat_opponent_touchdown_chances = np.append(stat_opponent_touchdown_chances, 0)


stat_attempt_yards = np.array([1, 3, 6, 10, 15])
stat_attempt_chances = np.array([0.9, 0.7, 0.5, 0.4, 0.2])
# df = pd.read_excel('attempt_stat.xlsx', header=None)
# stat_attempt_yards = df[df.columns[0]].values
# stat_attempt_chances = df[df.columns[1]].values
stat_attempt_chances = stat_attempt_chances[stat_attempt_yards < 20]
stat_attempt_yards = stat_attempt_yards[stat_attempt_yards < 20]

stat_attempt_yards = np.insert(stat_attempt_yards, 0, 0)
stat_attempt_chances = np.insert(stat_attempt_chances, 0, 1)
stat_attempt_yards = np.append(stat_attempt_yards, 20)
stat_attempt_chances = np.append(stat_attempt_chances, 0.01)


first_attempt_distribution = interp1d(stat_attempt_yards, stat_attempt_chances, kind='cubic')
own_touchdown_distribution = interp1d(stat_own_touchdown_yards, stat_own_touchdown_chances, kind='cubic')
opponent_touchdown_distribution = interp1d(stat_opponent_touchdown_yards, stat_opponent_touchdown_chances, kind='cubic')

field_yards = np.linspace(0, 100, num=101, endpoint=True)
attempt_yards = np.linspace(0, 20, num=21, endpoint=True)



# the probability distribution of taking the first attempt by the number of yards before the first attempt
first_attempt_chances = first_attempt_distribution(attempt_yards)

# probability distribution of touchdown from situation 1-10 along the field length
own_touchdown_chances = own_touchdown_distribution(field_yards)

# the probability distribution of missing a touchdown from situation 1-10 along the field length
opponent_touchdown_chances = opponent_touchdown_distribution(field_yards)

k = 30

i = 50
j = 5

play_4_damage = opponent_touchdown_chances[i] * (1 - first_attempt_chances[j]) + opponent_touchdown_chances[30 + k] * first_attempt_chances[j] - own_touchdown_chances[i] * first_attempt_chances[j]

pant_i = i + k
if pant_i > 99:
    pant_i = 99

pant_damage = opponent_touchdown_chances[pant_i]

print("From statistics:")
print("Chance to touchdown: {} \nChance to realize the attempt: {} \nChance to got touchdown if the attempt is unsuccessful: {} \nChance that we will be brought in the reciprocal possession, if the attempt is successful: {} \nChance to got touchdown after the pant: {}".format(
    own_touchdown_chances[i], first_attempt_chances[j], opponent_touchdown_chances[i], opponent_touchdown_chances[30 + k], opponent_touchdown_chances[pant_i]))

print()
print("Prior odds (before making a decision):")
print("Chance to make touchdown: {} \nChance to got touchdown if attempt fails: {} \nChance to got touchdown if attempt is successful: {}".format(
    (own_touchdown_chances[i] * first_attempt_chances[j]), (opponent_touchdown_chances[i] * (1 - first_attempt_chances[j])), (opponent_touchdown_chances[30 + k] * first_attempt_chances[j])))

print()
print("-----------------------------")
print()
print("Position on the field: {}, \nBefore the first down: {} \nPositions after the pant: {}".format(i, j, pant_i))
print()
print("-----------------------------")
print()
print("Balance (amount) of possible damage for two possessions:")
print("Damage when playing the 4th attempt: {0: 0.2f} points \nDamage when play the pant: {1: 0.2f} points".format(play_4_damage*6, pant_damage*6))

print()
if play_4_damage <= pant_damage:
    print("I recommend playing the 4th try, it is {0: 0.2f} more profitable for two possessions".format(pant_damage*6 - play_4_damage*6))
else:
    print("I recommend playing the pant, it is more profitable by {0: 0.2f} points for two possessions".format(play_4_damage*6 - pant_damage*6))