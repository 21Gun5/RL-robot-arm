#coding=utf-8

import pyglet
import numpy as np
'''
环境的编写主要是pyglet的应用，只追求实现效果，并未关注技术细节
'''
class ArmEnv(object):       # 手臂的运动（处理逻辑运行）
    viewer = None      # 最开始没有viewer
    dt = 0.1                                # 转动的速度和 dt 有关
    action_bound = [-1, 1]                  # 转动的角度范围
    goal = {'x': 100., 'y': 100., 'l': 40}  # 蓝色 goal 的 x,y 坐标和长度 l
    state_dim = 2                           # 两个观测值
    action_dim = 2  # 两个动作

    def __init__(self):
        self.arm_info = np.zeros(2, dtype=[('l', np.float32), ('r', np.float32)])   # 生成出(2,2)的矩阵
        self.arm_info['l'] = 100        # 两段手臂都 100 长
        self.arm_info['r'] = np.pi/6    # 两段手臂的端点角度
    def step(self, action):
        done = False
        r = 0.

        # 计算单位时间 dt 内旋转的角度, 将角度限制在360度以内
        action = np.clip(action, *self.action_bound)
        self.arm_info['r'] += action * self.dt
        self.arm_info['r'] %= np.pi * 2    # normalize

        # 我们可以将两截手臂的角度信息当做一个 state (之后会变)
        s = self.arm_info['r']

        # 如果手指接触到蓝色的 goal, 我们判定结束回合 (done)
        # 所以需要计算 finger 的坐标
        (a1l, a2l) = self.arm_info['l']  # radius, arm length
        (a1r, a2r) = self.arm_info['r']  # radian, angle
        a1xy = np.array([200., 200.])    # a1 start (x0, y0)
        a1xy_ = np.array([np.cos(a1r), np.sin(a1r)]) * a1l + a1xy  # a1 end and a2 start (x1, y1)
        finger = np.array([np.cos(a1r + a2r), np.sin(a1r + a2r)]) * a2l + a1xy_  # a2 end (x2, y2)

        # 根据 finger 和 goal 的坐标得出 done and reward
        if self.goal['x'] - self.goal['l']/2 < finger[0] < self.goal['x'] + self.goal['l']/2:
            if self.goal['y'] - self.goal['l']/2 < finger[1] < self.goal['y'] + self.goal['l']/2:
                done = True
                r = 1.      # finger 在 goal 以内
        return s, r, done
    def reset(self):
        self.arm_info['r'] = 2 * np.pi * np.random.rand(2)
        return self.arm_info['r']
    # 添加随机动作
    def sample_action(self):
        return np.random.rand(2)-0.5    # two radians
    def render(self):
        if self.viewer == None:     # 如果调用了render，且没有viewer，就生成一个
            self.viewer = Viewer(self.arm_info, self.goal)
        self.viewer.render()        # 调用Viewer中的render功能

class Viewer(pyglet.window.Window):     # 手臂的可视化
    bar_thc = 5         # 手臂的厚度

    def __init__(self, arm_info, goal):     # 画出手臂等
        # 创建窗口的继承
        # vsync 如果是 True, 按屏幕频率刷新, 反之不按那个频率
        super().__init__(width=400, height=400, resizable=False, caption='Arm', vsync=False)

        # 窗口背景颜色
        pyglet.gl.glClearColor(1, 1, 1, 1)

        # 将手臂的作图信息放入这个batch
        self.batch = pyglet.graphics.Batch()    # 创建batch对象

        # 添加arm信息
        self.arm_info = arm_info
        # 添加窗口中心点, 手臂的根
        self.center_coord = np.array([200, 200])

        # 添加goal至batch，蓝色goal的信息包括他的x,y坐标,goal的长度l
        self.goal = self.batch.add(
            4, pyglet.gl.GL_QUADS, None,
            ('v2f', [goal['x'] - goal['l'] / 2, goal['y'] - goal['l'] / 2,
                     goal['x'] - goal['l'] / 2, goal['y'] + goal['l'] / 2,
                     goal['x'] + goal['l'] / 2, goal['y'] + goal['l'] / 2,
                     goal['x'] + goal['l'] / 2, goal['y'] - goal['l'] / 2]),
            ('c3B', (86, 109, 249) * 4))

        # 添加第一条手臂至batch
        self.arm1 = self.batch.add(
                4, pyglet.gl.GL_QUADS, None,  # 4个顶点；GL_QUADS表矩形形式
                ('v2f', [250, 250, 250, 300, 260, 300, 260, 250]),   # v2f形式来表示点，两两一组，表x、y坐标
                ('c3B', (249, 86,86) * 4, ))    # c3B的形式来表示颜色，三原色的形式；*4表4个点都是此色

        # 添加第二条手臂至batch
        self.arm2 = self.batch.add(
                4, pyglet.gl.GL_QUADS, None,
                ('v2f', [100, 150, 100, 160, 200, 160, 200, 150]),
                ('c3B', (249, 86, 86) * 4,))


    def render(self):   # 刷新并呈现在屏幕上
        self._update_arm()  # 更新手臂内容 (暂时没有变化)
        self.switch_to()
        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()

    def on_draw(self):      # 刷新手臂等位置
        self.clear()        # 清屏
        self.batch.draw()   # 画上 batch 里面的内容

    def _update_arm(self):      # 更新手臂的位置信息
        (a1l, a2l) = self.arm_info['l']     # radius, arm length
        (a1r, a2r) = self.arm_info['r']     # radian, angle
        a1xy = self.center_coord            # a1 start (x0, y0)
        a1xy_ = np.array([np.cos(a1r), np.sin(a1r)]) * a1l + a1xy   # a1 end and a2 start (x1, y1)
        a2xy_ = np.array([np.cos(a1r+a2r), np.sin(a1r+a2r)]) * a2l + a1xy_  # a2 end (x2, y2)

        # 第一段手臂的4个点信息
        a1tr, a2tr = np.pi / 2 - self.arm_info['r'][0], np.pi / 2 - self.arm_info['r'].sum()
        xy01 = a1xy + np.array([-np.cos(a1tr), np.sin(a1tr)]) * self.bar_thc
        xy02 = a1xy + np.array([np.cos(a1tr), -np.sin(a1tr)]) * self.bar_thc
        xy11 = a1xy_ + np.array([np.cos(a1tr), -np.sin(a1tr)]) * self.bar_thc
        xy12 = a1xy_ + np.array([-np.cos(a1tr), np.sin(a1tr)]) * self.bar_thc

        # 第二段手臂的4个点信息
        xy11_ = a1xy_ + np.array([np.cos(a2tr), -np.sin(a2tr)]) * self.bar_thc
        xy12_ = a1xy_ + np.array([-np.cos(a2tr), np.sin(a2tr)]) * self.bar_thc
        xy21 = a2xy_ + np.array([-np.cos(a2tr), np.sin(a2tr)]) * self.bar_thc
        xy22 = a2xy_ + np.array([np.cos(a2tr), -np.sin(a2tr)]) * self.bar_thc

        # 将点信息都放入手臂显示中
        self.arm1.vertices = np.concatenate((xy01, xy02, xy11, xy12))
        self.arm2.vertices = np.concatenate((xy11_, xy12_, xy21, xy22))

# 测试一下效果
if __name__ == '__main__':
    env = ArmEnv()
    while True:
        env.render()
        env.step(env.sample_action())

