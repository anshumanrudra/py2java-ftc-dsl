# AprilTag Detection Example using FTC Python DSL
# Demonstrates computer vision with AprilTag detection

@autonomous("AprilTag Auto", "Vision")
class AprilTagDetectionRobot:
    def init_hardware(self):
        # Drive motors
        self.left_drive = motor("left_drive", "forward")
        self.right_drive = motor("right_drive", "reverse")
        self.front_left = motor("front_left", "forward")
        self.front_right = motor("front_right", "reverse")
        
        # Vision hardware
        self.webcam = webcam("Webcam 1")
        
        # Initialize AprilTag processor
        self.apriltag_processor = apriltag_processor()
        self.vision_portal = vision_portal(self.webcam, self.apriltag_processor)

    def init_apriltag(self):
        # Configure AprilTag detection
        apriltag_config = {
            "decimation": 2,
            "sigma": 0.0,
            "refine_edges": True,
            "tag_family": "TAG_36h11",
            "tag_library": "CENTER_STAGE"
        }
        self.apriltag_processor.configure(apriltag_config)

    def run(self):
        self.init_apriltag()
        
        # Wait for camera to initialize
        sleep(2000)
        
        # Main autonomous loop
        while opmode_is_active():
            detections = self.get_apriltag_detections()
            
            if detections:
                for detection in detections:
                    self.process_apriltag_detection(detection)
                    break  # Process first detection
            else:
                # Search for tags
                self.search_for_tags()
            
            sleep(50)  # Small delay

    def get_apriltag_detections(self):
        """Get current AprilTag detections"""
        return self.apriltag_processor.get_detections()

    def process_apriltag_detection(self, detection):
        """Process a detected AprilTag"""
        tag_id = detection.id
        
        # Get pose information
        x = detection.ftc_pose.x
        y = detection.ftc_pose.y
        z = detection.ftc_pose.z
        yaw = detection.ftc_pose.yaw
        pitch = detection.ftc_pose.pitch
        roll = detection.ftc_pose.roll
        
        # Get range and bearing
        range_distance = detection.ftc_pose.range
        bearing = detection.ftc_pose.bearing
        elevation = detection.ftc_pose.elevation
        
        # Telemetry
        telemetry_add("Tag ID", tag_id)
        telemetry_add("Range", range_distance)
        telemetry_add("Bearing", bearing)
        telemetry_add("X", x)
        telemetry_add("Y", y)
        telemetry_add("Z", z)
        
        # Navigate based on tag
        if tag_id == 1:
            self.navigate_to_tag_1(detection)
        elif tag_id == 2:
            self.navigate_to_tag_2(detection)
        elif tag_id == 3:
            self.navigate_to_tag_3(detection)

    def navigate_to_tag_1(self, detection):
        """Navigate to AprilTag ID 1 (Left position)"""
        range_distance = detection.ftc_pose.range
        bearing = detection.ftc_pose.bearing
        
        # Simple proportional control
        drive_power = self.calculate_drive_power(range_distance)
        turn_power = self.calculate_turn_power(bearing)
        
        # Apply powers
        self.mecanum_drive(drive_power, 0, turn_power)
        
        # Stop when close enough
        if range_distance < 12:  # 12 inches
            self.stop_all_motors()
            telemetry_add("Status", "Reached Tag 1")

    def navigate_to_tag_2(self, detection):
        """Navigate to AprilTag ID 2 (Center position)"""
        range_distance = detection.ftc_pose.range
        bearing = detection.ftc_pose.bearing
        
        drive_power = self.calculate_drive_power(range_distance)
        turn_power = self.calculate_turn_power(bearing)
        
        self.mecanum_drive(drive_power, 0, turn_power)
        
        if range_distance < 12:
            self.stop_all_motors()
            telemetry_add("Status", "Reached Tag 2")

    def navigate_to_tag_3(self, detection):
        """Navigate to AprilTag ID 3 (Right position)"""
        range_distance = detection.ftc_pose.range
        bearing = detection.ftc_pose.bearing
        
        drive_power = self.calculate_drive_power(range_distance)
        turn_power = self.calculate_turn_power(bearing)
        
        self.mecanum_drive(drive_power, 0, turn_power)
        
        if range_distance < 12:
            self.stop_all_motors()
            telemetry_add("Status", "Reached Tag 3")

    def search_for_tags(self):
        """Search for AprilTags by rotating"""
        telemetry_add("Status", "Searching for tags...")
        self.mecanum_drive(0, 0, 0.3)  # Slow rotation

    def calculate_drive_power(self, range_distance):
        """Calculate drive power based on distance to tag"""
        target_distance = 12.0  # Target distance in inches
        error = range_distance - target_distance
        
        # Simple proportional control
        kp = 0.02
        power = kp * error
        
        # Clamp power
        if power > 0.5:
            power = 0.5
        elif power < -0.5:
            power = -0.5
            
        return power

    def calculate_turn_power(self, bearing):
        """Calculate turn power based on bearing to tag"""
        # Simple proportional control for turning
        kp = 0.01
        power = kp * bearing
        
        # Clamp power
        if power > 0.3:
            power = 0.3
        elif power < -0.3:
            power = -0.3
            
        return power

    def mecanum_drive(self, drive, strafe, turn):
        """Mecanum drive function"""
        # Calculate individual motor powers
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
        
        # Set motor powers
        self.front_left.set_power(front_left_power)
        self.front_right.set_power(front_right_power)
        self.left_drive.set_power(back_left_power)
        self.right_drive.set_power(back_right_power)

    def stop_all_motors(self):
        """Stop all drive motors"""
        self.left_drive.set_power(0)
        self.right_drive.set_power(0)
        self.front_left.set_power(0)
        self.front_right.set_power(0)
