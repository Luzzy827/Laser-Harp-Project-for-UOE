import serial
import time

# Configuring the Serial Port
ser = serial.Serial('COM8', 9600)  # Change the port according to the actual situation

def is_increasing_sequence(sequence):
    return all(earlier < later for earlier, later in zip(sequence, sequence[1:]))

def is_decreasing_sequence(sequence):
    return all(earlier > later for earlier, later in zip(sequence, sequence[1:]))

def read_serial_data():
    num_sensors = 14
    previous_states = [1] * num_sensors  # Initialised to HIGH
    current_states = [1] * num_sensors
    start_times = [0] * num_sensors  # Initialize the start time
    confirmation_confirmed = False  # Marks whether the gesture is a confirmation gesture or not
    trigger_sequence = []
    trigger_timestamps = []
    last_trigger_time = time.time()

    while True:
        if ser.in_waiting:
            # Read a line of data from the serial port
            line = ser.readline().decode('utf-8').strip()

            # Checks if the line is empty
            if not line:
                continue

                # Split data into lists and convert to integers
            try:
                data = list(map(int, line.split(',')))
            except ValueError:
                print("Invalid data received:", line)
                continue

                # Make sure the data length is correct
            if len(data) == num_sensors:
                current_states = data

                # Detects triggers and releases
                for i in range(num_sensors):
                    if previous_states[i] == 1 and current_states[i] == 0:
                        # print(f"Pin {i + 2} triggered")
                        trigger_sequence.append(i)  # Add the triggered laser index to the list
                        trigger_timestamps.append(time.time())  # Record timestamps for each trigger time
                        last_trigger_time = time.time()  # Update last trigger time
                        start_times[i] = time.time()  # Record trigger time

                    elif previous_states[i] == 0 and current_states[i] == 1:
                        # print(f"Pin {i + 2} released")
                        start_times[i] = 0  # Reset start time after laser release

                #-------------- Checking the "confirm" gesture----------------------------------------
                any_long_occlusion = any(
                    current_states[i] == 0 and (time.time() - start_times[i] > 1)
                    for i in range(num_sensors)
                )

                if any_long_occlusion and not confirmation_confirmed:
                    print("confirm")
                    confirmation_confirmed = True  # Ensure that "Confirm" is output only once.

                # If all lasers have been released, reset the confirmation status
                if all(state == 1 for state in current_states):
                    confirmation_confirmed = False

            # # Update the previous status
            previous_states = current_states[:]

            #--------- Check the swipe left and right gesture----------------------------------------
            if len(trigger_sequence) >= 8: #Prevent one swipe from triggering twice
                print(f"Press sequence: {trigger_sequence}")
                print(f"Press timestamps: {trigger_timestamps}")
                if is_increasing_sequence(trigger_sequence):
                    print("Swipe from right to left")
                elif is_decreasing_sequence(trigger_sequence):
                    print("Swipe from left to right")

                # Clear the sequence to detect the next trigger direction
                trigger_sequence = []
                trigger_timestamps = []


            #---------- Checking for timeouts------------------------------------
            current_time = time.time()
            if current_time - last_trigger_time > 3:
                # print("Timeout, clearing press sequence")
                trigger_sequence = []
                trigger_timestamps = []

if __name__ == '__main__':
    try:
        read_serial_data()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ser.close()
        print("Serial port closed.")