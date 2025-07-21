# Mobile Controller Example using FTC Python DSL
# Demonstrates custom mobile dashboard and advanced telemetry

@teleop("Mobile Controller", "Advanced")
class MobileControllerRobot:
    def init_hardware(self):
        # Drive system
        self.left_drive = motor("left_drive", "forward")
        self.right_drive = motor("right_drive", "reverse")
        self.front_left = motor("front_left", "forward")
        self.front_right = motor("front_right", "reverse")
        
        # Manipulator systems
        self.arm_motor = motor("arm_motor", "forward")
        self.wrist_servo = servo("wrist_servo")
        self.claw_servo = servo("claw_servo")
        self.lift_motor = motor("lift_motor", "forward")
        
        # Sensors
        self.distance_sensor = distance_sensor("distance")
        self.color_sensor = color_sensor("color")
        self.imu = imu("imu")
        self.touch_sensor = touch_sensor("limit_switch")
        
        # Initialize dashboard variables
        self.dashboard_config = self.init_dashboard()
        
        # Robot state variables
        self.drive_mode = "NORMAL"  # NORMAL, SLOW, TURBO
        self.arm_position = "HOME"  # HOME, LOW, MID, HIGH
        self.claw_state = "OPEN"    # OPEN, CLOSED
        self.auto_functions_enabled = True

    def init_dashboard(self):
        """Initialize FTC Dashboard configuration"""
        config = {
            "drive_speed_multiplier": 1.0,
            "turn_speed_multiplier": 0.8,
            "arm_speed_multiplier": 0.6,
            "precision_mode_multiplier": 0.3,
            "auto_align_enabled": True,
            "safety_distance_cm": 15.0,
            "telemetry_update_rate": 50  # ms
        }
        
        # Register dashboard variables
        dashboard_register("Drive Speed", config["drive_speed_multiplier"])
        dashboard_register("Turn Speed", config["turn_speed_multiplier"])
        dashboard_register("Arm Speed", config["arm_speed_multiplier"])
        dashboard_register("Precision Multiplier", config["precision_mode_multiplier"])
        dashboard_register("Auto Align", config["auto_align_enabled"])
        dashboard_register("Safety Distance", config["safety_distance_cm"])
        
        return config

    def run(self):
        # Initialize IMU
        self.imu.initialize()
        
        # Main control loop
        self.control_loop()

    def control_loop(self):
        """Main robot control loop with mobile dashboard integration"""
        loop_count = 0
        
        while opmode_is_active():
            # Update dashboard values
            self.update_dashboard_config()
            
            # Handle drive controls
            self.handle_drive_controls()
            
            # Handle manipulator controls
            self.handle_manipulator_controls()
            
            # Handle special functions
            self.handle_special_functions()
            
            # Update sensors and telemetry
            self.update_telemetry()
            
            # Auto functions
            if self.auto_functions_enabled:
                self.run_auto_functions()
            
            # Dashboard and telemetry update
            if loop_count % 5 == 0:  # Update every 5 loops
                self.update_mobile_dashboard()
            
            loop_count += 1
            sleep(20)  # 50Hz control loop

    def update_dashboard_config(self):
        """Update configuration from FTC Dashboard"""
        self.dashboard_config["drive_speed_multiplier"] = dashboard_get("Drive Speed")
        self.dashboard_config["turn_speed_multiplier"] = dashboard_get("Turn Speed")
        self.dashboard_config["arm_speed_multiplier"] = dashboard_get("Arm Speed")
        self.dashboard_config["precision_mode_multiplier"] = dashboard_get("Precision Multiplier")
        self.dashboard_config["auto_align_enabled"] = dashboard_get("Auto Align")
        self.dashboard_config["safety_distance_cm"] = dashboard_get("Safety Distance")

    def handle_drive_controls(self):
        """Handle drive system controls with multiple modes"""
        # Get raw gamepad inputs
        drive = -gamepad1.left_stick_y
        strafe = gamepad1.left_stick_x
        turn = gamepad1.right_stick_x
        
        # Apply speed multipliers based on mode
        speed_multiplier = self.get_drive_speed_multiplier()
        
        drive *= speed_multiplier
        strafe *= speed_multiplier
        turn *= speed_multiplier * self.dashboard_config["turn_speed_multiplier"]
        
        # Precision mode
        if gamepad1.right_bumper:
            precision_mult = self.dashboard_config["precision_mode_multiplier"]
            drive *= precision_mult
            strafe *= precision_mult
            turn *= precision_mult
            self.drive_mode = "PRECISION"
        
        # Apply mecanum drive
        self.mecanum_drive(drive, strafe, turn)

    def get_drive_speed_multiplier(self):
        """Get drive speed multiplier based on current mode"""
        if gamepad1.left_bumper:
            self.drive_mode = "TURBO"
            return self.dashboard_config["drive_speed_multiplier"] * 1.2
        elif gamepad1.left_trigger > 0.5:
            self.drive_mode = "SLOW"
            return self.dashboard_config["drive_speed_multiplier"] * 0.5
        else:
            self.drive_mode = "NORMAL"
            return self.dashboard_config["drive_speed_multiplier"]

    def handle_manipulator_controls(self):
        """Handle arm, wrist, and claw controls"""
        # Arm control
        arm_power = -gamepad2.left_stick_y * self.dashboard_config["arm_speed_multiplier"]
        
        # Safety limits
        if self.touch_sensor.is_pressed() and arm_power < 0:
            arm_power = 0  # Don't go down if limit switch pressed
        
        self.arm_motor.set_power(arm_power)
        
        # Preset arm positions
        if gamepad2.dpad_down:
            self.move_arm_to_position("HOME")
        elif gamepad2.dpad_left:
            self.move_arm_to_position("LOW")
        elif gamepad2.dpad_up:
            self.move_arm_to_position("MID")
        elif gamepad2.dpad_right:
            self.move_arm_to_position("HIGH")
        
        # Wrist control
        if gamepad2.left_bumper:
            self.wrist_servo.set_position(0.2)  # Wrist up
        elif gamepad2.left_trigger > 0.5:
            self.wrist_servo.set_position(0.8)  # Wrist down
        
        # Claw control
        if gamepad2.a_button:
            self.claw_servo.set_position(0.0)  # Open
            self.claw_state = "OPEN"
        elif gamepad2.b_button:
            self.claw_servo.set_position(1.0)  # Close
            self.claw_state = "CLOSED"
        
        # Lift control
        lift_power = -gamepad2.right_stick_y * 0.8
        self.lift_motor.set_power(lift_power)

    def move_arm_to_position(self, position):
        """Move arm to preset position"""
        positions = {
            "HOME": 0,
            "LOW": 500,
            "MID": 1000,
            "HIGH": 1500
        }
        
        if position in positions:
            target_position = positions[position]
            self.arm_motor.set_target_position(target_position)
            self.arm_motor.set_mode("run_to_position")
            self.arm_motor.set_power(0.5)
            self.arm_position = position

    def handle_special_functions(self):
        """Handle special functions and macros"""
        # Toggle auto functions
        if gamepad1.back:
            self.auto_functions_enabled = not self.auto_functions_enabled
            sleep(200)  # Debounce
        
        # Emergency stop
        if gamepad1.start and gamepad2.start:
            self.emergency_stop()
        
        # Auto-align to nearest object
        if gamepad1.y_button and self.dashboard_config["auto_align_enabled"]:
            self.auto_align_to_object()
        
        # Intake sequence
        if gamepad2.x_button:
            self.run_intake_sequence()
        
        # Scoring sequence
        if gamepad2.y_button:
            self.run_scoring_sequence()

    def run_auto_functions(self):
        """Run automatic safety and assistance functions"""
        # Obstacle avoidance
        distance = self.distance_sensor.get_distance()
        if distance < self.dashboard_config["safety_distance_cm"]:
            # Reduce forward drive power
            if gamepad1.left_stick_y < -0.1:  # Moving forward
                telemetry_add("Warning", "OBSTACLE DETECTED")
                # Could reduce motor power here
        
        # Auto-level using IMU
        if gamepad1.x_button:
            self.auto_level_robot()

    def auto_align_to_object(self):
        """Auto-align robot to nearest detected object"""
        telemetry_add("Status", "Auto-aligning...")
        
        # Simple alignment based on distance sensor
        distance = self.distance_sensor.get_distance()
        
        if distance < 50:  # Object detected within 50cm
            # Center the robot on the object
            # This is a simplified version - real implementation would use vision
            self.mecanum_drive(0, 0, 0.2)  # Slight turn
            sleep(200)
            self.mecanum_drive(0, 0, 0)    # Stop
        
        telemetry_add("Status", "Alignment complete")

    def auto_level_robot(self):
        """Auto-level robot using IMU"""
        # Get current robot orientation
        pitch = self.imu.get_pitch()
        roll = self.imu.get_roll()
        
        # Simple leveling - move to counteract tilt
        if abs(pitch) > 5:  # 5 degree threshold
            if pitch > 0:
                self.mecanum_drive(-0.2, 0, 0)  # Move backward
            else:
                self.mecanum_drive(0.2, 0, 0)   # Move forward
            
            sleep(100)
            self.mecanum_drive(0, 0, 0)  # Stop

    def run_intake_sequence(self):
        """Automated intake sequence"""
        telemetry_add("Sequence", "Running Intake")
        
        # Lower arm
        self.move_arm_to_position("LOW")
        sleep(1000)
        
        # Open claw
        self.claw_servo.set_position(0.0)
        self.claw_state = "OPEN"
        sleep(500)
        
        # Move forward slightly
        self.mecanum_drive(0.2, 0, 0)
        sleep(500)
        self.mecanum_drive(0, 0, 0)
        
        # Close claw
        self.claw_servo.set_position(1.0)
        self.claw_state = "CLOSED"
        sleep(500)
        
        # Raise arm
        self.move_arm_to_position("MID")
        
        telemetry_add("Sequence", "Intake Complete")

    def run_scoring_sequence(self):
        """Automated scoring sequence"""
        telemetry_add("Sequence", "Running Scoring")
        
        # Raise arm to high position
        self.move_arm_to_position("HIGH")
        sleep(1500)
        
        # Position wrist
        self.wrist_servo.set_position(0.3)
        sleep(500)
        
        # Move to scoring position
        self.mecanum_drive(0.15, 0, 0)
        sleep(800)
        self.mecanum_drive(0, 0, 0)
        
        # Release object
        self.claw_servo.set_position(0.0)
        self.claw_state = "OPEN"
        sleep(500)
        
        # Back away
        self.mecanum_drive(-0.2, 0, 0)
        sleep(500)
        self.mecanum_drive(0, 0, 0)
        
        # Return to home position
        self.move_arm_to_position("HOME")
        
        telemetry_add("Sequence", "Scoring Complete")

    def emergency_stop(self):
        """Emergency stop all motors"""
        self.left_drive.set_power(0)
        self.right_drive.set_power(0)
        self.front_left.set_power(0)
        self.front_right.set_power(0)
        self.arm_motor.set_power(0)
        self.lift_motor.set_power(0)
        
        telemetry_add("EMERGENCY", "ALL MOTORS STOPPED")

    def update_telemetry(self):
        """Update telemetry with sensor readings and robot state"""
        # Sensor readings
        distance = self.distance_sensor.get_distance()
        color = self.color_sensor.get_color()
        
        # IMU readings
        heading = self.imu.get_heading()
        pitch = self.imu.get_pitch()
        roll = self.imu.get_roll()
        
        # Motor positions
        arm_position = self.arm_motor.get_current_position()
        
        # Basic telemetry
        telemetry_add("Drive Mode", self.drive_mode)
        telemetry_add("Arm Position", self.arm_position)
        telemetry_add("Claw State", self.claw_state)
        telemetry_add("Distance (cm)", distance)
        telemetry_add("Heading", heading)
        telemetry_add("Auto Functions", self.auto_functions_enabled)

    def update_mobile_dashboard(self):
        """Update mobile dashboard with detailed information"""
        # Create dashboard packet
        dashboard_packet = {
            "robot_state": {
                "drive_mode": self.drive_mode,
                "arm_position": self.arm_position,
                "claw_state": self.claw_state,
                "auto_functions": self.auto_functions_enabled
            },
            "sensors": {
                "distance_cm": self.distance_sensor.get_distance(),
                "heading_deg": self.imu.get_heading(),
                "pitch_deg": self.imu.get_pitch(),
                "roll_deg": self.imu.get_roll(),
                "arm_encoder": self.arm_motor.get_current_position(),
                "limit_switch": self.touch_sensor.is_pressed()
            },
            "controls": {
                "gamepad1_connected": True,  # Simplified
                "gamepad2_connected": True,
                "drive_power": abs(gamepad1.left_stick_y),
                "turn_power": abs(gamepad1.right_stick_x)
            },
            "config": self.dashboard_config
        }
        
        # Send to dashboard
        dashboard_send_packet(dashboard_packet)

    def mecanum_drive(self, drive, strafe, turn):
        """Mecanum drive with power normalization"""
        front_left_power = drive + strafe + turn
        front_right_power = drive - strafe - turn
        back_left_power = drive - strafe + turn
        back_right_power = drive + strafe - turn
        
        # Normalize powers
        max_power = max(abs(front_left_power), abs(front_right_power), 
                       abs(back_left_power), abs(back_right_power))
        
        if max_power > 1.0:
            front_left_power /= max_power
            front_right_power /= max_power
            back_left_power /= max_power
            back_right_power /= max_power
        
        self.front_left.set_power(front_left_power)
        self.front_right.set_power(front_right_power)
        self.left_drive.set_power(back_left_power)
        self.right_drive.set_power(back_right_power)
