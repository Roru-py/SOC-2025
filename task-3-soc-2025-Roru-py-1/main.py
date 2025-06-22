# Write code which will run all the different bandit agents together and:
# 1. Plot a common cumulative regret curves graph
# 2. Plot a common graph of average reward curves

import numpy as np
from base import Agent, MultiArmedBandit
import matplotlib.pyplot as plt
from epsilon_greedy import EpsilonGreedyAgent
from ucb import UCBAgent
from klucb import KLUCBAgent
from thompson import ThompsonSamplingAgent

TIME_HORIZON = 30_000

#Bandit S1

bandit = MultiArmedBandit(np.array([0.23,0.55,0.76,0.44]))
agents = []
agents.append(EpsilonGreedyAgent(TIME_HORIZON,bandit,0.05))
agents.append(UCBAgent(TIME_HORIZON,bandit))
agents.append(KLUCBAgent(TIME_HORIZON,bandit,3))
agents.append(ThompsonSamplingAgent(TIME_HORIZON,bandit))

for j in range(len(agents)):
    for i in range(TIME_HORIZON):
        agents[j].give_pull()
    agents[j].plot_cumulative_regret()
    bandit.cumulative_regret_array = [0]
plt.show()    

#Bandit S2

p = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
plt.figure(3,figsize=(8,4))
colors = ['r','g','b','y']
labels = ["Epsilon_Greedy","UCB","KL-UCB","Thompson"]
for i in range(len(agents)):
    y = []
    for j in p:
        bandit = MultiArmedBandit(np.array([j,j+0.1]))

        agents[0]=EpsilonGreedyAgent(TIME_HORIZON,bandit,0.05)
        agents[1]=UCBAgent(TIME_HORIZON,bandit)
        agents[2]=KLUCBAgent(TIME_HORIZON,bandit,3)
        agents[3]=ThompsonSamplingAgent(TIME_HORIZON,bandit)

        bandit.cumulative_regret_array = [0]
        for k in range(TIME_HORIZON):
            agents[i].give_pull()
        y.append(bandit.cumulative_regret_array[-1])
    plt.plot(range(1,len(p)+1),y,color=colors[i],label=labels[i])
    plt.xticks(range(1,len(p)+1), rotation=45)
    plt.xlabel("Game Index")
    plt.ylabel("Regret")
    plt.title("Total Regret for each game")
plt.legend(loc='upper left', fontsize=12)
plt.grid(axis="both")
plt.tight_layout()
plt.show()