""" IMPORTS """

# Import the Controller logic for the Ping-Pong Tower
from PingPongTowerController import Controller


""" MAIN """

if __name__ == '__main__':

    # Set the correct COM port
    com_port = "COM5"

    # Instantiate the python controller
    controller = Controller(com_port)
    # Toggle printing or logging of controller
    controller.toggle_printing(True)
    controller.toggle_logging(False)

    # Set point for ball height in mm
    set_point = 1000 # [mm]

    while True:
        
        # Get the high of the ball in mm
        ball_height = controller.get_ball_height()
        # Optional printing
        print(f"Ball height: {ball_height} mm")
         
        # Set the PWM
        # TODO: use your own PID to calculate the PWM
        pwm = 50 # %
        
        # Set the power (PWM) of the fan
        controller.set_pwm(pwm)
