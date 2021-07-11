import numpy as np
import pandas as pd
from gym.utils import seeding
import gym
from gym import spaces

import matplotlib.pyplot as plt

data_1 = pd.read_csv('/Users/xiongzhuoran/anaconda3/envs/venv/lib/python3.6/site-packages/gym/envs/zxstock/Data_Daily_Stock_Dow_Jones_30/dow_jones_30_daily_price.csv')

equal_4711_list = list(data_1.tic.value_counts() == 4711)
names = data_1.tic.value_counts().index

# select_stocks_list = ['NKE','KO']
select_stocks_list = list(names[equal_4711_list])+['NKE','KO']

data_2 = data_1[data_1.tic.isin(select_stocks_list)][~data_1.datadate.isin(['20010912','20010913'])]

data_3 = data_2[['iid','datadate','tic','prccd','ajexdi']]

data_3['adjcp'] = data_3['prccd'] / data_3['ajexdi']

train_data = data_3[(data_3.datadate > 20090000) & (data_3.datadate < 20160000)]

train_daily_data = []

for date in np.unique(train_data.datadate):
    train_daily_data.append(train_data[train_data.datadate == date])

iteration = 0


class StockEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, day = 0, money = 10 , scope = 1):
        self.day = day
        
        # buy or sell maximum 5 shares
        self.action_space = spaces.Box(low = -5, high = 5,shape = (28,),dtype=np.int8) 

        # [money]+[prices 1-28]+[owned shares 1-28]
        self.observation_space = spaces.Box(low=0, high=np.inf, shape = (57,))

        # # [money]+[prices 1-28]+[owned shares 1-28]
        # self.observation_space = spaces.Box(low=0, high=np.inf, shape = (5,))
        
        self.data = train_daily_data[self.day]
        
        self.terminal = False
        
        self.state = [10000] + self.data.adjcp.values.tolist() + [0 for i in range(28)]
        self.reward = 0
        
        self.asset_memory = [10000]

        self.reset()
        self._seed()


    def _sell_stock(self, index, action):

        self.state[0] += self.state[index+1]*min(abs(action), self.state[index+29])
        self.state[index+29] -= min(abs(action), self.state[index+3])
    
    def _buy_stock(self, index, action):
        available_amount = self.state[0] // self.state[index+1]
        # print('available_amount:{}'.format(available_amount))
        self.state[0] -= self.state[index+1]*min(available_amount, action)
        # print(min(available_amount, action))

        self.state[index+29] += min(available_amount, action)
        
    def step(self, actions):
        # print(self.day)
        self.terminal = self.day >= 1761
        print(actions)

        if self.terminal:
            plt.plot(self.asset_memory,'r')
            plt.savefig('/Users/xiongzhuoran/Documents/DQN/iteration_{}.png'.format(iteration))
            plt.close()
            print("total_reward:{}".format(self.state[0]+ sum(np.array(self.state[1:29])*np.array(self.state[29:]))- 10000 ))
            
            
            # print('total asset: {}'.format(self.state[0]+ sum(np.array(self.state[1:29])*np.array(self.state[29:]))))
            return self.state, self.reward, self.terminal,{}

        else:
            # print(np.array(self.state[1:29]))


            begin_total_asset = self.state[0]+ sum(np.array(self.state[1:29])*np.array(self.state[29:]))
            # print("begin_total_asset:{}".format(begin_total_asset))
            argsort_actions = np.argsort(actions)
            sell_index = argsort_actions[:np.where(actions < 0)[0].shape[0]]
            buy_index = argsort_actions[::-1][:np.where(actions > 0)[0].shape[0]]

            for index in sell_index:
                # print('take sell action'.format(actions[index]))
                self._sell_stock(index, actions[index])

            for index in buy_index:
                # print('take buy action: {}'.format(actions[index]))
                self._buy_stock(index, actions[index])

            self.day += 1
            self.data = train_daily_data[self.day]         


            print("stock_shares:{}".format(self.state[29:]))
            self.state =  [self.state[0]] + self.data.adjcp.values.tolist() + list(self.state[29:])
            end_total_asset = self.state[0]+ sum(np.array(self.state[1:29])*np.array(self.state[29:]))
            # print("end_total_asset:{}".format(end_total_asset))
            
            self.reward = end_total_asset - begin_total_asset            
            print("step_reward:{}".format(self.reward))

            self.asset_memory.append(end_total_asset)


        return self.state, self.reward, self.terminal, {}

    def reset(self):
        self.asset_memory = [10000]
        self.day = 0
        self.data = train_daily_data[self.day]
        self.state = [10000] + self.data.adjcp.values.tolist() + [0 for i in range(28)]
        
        # iteration += 1 
        return self.state
    
    def render(self, mode='human'):
        return self.state

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]