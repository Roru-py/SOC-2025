import numpy as np
from base import Agent, MultiArmedBandit
import matplotlib.pyplot as plt


class EpsilonGreedyAgent(Agent):
    epsilon : float
    reward_memory : np.ndarray # A per arm value of how much reward was gathered
    count_memory : np.ndarray # An array of the number of times an arm is pulled 

    def __init__(self, time_horizon, bandit:MultiArmedBandit, epsilon = 0.01):
        super().__init__(time_horizon, bandit)
        self.epsilon = epsilon
        self.bandit : MultiArmedBandit = bandit
        self.reward_memory = np.zeros(len(bandit.arms))
        self.count_memory = np.zeros(len(bandit.arms))
        self.time_step = 0

    def give_pull(self):
        if np.random.random() < self.epsilon: # Choose random action
           random_arm = np.random.choice(len(self.bandit.arms))
           reward =  self.bandit.pull(random_arm)
           self.reinforce(reward, random_arm)
        else: # Choose best known action!
           best_arm = np.argmax(self.reward_memory / self.count_memory)
           reward = self.bandit.pull(best_arm)
           self.reinforce(reward, best_arm)
           

    def reinforce(self, reward, arm):
        self.count_memory[arm] += 1
        self.reward_memory[arm] += reward
        self.time_step += 1
        self.rewards.append(reward)
        # print(self.count_memory, self.reward_memory)
 
    def plot_arm_graph(self):
        counts = self.count_memory
        indices = np.arange(len(counts))

        # Plot the data
        plt.figure(figsize=(12, 6))
        plt.bar(indices, counts, color='skyblue', edgecolor='black')

        # Formatting
        plt.title('Counts per Category', fontsize=16)
        plt.xlabel('Arm', fontsize=14)
        plt.ylabel('Pull Count', fontsize=14)
        plt.grid(axis='y', linestyle='-')  # Add grid lines for the y-axis
        plt.xticks(indices, [f'Category {i+1}' for i in indices], rotation=45, ha='right')
        # plt.yticks(np.arange(0, max(counts) + 2, step=2))

        # Annotate the bars with the count values
        for i, count in enumerate(counts):
            plt.text(i, count + 0.5, str(count), ha='center', va='bottom', fontsize=12, color='black')

        # Tight layout to ensure there's no clipping of labels
        plt.tight_layout()

        # Show plot
        plt.show()

    def plot_cumulative_regret(self):
        timesteps = np.arange(1, len(self.bandit.cumulative_regret_array) + 1)

        # Plot the data
        plt.figure(1,figsize=(8,4))
        plt.plot(timesteps, self.bandit.cumulative_regret_array, linestyle='-', color='r', label='Epsilon_Greedy')

        # Formatting
        plt.title('Cumulative Regret Over Time', fontsize=16)
        plt.xlabel('Timesteps', fontsize=14)
        plt.ylabel('Cumulative Regret', fontsize=14)
        plt.grid(True, which='both', linestyle='-', linewidth=0.5)
        plt.yticks(np.arange(0, max(self.bandit.cumulative_regret_array) + 5, step=5))

        # Add legend
        plt.legend(loc='upper left', fontsize=12)

        # Tight layout to ensure there's no clipping of labels
        plt.tight_layout()

        # Create an index for timesteps
        timesteps = np.arange(1, len(self.rewards) + 1)

        # Average out self.rewards
        avg_rewards = [np.mean(self.rewards[0:T+1]) for T in range(self.time_to_run)]

        # Plot the data
        plt.figure(2,figsize=(8,4))
        plt.plot(timesteps, avg_rewards, linestyle='-', color='r', label='Epsilon_Greedy')

        # Formatting
        plt.title('Average Reward Over Time', fontsize=16)
        plt.xlabel('Timesteps', fontsize=14)
        plt.ylabel('Mean Reward Value upto timestep t', fontsize=14)
        plt.grid(True, which='both', linestyle='-', linewidth=0.5)
        # plt.xticks(timesteps)  # Show all timesteps as x-axis ticks
        # plt.yticks(np.arange(0, max(self.rewards) + 5, step=5))

        # Add legend
        plt.legend(loc='lower right', fontsize=12)

        # Tight layout to ensure there's no clipping of labels
        plt.tight_layout()

    



# Code to test
if __name__ == "__main__":
    # Init Bandit
    TIME_HORIZON = 10_000
    bandit = MultiArmedBandit(np.array([0.23,0.55,0.76,0.44]))
    agent = EpsilonGreedyAgent(TIME_HORIZON, bandit, 0.05)

    # Loop
    for i in range(TIME_HORIZON):
        agent.give_pull()

    # Plot curves
    agent.plot_reward_vs_time_curve()
    agent.plot_arm_graph()
    bandit.plot_cumulative_regret()


            
        

    