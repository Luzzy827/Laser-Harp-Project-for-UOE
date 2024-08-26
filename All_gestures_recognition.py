import serial
import time

# Configuring the Serial Port
ser = serial.Serial('COM8', 9600)  # Change the port according to the actual situation

# def is_increasing_sequence(sequence):
#     return all(earlier < later for earlier, later in zip(sequence, sequence[1:]))
#
# def is_decreasing_sequence(sequence):
#     return all(earlier > later for earlier, later in zip(sequence, sequence[1:]))


# def is_increasing_sequence(sequence):
#     return sequence[-1] > sequence[0]
#
# def is_decreasing_sequence(sequence):
#     return sequence[-1] < sequence[0]

def is_increasing_sequence(sequence, tolerance=1):
    violations = 0
    for earlier, later in zip(sequence, sequence[1:]):
        if earlier >= later:
            violations += 1
            if violations > tolerance:
                return False
    return True

def is_decreasing_sequence(sequence, tolerance=1):
    violations = 0
    for earlier, later in zip(sequence, sequence[1:]):
        if earlier <= later:
            violations += 1
            if violations > tolerance:
                return False
    return True



def is_clap(left_sequence, right_sequence, max_time_difference):
    if len(left_sequence) > 3 and len(right_sequence) > 3:
        left_pos, left_time = left_sequence[-1]
        right_pos, right_time = right_sequence[-1]

        # Check whether the key time is close
        if abs(left_time - right_time) <= max_time_difference:
            # Make sure the keys are approached from both ends
            prev_left_pos, _ = left_sequence[-2]
            prev_right_pos, _ = right_sequence[-2]
            if prev_left_pos < left_pos and prev_right_pos > right_pos:
                return True
    return False

def read_serial_data(callback):
    num_sensors = 14
    previous_states = [1] * num_sensors  # Initialised to HIGH
    current_states = [1] * num_sensors
    start_times = [0] * num_sensors  # Initialize the start time
    confirmation_confirmed = False  # Marks whether the gesture is a confirmation gesture or not
    trigger_sequence = []
    trigger_timestamps = []
    left_sequence = []
    right_sequence = []
    max_time_difference = 0.001
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
                        current_time = time.time()
                        if i >= num_sensors // 2:
                            right_sequence.append((i, current_time))
                        else:
                            left_sequence.append((i, current_time))
                        last_press_time = current_time

                    elif previous_states[i] == 0 and current_states[i] == 1:
                        # print(f"Pin {i + 2} released")
                        start_times[i] = 0  # Reset start time after laser release

                #-------------- Checking the "confirm" gesture----------------------------------------
                any_long_occlusion = any(
                    current_states[i] == 0 and (time.time() - start_times[i] > 2)
                    for i in range(num_sensors)
                )

                if any_long_occlusion and not confirmation_confirmed:
                    print("confirm")
                    callback("confirm")
                    confirmation_confirmed = True  # Ensure that "Confirm" is output only once.

                # If all lasers have been released, reset the confirmation status
                if all(state == 1 for state in current_states):
                    confirmation_confirmed = False

            # # Update the previous status
            previous_states = current_states[:]

            #--------- Check the swipe left and right gesture----------------------------------------
            if len(trigger_sequence) >= 8: #Prevent one swipe from triggering twice
                print(f"Press sequence: {trigger_sequence}")
                # print(f"Press timestamps: {trigger_timestamps}")
                if is_increasing_sequence(trigger_sequence):
                    print("Swipe from left to right")
                    callback("Swipe right")
                elif is_decreasing_sequence(trigger_sequence):
                    print("Swipe from right to left")
                    callback("Swipe left")

                # Clear the sequence to detect the next trigger direction
                trigger_sequence = []
                trigger_timestamps = []


            #-------Check the clap-------
            if is_clap(left_sequence, right_sequence, max_time_difference):
                print("Clap")
                callback("Clap")

                # reset
                trigger_sequence = []
                trigger_timestamps = []
                left_sequence = []
                right_sequence = []
                continue  # restart the cycle


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
