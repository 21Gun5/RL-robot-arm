#coding=utf-8

# 导入环境和学习方法
from env import ArmEnv
from rl import DDPG

# 设置全局变量
MAX_EPISODES = 500
MAX_EP_STEPS = 200

# 设置环境
env = ArmEnv()
s_dim = env.state_dim
a_dim = env.action_dim
a_bound = env.action_bound

# 设置学习方法 (这里使用 DDPG)
rl = DDPG(a_dim, s_dim, a_bound)

# 开始训练
for i in range(MAX_EPISODES):   # range创建一个整数列表，多用于for循环
    s = env.reset()     # 初始化回合设置
    for j in range(MAX_EP_STEPS):
        env.render()    # 渲染环境
        a = rl.choose_action(s)     # RL选择动作
        s_, r, done = env.step(a)   # 在环境中施加动作

        # DDPG 算法需要存放记忆库
        rl.store_transition(s, a, r, s_)

        if rl.memory_full:
            rl.learn()      # 若记忆库满，则开始学习

        s = s_      # 变为下一回合



