import tkinter as tk
import threading
import All_gestures_recognition


class HarpApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#2D2D2D")
        self.root.title("Laser Harp")

        # 设置全屏
        self.root.attributes("-fullscreen", True)

        # 获取屏幕宽度和高度
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, width=self.screen_width, height=self.screen_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.select_option)
        self.root.bind("<Escape>", self.go_back)
        self.root.bind("<Delete>", self.exit_fullscreen)  # 绑定Delete键退出全屏

        self.page_history = []
        self.current_page = "Menu"
        self.menu_options = ["Free Play Mode", "Harp Hero", "Setting"]
        self.FPM_options = ["Harp", "Piano", "Guitar"]
        self.harphero_options = ["Select Song", "Select Difficulty"]
        self.setting_options = ["Volume", "Equipment Inspection"]
        self.current_selection = 0  # 这里后面循环选择要用

        # 设置按钮的宽度和高度
        self.button_width = 300
        self.button_height = 300
        self.button_spacing = 100  # 按钮之间的间距

        # 计算三个按钮的总宽度和起始x坐标，使其水平居中
        self.total_width1 = 3 * self.button_width + 2 * self.button_spacing
        self.start_x1 = (self.screen_width - self.total_width1) / 2
        self.start_x2 = self.start_x1 + self.button_width + self.button_spacing
        self.start_x3 = self.start_x1 + 2 * (self.button_width + self.button_spacing)

        # 计算两个按钮的总宽度和起始x坐标，使其水平居中
        self.total_width2 = 2 * self.button_width + self.button_spacing
        self.start_x4 = (self.screen_width - self.total_width2) / 2
        self.start_x5 = self.start_x4 + self.button_width + self.button_spacing

        # 垂直中心位置（稍微靠下，给标题留空间）
        self.y_position = (self.screen_height / 2) - 150

        self.create_menu_page()
        # 启动手势识别线程
        threading.Thread(target=self.start_gesture_recognition, daemon=True).start()


    def create_menu_page(self):
        self.page_history.clear()  # Clear history when returning to menu
        self.canvas.delete("all")
        self.current_page = "Menu"
        self.parent_page = "Menu"
        self.current_selection = 0

        # 添加一个标题
        self.title_label = tk.Label(self.canvas, text="Menu", font=("Comic Sans MS", 52, "bold"), bg="#F0F0F0")
        self.title_label_window = self.canvas.create_window(self.screen_width // 2, 100, window=self.title_label,anchor="n")  # 垂直居中对齐

        # 创建并放置按钮
        self.FPM_button = tk.Button(self.canvas, text="Free\nPlay\nMode", font=("Comic Sans MS", 34), bg="white", width=self.button_width, height=self.button_height)
        self.FPM_button_window = self.canvas.create_window(self.start_x1, self.y_position, window=self.FPM_button, anchor="nw", width=self.button_width, height=self.button_height)

        self.harphero_button = tk.Button(self.canvas, text="Harp\nHero", font=("Comic Sans MS", 34), bg="white", width=self.button_width, height=self.button_height)
        self.harphero_button_window = self.canvas.create_window(self.start_x2, self.y_position, window=self.harphero_button, anchor="nw", width=self.button_width, height=self.button_height)

        self.set_button = tk.Button(self.canvas, text="Setting", font=("Comic Sans MS", 34), bg="white", width=self.button_width, height=self.button_height)
        self.set_button_window = self.canvas.create_window(self.start_x3, self.y_position, window=self.set_button, anchor="nw", width=self.button_width, height=self.button_height)

        self.update_selection()

    def create_FPM_page(self):  # Create new page for Free Play Mode
        self.canvas.delete("all")
        self.current_page = "Free Play Mode"
        self.parent_page = "Menu"
        self.current_selection = 0

        self.title_label = tk.Label(self.canvas, text="Select your favourite instrument sound",font=("Comic Sans MS", 48, "bold"), bg="#F0F0F0")
        self.title_label_window = self.canvas.create_window(self.screen_width // 2, 100, window=self.title_label,anchor="n")  # 垂直居中对齐

        self.Laserharp_button = tk.Button(self.canvas, text="Laser harp", font=("Comic Sans MS", 34), bg="white", width=self.button_width, height=self.button_height)
        self.Laserharp_window = self.canvas.create_window(self.start_x1, self.y_position, window=self.Laserharp_button, anchor="nw", width=self.button_width, height=self.button_height)

        self.piano_button = tk.Button(self.canvas, text="Piano", font=("Comic Sans MS", 34), bg="white", width=self.button_width, height=self.button_height)
        self.piano_button_window = self.canvas.create_window(self.start_x2, self.y_position, window=self.piano_button, anchor="nw", width=self.button_width, height=self.button_height)

        self.guitar_button = tk.Button(self.canvas, text="Guitar", font=("Comic Sans MS", 34), bg="white", width=self.button_width, height=self.button_height)
        self.guitar_button_window = self.canvas.create_window(self.start_x3, self.y_position, window=self.guitar_button, anchor="nw", width=self.button_width, height=self.button_height)

        self.create_back_text()
        self.update_selection()

    def create_harphero_page(self):  # Create new page for harp
        self.canvas.delete("all")
        self.current_page = "Harp Hero"
        self.parent_page = "Menu"
        self.current_selection = 0

        self.title_label = tk.Label(self.canvas, text="Welcome to the Harp Hero!", font=("Comic Sans MS", 52, "bold"),bg="#F0F0F0")
        self.title_label_window = self.canvas.create_window(self.screen_width // 2, 100, window=self.title_label,anchor="n")  # 垂直居中对齐

        self.Song_button = tk.Button(self.canvas, text="Select\nthe\nSong", font=("Comic Sans MS", 34), bg="white", width=self.button_width, height=self.button_height)
        self.Song_button_window = self.canvas.create_window(self.start_x4, self.y_position, window=self.Song_button, anchor="nw", width=self.button_width, height=self.button_height)

        self.Difficulty_button = tk.Button(self.canvas, text="Select\nthe\nDifficulty", font=("Comic Sans MS", 34), bg="white", width=self.button_width, height=self.button_height)
        self.Difficulty_button_window = self.canvas.create_window(self.start_x5, self.y_position, window=self.Difficulty_button, anchor="nw", width=self.button_width, height=self.button_height)

        self.create_back_text()
        self.update_selection()

    def create_setting_page(self):  # Create new page for harp
        self.canvas.delete("all")
        self.current_page = "Setting"
        self.parent_page = "Menu"
        self.current_selection = 0

        self.title_label = tk.Label(self.canvas, text="Setting", font=("Comic Sans MS", 52, "bold"), bg="#F0F0F0")
        self.title_label_window = self.canvas.create_window(self.screen_width // 2, 100, window=self.title_label,anchor="n")  # 垂直居中对齐


        self.volume_button = tk.Button(self.canvas, text="Volume", font=("Comic Sans MS", 34), bg="white", width=self.button_width, height=self.button_height)
        self.volume_button_window = self.canvas.create_window(self.start_x4, self.y_position, window=self.volume_button, anchor="nw", width=self.button_width, height=self.button_height)

        self.Inspection_button = tk.Button(self.canvas, text="Equipment\nInspection", font=("Comic Sans MS", 34), bg="white", width=self.button_width, height=self.button_height)
        self.Inspection_button_window = self.canvas.create_window(self.start_x5, self.y_position, window=self.Inspection_button, anchor="nw", width=self.button_width, height=self.button_height)

        self.create_back_text()
        self.update_selection()

    def create_back_text(self):
        full_text = "'Clap' to go back to the last page"
        self.canvas.create_text(self.screen_width - 10, self.screen_height - 10, text=full_text,font=("Comic Sans MS", 22), fill="dark gray", anchor="se")

    # 左键功能
    def move_left(self, event):
        if self.current_page == "Menu":
            self.current_selection = (self.current_selection - 1) % len(self.menu_options)
        elif self.current_page == "Free Play Mode":
            self.current_selection = (self.current_selection - 1) % len(self.FPM_options)
        elif self.current_page == "Harp Hero":
            self.current_selection = (self.current_selection - 1) % len(self.harphero_options)
        elif self.current_page == "Setting":
            self.current_selection = (self.current_selection - 1) % len(self.setting_options)

        self.update_selection()

    def move_right(self, event):
        if self.current_page == "Menu":
            self.current_selection = (self.current_selection + 1) % len(self.menu_options)
        elif self.current_page == "Free Play Mode":
            self.current_selection = (self.current_selection + 1) % len(self.FPM_options)
        elif self.current_page == "Harp Hero":
            self.current_selection = (self.current_selection + 1) % len(self.harphero_options)
        elif self.current_page == "Setting":
            self.current_selection = (self.current_selection + 1) % len(self.setting_options)

        self.update_selection()

    def start_gesture_recognition(self):
        # 这里导入并运行手势识别程序
        All_gestures_recognition.read_serial_data(self.handle_gesture)  # 调用正确的函数

    # def start_inspection(self):    # 启动 Inspection 并将数据放入队列中
    #     Inspection.main(self.ser,self.data_queue)

    def handle_gesture(self, gesture):
        if gesture == "confirm":
            self.select_option(None)  # 调用空格键功能
        elif gesture == "Swipe right":
            self.move_right(None)  # 调用右键功能
        elif gesture == "Swipe left":
            self.move_left(None)  # 调用左键功能
        elif gesture == "Clap":
            self.go_back(None)

    # 空格键的选择功能
    def select_option(self, event):
        if self.current_page == "Menu":
            if self.current_selection == 0:
                self.create_FPM_page()
            elif self.current_selection == 1:
                self.create_harphero_page()
            elif self.current_selection == 2:
                self.create_setting_page()

        elif self.current_page == "Free Play Mode":
            if self.current_selection == 0:
                # self.create_harp_page()
                print("Harp")
            elif self.current_selection == 1:
                # self.create_guitar_page()
                print("Piano")
            elif self.current_selection == 2:
                # self.create_piano_page()
                print("Guitar")

        elif self.current_page == "Harp Hero":
            if self.current_selection == 0:
                # self.create_songselect_page()
                print("Select the song")
            elif self.current_selection == 1:
                # self.create_Difficulty_page()
                print("Select the difficulty")

        elif self.current_page == "Setting":
            if self.current_selection == 0:
                # self.create_volume_page()
                print("volume")
            elif self.current_selection == 1:
                print("Inspection")

    def update_selection(self):
        if self.current_page == "Menu":
            buttons = [self.FPM_button, self.harphero_button, self.set_button]
        elif self.current_page == "Free Play Mode":
            buttons = [self.Laserharp_button, self.piano_button, self.guitar_button]
        elif self.current_page == "Harp Hero":
            buttons = [self.Song_button, self.Difficulty_button]
        elif self.current_page == "Setting":
            buttons = [self.volume_button, self.Inspection_button]

        # 选中按钮的变色功能实现
        for i, button in enumerate(buttons):
            button.config(bg="lightgreen" if i == self.current_selection else "white")


    def go_back(self, event=None):
        if self.parent_page == "Menu":
            self.create_menu_page()

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)

if __name__ == "__main__":
    root = tk.Tk()
    app = HarpApp(root)
    root.mainloop()
