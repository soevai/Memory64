import os, sys
from .Function import (
    FindWindowPid, GetWindRect,
    init_Library
)

try:
    import pygame
except ImportError:
    os.system('pip install pygame -i https://pypi.tuna.tsinghua.edu.cn/simple')
    print('安装模块中, 请耐心等待..')
    import pygame

class ExecDraw():
    def __init__(self, hwnd):
        pygame.init()
        self.firstHwnd = hwnd
        self.Timer = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('D3Gui')
        left, top, right, bottom = GetWindRect(self.firstHwnd)
        Width, Height = right - left, bottom - top
        self.screen = pygame.display.set_mode([Width, Height], pygame.NOFRAME)
        self.hwnd = FindWindowPid('pygame', 'D3Gui')[0]
        init_Library.setWindowLong(self.hwnd, -20, 524288)
        init_Library.setLayeredWindowAttributes(self.hwnd, 0, 0, 1)
        init_Library.setWindowPos(self.hwnd, -1, left, top, Width, Height, 1)


    def drawText(self, text, size, x, y, color):
        '''
        :func: 绘制文字
        :param text: 内容
        :param size: 文字大小
        :param x: 横坐标
        :param y: 纵坐标
        :param color: RGB 颜色 如: (255, 0, 0)
        :return:
        '''
        textFont = pygame.font.SysFont('simhei', size)
        text_fmt = textFont.render(text,1 ,color)
        self.screen.blit(text_fmt,(x,y))

    def drawRect(self, x, y, width, height, c, color):
        '''
        :func: 绘制矩形
        :param x: 横坐标
        :param y: 纵坐标
        :param width: 宽度
        :param height: 高度
        :param c: 粗细
        :param color: RGB 颜色
        :return:
        '''
        pygame.draw.rect(self.screen, color, (x, y, width, height), c)

    def drawLine(self,startX,startY, endX, endY, width, color):
        '''
        :func: 绘制直线
        :param startX: 开始x坐标
        :param startY: 开始y坐标
        :param endX: 结束x坐标
        :param endY: 结束y坐标
        :param width: 粗细
        :param color: RGB 颜色
        :return:
        '''
        pygame.draw.line(self.screen, color, (startX,startY),(endX,endY), width)

    def drawCircle(self,x, y, c, color):
        '''
        :func: 绘制圆
        :param x: 横坐标
        :param y: 纵坐标
        :param c: 粗细
        :param color: RGB 颜色
        :return:
        '''
        pygame.draw.circle(self.screen, color, (x, y), c)

    def startLoop(self):
        '''
        :func: 开始 (必须)
        :return:
        '''
        self.Timer.tick(60)
        self.screen.fill((0, 0, 0))

    def endLoop(self):
        '''
        :func: 结束 (必须)
        :return:
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        left, top, right, bottom = GetWindRect(self.firstHwnd)
        Width, Height = right - left, bottom - top
        if not any([left, top, right, bottom]):
            sys.exit('进程不存在，已安全退出！')
        init_Library.setWindowPos(self.hwnd, -1, left, top, Width, Height , 1)
        pygame.display.update()