import pygame
import serial
import time

# 初始化Pygame
pygame.init()

# 获取屏幕尺寸并设置全屏模式
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.DOUBLEBUF)

# 设置颜色
white = (255, 255, 255)
red = (255, 0, 0)
gray = (169, 169, 169)
blue = (0, 0, 255)

# 初始化串口通信，修改为你的串口端口
ser = serial.Serial('COM8', 9600, timeout=0.01)  # 调整波特率为115200，增加串口通信速度
time.sleep(2)  # 等待串口稳定

def get_data(serial_port):
    try:
        data = serial_port.readline().decode().strip()
        if data:
            print(f"Received data: {data}")  # 调试信息
            values = list(map(float, data.split(',')))
            if len(values) == 18:  # 修改为18个值
                return values
    except ValueError:
        print("Error parsing data")  # 调试信息
        pass
    return None

def calculate_dot_y(distance, section_height):
    # 将距离转换为屏幕上的y坐标
    return section_height - (distance - 5) / 20 * section_height

# 主循环
running = True
previous_data = None  # 保存上一帧的数据用于对比
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # 从串口读取数据
    data = get_data(ser)

    # 判断数据是否发生变化
    if data is not None and data != previous_data:
        previous_data = data
        print(f"Valid data: {data}")  # 调试信息
        screen.fill(white)  # 仅在数据变化时清屏

        button_states = data[:14]
        distances = data[14:]

        # 计算每个区域的宽度
        section_width = screen_width // 14

        # 绘制竖线和小圆点
        for i, state in enumerate(button_states):
            line_x = int(section_width * (i + 0.5))
            color = gray if state == 0 else red
            pygame.draw.line(screen, color, (line_x, 0), (line_x, screen_height), 5)

            # 处理第一个距离传感器，映射到第一条竖线
            if i == 0 and state == 0 and 5 <= distances[0] <= 25:
                dot_y = calculate_dot_y(distances[0], screen_height)
                pygame.draw.circle(screen, blue, (line_x, int(dot_y)), 10)

            # 处理第二个距离传感器，映射到第2到第7条竖线
            elif 1 <= i <= 6 and state == 0 and 5 <= distances[1] <= 25:
                dot_y = calculate_dot_y(distances[1], screen_height)
                pygame.draw.circle(screen, blue, (line_x, int(dot_y)), 10)

            # 处理第三个距离传感器，映射到第8到第13条竖线
            elif 7 <= i <= 12 and state == 0 and 5 <= distances[2] <= 25:
                dot_y = calculate_dot_y(distances[2], screen_height)
                pygame.draw.circle(screen, blue, (line_x, int(dot_y)), 10)

            # 处理第四个距离传感器，映射到第14条竖线
            elif i == 13 and state == 0 and 5 <= distances[3] <= 25:
                dot_y = calculate_dot_y(distances[3], screen_height)
                pygame.draw.circle(screen, blue, (line_x, int(dot_y)), 10)

        # 更新显示
        pygame.display.flip()

    # 将延迟减少到更小的值
    time.sleep(0.01)

# 关闭串口
ser.close()
