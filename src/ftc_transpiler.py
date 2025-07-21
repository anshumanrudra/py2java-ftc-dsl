#!/usr/bin/env python3
"""
FTC DSL Python-to-Java Transpiler

A Domain-Specific Language transpiler that converts Python-like syntax
to FTC-compatible Java code for FIRST Tech Challenge robotics programming.

Features:
- FTC-specific decorators and annotations
- Hardware mapping abstractions
- OpMode lifecycle management
- Sensor and actuator APIs
- Gamepad input handling
- Autonomous and TeleOp modes

Usage:
    python ftc_transpiler.py input_robot.py output_robot.java
"""

import ast
import sys
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class OpModeType(Enum):
    TELEOP = "TeleOp"
    AUTONOMOUS = "Autonomous"
    DISABLED = "Disabled"

@dataclass
class HardwareComponent:
    name: str
    type: str
    config_name: str
    direction: Optional[str] = None

@dataclass
class OpModeInfo:
    name: str
    group: str
    type: OpModeType

class FTCTranspiler(ast.NodeVisitor):
    def __init__(self):
        self.java_code = []
        self.imports = set()
        self.hardware_components = {}
        self.opmode_info = None
        self.class_name = ""
        self.indent_level = 0
        
        # FTC API mappings
        self.hardware_types = {
            'motor': 'DcMotor',
            'servo': 'Servo',
            'color_sensor': 'ColorSensor',
            'distance_sensor': 'DistanceSensor',
            'gyro': 'GyroSensor',
            'touch_sensor': 'TouchSensor',
            'light_sensor': 'LightSensor',
            'imu': 'IMU'
        }
        
        self.motor_directions = {
            'forward': 'DcMotor.Direction.FORWARD',
            'reverse': 'DcMotor.Direction.REVERSE'
        }
        
        self.motor_modes = {
            'run_using_encoder': 'DcMotor.RunMode.RUN_USING_ENCODER',
            'run_without_encoder': 'DcMotor.RunMode.RUN_WITHOUT_ENCODER',
            'run_to_position': 'DcMotor.RunMode.RUN_TO_POSITION',
            'stop_and_reset_encoder': 'DcMotor.RunMode.STOP_AND_RESET_ENCODER'
        }
        
        # Standard FTC imports
        self.standard_imports = {
            'com.qualcomm.robotcore.eventloop.opmode.LinearOpMode',
            'com.qualcomm.robotcore.eventloop.opmode.TeleOp',
            'com.qualcomm.robotcore.eventloop.opmode.Autonomous',
            'com.qualcomm.robotcore.hardware.DcMotor',
            'com.qualcomm.robotcore.hardware.Servo',
            'com.qualcomm.robotcore.hardware.ColorSensor',
            'com.qualcomm.robotcore.hardware.DistanceSensor',
            'com.qualcomm.robotcore.hardware.TouchSensor',
            'com.qualcomm.robotcore.hardware.LightSensor',
            'com.qualcomm.robotcore.hardware.IMU',
            'org.firstinspires.ftc.robotcore.external.navigation.DistanceUnit',
            'org.firstinspires.ftc.robotcore.external.navigation.AngleUnit'
        }

    def indent(self) -> str:
        return "    " * self.indent_level

    def add_line(self, line: str):
        self.java_code.append(self.indent() + line)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.class_name = node.name
        
        # Process decorators for OpMode info
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                if decorator.func.id == 'teleop':
                    self.opmode_info = OpModeInfo(
                        name=self.get_string_arg(decorator, 0, node.name),
                        group=self.get_string_arg(decorator, 1, "Linear Opmode"),
                        type=OpModeType.TELEOP
                    )
                elif decorator.func.id == 'autonomous':
                    self.opmode_info = OpModeInfo(
                        name=self.get_string_arg(decorator, 0, node.name),
                        group=self.get_string_arg(decorator, 1, "Linear Opmode"),
                        type=OpModeType.AUTONOMOUS
                    )

        # Generate Java class header
        if self.opmode_info:
            self.add_line(f"@{self.opmode_info.type.value}(name=\"{self.opmode_info.name}\", group=\"{self.opmode_info.group}\")")
        
        self.add_line(f"public class {self.class_name} extends LinearOpMode {{")
        self.indent_level += 1
        
        # Add hardware component declarations
        if self.hardware_components:
            self.add_line("// Hardware components")
            for comp_name, comp in self.hardware_components.items():
                self.add_line(f"private {comp.type} {comp_name} = null;")
            self.add_line("")
        
        # Process class body to find hardware components first
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == 'init_hardware':
                self.scan_hardware_components(item)
        
        # Add hardware component declarations after scanning
        if self.hardware_components:
            self.java_code.insert(-1, self.indent() + "// Hardware components")
            for comp_name, comp in self.hardware_components.items():
                self.java_code.insert(-1, self.indent() + f"private {comp.type} {comp_name} = null;")
            self.java_code.insert(-1, self.indent() + "")
        
        # Process class body
        for item in node.body:
            self.visit(item)
        
        self.indent_level -= 1
        self.add_line("}")

    def scan_hardware_components(self, node: ast.FunctionDef):
        """Pre-scan to identify hardware components for declaration"""
        for stmt in node.body:
            if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
                if isinstance(stmt.targets[0], ast.Attribute):
                    attr = stmt.targets[0]
                    if isinstance(attr.value, ast.Name) and attr.value.id == 'self':
                        if isinstance(stmt.value, ast.Call) and isinstance(stmt.value.func, ast.Name):
                            func_name = stmt.value.func.id
                            if func_name in self.hardware_types:
                                config_name = self.get_string_arg(stmt.value, 0, attr.attr)
                                direction = self.get_string_arg(stmt.value, 1, None)
                                
                                comp = HardwareComponent(
                                    name=attr.attr,
                                    type=self.hardware_types[func_name],
                                    config_name=config_name,
                                    direction=direction
                                )
                                self.hardware_components[attr.attr] = comp

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name == 'init_hardware':
            self.generate_init_hardware(node)
        elif node.name == 'run':
            self.generate_run_opmode(node)
        elif node.name == 'loop':
            self.generate_loop_method(node)
        else:
            self.generate_regular_method(node)

    def generate_init_hardware(self, node: ast.FunctionDef):
        self.add_line("private void initHardware() {")
        self.indent_level += 1
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.indent_level -= 1
        self.add_line("}")
        self.add_line("")

    def generate_run_opmode(self, node: ast.FunctionDef):
        self.add_line("@Override")
        self.add_line("public void runOpMode() {")
        self.indent_level += 1
        
        # Add standard initialization
        self.add_line("initHardware();")
        self.add_line("")
        self.add_line("telemetry.addData(\"Status\", \"Initialized\");")
        self.add_line("telemetry.update();")
        self.add_line("")
        self.add_line("waitForStart();")
        self.add_line("")
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.indent_level -= 1
        self.add_line("}")

    def generate_loop_method(self, node: ast.FunctionDef):
        self.add_line("while (opModeIsActive()) {")
        self.indent_level += 1
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.add_line("telemetry.update();")
        self.indent_level -= 1
        self.add_line("}")

    def generate_regular_method(self, node: ast.FunctionDef):
        # Determine return type (simplified)
        return_type = "void"  # Default
        
        # Check for parameters
        params = []
        for arg in node.args.args:
            if arg.arg != 'self':
                params.append(f"double {arg.arg}")
        
        param_str = ", ".join(params)
        self.add_line(f"private {return_type} {node.name}({param_str}) {{")
        self.indent_level += 1
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.indent_level -= 1
        self.add_line("}")
        self.add_line("")

    def visit_Assign(self, node: ast.Assign):
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Attribute):
            attr = node.targets[0]
            if isinstance(attr.value, ast.Name) and attr.value.id == 'self':
                # Hardware component assignment
                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    func_name = node.value.func.id
                    if func_name in self.hardware_types:
                        config_name = self.get_string_arg(node.value, 0, attr.attr)
                        direction = self.get_string_arg(node.value, 1, None)
                        
                        self.add_line(f"{attr.attr} = hardwareMap.get({self.hardware_types[func_name]}.class, \"{config_name}\");")
                        
                        if direction and func_name == 'motor':
                            java_direction = self.motor_directions.get(direction, direction)
                            self.add_line(f"{attr.attr}.setDirection({java_direction});")
                
                else:
                    # Regular attribute assignment
                    value = self.visit_expression(node.value)
                    self.add_line(f"{attr.attr} = {value};")
        
        elif len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            # Local variable assignment
            var_name = node.targets[0].id
            value = self.visit_expression(node.value)
            self.add_line(f"double {var_name} = {value};")

    def visit_expression(self, node) -> str:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            return str(node.value)
        
        elif isinstance(node, ast.Name):
            return node.id
        
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                if node.value.id == 'gamepad1':
                    return f"gamepad1.{self.convert_gamepad_attr(node.attr)}"
                elif node.value.id == 'gamepad2':
                    return f"gamepad2.{self.convert_gamepad_attr(node.attr)}"
                else:
                    return f"{node.value.id}.{node.attr}"
        
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            operand = self.visit_expression(node.operand)
            return f"-{operand}"
        
        elif isinstance(node, ast.BinOp):
            left = self.visit_expression(node.left)
            right = self.visit_expression(node.right)
            op = self.convert_binary_op(node.op)
            return f"{left} {op} {right}"
        
        elif isinstance(node, ast.Call):
            return self.visit_call_expression(node)
        
        return "/* UNKNOWN EXPRESSION */"

    def visit_call_expression(self, node: ast.Call) -> str:
        if isinstance(node.func, ast.Attribute):
            obj = self.visit_expression(node.func.value)
            method = node.func.attr
            
            # Convert Python method names to Java equivalents
            if method == 'set_power':
                arg = self.visit_expression(node.args[0])
                return f"{obj}.setPower({arg})"
            elif method == 'set_position':
                arg = self.visit_expression(node.args[0])
                return f"{obj}.setPosition({arg})"
            elif method == 'get_distance':
                return f"{obj}.getDistance(DistanceUnit.CM)"
            elif method == 'is_pressed':
                return f"{obj}.isPressed()"
            elif method == 'get_current_position':
                return f"{obj}.getCurrentPosition()"
            elif method == 'set_target_position':
                arg = self.visit_expression(node.args[0])
                return f"{obj}.setTargetPosition({arg})"
            elif method == 'set_mode':
                if len(node.args) > 0:
                    mode_arg = self.visit_expression(node.args[0])
                    if mode_arg.strip('"') in self.motor_modes:
                        java_mode = self.motor_modes[mode_arg.strip('"')]
                        return f"{obj}.setMode({java_mode})"
                return f"{obj}.setMode(/* UNKNOWN MODE */)"
        
        elif isinstance(node.func, ast.Name):
            if node.func.id == 'telemetry_add':
                if len(node.args) >= 2:
                    key = self.visit_expression(node.args[0])
                    value = self.visit_expression(node.args[1])
                    return f"telemetry.addData({key}, {value})"
            elif node.func.id == 'sleep':
                if len(node.args) > 0:
                    time_ms = self.visit_expression(node.args[0])
                    return f"sleep({time_ms})"
        
        return "/* UNKNOWN CALL */"

    def visit_Expr(self, node: ast.Expr):
        if isinstance(node.value, ast.Call):
            call_str = self.visit_call_expression(node.value)
            if not call_str.startswith("/*"):
                self.add_line(f"{call_str};")

    def visit_If(self, node: ast.If):
        condition = self.visit_expression(node.test)
        self.add_line(f"if ({condition}) {{")
        self.indent_level += 1
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.indent_level -= 1
        
        if node.orelse:
            self.add_line("} else {")
            self.indent_level += 1
            
            for stmt in node.orelse:
                self.visit(stmt)
            
            self.indent_level -= 1
        
        self.add_line("}")

    def visit_While(self, node: ast.While):
        condition = self.visit_expression(node.test)
        self.add_line(f"while ({condition}) {{")
        self.indent_level += 1
        
        for stmt in node.body:
            self.visit(stmt)
        
        self.indent_level -= 1
        self.add_line("}")

    def convert_gamepad_attr(self, attr: str) -> str:
        gamepad_mappings = {
            'left_stick_y': 'left_stick_y',
            'right_stick_x': 'right_stick_x',
            'left_stick_x': 'left_stick_x',
            'right_stick_y': 'right_stick_y',
            'a_button': 'a',
            'b_button': 'b',
            'x_button': 'x',
            'y_button': 'y',
            'dpad_up': 'dpad_up',
            'dpad_down': 'dpad_down',
            'dpad_left': 'dpad_left',
            'dpad_right': 'dpad_right',
            'left_bumper': 'left_bumper',
            'right_bumper': 'right_bumper',
            'left_trigger': 'left_trigger',
            'right_trigger': 'right_trigger'
        }
        return gamepad_mappings.get(attr, attr)

    def convert_binary_op(self, op) -> str:
        if isinstance(op, ast.Add):
            return "+"
        elif isinstance(op, ast.Sub):
            return "-"
        elif isinstance(op, ast.Mult):
            return "*"
        elif isinstance(op, ast.Div):
            return "/"
        elif isinstance(op, ast.Lt):
            return "<"
        elif isinstance(op, ast.Gt):
            return ">"
        elif isinstance(op, ast.LtE):
            return "<="
        elif isinstance(op, ast.GtE):
            return ">="
        elif isinstance(op, ast.Eq):
            return "=="
        elif isinstance(op, ast.NotEq):
            return "!="
        return "?"

    def get_string_arg(self, call_node: ast.Call, index: int, default: str) -> str:
        if len(call_node.args) > index and isinstance(call_node.args[index], ast.Constant):
            return call_node.args[index].value
        return default

    def generate_java_code(self) -> str:
        # Generate imports
        imports = []
        for imp in sorted(self.standard_imports):
            imports.append(f"import {imp};")
        
        # Combine imports and class code
        result = "\n".join(imports) + "\n\n" + "\n".join(self.java_code)
        return result

def transpile_ftc_python_to_java(python_code: str) -> str:
    """
    Transpile FTC Python DSL code to Java.
    
    Args:
        python_code: Python source code using FTC DSL
        
    Returns:
        Generated Java code for FTC
    """
    try:
        tree = ast.parse(python_code)
        transpiler = FTCTranspiler()
        transpiler.visit(tree)
        return transpiler.generate_java_code()
    except Exception as e:
        return f"// Transpilation error: {str(e)}\n// Original Python code:\n/*\n{python_code}\n*/"

def main():
    if len(sys.argv) != 3:
        print("Usage: python ftc_transpiler.py input.py output.java")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        with open(input_file, 'r') as f:
            python_code = f.read()
        
        java_code = transpile_ftc_python_to_java(python_code)
        
        with open(output_file, 'w') as f:
            f.write(java_code)
        
        print(f"Successfully transpiled {input_file} to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
