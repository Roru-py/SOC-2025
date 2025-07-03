import gymnasium as gym
import numpy as np

# Hyperparameters
LEARNING_RATE_ACTOR = 1e-3
LEARNING_RATE_CRITIC = 1e-3
GAMMA = 0.99
EPISODES = 2000
STATE_DIM = 8
ACTION_DIM = 4

# Initialize environment
env = gym.make("LunarLander-v3", render_mode="human")

# Linear policy (actor) and value function (critic)
theta = np.random.randn(STATE_DIM, ACTION_DIM) * 0.1  # Policy weights
w = np.random.randn(STATE_DIM) * 0.1  # Value function weights

def softmax_policy(state):
    logits = np.dot(state, theta)
    probs = np.exp(logits - np.max(logits)) / np.sum(np.exp(logits - np.max(logits)))
    return np.random.choice(ACTION_DIM, p=probs)

def value_function(state):
    return np.dot(state, w)

for episode in range(EPISODES):
    state, _ = env.reset()
    episode_reward = 0
    done = False
    
    while not done:
        # 1. Choose action
        action = softmax_policy(state)
        
        # 2. Take step
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        episode_reward += reward
        
        # 3. Compute TD error (advantage)
        V = value_function(state)
        V_next = value_function(next_state) if not done else 0
        td_error = reward + GAMMA * V_next - V
        
        # 4. Update actor (policy gradient)
        logits = np.dot(state, theta)
        probs = np.exp(logits - np.max(logits)) / np.sum(np.exp(logits - np.max(logits)))
        grad_theta = np.outer(state, (np.eye(ACTION_DIM)[action] - probs))
        theta += LEARNING_RATE_ACTOR * td_error * grad_theta
        
        # 5. Update critic (value function)
        grad_w = state * td_error
        w += LEARNING_RATE_CRITIC * grad_w
        
        state = next_state
    
    if episode % 10 == 0:
        print(f"Episode {episode}, Reward: {episode_reward:.1f}")

env.close()