import serial
import time

# Configuring the Serial Port
ser = serial.Serial('COM8', 9600)  # Change the port according to the actual situation

# 初始化
last_distances = [None, None, None, None]  # Save the last distance measured by the four sensors
threshold = 5  # Threshold, which is used to determine whether the movement is up or down
last_valid_time = time.time()  # The last time valid distance data was recorded


def detect_gesture(current_distances):
    global last_valid_time

    valid_data_detected = False  # Mark whether there is valid data

    for i in range(4):  # Traverse the data from four range sensors
        distance = current_distances[i]
        last_distance = last_distances[i]

        # Process only when the distance is within the effective range
        if 5 < distance < 25:
            valid_data_detected = True  # Valid data detected
            if last_distance is not None:
                if abs(distance - last_distance) > threshold:
                    if distance > last_distance:
                        print(f"Sensor {i + 1}: up")
                    elif distance < last_distance:
                        print(f"Sensor {i + 1}: down")
            last_distances[i] = distance  # Updates the last measured distance only if the data is within a valid range

    # Update last_valid_time if there is valid data
    if valid_data_detected:
        last_valid_time = time.time()
    else:
        # Check if there is no valid data for more than 1 second
        if time.time() - last_valid_time > 1:
            # print("No valid data for 1 second, resetting sensor data.")
            last_distances[:] = [None, None, None, None]  # Reset the status of all sensors


def main():
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                data = line.split(",")

                # Convert received data to integers
                current_distances = [int(val) for val in data[-4:]]  # Read the last four are distance data

                # Detecting gestures
                detect_gesture(current_distances)

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
