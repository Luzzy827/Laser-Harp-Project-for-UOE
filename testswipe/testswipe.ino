const int numSensors = 14;
const int sensors[numSensors] = {40,39,38,37,36,35,34,33,32,30,29,28,27};

void setup() {
  // 初始化串口通信
  Serial.begin(9600);

  // 初始化激光传感器引脚为输入
  for (int i = 0; i < numSensors; i++) {
    pinMode(sensors[i], INPUT);
  }
}

void loop() {
  // 用于存储每个引脚的状态
  String output = "";

  // 读取激光传感器的高低电平状态
  for (int i = 0; i < numSensors; i++) {
    int state = digitalRead(sensors[i]);
    output += String(state);
    
    // 如果不是最后一个引脚，则在状态之间添加逗号
    if (i < numSensors-1) {
      output += ",";
    }
  }

  // 输出状态
  Serial.println(output);

  // 等待一段时间再进行下一次读取
  delay(10);
}
