import gymnasium as gym
import numpy as np

env = gym.make("LunarLander-v3")
obs,_ = env.reset()
total=0
gamma = 0.99
alpha = 1e-3
state_size = 8
action_size = 4
EPISODES = 1000

w = np.random.rand(len(obs))
theta = np.random.rand(state_size*action_size)

def softmax_sample(state):
    arr=[]
    for i in range(4):
        feature_sa = np.zeros(state_size*action_size) 
        start = i*state_size
        feature_sa[start:start+state_size] = state
        arr.append(np.dot(feature_sa,theta))
    arr = np.array(arr)
    arr = np.exp(arr-np.max(arr))
    arr = arr/np.sum(arr)
    p = np.random.rand()
    sum = 0
    for i in range(4):
        sum+=arr[i]
        if(p<=sum):
            return i

def lin_valfunc_approx(state):
    return np.dot(np.array(state),w)

def pol_grad(feature):
    state = feature[:len(obs)]
    f = np.zeros(state_size*action_size)
    arr=[]
    for i in range(4):
        feature_sa = np.zeros(state_size*action_size) 
        start = i*state_size
        feature_sa[start:start+state_size] = state
        arr.append(np.dot(feature_sa,theta))
    arr = np.array(arr)
    arr = np.exp(arr-np.max(arr))
    arr = arr/np.sum(arr)

    for i in range(4):
        feature_saa = np.zeros(state_size*action_size) 
        start = i*state_size
        feature_saa[start:start+state_size] = state
        f = f + feature_saa*arr[i]
    return feature - f      

for i in range(EPISODES):  
    total=0
    state,_ = env.reset()
    action = softmax_sample(state)
    done = False
    while not done:
    
        feature_sa = np.zeros(state_size*action_size) 
        start = action*state_size
        feature_sa[start:start+state_size] = state

        next_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        if done==False:
            delta = reward+gamma*lin_valfunc_approx(next_state)-lin_valfunc_approx(state)
        else:
            delta = reward - lin_valfunc_approx(state)

        theta = theta + alpha*delta*pol_grad(feature_sa)
        w = w + alpha*delta*np.array(state)

        action = softmax_sample(next_state)
        state = next_state
        total += reward
    print("Episode ",i,":",total)

env.close()