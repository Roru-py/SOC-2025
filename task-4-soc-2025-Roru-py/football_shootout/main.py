from env import footballEnv
from agent import agent
import matplotlib.pyplot as plt

policy1 = {}
policy2={}
policy3={}
states = [] #list of tuples
#states
for i in range(1,17):
    for j in range(1,17):
        for k in range(1,17):
            states.append((i,j,k,1))
            states.append((i,j,k,2))

#policy1 = greedy defence
for s in states:
    t = s[s[3]-1]
    tx = (t-1)%4
    ty = (t-1)//4
    rx = (s[2]-1)%4
    ry = (s[2]-1)//4
    if abs(rx-tx) > abs(ry-ty):
        if rx > tx:
            policy1[s]=(1,0,0,0)
        else:
            policy1[s]=(0,1,0,0)
    else:
        if ry > ty:
            policy1[s]=(0,0,1,0)
        else:
            policy1[s]=(0,0,0,1)
    
    if t==s[2]:
        if s[2]==1:
            policy1[s]=(0,0.5,0,0.5)
        elif s[2]==4:
            policy1[s]=(0.5,0,0,0.5)
        elif s[2]==12:
            policy1[s]=(0,0.5,0.5,0)
        elif s[2]==16:
            policy1[s]=(0.5,0,0.5,0)
        elif rx==0:
            policy1[s]=(0,0.34,0.33,0.33)
        elif rx==3:
            policy1[s]=(0.33,0,0.33,0.34)
        elif ry==0:
            policy1[s]=(0.33,0.34,0,0.33)
        elif ry==3:
            policy1[s]=(0.33,0.34,0.33,0)
        else:
            policy1[s]=(0.25,0.25,0.25,0.25)


#policy2 = park the bus
for s in states:
    rx = (s[2]-1)%4
    if rx != 3:
        policy2[s]=(0,1,0,0)
    elif s[2]==4:
        policy2[s]=(0,0,0,1)
    elif s[2]==16:
        policy2[s]=(0,0,1,0)
    else: policy2[s]=(0,0,0.5,0.5)

#policy3 = random policy
for s in states:
    rx = (s[2]-1)%4
    ry = (s[2]-1)//4
    if s[2]==1:
        policy3[s]=(0,0.5,0,0.5)
    elif s[2]==4:
        policy3[s]=(0.5,0,0,0.5)
    elif s[2]==12:
        policy3[s]=(0,0.5,0.5,0)
    elif s[2]==16:
        policy3[s]=(0.5,0,0.5,0)
    elif rx==0:
        policy3[s]=(0,0.34,0.33,0.33)
    elif rx==3:
        policy3[s]=(0.33,0,0.33,0.34)
    elif ry==0:
        policy3[s]=(0.33,0.34,0,0.33)
    elif ry==3:
        policy3[s]=(0.33,0.34,0.33,0)
    else:
        policy3[s]=(0.25,0.25,0.25,0.25)

#Task-1 (evaluate all policies)
Env1 = footballEnv(0.3,0.7,policy1)
Env2 = footballEnv(0.3,0.7,policy2)
Env3 = footballEnv(0.3,0.7,policy3)

gamma = 0.7 #best gamma after plotting for diff values of gamma

agent1 = agent(Env1,gamma)
agent2 = agent(Env2,gamma)
agent3 = agent(Env3,gamma)

agent1.val_iteration()
agent2.val_iteration()
agent3.val_iteration()
#once we do this optimal policy is stored in the agent, so no need to do again

len = 10_000
print(agent1.goals(len)) #Excepted no.of goals againts policy-1 over random start
print(agent2.goals(len)) #Excepted no.of goals againts policy-2 over random start
print(agent3.goals(len)) #Excepted no.of goals againts policy-3 over random start

#easy to tough (scoring goal) -> policy3,policy1,policy2

#Graph-1
p_list=[0.1, 0.2, 0.3, 0.4, 0.5]
win_p = []
start = (5,9,8,1) #change it and check for different values (especially near goal)
q=0.7
len = 10_000
for p in p_list:
    env = footballEnv(p,q,policy1)
    player = agent(env,gamma) 
    player.val_iteration() #get optimal policy for given env
    win_p.append(player.win_prob(len,start))
print(win_p)
plt.plot(p_list, win_p,'r')
plt.title("Win Probability v/s p")
plt.xlabel("p")
plt.ylabel("Win Probability")
plt.grid(True)
plt.show()

#Graph-2
q_list=[0.6, 0.7, 0.8, 0.9,1]
win_p = []
start = (5,9,8,1)
p=0.3

for q in q_list:
    env = footballEnv(p,q,policy1)
    player = agent(env,gamma) 
    player.val_iteration() #get optimal policy for given env
    win_p.append(player.win_prob(len,start))
print(win_p)
plt.plot(q_list, win_p,'g')
plt.title("Win Probability v/s q")
plt.xlabel("q")
plt.ylabel("Win Probability")
plt.grid(True)
plt.show()

#change the start values,len or gamma to experiment with values
#comment out unwanted quantities to run code faster