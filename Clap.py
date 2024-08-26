import serial
import time

# Configuring the Serial Port
ser = serial.Serial('COM8', 9600)

def read_serial_data():
    num_sensors = 14
    previous_states = [1] * num_sensors
    current_states = [1] * num_sensors
    left_sequence = []
    right_sequence = []
    last_press_time = time.time()
    timeout = 2  # set Timeout time as 2 seconds
    max_time_difference = 0.01  # 两端按键触发的最大时间差 Maximum time difference between key triggering at both ends

    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()

            if not line:
                continue

            try:
                data = list(map(int, line.split(',')))
            except ValueError:
                print("Invalid data received:", line)
                continue

            if len(data) == num_sensors:
                current_states = data

                for i in range(num_sensors):
                    if previous_states[i] == 1 and current_states[i] == 0:
                        print(f"Pin {i} triggered")
                        current_time = time.time()
                        if i < num_sensors // 2:
                            left_sequence.append((i, current_time))
                        else:
                            right_sequence.append((i, current_time))
                        last_press_time = current_time
                    elif previous_states[i] == 0 and current_states[i] == 1:
                        print(f"Pin {i } released")

                # 更新之前的状态
                previous_states = current_states[:]

                # 检查是否满足汇合动作
                if len(left_sequence) > 3 and len(right_sequence) > 3:
                    # 获取最新的按键
                    left_pos, left_time = left_sequence[-1]
                    right_pos, right_time = right_sequence[-1]

                    # 检查按键时间是否接近
                    if abs(left_time - right_time) <= max_time_difference:
                        # 确保按键是从两端靠近的
                        prev_left_pos, _ = left_sequence[-2]
                        prev_right_pos, _ = right_sequence[-2]
                        if prev_left_pos < left_pos and prev_right_pos > right_pos:
                            print("Clap gesture detected!")
                            # 清空序列以检测下一次按键方向
                            left_sequence = []
                            right_sequence = []

            # 检查是否超时
            current_time = time.time()
            if current_time - last_press_time > timeout:
                # 清空序列，重置状态
                left_sequence = []
                right_sequence = []

if __name__ == '__main__':
    try:
        read_serial_data()
    except KeyboardInterrupt:
        # 关闭串口
        ser.close()
        print("Serial port closed.")
