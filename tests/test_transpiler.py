#!/usr/bin/env python3
"""
Unit tests for FTC DSL Python-to-Java Transpiler

Tests the core functionality of the transpiler including:
- Basic syntax conversion
- Hardware component handling
- OpMode generation
- Expression translation
- Error handling
"""

import unittest
import sys
import os
import ast
from unittest.mock import patch, mock_open

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ftc_transpiler import FTCTranspiler, transpile_ftc_python_to_java, OpModeType

class TestFTCTranspiler(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.transpiler = FTCTranspiler()
    
    def test_basic_class_creation(self):
        """Test basic class structure generation"""
        python_code = '''
@teleop("Test Robot", "Test Group")
class TestRobot:
    def run(self):
        pass
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        self.assertIn('@TeleOp(name="Test Robot", group="Test Group")', java_code)
        self.assertIn('public class TestRobot extends LinearOpMode', java_code)
        self.assertIn('@Override', java_code)
        self.assertIn('public void runOpMode()', java_code)
    
    def test_autonomous_decorator(self):
        """Test autonomous OpMode decorator"""
        python_code = '''
@autonomous("Auto Robot", "Auto Group")
class AutoRobot:
    def run(self):
        pass
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        self.assertIn('@Autonomous(name="Auto Robot", group="Auto Group")', java_code)
    
    def test_hardware_component_declaration(self):
        """Test hardware component declarations"""
        python_code = '''
@teleop("Hardware Test", "Test")
class HardwareRobot:
    def init_hardware(self):
        self.left_motor = motor("left_drive", "forward")
        self.right_motor = motor("right_drive", "reverse")
        self.test_servo = servo("test_servo")
        self.distance = distance_sensor("distance")
    
    def run(self):
        pass
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        # Check hardware declarations
        self.assertIn('private DcMotor left_motor = null;', java_code)
        self.assertIn('private DcMotor right_motor = null;', java_code)
        self.assertIn('private Servo test_servo = null;', java_code)
        self.assertIn('private DistanceSensor distance = null;', java_code)
        
        # Check hardware initialization
        self.assertIn('left_motor = hardwareMap.get(DcMotor.class, "left_drive");', java_code)
        self.assertIn('left_motor.setDirection(DcMotor.Direction.FORWARD);', java_code)
        self.assertIn('right_motor.setDirection(DcMotor.Direction.REVERSE);', java_code)
    
    def test_motor_control_methods(self):
        """Test motor control method translation"""
        python_code = '''
@teleop("Motor Test", "Test")
class MotorRobot:
    def init_hardware(self):
        self.motor = motor("test_motor", "forward")
    
    def run(self):
        self.loop()
    
    def loop(self):
        self.motor.set_power(0.5)
        self.motor.set_mode("run_using_encoder")
        position = self.motor.get_current_position()
        self.motor.set_target_position(1000)
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        self.assertIn('motor.setPower(0.5);', java_code)
        self.assertIn('motor.setMode(DcMotor.RunMode.RUN_USING_ENCODER);', java_code)
        self.assertIn('motor.getCurrentPosition()', java_code)
        self.assertIn('motor.setTargetPosition(1000);', java_code)
    
    def test_gamepad_input_translation(self):
        """Test gamepad input translation"""
        python_code = '''
@teleop("Gamepad Test", "Test")
class GamepadRobot:
    def init_hardware(self):
        self.motor = motor("test_motor", "forward")
    
    def run(self):
        self.loop()
    
    def loop(self):
        drive = -gamepad1.left_stick_y
        turn = gamepad1.right_stick_x
        
        if gamepad1.a_button:
            self.motor.set_power(1.0)
        elif gamepad2.b_button:
            self.motor.set_power(0.0)
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        self.assertIn('double drive = -gamepad1.left_stick_y;', java_code)
        self.assertIn('double turn = gamepad1.right_stick_x;', java_code)
        self.assertIn('if (gamepad1.a)', java_code)
        self.assertIn('} else if (gamepad2.b)', java_code)
    
    def test_sensor_reading_translation(self):
        """Test sensor reading method translation"""
        python_code = '''
@teleop("Sensor Test", "Test")
class SensorRobot:
    def init_hardware(self):
        self.distance = distance_sensor("distance")
        self.touch = touch_sensor("touch")
    
    def run(self):
        self.loop()
    
    def loop(self):
        dist = self.distance.get_distance()
        pressed = self.touch.is_pressed()
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        self.assertIn('distance.getDistance(DistanceUnit.CM)', java_code)
        self.assertIn('touch.isPressed()', java_code)
    
    def test_telemetry_translation(self):
        """Test telemetry method translation"""
        python_code = '''
@teleop("Telemetry Test", "Test")
class TelemetryRobot:
    def run(self):
        self.loop()
    
    def loop(self):
        telemetry_add("Status", "Running")
        telemetry_add("Power", 0.5)
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        self.assertIn('telemetry.addData("Status", "Running");', java_code)
        self.assertIn('telemetry.addData("Power", 0.5);', java_code)
    
    def test_mathematical_expressions(self):
        """Test mathematical expression translation"""
        python_code = '''
@teleop("Math Test", "Test")
class MathRobot:
    def run(self):
        self.loop()
    
    def loop(self):
        result = 1.0 + 2.0 - 3.0 * 4.0 / 5.0
        power = -gamepad1.left_stick_y + gamepad1.right_stick_x
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        self.assertIn('1.0 + 2.0 - 3.0 * 4.0 / 5.0', java_code)
        self.assertIn('-gamepad1.left_stick_y + gamepad1.right_stick_x', java_code)
    
    def test_conditional_statements(self):
        """Test if/else statement translation"""
        python_code = '''
@teleop("Conditional Test", "Test")
class ConditionalRobot:
    def init_hardware(self):
        self.motor = motor("test_motor", "forward")
    
    def run(self):
        self.loop()
    
    def loop(self):
        if gamepad1.a_button:
            self.motor.set_power(1.0)
        elif gamepad1.b_button:
            self.motor.set_power(0.5)
        else:
            self.motor.set_power(0.0)
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        self.assertIn('if (gamepad1.a) {', java_code)
        self.assertIn('} else if (gamepad1.b) {', java_code)
        self.assertIn('} else {', java_code)
    
    def test_while_loop_translation(self):
        """Test while loop translation"""
        python_code = '''
@teleop("Loop Test", "Test")
class LoopRobot:
    def init_hardware(self):
        self.motor = motor("test_motor", "forward")
    
    def run(self):
        count = 0
        while count < 10:
            self.motor.set_power(0.1)
            count = count + 1
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        self.assertIn('while (count < 10) {', java_code)
        self.assertIn('count = count + 1;', java_code)
    
    def test_imports_generation(self):
        """Test that proper imports are generated"""
        python_code = '''
@teleop("Import Test", "Test")
class ImportRobot:
    def init_hardware(self):
        self.motor = motor("test_motor", "forward")
        self.servo = servo("test_servo")
        self.distance = distance_sensor("distance")
    
    def run(self):
        pass
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        expected_imports = [
            'import com.qualcomm.robotcore.eventloop.opmode.LinearOpMode;',
            'import com.qualcomm.robotcore.eventloop.opmode.TeleOp;',
            'import com.qualcomm.robotcore.hardware.DcMotor;',
            'import com.qualcomm.robotcore.hardware.Servo;',
            'import com.qualcomm.robotcore.hardware.DistanceSensor;',
            'import org.firstinspires.ftc.robotcore.external.navigation.DistanceUnit;'
        ]
        
        for import_stmt in expected_imports:
            self.assertIn(import_stmt, java_code)
    
    def test_method_parameters(self):
        """Test method with parameters"""
        python_code = '''
@teleop("Method Test", "Test")
class MethodRobot:
    def init_hardware(self):
        self.motor = motor("test_motor", "forward")
    
    def run(self):
        self.set_motor_power(0.5)
    
    def set_motor_power(self, power):
        self.motor.set_power(power)
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        self.assertIn('private void set_motor_power(double power) {', java_code)
        self.assertIn('motor.setPower(power);', java_code)
    
    def test_error_handling(self):
        """Test error handling for invalid Python code"""
        invalid_python = '''
@teleop("Error Test", "Test")
class ErrorRobot
    def run(self):  # Missing colon
        pass
'''
        java_code = transpile_ftc_python_to_java(invalid_python)
        
        self.assertIn('// Transpilation error:', java_code)
        self.assertIn('// Original Python code:', java_code)
    
    def test_hardware_type_mapping(self):
        """Test hardware type mapping"""
        transpiler = FTCTranspiler()
        
        self.assertEqual(transpiler.hardware_types['motor'], 'DcMotor')
        self.assertEqual(transpiler.hardware_types['servo'], 'Servo')
        self.assertEqual(transpiler.hardware_types['distance_sensor'], 'DistanceSensor')
        self.assertEqual(transpiler.hardware_types['color_sensor'], 'ColorSensor')
        self.assertEqual(transpiler.hardware_types['imu'], 'IMU')
    
    def test_motor_direction_mapping(self):
        """Test motor direction mapping"""
        transpiler = FTCTranspiler()
        
        self.assertEqual(transpiler.motor_directions['forward'], 'DcMotor.Direction.FORWARD')
        self.assertEqual(transpiler.motor_directions['reverse'], 'DcMotor.Direction.REVERSE')
    
    def test_gamepad_attribute_mapping(self):
        """Test gamepad attribute mapping"""
        transpiler = FTCTranspiler()
        
        self.assertEqual(transpiler.convert_gamepad_attr('left_stick_y'), 'left_stick_y')
        self.assertEqual(transpiler.convert_gamepad_attr('a_button'), 'a')
        self.assertEqual(transpiler.convert_gamepad_attr('dpad_up'), 'dpad_up')
        self.assertEqual(transpiler.convert_gamepad_attr('left_bumper'), 'left_bumper')
    
    def test_binary_operator_conversion(self):
        """Test binary operator conversion"""
        transpiler = FTCTranspiler()
        
        self.assertEqual(transpiler.convert_binary_op(ast.Add()), '+')
        self.assertEqual(transpiler.convert_binary_op(ast.Sub()), '-')
        self.assertEqual(transpiler.convert_binary_op(ast.Mult()), '*')
        self.assertEqual(transpiler.convert_binary_op(ast.Div()), '/')
        self.assertEqual(transpiler.convert_binary_op(ast.Lt()), '<')
        self.assertEqual(transpiler.convert_binary_op(ast.Gt()), '>')
        self.assertEqual(transpiler.convert_binary_op(ast.Eq()), '==')
    
    def test_complex_robot_example(self):
        """Test a complex robot example with multiple features"""
        python_code = '''
@teleop("Complex Robot", "Advanced")
class ComplexRobot:
    def init_hardware(self):
        self.left_drive = motor("left_drive", "forward")
        self.right_drive = motor("right_drive", "reverse")
        self.arm_motor = motor("arm_motor", "forward")
        self.claw_servo = servo("claw_servo")
        self.distance_sensor = distance_sensor("distance")
        
        self.left_drive.set_mode("run_using_encoder")
        self.right_drive.set_mode("run_using_encoder")
    
    def run(self):
        self.loop()
    
    def loop(self):
        # Drive control
        drive = -gamepad1.left_stick_y
        turn = gamepad1.right_stick_x
        
        left_power = drive + turn
        right_power = drive - turn
        
        self.left_drive.set_power(left_power)
        self.right_drive.set_power(right_power)
        
        # Arm control
        arm_power = -gamepad2.left_stick_y
        self.arm_motor.set_power(arm_power)
        
        # Claw control
        if gamepad2.a_button:
            self.claw_servo.set_position(0.0)
        elif gamepad2.b_button:
            self.claw_servo.set_position(1.0)
        
        # Safety check
        distance = self.distance_sensor.get_distance()
        if distance < 10:
            self.left_drive.set_power(0)
            self.right_drive.set_power(0)
        
        # Telemetry
        telemetry_add("Drive", drive)
        telemetry_add("Turn", turn)
        telemetry_add("Distance", distance)
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        # Verify key components are present
        self.assertIn('@TeleOp(name="Complex Robot", group="Advanced")', java_code)
        self.assertIn('public class ComplexRobot extends LinearOpMode', java_code)
        self.assertIn('private DcMotor left_drive = null;', java_code)
        self.assertIn('private Servo claw_servo = null;', java_code)
        self.assertIn('private DistanceSensor distance_sensor = null;', java_code)
        self.assertIn('left_drive.setMode(DcMotor.RunMode.RUN_USING_ENCODER);', java_code)
        self.assertIn('if (gamepad2.a) {', java_code)
        self.assertIn('if (distance < 10) {', java_code)
        self.assertIn('telemetry.addData("Distance", distance);', java_code)


class TestTranspilerIntegration(unittest.TestCase):
    """Integration tests for the transpiler"""
    
    @patch('builtins.open', new_callable=mock_open, read_data='@teleop("Test", "Test")\nclass Test:\n    def run(self):\n        pass')
    @patch('sys.argv', ['ftc_transpiler.py', 'input.py', 'output.java'])
    def test_main_function_file_processing(self, mock_file):
        """Test main function file processing"""
        from ftc_transpiler import main
        
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_with("Successfully transpiled input.py to output.java")
    
    def test_empty_class(self):
        """Test handling of empty class"""
        python_code = '''
@teleop("Empty", "Test")
class EmptyRobot:
    pass
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        self.assertIn('public class EmptyRobot extends LinearOpMode', java_code)
        self.assertIn('@Override', java_code)
        self.assertIn('public void runOpMode()', java_code)
    
    def test_no_decorator(self):
        """Test class without OpMode decorator"""
        python_code = '''
class NoDecoratorRobot:
    def run(self):
        pass
'''
        java_code = transpile_ftc_python_to_java(python_code)
        
        # Should still generate basic class structure
        self.assertIn('public class NoDecoratorRobot extends LinearOpMode', java_code)
        # But no OpMode annotation
        self.assertNotIn('@TeleOp', java_code)
        self.assertNotIn('@Autonomous', java_code)


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test cases
    test_suite.addTest(unittest.makeSuite(TestFTCTranspiler))
    test_suite.addTest(unittest.makeSuite(TestTranspilerIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
