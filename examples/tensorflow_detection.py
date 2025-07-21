# TensorFlow Object Detection Example using FTC Python DSL
# Demonstrates machine learning object recognition

@autonomous("TensorFlow Auto", "Machine Learning")
class TensorFlowDetectionRobot:
    def init_hardware(self):
        # Drive motors
        self.left_drive = motor("left_drive", "forward")
        self.right_drive = motor("right_drive", "reverse")
        self.front_left = motor("front_left", "forward")
        self.front_right = motor("front_right", "reverse")
        
        # Arm and intake
        self.arm_motor = motor("arm_motor", "forward")
        self.intake_motor = motor("intake_motor", "forward")
        
        # Vision hardware
        self.webcam = webcam("Webcam 1")
        
        # Initialize TensorFlow processor
        self.tensorflow_processor = tensorflow_processor()
        self.vision_portal = vision_portal(self.webcam, self.tensorflow_processor)

    def init_tensorflow(self):
        """Initialize TensorFlow object detection"""
        # Configure TensorFlow model
        tf_config = {
            "model_asset_name": "PowerPlay.tflite",
            "model_labels": ["Bolt", "Bulb", "Panel"],
            "is_model_tensor_flow2": True,
            "is_model_quantized": True,
            "input_size": 300,
            "confidence_threshold": 0.7,
            "max_num_detections": 10
        }
        self.tensorflow_processor.configure(tf_config)

    def run(self):
        self.init_tensorflow()
        
        # Wait for camera and model to initialize
        sleep(3000)
        
        telemetry_add("Status", "TensorFlow initialized")
        
        # Main autonomous sequence
        self.autonomous_sequence()

    def autonomous_sequence(self):
        """Main autonomous sequence with object detection"""
        # Phase 1: Search for objects
        objects_found = self.search_for_objects()
        
        if objects_found:
            # Phase 2: Analyze detected objects
            target_object = self.analyze_objects(objects_found)
            
            if target_object:
                # Phase 3: Navigate to target object
                self.navigate_to_object(target_object)
                
                # Phase 4: Interact with object
                self.interact_with_object(target_object)
        
        # Phase 5: Complete autonomous
        self.complete_autonomous()

    def search_for_objects(self):
        """Search for objects using TensorFlow detection"""
        search_time = 0
        max_search_time = 10000  # 10 seconds
        
        while opmode_is_active() and search_time < max_search_time:
            detections = self.get_tensorflow_detections()
            
            if detections:
                telemetry_add("Objects Found", len(detections))
                return detections
            
            # Rotate to search
            self.mecanum_drive(0, 0, 0.2)
            sleep(100)
            search_time += 100
        
        # Stop searching
        self.stop_all_motors()
        telemetry_add("Status", "No objects found")
        return None

    def get_tensorflow_detections(self):
        """Get current TensorFlow detections"""
        return self.tensorflow_processor.get_recognitions()

    def analyze_objects(self, detections):
        """Analyze detected objects and choose target"""
        best_detection = None
        best_confidence = 0.0
        
        for detection in detections:
            label = detection.label
            confidence = detection.confidence
            
            telemetry_add(f"Object: {label}", f"Conf: {confidence:.2f}")
            
            # Prioritize certain objects
            priority_score = self.get_object_priority(label) * confidence
            
            if priority_score > best_confidence:
                best_confidence = priority_score
                best_detection = detection
        
        if best_detection:
            telemetry_add("Target Object", best_detection.label)
            telemetry_add("Target Confidence", best_detection.confidence)
        
        return best_detection

    def get_object_priority(self, label):
        """Get priority score for different objects"""
        priorities = {
            "Bolt": 1.0,      # Highest priority
            "Bulb": 0.8,      # Medium priority
            "Panel": 0.6      # Lower priority
        }
        return priorities.get(label, 0.5)

    def navigate_to_object(self, detection):
        """Navigate to the detected object"""
        # Get object position in image
        left = detection.left
        right = detection.right
        top = detection.top
        bottom = detection.bottom
        
        # Calculate object center
        center_x = (left + right) / 2
        center_y = (top + bottom) / 2
        
        # Image dimensions (typical webcam)
        image_width = 640
        image_height = 480
        
        # Calculate error from image center
        x_error = center_x - (image_width / 2)
        y_error = center_y - (image_height / 2)
        
        # Calculate object size (for distance estimation)
        object_width = right - left
        object_height = bottom - top
        object_area = object_width * object_height
        
        # Navigation control
        navigation_time = 0
        max_navigation_time = 5000  # 5 seconds
        
        while opmode_is_active() and navigation_time < max_navigation_time:
            # Get fresh detection
            current_detections = self.get_tensorflow_detections()
            current_detection = self.find_matching_detection(current_detections, detection.label)
            
            if current_detection:
                # Update position
                center_x = (current_detection.left + current_detection.right) / 2
                x_error = center_x - (image_width / 2)
                object_area = (current_detection.right - current_detection.left) * \
                             (current_detection.bottom - current_detection.top)
                
                # Calculate control signals
                turn_power = self.calculate_turn_from_x_error(x_error)
                drive_power = self.calculate_drive_from_area(object_area)
                
                # Apply control
                self.mecanum_drive(drive_power, 0, turn_power)
                
                # Check if close enough
                if object_area > 15000:  # Object is large enough (close)
                    break
            else:
                # Lost object, stop
                self.stop_all_motors()
                break
            
            sleep(50)
            navigation_time += 50
        
        self.stop_all_motors()
        telemetry_add("Status", "Navigation complete")

    def find_matching_detection(self, detections, target_label):
        """Find detection matching the target label"""
        if not detections:
            return None
        
        for detection in detections:
            if detection.label == target_label:
                return detection
        
        return None

    def calculate_turn_from_x_error(self, x_error):
        """Calculate turn power from horizontal error"""
        # Proportional control
        kp = 0.001
        turn_power = kp * x_error
        
        # Clamp power
        if turn_power > 0.3:
            turn_power = 0.3
        elif turn_power < -0.3:
            turn_power = -0.3
        
        return turn_power

    def calculate_drive_from_area(self, object_area):
        """Calculate drive power from object area (distance estimate)"""
        target_area = 15000  # Target object area
        
        if object_area < target_area:
            # Object is far, drive forward
            drive_power = 0.3
        else:
            # Object is close, slow down or stop
            drive_power = 0.0
        
        return drive_power

    def interact_with_object(self, detection):
        """Interact with the detected object"""
        object_label = detection.label
        
        telemetry_add("Interacting with", object_label)
        
        if object_label == "Bolt":
            self.collect_bolt()
        elif object_label == "Bulb":
            self.collect_bulb()
        elif object_label == "Panel":
            self.interact_with_panel()

    def collect_bolt(self):
        """Collect a bolt object"""
        telemetry_add("Action", "Collecting Bolt")
        
        # Lower arm
        self.arm_motor.set_power(-0.5)
        sleep(1000)
        self.arm_motor.set_power(0)
        
        # Run intake
        self.intake_motor.set_power(1.0)
        sleep(2000)
        self.intake_motor.set_power(0)
        
        # Raise arm
        self.arm_motor.set_power(0.5)
        sleep(1000)
        self.arm_motor.set_power(0)

    def collect_bulb(self):
        """Collect a bulb object"""
        telemetry_add("Action", "Collecting Bulb")
        
        # Similar to bolt but different timing
        self.arm_motor.set_power(-0.3)
        sleep(800)
        self.arm_motor.set_power(0)
        
        self.intake_motor.set_power(0.8)
        sleep(1500)
        self.intake_motor.set_power(0)
        
        self.arm_motor.set_power(0.3)
        sleep(800)
        self.arm_motor.set_power(0)

    def interact_with_panel(self):
        """Interact with a panel"""
        telemetry_add("Action", "Interacting with Panel")
        
        # Push against panel
        self.mecanum_drive(0.2, 0, 0)
        sleep(1000)
        self.stop_all_motors()

    def complete_autonomous(self):
        """Complete the autonomous routine"""
        telemetry_add("Status", "Autonomous Complete")
        
        # Return to starting position or park
        self.mecanum_drive(-0.3, 0, 0)  # Back up
        sleep(1000)
        self.stop_all_motors()

    def mecanum_drive(self, drive, strafe, turn):
        """Mecanum drive function"""
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

    def stop_all_motors(self):
        """Stop all motors"""
        self.left_drive.set_power(0)
        self.right_drive.set_power(0)
        self.front_left.set_power(0)
        self.front_right.set_power(0)
        self.arm_motor.set_power(0)
        self.intake_motor.set_power(0)
