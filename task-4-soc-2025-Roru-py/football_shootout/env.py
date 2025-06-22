import numpy as np
import random
import matplotlib.pyplot as plt

class footballEnv:
    def __init__(self,p,q,opp_policy):
        self.p = p
        self.q = q
        self.opp = opp_policy
    
    def get_rnxt(self,state): #for a given state, this function returns probabilities of R's movement
        r_nxt = []
        prob = self.opp[state] #P(l,r,u,d)
        rx=(state[2]-1)%4
        ry=(state[2]-1)//4
        for i in range(4):
            if prob[i]==0:
                r_nxt.append(state[2])
            else:
                if i==0:
                    rx-=1
                elif i==1:
                    rx+=1
                elif i==2:
                    ry-=1
                else:
                    ry+=1
                r_nxt.append(ry*4+rx+1)
        return r_nxt

    def get_nxt_state(self,state,action): #samples from the env directly (experimental)
        prob = np.random.rand()
        end = False
        notkl=1
        r_next = 0
        r_list = self.get_rnxt(tuple(state))
        for i in range(2):
            p = list(self.opp[tuple(state)])[:]
            p[i+1]+=p[i]
            if prob < p[i]:
                r_next = r_list[i]
                break
        if r_next==0:
            r_next = r_list[3]
        
        if action<8:
            if action<4:
                bx=(state[0]-1)%4
                by=(state[0]-1)//4
            elif action<8:
                bx=(state[1]-1)%4
                by=(state[1]-1)//4

            if action%4==0:
                bx = bx-1
            elif action%4==1:
                bx = bx+1
            elif action%4==2:
                by = by-1
            elif action%4==3: 
                by = by+1
            
            if bx>3 or bx<0 or by>3 or by<0:
                b_next = 0
                end = True
                reward = -100
                tp=1
                return [tuple(state),tp,reward,end]
            else: 
                b_next = by*4+bx+1

            if ((state[3]==1 and action<4) or (state[3]==2 and action//4==1))  and (r_next==b_next or (r_next==state[0] and b_next==state[2])):
                notkl = 0.5

            if (state[3]==1 and action<4) or (state[3]==2 and action//4==1):
                tp = notkl*(1-2*self.p)
                reward = 2.5
            else:
                tp = notkl*(1-self.p)
                reward = 1.5

            if b_next!=0 and prob > tp: 
                b_next = -1
                reward = -1
                end = True
            else:
                state[2]=r_next
                if(action<4):
                    state[0]=b_next
                else:
                    state[1]=b_next
        elif action==8:
            x1=(state[0]-1)%4
            y1=(state[0]-1)//4
            x2=(state[1]-1)%4
            y2=(state[1]-1)//4
            rx=(r_next-1)%4
            ry=(r_next-1)//4        
            if (x1-x2)*(y1-ry)==(y1-y2)*(x1-rx) and rx >= min(x1,x2) and rx <= max(x1,x2) and ry >= min(y1,y2) and ry <= max(y1,y2):
                notkl=0.5
            tp = notkl*(self.q-0.1*max(abs(x1-x2),abs(y1-y2)))
            if prob <= tp:
                if state[3]==1:
                    state[3]=2
                else:
                    state[3]=1
                state[2]=r_next
                reward = 5
            else:
                end = True
                reward = -2.5
                
        elif action==9:
            if r_next==8 or r_next==12:
                notkl=0.5
            x = (state[(state[3])-1]-1)%4
            tp = notkl*(self.q-0.2*(3-x))
            if prob <= tp:
                state[3]=0
                end=True
                reward = 40
            else:
                reward = -5
            end = True
        
        return [tuple(state),tp,reward,end] #tp and reward are not used since its model based
    #they need to be used in model free like TD(0)
    

    def nxt_state_data(self,state,action,r_next): #gives all states with probabilites (theoritical)
        end = []
        notkl=1
        reward = []
        next_state = []
        prob = []
        
        if action<8:
            if action<4:
                bx=(state[0]-1)%4
                by=(state[0]-1)//4
            elif action<8:
                bx=(state[1]-1)%4
                by=(state[1]-1)//4

            if action%4==0:
                bx = bx-1
            elif action%4==1:
                bx = bx+1
            elif action%4==2:
                by = by-1
            elif action%4==3: 
                by = by+1
            
            if bx>3 or bx<0 or by>3 or by<0:
                b_next = 0
                end.append(True)
                reward.append(-100) ##reward (to completely avoid)
                next_state.append((state))
                prob.append(1)
                return [reward,next_state,prob,end]
            else: 
                b_next = by*4+bx+1

            if ((state[3]==1 and action<4) or (state[3]==2 and action//4==1))  and (r_next==b_next or (r_next==state[0] and b_next==state[2])):
                notkl = 0.5

            if (state[3]==1 and action<4) or (state[3]==2 and action//4==1):
                tp = notkl*(1-2*self.p)
                reward = [2.5,-1] ##reward
            else:
                tp = notkl*(1-self.p)
                reward = [1.5,-1] ##reward
            prob.append(tp)
            prob.append(1-tp)
            end = [False,True]
            state[2]=r_next
            if(action<4):
                state[0]=b_next
            else:
                state[1]=b_next
            next_state.append(state)

        elif action==8:
            x1=(state[0]-1)%4
            y1=(state[0]-1)//4
            x2=(state[1]-1)%4
            y2=(state[1]-1)//4
            rx=(r_next-1)%4
            ry=(r_next-1)//4        
            if (x1-x2)*(y1-ry)==(y1-y2)*(x1-rx) and rx >= min(x1,x2) and rx <= max(x1,x2) and ry >= min(y1,y2) and ry <= max(y1,y2):
                notkl=0.5
            tp = notkl*(self.q-0.1*max(abs(x1-x2),abs(y1-y2)))
            prob = [tp,1-tp]
            end = [False,True]
            if state[3]==1:
                state[3]=2
            else:
                state[3]=1
            state[2]=r_next
            next_state.append(state)
            reward = [5,-2.5] ##reward
                
        elif action==9:
            if r_next==8 or r_next==12:
                notkl=0.5
            x = (state[(state[3])-1]-1)%4
            tp = notkl*(self.q-0.2*(3-x))
            prob = [tp,1-tp]
            end = [True,True]
            reward = [40,-5] ##reward
        
        return [reward,next_state,prob,end]
    
#the reward for each action are set such that we get high wins for different values of p and q. (Experimented by me)
