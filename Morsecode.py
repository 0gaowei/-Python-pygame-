import time
import pygame
from sys import exit
from pygame.locals import *

pygame.init()
pygame.mixer.init()
#  gym界面没输入bug,欢迎界面加载效果，统计正确率效果并显示在*_done块，bgm效果
# 图片库
icon_photo = "photo/welcome.jpg"
welcome_photo = "photo/welcome.jpg"
section1_photo = "photo/introduction.jpg"
section2_challenge_photo = "photo/challenge.jpg"
section2_gym_photo = "photo/gym.jpg"
challenge_get = "photo/challenge_done.png"
gym_get = "photo/gym_succeed.jpg"
choose_photo = "photo/input.jpg"
introduction_photo = "photo/introduction_bg.jpg"
# 音乐库
bgm_music = "music/bg_welcome_music.mp3"
bgm_challenge = "music/challenge_music.mp3"
bgm_challenge_succeed = "music/challenge_done.mp3"
bgm_input = "music/flower_dance.mp3"
bgm_gym = "music/flower_dance.mp3"
bgm_gym_succeed = "music/flower_sea.mp3"
# 字体库
font_equal = "font/VictorMono-Bold-2.otf"
font_xingshu = "font/xingshu.otf"
font_thin_alpha = "font/VictorMono-Thin-19.otf"
font_fangzheng = "font/fangzheng.ttf"
font_kaishu = "font/kaishu.ttf"
font_1 = "font/1.ttf"
# 颜色库
red = (204, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
purple = (102, 0, 204)
white = (255, 255, 255)
green = (0, 166, 100)
qiguaidehei = (35, 12, 6)
jiu_red = (100, 40, 40)
# 摩斯电码字典
dic_morse = {'A': '.|', 'B': '|...', 'C': '|.|.', 'D': '|..', 'E': '.', 'F': '..|.',  # A-Z      # Morse 电码字典
             'G': '||.', 'H': '....', 'I': '..', 'J': '.|||', 'K': '|.|', 'L': '.|..',
             'M': '||', 'N': '|.', 'O': '|||', 'P': '.||.', 'Q': '||.|', 'R': '.||',
             'S': '...', 'T': '|', 'U': '..|', 'V': '...|', 'W': '.||', 'X': '|..|',
             'Y': '|.||', 'Z': '||..',
             '1': '.||||', '2': '..|||', '3': '...||', '4': '....|', '5': '.....',  # 0-9
             '6': '|....', '7': '||...', '8': '|||..', '9': '||||.', '0': '|||||',
             ' ': '0', '.': '.|.|.|', ',': '||..||', ';': '|.|.|.',  # 标点符号
             "'": '.|..|.', '/': '||..|.', '[': '|.||.', ']': '|.||.|', '+': '.|.|.', '-': '|....|', '*': '|..|'}
# 选择界面文字介绍
introduction_text = "1938年 上海                         " \
                    "这里是帝国主义侵略中国的大本营，也是蒋介石勾结日寇搞卖国活动的秘密接头点 " \
                    "我党地下组织的电台被敌人破坏了，延安解放区我军电台政委李侠奉命前往上海，加强秘密电台的工作。" \
                    "现地下党组织同时还派你协助李侠工作。现有训练和挑战两个模式，时间紧急，快做出你的选择吧。"

# 挑战明文
messages = "YOU NEI GUI, TING ZHI JIAO YI. NEI GUI SHI SUN SI HAN. YI DIAN LIU JI DE YOU XI. GAN WAN ME."
# 游戏说明书
directory = " 这是模拟摩斯电码发报的小游戏，游戏中的摩斯电码用 0来表示空格,用 | 表示 — , 点 · 即为 ·" \
            " 游戏分为训练模式与挑战模式。            在训练模式中，你可输入想练习的字符，确认后，摩斯电码将会自动给出，请按照密文输入吧。" \
            "          在挑战模式中，明文情报已给出，请你完成情报的发送。注意：挑战模式你将无法删除已输入的电码。" \
            "      （按4键返回选择界面，你可随时按q键关闭游戏）"


# 背景音乐
def music_load(music, volume):
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(volume)


# 返回摩斯电码函数
def morse_code(messages_get):
    morse_messages = ""
    for char in messages_get:
        morse_messages = morse_messages + dic_morse[char]
    return morse_messages


# 退出函数
def quit_function(event):
    if event.type == QUIT:
        pygame.mixer.music.stop()
        exit()
    elif event.type == KEYUP:
        if event.key == K_q:
            pygame.mixer.music.stop()
            exit()


# 图片加载刷新函数
def screen_load(load_photo, x, y):
    photo = pygame.image.load(load_photo)
    screen.blit(photo, (x, y))
    pygame.display.update()


# 行字体加载函数
def font_refresh(text, font, color, size, x, y):
    my_font = pygame.font.Font(font, size)
    my_text = my_font.render(text, True, color)
    screen.blit(my_text, (x, y))
    pygame.display.update()


# 绘制矩形函数
def create_rect(x, y, width, height, color):
    pygame.draw.rect(screen, color, [x, y, width, height], 0)
    pygame.display.flip()


# 逐字显示效果,无删除事件
def load_char(messages_list, font, color, size, x, y, delta_x, delta_y, right):
    cur_list = ""
    x_pre = x
    for i in messages_list:
        x_pre += delta_x
        cur_list += i
        font_refresh(cur_list, font, color, size, x, y)
        if x_pre >= right:
            y += delta_y
            cur_list = ""
            x_pre = x


# 答复函数，有延时
def response(answer, color, size, x, y):
    font_refresh(answer, font_xingshu, color, size, x, y)
    time.sleep(2)


# 得到用户训练部分输入且有输出函数
def show_input_message(color):
    my_input = ""
    # 绘制输入界面
    screen.fill(black)
    screen_load(choose_photo, 0, 42)
    music_load(bgm_input, 0.2)
    pygame.mixer.music.play(-1, 0)
    # 输入界面上的提示
    load_char("请输入你的训练信息:你可输入 0-9,A-Z及符号,./;'[]-+-* 按ENTER键完成输入进入训练）",
              font_xingshu, yellow, 20, 0, 0, 7, 20, 300)
    # 输入事件
    while True:
        for event3 in pygame.event.get():
            # 关闭游戏按钮
            if event3.type == QUIT:
                pygame.mixer.music.stop()
                exit()
            elif event3.type == KEYUP:
                i = event3.key
                if i == K_RETURN:
                    if len(my_input) == 0:
                        response("啥都没输入哦", yellow, 50, 200, 400)
                        screen_load(choose_photo, 0, 42)
                    else:
                        return my_input
                elif len(my_input) <= 80 and (ord('0') <= i <= ord('9') or
                                              i == ord(' ') or i == ord('.') or i == ord(',') or i == ord("'") or
                                              i == ord(';') or i == ord('[') or i == ord(']') or
                                              i == ord('+') or i == ord('-') or i == ord('*') or i == ord('/')):
                    my_input += chr(i)
                    load_char(my_input, font_1, color, 80, 20, 42, 15, 80, 300)
                elif len(my_input) <= 80 and ord('a') <= i <= ord('z'):
                    my_input += chr(i - 32)
                    load_char(my_input, font_1, color, 80, 20, 42, 15, 80, 300)
                elif i == ord('\b'):
                    screen_load(choose_photo, 0, 42)
                    my_input = my_input[:-1]
                    load_char(my_input, font_1, color, 80, 20, 42, 15, 80, 300)


# 模拟用户开始发电报中的刷新函数
def refresh(user_input, wrong_input, right_color, wrong_color):
    load_char(user_input, font_equal, right_color, 30, 25, 373, 6, 36, 300)
    load_char(wrong_input, font_equal, wrong_color, 30, 25, 373, 6, 36, 300)


# 模拟用户开始发电报函数
def print_morse(text_morse, bg_color, right_color, wrong_color, t):
    user_input = ""  # 读取用户输入
    wrong_input = ""  # 错误显示列表
    counts = '-'
    show_time(counts)
    flag = False
    while True:
        for event3 in pygame.event.get():
            # 关闭游戏按钮
            quit_function(event3)
            if event3.type == COUNT and flag:  # 判断事件是否为计时事件
                counts = counts + 1
                show_time(counts)
            if event3.type == KEYUP:
                if not flag:  # 按下按键后初始化计时器
                    counts = 0
                    flag = True
                i = event3.key
                if len(user_input) == len(text_morse):
                    if i == K_3:  # 返回主界面按钮
                        pygame.mixer.music.stop()
                        return main()
                    elif i == K_RETURN:  # 完成按钮（全部输入后有效），返回值用在调到统计函数那里
                        if len(user_input) == len(text_morse):
                            pygame.mixer.music.stop()
                            return user_input
                    elif i == ord('\b') and t != 1:  # 删除操作
                        create_rect(20, 376, 760, 210, bg_color)
                        user_input = user_input[:-1]
                        wrong_input = wrong_input[:-1]
                        refresh(user_input, wrong_input, right_color, wrong_color)
                        refresh(user_input, wrong_input, right_color, wrong_color)
                    continue  # 限制输入长度
                if i == K_3:  # 返回主界面按钮
                    return main()
                elif i == K_RETURN:  # 完成按钮，返回值用在调到统计函数那里
                    if len(user_input) == len(text_morse):
                        return user_input
                elif i == ord('0'):
                    user_input += '0'
                    if text_morse[len(user_input) - 1] == user_input[-1]:
                        wrong_input += ' '
                    else:
                        wrong_input += '0'
                    refresh(user_input, wrong_input, right_color, wrong_color)
                elif i == ord('-'):
                    user_input += '.'
                    if text_morse[len(user_input) - 1] == user_input[-1]:
                        wrong_input += ' '
                    else:
                        wrong_input += '.'
                    refresh(user_input, wrong_input, right_color, wrong_color)
                elif i == ord('='):
                    user_input += '|'
                    if text_morse[len(user_input) - 1] == user_input[-1]:
                        wrong_input += ' '
                    else:
                        wrong_input += '|'
                    refresh(user_input, wrong_input, right_color, wrong_color)
                elif i == ord('\b') and t != 1:
                    create_rect(20, 376, 760, 210, bg_color)
                    user_input = user_input[:-1]
                    wrong_input = wrong_input[:-1]
                    refresh(user_input, wrong_input, right_color, wrong_color)


# 返回正确率函数
def compare(morse_right, morse_input):
    flag = 0
    for i in range(len(morse_right)):
        if morse_right[i] == morse_input[i]:
            flag += 1
    return round(flag / len(morse_right) * 100, 2)


# 自定义计时事件
COUNT = pygame.USEREVENT + 1
# 每隔1秒发送一次自定义事件
pygame.time.set_timer(COUNT, 1000)


def show_time(counts):
    create_rect(770, 17, 30, 30, white)
    font_refresh(str(counts), font_xingshu, black, 20, 770, 23)


######################################################################################################################
# 按键说明界面
def game_directory():
    # 绘制说明界面
    screen_load(introduction_photo, 0, 0)
    # 介绍背景矩形
    create_rect(0, 238, 800, 362, white)
    # 按键介绍文字
    load_char(directory, font_kaishu, black, 30, 12, 240, 11.5, 37, 300)
    while True:
        for event in pygame.event.get():
            # 关闭游戏按钮
            quit_function(event)
            if event.type == KEYUP:
                if event.key == K_4:
                    return section1()
                elif event.key == K_3:
                    return main()


# 选择界面
def section1():
    # 绘制选择界面
    screen_load(section1_photo, 0, 0)
    # 选择界面上的介绍文字
    load_char(introduction_text, font_fangzheng, qiguaidehei, 25, 20, 15, 9, 44, 300)
    load_char("游戏介绍：按4键查看游戏说明。按2键开始训练,按1键进入挑战。", font_xingshu, white, 40, 20, 400, 15, 44, 300)
    while True:
        for event1 in pygame.event.get():
            # 关闭游戏按钮
            quit_function(event1)
            if event1.type == KEYUP:
                if event1.key == K_1:  # 按1进入挑战模式，按2进入训练模式
                    pygame.mixer.music.stop()
                    create_rect(20, 350, 680, 50, white)
                    response("我将即刻行动！感谢组织信任。", red, 50, 20, 350)
                    return section2_challenge()
                elif event1.key == K_4:
                    return game_directory()
                elif event1.key == K_2:
                    pygame.mixer.music.stop()
                    create_rect(20, 350, 420, 50, white)
                    response("我选择训练！", jiu_red, 50, 20, 350)
                    return section2_gym()
                elif event1.key == K_3:
                    return main()


# 挑战界面
def section2_challenge():
    # 绘制挑战界面
    screen_load(section2_challenge_photo, 0, 0)
    music_load(bgm_challenge, 0.2)
    pygame.mixer.music.play(-1, 0)
    # 选择界面上的提示
    font_refresh("(q键关闭游戏，按3键返回欢迎界面,0键模拟空格，-键模拟点，=键模拟竖线，Enter键提交)", font_xingshu, white,
                 20, 0, 0)
    font_refresh("明文:", font_xingshu, white, 25, 20, 23)
    font_refresh("密文:", font_xingshu, white, 25, 20, 110)
    font_refresh("输入:", font_xingshu, white, 25, 20, 345)
    # 时间背景
    create_rect(770, 20, 30, 30, white)
    # 显示明文
    load_char(messages, font_thin_alpha, white, 30, 25, 43, 6, 30, 300)
    # 显示密文
    load_char(morse_code(messages), font_equal, white, 30, 25, 140, 6, 36, 300)
    # 用户开始输入
    usr_morse = print_morse(morse_code(messages), blue, green, red, 1)
    # 统计正确率
    rate = "你的正确率为" + str(compare(morse_code(messages), usr_morse)) + "%"
    # 呈现胜利框框
    music_load(bgm_challenge_succeed, 0.2)
    pygame.mixer.music.play()
    screen_load(challenge_get, 0, 50)
    # 返回欢迎界面提示
    font_refresh("恭喜你成功将情报传出", font_xingshu, white, 45, 105, 200)
    font_refresh(rate, font_xingshu, white, 45, 105, 250)
    font_refresh("请按空格（SPACE）关闭电台", font_xingshu, jiu_red, 45, 105, 400)
    while True:
        for event_challenge in pygame.event.get():
            # 返回欢迎界面事件
            quit_function(event_challenge)
            if event_challenge.type == KEYUP:
                if event_challenge.key == K_SPACE:
                    pygame.mixer.music.stop()
                    return main()


# 训练界面
def section2_gym():
    # 用户自定义输入界面
    get_input = show_input_message(blue)
    # 绘制挑战界面
    screen_load(section2_gym_photo, 0, 0)
    # 选择界面上的提示
    font_refresh("(按q键关闭游戏，3键返回开始界面,0键模拟空格，-键模拟点，=键模拟竖线,Enter键提交)", font_xingshu, black,
                 20, 0, 0)
    create_rect(20, 46, 760, 70, white)
    create_rect(20, 143, 760, 210, white)
    create_rect(20, 376, 760, 210, white)
    font_refresh("明文:", font_xingshu, black, 25, 20, 22)
    font_refresh("密文:", font_xingshu, black, 25, 20, 116)
    font_refresh("输入:", font_xingshu, black, 25, 20, 351)
    # 明文
    load_char(get_input, font_thin_alpha, black, 30, 25, 43, 6, 30, 300)
    # 密文
    load_char(morse_code(get_input), font_equal, green, 30, 25, 141, 6, 36, 300)
    # 用户开始输入
    usr_morse = print_morse(morse_code(get_input), white, black, red, 0)
    # 统计正确率
    rate = "你的正确率为" + str(compare(morse_code(get_input), usr_morse)) + "%"
    # 呈现完成框框
    screen_load(gym_get, 0, 47)
    music_load(bgm_gym_succeed, 0.2)
    pygame.mixer.music.play(-1, 0)
    # 显示返回提示
    font_refresh("恭喜你完成训练", font_xingshu, yellow, 45, 390, 200)
    font_refresh(rate, font_xingshu, yellow, 45, 390, 250)
    font_refresh("请按空格(SPACE)", font_xingshu, yellow, 45, 390, 400)
    font_refresh("返回选择界面", font_xingshu, yellow, 45, 390, 450)
    while True:
        for event_gym in pygame.event.get():
            # 返回选择界面事件
            quit_function(event_gym)
            if event_gym.type == KEYUP:
                if event_gym.key == K_SPACE:
                    pygame.mixer.music.stop()
                    return main()


# 游戏主循环
def main():
    # 绘制欢迎界面
    screen_load(welcome_photo, 0, 0)
    music_load(bgm_music, 0.2)
    pygame.mixer.music.play(-1, 0)
    # 欢迎引导字体
    font_refresh("欢 迎 ！ 请 按 ENTER 键 以 开 始 游 戏 ......", font_xingshu, yellow, 20, 180, 550)
    while True:
        for event in pygame.event.get():
            # 关闭游戏按钮
            quit_function(event)
            # 画面跳转按钮
            if event.type == KEYUP:
                if event.key == K_RETURN:
                    response("加载中......", white, 30, 250, 400)
                    return section1()


# 创建游戏主窗口及图标与标题
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("永不消逝的电波")
icon = pygame.image.load(icon_photo)
pygame.display.set_icon(icon)

# 主函数
main()
