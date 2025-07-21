# Example FTC Robot using Python DSL
# This will be transpiled to Java for FTC

@teleop("Basic Drive", "Linear OpMode")
class BasicDriveRobot:
    def init_hardware(self):
        # Initialize motors
        self.left_drive = motor("left_drive", "forward")
        self.right_drive = motor("right_drive", "reverse")
        self.arm_motor = motor("arm_motor", "forward")
        
        # Initialize servos
        self.claw_servo = servo("claw_servo")
        
        # Initialize sensors
        self.distance_sensor = distance_sensor("distance")
        self.color_sensor = color_sensor("color")
        
        # Set motor modes
        self.left_drive.set_mode("run_using_encoder")
        self.right_drive.set_mode("run_using_encoder")
        self.arm_motor.set_mode("run_using_encoder")

    def run(self):
        self.loop()

    def loop(self):
        # Get gamepad input
        drive = -gamepad1.left_stick_y
        turn = gamepad1.right_stick_x
        arm_power = gamepad2.left_stick_y
        
        # Calculate motor powers
        left_power = drive + turn
        right_power = drive - turn
        
        # Set motor powers
        self.left_drive.set_power(left_power)
        self.right_drive.set_power(right_power)
        self.arm_motor.set_power(arm_power)
        
        # Servo control
        if gamepad1.a_button:
            self.claw_servo.set_position(0.0)  # Open
        elif gamepad1.b_button:
            self.claw_servo.set_position(1.0)  # Close
        
        # Sensor readings
        distance = self.distance_sensor.get_distance()
        
        # Telemetry
        telemetry_add("Drive Power", drive)
        telemetry_add("Turn Power", turn)
        telemetry_add("Distance (cm)", distance)
        
        # Safety check
        if distance < 10:
            self.left_drive.set_power(0)
            self.right_drive.set_power(0)
            telemetry_add("Status", "OBSTACLE DETECTED!")
