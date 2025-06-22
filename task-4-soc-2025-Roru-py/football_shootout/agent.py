import random
from env import footballEnv

class agent: #Based on value iteration 
    def __init__(self,env:footballEnv,gamma=1): 
        self.env = env
        self.gamma = gamma
        self.all_states = []
        self.policy = {}
        self.value = {}
        for i in range(1,17):
            for j in range(1,17):
                for k in range(1,17):
                    self.all_states.append((i,j,k,1))
                    self.all_states.append((i,j,k,2))
        for i in self.all_states:
            self.policy[i] = random.choice(range(10))  #random action (no need to set for value iteration but needed for policy iteration)
            self.value[i] = 0.0 #we start with this
        
    def val_iteration(self,delta=1e-4): #error is delta here
        run = True
        while(run): 
            diff = 0   
            for s in self.all_states: #uses bellman optimality eqn to improve value function
                max = 0
                mararg=0
                for i in range(10):    
                    r_prob = self.env.opp[s]
                    r_nxt = self.env.get_rnxt(s)
                    val = 0
                    for j in range(4):
                        if r_prob[j]!=0:
                            data = self.env.nxt_state_data(list(s),i,r_nxt[j])
                            for k in range(len(data[3])):
                                if data[3][k]==True:
                                    val += r_prob[j]*data[2][k]*data[0][k]
                                else:
                                    if data[1][k]==[2,1,-2,1]: print(s,r_prob,r_nxt)
                                    val += r_prob[j]*data[2][k]*(data[0][k]+self.gamma*self.value[tuple(data[1][k])])
                    
                    if i==0 or val > max:
                        max = val
                        maxarg = i
                if diff < abs(max-self.value[s]):
                    diff = abs(max-self.value[s])
                self.value[s]=max
                self.policy[s]=maxarg
            
            if diff <= delta:
                run = False
    

    def goals(self,sample_len): #calculates expectation of goals for a given policy (stored)
        goal = 0
        for i in range(sample_len):
            state = list(random.choice(self.all_states))
            while(True):
                data = self.env.get_nxt_state(state,self.policy[tuple(state)])
                if data[3] == True:
                    if data[0][3]==0:
                        goal += 1
                    break
                if data[3] == False:
                    state = list(data[0])
        return goal/sample_len

    def win_prob(self,length,start): #calculates probability of scoring if we start from particular state
        
        wins = 0
        for i in range(length): #length is large to stabilize
            state = list(start)[:]
            while(True):
                action = self.policy[tuple(state)]
                data = self.env.get_nxt_state(state,action)
                if data[3] == True:
                    if data[0][3]==0: #goal scored
                        wins += 1
                    break
                if data[3] == False:
                    state = list(data[0])
        return wins/length