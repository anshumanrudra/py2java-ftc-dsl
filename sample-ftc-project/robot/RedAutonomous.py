# Red Alliance Autonomous Program
# Team: Sample FTC Team
# Season: 2024-2025

@autonomous("Red Alliance Auto", "Competition")
class RedAutonomous:
    def init_hardware(self):
        # Drive system
        self.front_left = motor("front_left", "forward")
        self.front_right = motor("front_right", "reverse")
        self.back_left = motor("back_left", "forward")
        self.back_right = motor("back_right", "reverse")
        
        # Manipulator
        self.arm_motor = motor("arm_motor", "forward")
        self.claw_servo = servo("claw_servo")
        
        # Sensors
        self.distance_sensor = distance_sensor("distance")
        self.imu = imu("imu")
        
        # Vision (if available)
        self.webcam = webcam("Webcam 1")
        self.apriltag_processor = apriltag_processor()
        self.vision_portal = vision_portal(self.webcam, self.apriltag_processor)
        
        # Set motor modes for autonomous
        self.front_left.set_mode("stop_and_reset_encoder")
        self.front_right.set_mode("stop_and_reset_encoder")
        self.back_left.set_mode("stop_and_reset_encoder")
        self.back_right.set_mode("stop_and_reset_encoder")
        
        self.front_left.set_mode("run_using_encoder")
        self.front_right.set_mode("run_using_encoder")
        self.back_left.set_mode("run_using_encoder")
        self.back_right.set_mode("run_using_encoder")

    def run(self):
        # Initialize IMU
        self.imu.initialize()
        
        # Wait for vision to initialize
        sleep(2000)
        
        telemetry_add("Status", "Starting Red Alliance Autonomous")
        
        # Execute autonomous sequence
        self.autonomous_sequence()

    def autonomous_sequence(self):
        """Main autonomous sequence for red alliance"""
        
        # Phase 1: Pre-loaded game element scoring
        telemetry_add("Phase", "1 - Preload Scoring")
        self.score_preload()
        
        # Phase 2: Navigate to game elements
        telemetry_add("Phase", "2 - Navigate to Elements")
        self.navigate_to_game_elements()
        
        # Phase 3: Collect and score additional elements
        telemetry_add("Phase", "3 - Collect and Score")
        self.collect_and_score_elements()
        
        # Phase 4: Park in designated area
        telemetry_add("Phase", "4 - Parking")
        self.park_robot()
        
        telemetry_add("Status", "Autonomous Complete")

    def score_preload(self):
        """Score the pre-loaded game element"""
        # Raise arm to scoring position
        self.arm_motor.set_target_position(1200)
        self.arm_motor.set_mode("run_to_position")
        self.arm_motor.set_power(0.6)
        
        # Wait for arm to reach position
        sleep(1500)
        
        # Drive forward to scoring position
        self.drive_straight(24, 0.4)  # 24 inches forward
        
        # Score the element
        self.claw_servo.set_position(0.0)  # Open claw
        sleep(500)
        
        # Back away from scoring area
        self.drive_straight(-12, 0.4)  # 12 inches backward
        
        # Lower arm
        self.arm_motor.set_target_position(0)
        self.arm_motor.set_power(0.4)

    def navigate_to_game_elements(self):
        """Navigate to game element collection area"""
        # Turn towards game elements (90 degrees left for red alliance)
        self.turn_to_heading(-90)
        
        # Drive to collection area
        self.drive_straight(36, 0.5)  # 36 inches
        
        # Use vision to locate specific elements
        self.locate_game_elements_with_vision()

    def locate_game_elements_with_vision(self):
        """Use AprilTag vision to locate game elements"""
        search_time = 0
        max_search_time = 3000  # 3 seconds
        
        while opmode_is_active() and search_time < max_search_time:
            detections = self.apriltag_processor.get_detections()
            
            if detections:
                for detection in detections:
                    tag_id = detection.id
                    
                    # Look for specific tags (example: tags 1, 2, 3)
                    if tag_id >= 1 and tag_id <= 3:
                        telemetry_add("Found Tag", tag_id)
                        self.align_to_apriltag(detection)
                        return
            
            # Continue searching
            self.turn_robot(0.2)  # Slow turn to search
            sleep(100)
            search_time += 100
        
        # If no tags found, use dead reckoning
        telemetry_add("Vision", "No tags found, using dead reckoning")

    def align_to_apriltag(self, detection):
        """Align robot to detected AprilTag"""
        range_distance = detection.ftc_pose.range
        bearing = detection.ftc_pose.bearing
        
        # Turn to face the tag
        if abs(bearing) > 5:  # 5 degree tolerance
            turn_power = bearing * 0.01  # Proportional control
            self.turn_robot(turn_power)
            sleep(200)
        
        # Drive to optimal distance
        if range_distance > 18:  # Want to be 18 inches away
            drive_distance = range_distance - 18
            self.drive_straight(drive_distance, 0.3)

    def collect_and_score_elements(self):
        """Collect game elements and score them"""
        # Lower arm for collection
        self.arm_motor.set_target_position(200)
        self.arm_motor.set_mode("run_to_position")
        self.arm_motor.set_power(0.5)
        sleep(1000)
        
        # Open claw
        self.claw_servo.set_position(0.0)
        sleep(500)
        
        # Drive forward to collect element
        self.drive_straight(8, 0.2)  # Slow approach
        
        # Close claw to grab element
        self.claw_servo.set_position(1.0)
        sleep(500)
        
        # Raise arm
        self.arm_motor.set_target_position(800)
        self.arm_motor.set_power(0.6)
        sleep(1000)
        
        # Navigate back to scoring area
        self.turn_to_heading(0)  # Face forward
        self.drive_straight(30, 0.5)  # Drive to scoring area
        
        # Score the collected element
        self.arm_motor.set_target_position(1200)
        self.arm_motor.set_power(0.6)
        sleep(1000)
        
        self.claw_servo.set_position(0.0)  # Release
        sleep(500)

    def park_robot(self):
        """Park robot in designated parking area"""
        # Navigate to parking area (example: drive to corner)
        self.turn_to_heading(45)  # Turn towards parking area
        self.drive_straight(24, 0.4)  # Drive to parking spot
        
        # Lower arm to safe position
        self.arm_motor.set_target_position(0)
        self.arm_motor.set_power(0.3)
        
        telemetry_add("Status", "Parked Successfully")

    def drive_straight(self, distance_inches, power):
        """Drive straight for specified distance"""
        # Calculate encoder counts (example: 1120 counts per revolution, 4 inch wheels)
        counts_per_inch = 1120 / (4 * 3.14159)
        target_counts = int(distance_inches * counts_per_inch)
        
        # Reset encoders
        self.front_left.set_mode("stop_and_reset_encoder")
        self.front_right.set_mode("stop_and_reset_encoder")
        self.back_left.set_mode("stop_and_reset_encoder")
        self.back_right.set_mode("stop_and_reset_encoder")
        
        # Set target positions
        self.front_left.set_target_position(target_counts)
        self.front_right.set_target_position(target_counts)
        self.back_left.set_target_position(target_counts)
        self.back_right.set_target_position(target_counts)
        
        # Set to run to position mode
        self.front_left.set_mode("run_to_position")
        self.front_right.set_mode("run_to_position")
        self.back_left.set_mode("run_to_position")
        self.back_right.set_mode("run_to_position")
        
        # Set power
        self.front_left.set_power(power)
        self.front_right.set_power(power)
        self.back_left.set_power(power)
        self.back_right.set_power(power)
        
        # Wait for movement to complete
        while (opmode_is_active() and 
               (abs(self.front_left.get_current_position() - target_counts) > 10)):
            telemetry_add("Target", target_counts)
            telemetry_add("Current", self.front_left.get_current_position())
            sleep(50)
        
        # Stop motors
        self.front_left.set_power(0)
        self.front_right.set_power(0)
        self.back_left.set_power(0)
        self.back_right.set_power(0)

    def turn_to_heading(self, target_heading):
        """Turn robot to specific heading using IMU"""
        current_heading = self.imu.get_heading()
        error = target_heading - current_heading
        
        # Normalize error to -180 to 180 degrees
        while error > 180:
            error -= 360
        while error < -180:
            error += 360
        
        # Turn until within tolerance
        while opmode_is_active() and abs(error) > 2:  # 2 degree tolerance
            turn_power = error * 0.01  # Proportional control
            
            # Limit turn power
            if turn_power > 0.3:
                turn_power = 0.3
            elif turn_power < -0.3:
                turn_power = -0.3
            
            self.turn_robot(turn_power)
            
            sleep(50)
            current_heading = self.imu.get_heading()
            error = target_heading - current_heading
            
            # Normalize error
            while error > 180:
                error -= 360
            while error < -180:
                error += 360
            
            telemetry_add("Target Heading", target_heading)
            telemetry_add("Current Heading", current_heading)
            telemetry_add("Error", error)
        
        # Stop turning
        self.turn_robot(0)

    def turn_robot(self, turn_power):
        """Turn robot with specified power"""
        self.front_left.set_power(turn_power)
        self.front_right.set_power(-turn_power)
        self.back_left.set_power(turn_power)
        self.back_right.set_power(-turn_power)
