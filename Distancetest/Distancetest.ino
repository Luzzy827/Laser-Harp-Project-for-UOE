const int numSensors = 14;
const int sensors[numSensors] = {40,39,38,37,36,35,34,33,32,31,30,29,28,27};
const int trigPins[4] = { 47, 49, 51, 53 };
const int echoPins[4] = { 46, 48, 50, 52 };

long duration[4];
int distances[4];

void setup() {
  // 初始化串口通信
  Serial.begin(9600);

  // 初始化激光传感器引脚为输入
  for (int i = 0; i < numSensors; i++) {
    pinMode(sensors[i], INPUT);
  }
  
  // 初始化距离传感器Trigger引脚为输出，Echo引脚为输入
  for (int i = 0; i < 4; i++) {
    pinMode(trigPins[i], OUTPUT);
    pinMode(echoPins[i], INPUT);
  }
}

void loop() {
  String output = "";
  
  // 读取激光传感器的高低电平状态
  for (int i = 0; i < numSensors; i++) {
    int state = digitalRead(sensors[i]);
    output += String(state);
    if (i < numSensors - 1) {
      output += ","; // 用逗号分隔
    }
  }

  // 读取距离传感器的数据
  for (int i = 0; i < 4; i++) {
    distances[i] = measureDistance(trigPins[i], echoPins[i]);

    // 过滤掉无效数据
    if (distances[i] < 2 || distances[i] > 400) {
      distances[i] = -1;
    }
    
    output += "," + String(distances[i]);
  }

  // 输出数据到串口监视器
  Serial.println(output);

  delay(500); // 延时500毫秒
}

long measureDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000); // 增加超时，防止无限等待

  // 计算距离
  long distance = duration * 0.034 / 2;

  // 返回测量距离，单位为厘米
  return distance;
}




    