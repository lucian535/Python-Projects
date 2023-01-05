'''
Program which runs in a infinite loop which takes in data from a distance sensor which activates motor actuators through a raspberry pi

more information of this project may be found on the notion protfiolio linked in the readme
'''

# Import Libraries
from sensor_library import * 
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory # Imports the library to control the motors more efficiently
import time
import sys

# Initiate the distance sensor and the motors
factory = PiGPIOFactory() # Initializing a variable to control the motors

sensor = Distance_Sensor() 

door_motor = Servo(8, pin_factory=factory) # Initializes the servo motors with pigpio
shelf_motor = Servo(14, pin_factory=factory)

# Sets the initial position of the door and the shelf to be in the closed position
door_motor.min()
shelf_motor.min()


''' Function Definitions '''

# Function to collect input data
def input_data():
    default_val = 8190 # Maximum distance that the distance sensor reads in mm (8.19m)
    thres_dist = 150 # Threshold distance that we determined based on the height of the housing 
    dist = sensor.distance() # Collects the distance in mm

    # Collect input data from distance sensors
    if dist < thres_dist: # Checks to see if the distance sensed is within the threshold value to return appropriate number or else it returns a default value
        return dist
    else:
        return default_val

# Function to calculate the rolling average of the 15 most recent data points collected
def calc_roll_avg(input_data, current_data_list):
    list_length = 10
        
    if len(current_data_list) >= list_length: # Removes the oldest data point inside the list in place for the latest
        current_data_list.remove(current_data_list[0])
        current_data_list.append(input_data)
        roll_avg = sum(current_data_list)/len(current_data_list) # Calculates the rolling average
        roll_avg = round(roll_avg, 2) # Rounds the roll_avg variable to 2 decimal places
        
    else: # Will add values into the data list if the length of the data list is less than 15
        current_data_list.append(input_data)
        roll_avg = None

    return roll_avg, current_data_list

# Function to activate the door motors
def activate_door_motor(state, roll_avg, thres_val):
    if roll_avg <= thres_val: # Checks if rolling average calculated is less than the assigned threshold value
        if not state: # If the door_is_open variable is False, it will open the door
            door_motor.max()
        else: # If the door_is_open variable is True, it will close the door
            door_motor.min()

# Function to activate the shelf motors
def activate_shelf_motor(state, roll_avg, thres_val):
    if roll_avg <= thres_val: # Process to compare rolling average to the threshold value
        if not state: # Drops shelf if door_is_open is False
            shelf_motor.max()
        else: # Retracts shelf if door_is_open is True
            shelf_motor.min()

# Function to print which the current function and the current motors working
def print_action(state, obj, roll_avg, thres_val):
    
    msg = '=================================\n' # Text to aid in neater prints
    
    if roll_avg <= thres_val:
        if not state:
            if obj == 'Door':
                print(msg + 'Opening Door\n' + 'Door Motor Active\n' + msg)
            elif obj == 'Shelf':
                print(msg + 'Dropping Shelf\n' + 'Shelf Motor Active\n' + msg)
        else:
            if obj == 'Door':
                print(msg + 'Closing Door\n' + 'Door Motor Active\n' + msg)
            elif obj == 'Shelf':
                print(msg + 'Retracting Shelf\n' + 'Shelf Motor Active\n' + msg)
        time.sleep(4) # Waits 4 seconds for ample time for doors or shelfs to move
        
# Function to print the state of the machine, whether it is ready to accept inputs or not
def print_status(idle, roll_avg, thres_val):
    if idle:
        print('~~~~~~~~~~~~~ READY ~~~~~~~~~~~~~')
    else:
        if roll_avg <= thres_val:
            print('~~~~~~~~~~~~ IN  USE ~~~~~~~~~~~~')
        
# Function to change the state of the contraption ie. if the shelf is in the open or closed position
def change_state(state, roll_avg, thres_val):
    if roll_avg <= thres_val:
        if state:
            return False
        elif not state:
            return True
    else:
        return state

# Function to detect false inputs from the sensor ie. distance points <= 15mm
def false_detection(roll_avg, datalist, threshold):
    second_list = datalist.copy() # Copies the initial data list to have a raw unedited list
    counter = 0 # Initializes a counter variable
    false_detect_thres = 15

    # For loop to count how many inputs <= 15mm are in the raw data list
    for i in datalist:
        if i <= false_detect_thres:
            counter += 1
            
    # If statement to check if there is one data point that is out of line and removes it from the list for correction        
    if counter == 1 and roll_avg <= threshold:
        for i in range(len(datalist)):
            if datalist[i-1] <= false_detect_thres:

                # Prints that a false input was detected with the associated distance sensed
                print('#################################################')
                print(f'false Input Detected, distance: {datalist[i-1]}')
                print('#################################################')
                
                datalist.remove(datalist[i-1]) # Removes the false input

        return True, datalist, second_list # Returns the decision if a false input was made, the edited data list and the raw data_list
    else: # If the counter > 1 (ie. 2), it is assumed that the input is not accidental and it is intentional
        return False, datalist, second_list 
            

# Function to print the set of data collected regarding the status of the outputs
def print_data(current_data_list, roll_avg, idle, motor_status, false_detect):
    print(f'{current_data_list[-1]}\t\t{roll_avg}\t\t{idle}\t\t{false_detect}\t\t{motor_status}\t\t{motor_status}')


''' Main function definition '''
# Main function
def main():
    threshold_roll_avg = 69 # Sets an initial arbitrary rolling average threshold value
    roll_avg = 0 # Initializes the rolling average variable to initially be 0 to aid in print statements
    idle = True # Sets the idle variable to True, meaning it is able to accept inputs
    current_data_list = [] # Initializes the raw data list variable
    
    door_is_open = False # Sets the door is open variable to initially be false (ie. cabinet is in closed position)
    false_detect = False # Sets False detect to initially be false

    print_status(idle, roll_avg, threshold_roll_avg) # Prints the status of the contraption (ie. ready to accept data)

    print('Distance (raw)\tDistance (avg)\tReady Sensor\tFalse Detection\tDoor Motor\tShelf Motor') # Prints the heading

    # Initializes the obj1 and obj2 variables to aid in print statements
    obj1 = 'Door'
    obj2 = 'Shelf'

    # Initially sets the status of both motors to be off
    motor_status = 'Off'

    # While True loop to continuosly input data
    run = True
    while run:
        newdata = input_data() # Calls the input data function to collect data from the distance sensor
        roll_avg, current_data_list = calc_roll_avg(newdata, current_data_list) # Calculates the rolling average and returns the roll_avg and the raw data list

        # If statement to check if roll_avg is an actual number
        if roll_avg != None:

            # Calls the false detection function to determine whether or not the most recent data point is deemed to be a false detection and corrects itself
            false_detect, current_data_list, second_list = false_detection(roll_avg, current_data_list, threshold_roll_avg)

            if not false_detect: # If statement to work when the input is deemed to be intentional
                if not door_is_open: # Checks if the status of the shelf is in the closed position

                    if roll_avg <= threshold_roll_avg: # Checks rolling average to print the new status with motors in the on position
                        idle = False

                        motor_status = 'On' # Sets motor status to be in the ON state
                        print_data(current_data_list, roll_avg, idle, motor_status, false_detect) # Prints the data
                        motor_status = 'Off' # Resets the motor status to b in the OFF state
                        
                        print_status(idle, roll_avg, threshold_roll_avg) # Prints that the shelf is currently in use
                    else:
                        print_data(current_data_list, roll_avg, idle, motor_status, false_detect) # If the roll_avg <= threshold rolling average value, prints the default data
                        
                    activate_door_motor(door_is_open, roll_avg, threshold_roll_avg) # Calls the function to activate the motor that controls the door

                    print_action(door_is_open, obj1, roll_avg, threshold_roll_avg) # Prints the action of the door and the activation of the motor
                    
                    activate_shelf_motor(door_is_open, roll_avg, threshold_roll_avg) # Calls the function to activate the shelf motors

                    print_action(door_is_open, obj2, roll_avg, threshold_roll_avg) # Prints the action of the shelf motor and activation of the motor
                    
                    # Calls the change state function to change the state of the shelf to open (ie door_is_open = True)
                    if change_state(door_is_open, roll_avg, threshold_roll_avg):
                        door_is_open = True # Changes the state
                        current_data_list.clear() # Clears the raw data list to collect new data points
                        idle = True # Sets idle to be true
                        print_status(idle, roll_avg, threshold_roll_avg) # Prints that the shelf is ready to accept data
                        print('Distance (raw)\tDistance (avg)\tReady Sensor\tFalse Detection\tDoor Motor\tShelf Motor')
                    
                
                elif door_is_open: # Checks to see if the cabinet is in the open position
                    if roll_avg <= threshold_roll_avg: # Check if the rolling average is less than the threshold rolling average value
                        idle = False # Changes Idle to be false
                            
                        motor_status = 'On' # Changes the motor status to On
                        print_data(current_data_list, roll_avg, idle, motor_status, false_detect) # Prints the new data
                        motor_status = 'Off' # Sets the motor_status to be Off

                        print_status(idle, roll_avg, threshold_roll_avg) # Prints that the machine is in use (not able to accept data)
                    else: 
                        print_data(current_data_list, roll_avg, idle, motor_status, false_detect) # Prints the original data points
                        
                    activate_shelf_motor(door_is_open, roll_avg, threshold_roll_avg) # Calls the function to activate the shelf motor to retract

                    print_action(door_is_open, obj2, roll_avg, threshold_roll_avg) # Prints the action of the shelf motor and the status of the motor
                        
                    activate_door_motor(door_is_open, roll_avg, threshold_roll_avg) # Calls the function to activate the door motor and closes the door

                    print_action(door_is_open, obj1, roll_avg, threshold_roll_avg) # Prints the action of the door motor and teh status of the motor
                    
                    # Calls the change state function to determine if the state of the door needs to be changed in regards to rolling average 
                    if not change_state(door_is_open, roll_avg, threshold_roll_avg):
                        door_is_open = False # Changes the state of the contraption to Closed
                        current_data_list.clear() # Clears the list of data to collect new raw data
                        idle = True # Sets idle to be True
                        print_status(idle, roll_avg, threshold_roll_avg) # Prints that the sensor is ready to collect more data
                        print('Distance (raw)\tDistance (avg)\tReady Sensor\tFalse Detection\tDoor Motor\tShelf Motor')
                        
            elif false_detect: # If a false detection has occured
                roll_avg = round(sum(current_data_list)/len(current_data_list), 2)
                print_data(second_list, roll_avg, idle, motor_status, false_detect) # It will print data with the latest data point that was a false detection
                
                        
        else:
            print_data(current_data_list, roll_avg, idle, motor_status, false_detect) #Prints the data
            
        time.sleep(0.05) # Waits 0.05 seconds delay between inputting more data,to ensure that the collected data is accurate

''' Call main function '''
main()


