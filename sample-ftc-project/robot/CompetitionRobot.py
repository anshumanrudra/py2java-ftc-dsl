# Competition Robot - Main TeleOp Robot for Competition
# Team: Sample FTC Team
# Season: 2024-2025

@teleop("Competition Robot", "Competition")
class CompetitionRobot:
    def init_hardware(self):
        # Drive system - Mecanum drive
        self.front_left = motor("front_left", "forward")
        self.front_right = motor("front_right", "reverse")
        self.back_left = motor("back_left", "forward")
        self.back_right = motor("back_right", "reverse")
        
        # Manipulator system
        self.arm_motor = motor("arm_motor", "forward")
        self.wrist_servo = servo("wrist_servo")
        self.claw_servo = servo("claw_servo")
        
        # Intake system
        self.intake_motor = motor("intake_motor", "forward")
        
        # Sensors
        self.distance_sensor = distance_sensor("distance")
        self.color_sensor = color_sensor("color")
        self.touch_sensor = touch_sensor("limit_switch")
        
        # Set motor modes
        self.front_left.set_mode("run_using_encoder")
        self.front_right.set_mode("run_using_encoder")
        self.back_left.set_mode("run_using_encoder")
        self.back_right.set_mode("run_using_encoder")
        self.arm_motor.set_mode("run_using_encoder")

    def run(self):
        self.main_loop()

    def main_loop(self):
        # Mecanum drive control
        drive = -gamepad1.left_stick_y
        strafe = gamepad1.left_stick_x
        turn = gamepad1.right_stick_x
        
        # Apply speed control
        speed_multiplier = 1.0
        if gamepad1.right_bumper:
            speed_multiplier = 0.3  # Precision mode
        elif gamepad1.left_bumper:
            speed_multiplier = 1.5  # Turbo mode
        
        drive = drive * speed_multiplier
        strafe = strafe * speed_multiplier
        turn = turn * speed_multiplier * 0.8  # Reduce turn sensitivity
        
        # Calculate mecanum drive powers
        front_left_power = drive + strafe + turn
        front_right_power = drive - strafe - turn
        back_left_power = drive - strafe + turn
        back_right_power = drive + strafe - turn
        
        # Normalize powers if any exceed 1.0
        max_power = max(abs(front_left_power), abs(front_right_power),
                       abs(back_left_power), abs(back_right_power))
        
        if max_power > 1.0:
            front_left_power = front_left_power / max_power
            front_right_power = front_right_power / max_power
            back_left_power = back_left_power / max_power
            back_right_power = back_right_power / max_power
        
        # Set drive motor powers
        self.front_left.set_power(front_left_power)
        self.front_right.set_power(front_right_power)
        self.back_left.set_power(back_left_power)
        self.back_right.set_power(back_right_power)
        
        # Arm control
        arm_power = -gamepad2.left_stick_y * 0.8
        
        # Safety limit - don't go down if limit switch pressed
        if self.touch_sensor.is_pressed() and arm_power < 0:
            arm_power = 0
        
        self.arm_motor.set_power(arm_power)
        
        # Preset arm positions
        if gamepad2.dpad_down:
            self.move_arm_to_position(0)      # Home position
        elif gamepad2.dpad_left:
            self.move_arm_to_position(500)    # Low position
        elif gamepad2.dpad_up:
            self.move_arm_to_position(1000)   # Mid position
        elif gamepad2.dpad_right:
            self.move_arm_to_position(1500)   # High position
        
        # Wrist control
        if gamepad2.left_bumper:
            self.wrist_servo.set_position(0.2)  # Wrist up
        elif gamepad2.left_trigger > 0.5:
            self.wrist_servo.set_position(0.8)  # Wrist down
        
        # Claw control
        if gamepad2.a_button:
            self.claw_servo.set_position(0.0)  # Open
        elif gamepad2.b_button:
            self.claw_servo.set_position(1.0)  # Close
        
        # Intake control
        intake_power = 0
        if gamepad2.right_bumper:
            intake_power = 1.0   # Intake
        elif gamepad2.right_trigger > 0.5:
            intake_power = -1.0  # Outtake
        
        self.intake_motor.set_power(intake_power)
        
        # Automated sequences
        if gamepad2.x_button:
            self.intake_sequence()
        elif gamepad2.y_button:
            self.scoring_sequence()
        
        # Safety features
        distance = self.distance_sensor.get_distance()
        if distance < 15 and drive > 0:  # Obstacle ahead while moving forward
            # Reduce forward power
            self.front_left.set_power(front_left_power * 0.3)
            self.front_right.set_power(front_right_power * 0.3)
            self.back_left.set_power(back_left_power * 0.3)
            self.back_right.set_power(back_right_power * 0.3)
            telemetry_add("Warning", "OBSTACLE DETECTED")
        
        # Telemetry
        telemetry_add("Drive", drive)
        telemetry_add("Strafe", strafe)
        telemetry_add("Turn", turn)
        telemetry_add("Speed Mode", self.get_speed_mode_name(speed_multiplier))
        telemetry_add("Arm Power", arm_power)
        telemetry_add("Arm Position", self.arm_motor.get_current_position())
        telemetry_add("Distance", distance)
        telemetry_add("Limit Switch", self.touch_sensor.is_pressed())

    def move_arm_to_position(self, target_position):
        """Move arm to preset position using encoders"""
        self.arm_motor.set_target_position(target_position)
        self.arm_motor.set_mode("run_to_position")
        self.arm_motor.set_power(0.6)

    def get_speed_mode_name(self, multiplier):
        """Get human-readable speed mode name"""
        if multiplier <= 0.5:
            return "PRECISION"
        elif multiplier >= 1.2:
            return "TURBO"
        else:
            return "NORMAL"

    def intake_sequence(self):
        """Automated intake sequence"""
        # Lower arm to intake position
        self.move_arm_to_position(200)
        sleep(1000)
        
        # Position wrist
        self.wrist_servo.set_position(0.7)
        sleep(500)
        
        # Open claw
        self.claw_servo.set_position(0.0)
        sleep(500)
        
        # Run intake
        self.intake_motor.set_power(1.0)
        sleep(1500)
        self.intake_motor.set_power(0)
        
        # Close claw
        self.claw_servo.set_position(1.0)
        sleep(500)
        
        # Raise arm
        self.move_arm_to_position(800)

    def scoring_sequence(self):
        """Automated scoring sequence"""
        # Raise arm to scoring position
        self.move_arm_to_position(1400)
        sleep(1500)
        
        # Position wrist for scoring
        self.wrist_servo.set_position(0.3)
        sleep(500)
        
        # Move forward slightly (if safe)
        distance = self.distance_sensor.get_distance()
        if distance > 20:
            self.front_left.set_power(0.2)
            self.front_right.set_power(0.2)
            self.back_left.set_power(0.2)
            self.back_right.set_power(0.2)
            sleep(800)
            
            # Stop
            self.front_left.set_power(0)
            self.front_right.set_power(0)
            self.back_left.set_power(0)
            self.back_right.set_power(0)
        
        # Release game element
        self.claw_servo.set_position(0.0)
        sleep(500)
        
        # Back away
        self.front_left.set_power(-0.3)
        self.front_right.set_power(-0.3)
        self.back_left.set_power(-0.3)
        self.back_right.set_power(-0.3)
        sleep(500)
        
        # Stop
        self.front_left.set_power(0)
        self.front_right.set_power(0)
        self.back_left.set_power(0)
        self.back_right.set_power(0)
        
        # Return arm to safe position
        self.move_arm_to_position(500)
