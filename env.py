#coding=utf-8

import pyglet

class ArmEnv(object):       # 手臂的运动（处理逻辑运行）
    def __init__(self):
        self.viewer = None      # 最开始没有viewer
       # self.state_dim =
       # self.action_dim =
       # self.action_bound =
    def step(self, action):
        pass
    def reset(self):
        pass
    def render(self):
        if self.viewer == None:     # 如果调用了render，且没有viewer，就生成一个
            self.viewer = Viewer()
        self.viewer.render()        # 调用Viewer中的render功能

class Viewer(pyglet.window.Window):     # 手臂的可视化
    def __init__(self):     # 画出手臂等
        bar_thk = 5         # 手臂的厚度
        # 创建窗口的继承
        # vsync 如果是 True, 按屏幕频率刷新, 反之不按那个频率
        super().__init__(width=400, height=400, resizable=False, caption='Arm', vsync=False)

        # 窗口背景颜色
        pyglet.gl.glClearColor(1, 1, 1, 1)

        # 将手臂的作图信息放入这个batch
        self.batch = pyglet.graphics.Batch()    # 创建batch对象

        # 添加蓝点至batch
        self.point = self.batch.add(
                4, pyglet.gl.GL_QUADS, None,    # 4个顶点；GL_QUADS表矩形形式
                ('v2f', [50, 50, 50, 100,100, 100, 100, 50]),   # v2f形式来表示点，两两一组，表x、y坐标
                ('c3B', (86, 109, 249) * 4))    # c3B的形式来表示颜色，三原色的形式；*4表4个点都是此色

        # 添加第一条手臂
        self.arm1 = self.batch.add(
                4, pyglet.gl.GL_QUADS, None,
                ('v2f', [250, 250, 250, 300, 260, 300, 260, 250]),
                ('c3B', (249, 86,86) * 4, ))

        # 添加第二条手臂，同上理
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
        pass

# 测试一下效果
if __name__ == '__main__':
    env = ArmEnv()
    while True:
        env.render()
