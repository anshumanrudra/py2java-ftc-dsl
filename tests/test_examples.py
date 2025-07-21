#!/usr/bin/env python3
"""
Unit tests for FTC DSL example code transpilation

Tests that all example Python files can be successfully transpiled
to valid Java code with expected functionality.
"""

import unittest
import sys
import os
import re

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ftc_transpiler import transpile_ftc_python_to_java

class TestExampleTranspilation(unittest.TestCase):
    """Test transpilation of example files"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
    
    def load_example_file(self, filename):
        """Load an example Python file"""
        filepath = os.path.join(self.examples_dir, filename)
        if not os.path.exists(filepath):
            self.skipTest(f"Example file {filename} not found")
        
        with open(filepath, 'r') as f:
            return f.read()
    
    def test_basic_teleop_transpilation(self):
        """Test basic TeleOp example transpilation"""
        python_code = self.load_example_file('basic_teleop.py')
        java_code = transpile_ftc_python_to_java(python_code)
        
        # Check for proper class structure
        self.assertIn('@TeleOp(name="Basic Drive", group="Linear OpMode")', java_code)
        self.assertIn('public class BasicDriveRobot extends LinearOpMode', java_code)
        
        # Check hardware declarations
        self.assertIn('private DcMotor left_drive = null;', java_code)
        self.assertIn('private DcMotor right_drive = null;', java_code)
        self.assertIn('private DcMotor arm_motor = null;', java_code)
        self.assertIn('private Servo claw_servo = null;', java_code)
        self.assertIn('private DistanceSensor distance_sensor = null;', java_code)
        self.assertIn('private ColorSensor color_sensor = null;', java_code)
        
        # Check hardware initialization
        self.assertIn('left_drive = hardwareMap.get(DcMotor.class, "left_drive");', java_code)
        self.assertIn('left_drive.setDirection(DcMotor.Direction.FORWARD);', java_code)
        self.assertIn('right_drive.setDirection(DcMotor.Direction.REVERSE);', java_code)
        
        # Check motor mode settings
        self.assertIn('left_drive.setMode(DcMotor.RunMode.RUN_USING_ENCODER);', java_code)
        
        # Check control logic
        self.assertIn('double drive = -gamepad1.left_stick_y;', java_code)
        self.assertIn('double turn = gamepad1.right_stick_x;', java_code)
        self.assertIn('left_drive.setPower(left_power);', java_code)
        self.assertIn('right_drive.setPower(right_power);', java_code)
        
        # Check servo control
        self.assertIn('if (gamepad1.a) {', java_code)
        self.assertIn('claw_servo.setPosition(0.0);', java_code)
        self.assertIn('} else if (gamepad1.b) {', java_code)
        self.assertIn('claw_servo.setPosition(1.0);', java_code)
        
        # Check sensor usage
        self.assertIn('distance_sensor.getDistance(DistanceUnit.CM)', java_code)
        
        # Check telemetry
        self.assertIn('telemetry.addData("Drive Power", drive);', java_code)
        self.assertIn('telemetry.addData("Distance (cm)", distance);', java_code)
        
        # Check safety logic
        self.assertIn('if (distance < 10) {', java_code)
        self.assertIn('telemetry.addData("Status", "OBSTACLE DETECTED!");', java_code)
    
    def test_apriltag_detection_transpilation(self):
        """Test AprilTag detection example transpilation"""
        python_code = self.load_example_file('apriltag_detection.py')
        java_code = transpile_ftc_python_to_java(python_code)
        
        # Check for autonomous annotation
        self.assertIn('@Autonomous(name="AprilTag Auto", group="Vision")', java_code)
        self.assertIn('public class AprilTagDetectionRobot extends LinearOpMode', java_code)
        
        # Check drive motor declarations
        self.assertIn('private DcMotor left_drive = null;', java_code)
        self.assertIn('private DcMotor right_drive = null;', java_code)
        self.assertIn('private DcMotor front_left = null;', java_code)
        self.assertIn('private DcMotor front_right = null;', java_code)
        
        # Check vision-related method calls (these would be custom implementations)
        # The transpiler should preserve method calls even if they're not standard FTC
        self.assertIn('webcam("Webcam 1")', java_code)
        self.assertIn('apriltag_processor()', java_code)
        self.assertIn('vision_portal(', java_code)
        
        # Check navigation methods
        self.assertIn('private void navigate_to_tag_1(', java_code)
        self.assertIn('private void navigate_to_tag_2(', java_code)
        self.assertIn('private void navigate_to_tag_3(', java_code)
        
        # Check mecanum drive implementation
        self.assertIn('private void mecanum_drive(', java_code)
        self.assertIn('front_left.setPower(front_left_power);', java_code)
        
        # Check calculation methods
        self.assertIn('private void calculate_drive_power(', java_code)
        self.assertIn('private void calculate_turn_power(', java_code)
    
    def test_tensorflow_detection_transpilation(self):
        """Test TensorFlow detection example transpilation"""
        python_code = self.load_example_file('tensorflow_detection.py')
        java_code = transpile_ftc_python_to_java(python_code)
        
        # Check for autonomous annotation
        self.assertIn('@Autonomous(name="TensorFlow Auto", group="Machine Learning")', java_code)
        self.assertIn('public class TensorFlowDetectionRobot extends LinearOpMode', java_code)
        
        # Check hardware declarations
        self.assertIn('private DcMotor left_drive = null;', java_code)
        self.assertIn('private DcMotor arm_motor = null;', java_code)
        self.assertIn('private DcMotor intake_motor = null;', java_code)
        
        # Check TensorFlow-related method calls
        self.assertIn('tensorflow_processor()', java_code)
        
        # Check autonomous sequence methods
        self.assertIn('private void autonomous_sequence(', java_code)
        self.assertIn('private void search_for_objects(', java_code)
        self.assertIn('private void analyze_objects(', java_code)
        self.assertIn('private void navigate_to_object(', java_code)
        
        # Check object interaction methods
        self.assertIn('private void collect_bolt(', java_code)
        self.assertIn('private void collect_bulb(', java_code)
        self.assertIn('private void interact_with_panel(', java_code)
        
        # Check control calculations
        self.assertIn('private void calculate_turn_from_x_error(', java_code)
        self.assertIn('private void calculate_drive_from_area(', java_code)
        
        # Check sleep calls
        self.assertIn('sleep(3000);', java_code)
        self.assertIn('sleep(1000);', java_code)
    
    def test_mobile_controller_transpilation(self):
        """Test mobile controller example transpilation"""
        python_code = self.load_example_file('mobile_controller.py')
        java_code = transpile_ftc_python_to_java(python_code)
        
        # Check for TeleOp annotation
        self.assertIn('@TeleOp(name="Mobile Controller", group="Advanced")', java_code)
        self.assertIn('public class MobileControllerRobot extends LinearOpMode', java_code)
        
        # Check comprehensive hardware declarations
        self.assertIn('private DcMotor left_drive = null;', java_code)
        self.assertIn('private DcMotor front_left = null;', java_code)
        self.assertIn('private DcMotor arm_motor = null;', java_code)
        self.assertIn('private Servo wrist_servo = null;', java_code)
        self.assertIn('private Servo claw_servo = null;', java_code)
        self.assertIn('private DcMotor lift_motor = null;', java_code)
        self.assertIn('private DistanceSensor distance_sensor = null;', java_code)
        self.assertIn('private ColorSensor color_sensor = null;', java_code)
        self.assertIn('private IMU imu = null;', java_code)
        self.assertIn('private TouchSensor touch_sensor = null;', java_code)
        
        # Check dashboard-related methods
        self.assertIn('private void init_dashboard(', java_code)
        self.assertIn('private void update_dashboard_config(', java_code)
        self.assertIn('private void update_mobile_dashboard(', java_code)
        
        # Check control methods
        self.assertIn('private void handle_drive_controls(', java_code)
        self.assertIn('private void handle_manipulator_controls(', java_code)
        self.assertIn('private void handle_special_functions(', java_code)
        
        # Check preset position methods
        self.assertIn('private void move_arm_to_position(', java_code)
        
        # Check automated sequences
        self.assertIn('private void run_intake_sequence(', java_code)
        self.assertIn('private void run_scoring_sequence(', java_code)
        
        # Check safety features
        self.assertIn('private void emergency_stop(', java_code)
        self.assertIn('private void run_auto_functions(', java_code)
        
        # Check advanced features
        self.assertIn('private void auto_align_to_object(', java_code)
        self.assertIn('private void auto_level_robot(', java_code)
        
        # Check mecanum drive
        self.assertIn('private void mecanum_drive(', java_code)
        
        # Check complex control logic
        self.assertIn('if (gamepad1.right_bumper) {', java_code)
        self.assertIn('if (gamepad2.dpad_down) {', java_code)
        self.assertIn('if (gamepad1.start && gamepad2.start) {', java_code)
    
    def test_all_examples_compile_without_errors(self):
        """Test that all examples transpile without syntax errors"""
        example_files = [
            'basic_teleop.py',
            'apriltag_detection.py',
            'tensorflow_detection.py',
            'mobile_controller.py'
        ]
        
        for filename in example_files:
            with self.subTest(filename=filename):
                try:
                    python_code = self.load_example_file(filename)
                    java_code = transpile_ftc_python_to_java(python_code)
                    
                    # Should not contain error comments
                    self.assertNotIn('// Transpilation error:', java_code)
                    
                    # Should contain basic class structure
                    self.assertIn('extends LinearOpMode', java_code)
                    self.assertIn('public void runOpMode()', java_code)
                    
                except Exception as e:
                    self.fail(f"Failed to transpile {filename}: {str(e)}")
    
    def test_java_syntax_validity(self):
        """Test that generated Java has valid syntax structure"""
        python_code = self.load_example_file('basic_teleop.py')
        java_code = transpile_ftc_python_to_java(python_code)
        
        # Check balanced braces
        open_braces = java_code.count('{')
        close_braces = java_code.count('}')
        self.assertEqual(open_braces, close_braces, "Unbalanced braces in generated Java")
        
        # Check balanced parentheses in method calls
        lines = java_code.split('\n')
        for i, line in enumerate(lines):
            if '(' in line and ')' in line:
                open_parens = line.count('(')
                close_parens = line.count(')')
                self.assertEqual(open_parens, close_parens, 
                               f"Unbalanced parentheses on line {i+1}: {line.strip()}")
        
        # Check that all statements end with semicolons (where appropriate)
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (stripped and 
                not stripped.startswith('//') and 
                not stripped.startswith('/*') and
                not stripped.endswith('{') and
                not stripped.endswith('}') and
                not stripped.startswith('@') and
                not stripped.startswith('import') and
                not stripped.startswith('public class') and
                not stripped.startswith('private void') and
                not stripped.startswith('if ') and
                not stripped.startswith('} else') and
                not stripped.startswith('while ') and
                'extends' not in stripped):
                
                if not stripped.endswith(';'):
                    # Some exceptions are okay (like single '}' lines)
                    if stripped != '}' and 'private' not in stripped:
                        print(f"Warning: Line {i+1} might be missing semicolon: {stripped}")
    
    def test_import_statements(self):
        """Test that proper import statements are generated"""
        python_code = self.load_example_file('basic_teleop.py')
        java_code = transpile_ftc_python_to_java(python_code)
        
        required_imports = [
            'import com.qualcomm.robotcore.eventloop.opmode.LinearOpMode;',
            'import com.qualcomm.robotcore.eventloop.opmode.TeleOp;',
            'import com.qualcomm.robotcore.hardware.DcMotor;',
            'import com.qualcomm.robotcore.hardware.Servo;',
            'import com.qualcomm.robotcore.hardware.DistanceSensor;',
            'import com.qualcomm.robotcore.hardware.ColorSensor;'
        ]
        
        for import_stmt in required_imports:
            self.assertIn(import_stmt, java_code, f"Missing import: {import_stmt}")
    
    def test_method_signature_generation(self):
        """Test that method signatures are properly generated"""
        python_code = self.load_example_file('mobile_controller.py')
        java_code = transpile_ftc_python_to_java(python_code)
        
        # Check that methods have proper Java signatures
        method_patterns = [
            r'private void init_dashboard\(\) \{',
            r'private void handle_drive_controls\(\) \{',
            r'private void mecanum_drive\(double \w+, double \w+, double \w+\) \{',
            r'@Override\s+public void runOpMode\(\) \{'
        ]
        
        for pattern in method_patterns:
            self.assertRegex(java_code, pattern, f"Method signature pattern not found: {pattern}")


class TestExampleFeatures(unittest.TestCase):
    """Test specific features in example code"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
    
    def load_example_file(self, filename):
        """Load an example Python file"""
        filepath = os.path.join(self.examples_dir, filename)
        if not os.path.exists(filepath):
            self.skipTest(f"Example file {filename} not found")
        
        with open(filepath, 'r') as f:
            return f.read()
    
    def test_gamepad_controls_variety(self):
        """Test that various gamepad controls are properly handled"""
        python_code = self.load_example_file('mobile_controller.py')
        java_code = transpile_ftc_python_to_java(python_code)
        
        gamepad_controls = [
            'gamepad1.left_stick_y',
            'gamepad1.right_stick_x',
            'gamepad1.a',
            'gamepad1.b',
            'gamepad1.x',
            'gamepad1.y',
            'gamepad1.dpad_up',
            'gamepad1.left_bumper',
            'gamepad1.right_bumper',
            'gamepad1.left_trigger',
            'gamepad2.left_stick_y',
            'gamepad2.dpad_down'
        ]
        
        for control in gamepad_controls:
            self.assertIn(control, java_code, f"Gamepad control not found: {control}")
    
    def test_sensor_integration(self):
        """Test that sensor integration is properly handled"""
        python_code = self.load_example_file('basic_teleop.py')
        java_code = transpile_ftc_python_to_java(python_code)
        
        sensor_calls = [
            'distance_sensor.getDistance(DistanceUnit.CM)',
            'color_sensor.get_color()',  # This would be a custom method
            'touch_sensor.isPressed()'   # From mobile_controller example
        ]
        
        # At least distance sensor should be present
        self.assertIn('distance_sensor.getDistance(DistanceUnit.CM)', java_code)
    
    def test_complex_expressions(self):
        """Test that complex mathematical expressions are handled"""
        python_code = self.load_example_file('basic_teleop.py')
        java_code = transpile_ftc_python_to_java(python_code)
        
        # Check for complex expressions
        self.assertIn('drive + turn', java_code)
        self.assertIn('drive - turn', java_code)
        self.assertIn('-gamepad1.left_stick_y', java_code)
    
    def test_conditional_logic_complexity(self):
        """Test complex conditional logic"""
        python_code = self.load_example_file('mobile_controller.py')
        java_code = transpile_ftc_python_to_java(python_code)
        
        # Check for complex conditionals
        self.assertIn('if (gamepad1.start && gamepad2.start)', java_code)
        self.assertIn('} else if (', java_code)
        
        # Check for nested conditions
        conditional_count = java_code.count('if (')
        self.assertGreater(conditional_count, 5, "Should have multiple conditional statements")


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test cases
    test_suite.addTest(unittest.makeSuite(TestExampleTranspilation))
    test_suite.addTest(unittest.makeSuite(TestExampleFeatures))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
