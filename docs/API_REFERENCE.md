# FTC DSL API Reference

Complete reference for the FTC Python-to-Java DSL syntax and features.

## Table of Contents

- [OpMode Decorators](#opmode-decorators)
- [Hardware Components](#hardware-components)
- [Motor Control](#motor-control)
- [Servo Control](#servo-control)
- [Sensor Reading](#sensor-reading)
- [Gamepad Input](#gamepad-input)
- [Telemetry](#telemetry)
- [Vision Processing](#vision-processing)
- [Dashboard Integration](#dashboard-integration)
- [Utility Functions](#utility-functions)

## OpMode Decorators

### @teleop(name, group)

Declares a TeleOp OpMode.

**Parameters:**
- `name` (str): Display name in Driver Station
- `group` (str): OpMode group/category

**Example:**
```python
@teleop("My Robot", "Competition")
class MyRobot:
    pass
```

**Generated Java:**
```java
@TeleOp(name="My Robot", group="Competition")
public class MyRobot extends LinearOpMode {
    // ...
}
```

### @autonomous(name, group)

Declares an Autonomous OpMode.

**Parameters:**
- `name` (str): Display name in Driver Station
- `group` (str): OpMode group/category

**Example:**
```python
@autonomous("Auto Red", "Competition")
class AutoRobot:
    pass
```

**Generated Java:**
```java
@Autonomous(name="Auto Red", group="Competition")
public class AutoRobot extends LinearOpMode {
    // ...
}
```

## Hardware Components

### motor(config_name, direction)

Declares a DC motor.

**Parameters:**
- `config_name` (str): Hardware configuration name
- `direction` (str): "forward" or "reverse"

**Example:**
```python
self.drive_motor = motor("left_drive", "forward")
```

**Generated Java:**
```java
private DcMotor drive_motor = null;
// In initHardware():
drive_motor = hardwareMap.get(DcMotor.class, "left_drive");
drive_motor.setDirection(DcMotor.Direction.FORWARD);
```

### servo(config_name)

Declares a servo motor.

**Parameters:**
- `config_name` (str): Hardware configuration name

**Example:**
```python
self.claw_servo = servo("claw")
```

**Generated Java:**
```java
private Servo claw_servo = null;
// In initHardware():
claw_servo = hardwareMap.get(Servo.class, "claw");
```

### distance_sensor(config_name)

Declares a distance sensor.

**Parameters:**
- `config_name` (str): Hardware configuration name

**Example:**
```python
self.distance = distance_sensor("distance")
```

**Generated Java:**
```java
private DistanceSensor distance = null;
// In initHardware():
distance = hardwareMap.get(DistanceSensor.class, "distance");
```

### color_sensor(config_name)

Declares a color sensor.

**Parameters:**
- `config_name` (str): Hardware configuration name

**Example:**
```python
self.color = color_sensor("color")
```

**Generated Java:**
```java
private ColorSensor color = null;
// In initHardware():
color = hardwareMap.get(ColorSensor.class, "color");
```

### touch_sensor(config_name)

Declares a touch sensor.

**Parameters:**
- `config_name` (str): Hardware configuration name

**Example:**
```python
self.limit_switch = touch_sensor("limit")
```

**Generated Java:**
```java
private TouchSensor limit_switch = null;
// In initHardware():
limit_switch = hardwareMap.get(TouchSensor.class, "limit");
```

### imu(config_name)

Declares an IMU (Inertial Measurement Unit).

**Parameters:**
- `config_name` (str): Hardware configuration name

**Example:**
```python
self.imu = imu("imu")
```

**Generated Java:**
```java
private IMU imu = null;
// In initHardware():
imu = hardwareMap.get(IMU.class, "imu");
```

## Motor Control

### set_power(power)

Sets motor power.

**Parameters:**
- `power` (float): Power level (-1.0 to 1.0)

**Example:**
```python
motor.set_power(0.5)
```

**Generated Java:**
```java
motor.setPower(0.5);
```

### set_mode(mode)

Sets motor run mode.

**Parameters:**
- `mode` (str): Motor run mode

**Valid modes:**
- `"run_using_encoder"`
- `"run_without_encoder"`
- `"run_to_position"`
- `"stop_and_reset_encoder"`

**Example:**
```python
motor.set_mode("run_using_encoder")
```

**Generated Java:**
```java
motor.setMode(DcMotor.RunMode.RUN_USING_ENCODER);
```

### get_current_position()

Gets current encoder position.

**Returns:** Current encoder position

**Example:**
```python
position = motor.get_current_position()
```

**Generated Java:**
```java
double position = motor.getCurrentPosition();
```

### set_target_position(position)

Sets target position for RUN_TO_POSITION mode.

**Parameters:**
- `position` (int): Target encoder position

**Example:**
```python
motor.set_target_position(1000)
```

**Generated Java:**
```java
motor.setTargetPosition(1000);
```

## Servo Control

### set_position(position)

Sets servo position.

**Parameters:**
- `position` (float): Position (0.0 to 1.0)

**Example:**
```python
servo.set_position(0.5)
```

**Generated Java:**
```java
servo.setPosition(0.5);
```

## Sensor Reading

### get_distance()

Gets distance reading in centimeters.

**Returns:** Distance in cm

**Example:**
```python
distance = sensor.get_distance()
```

**Generated Java:**
```java
double distance = sensor.getDistance(DistanceUnit.CM);
```

### is_pressed()

Checks if touch sensor is pressed.

**Returns:** True if pressed

**Example:**
```python
pressed = touch_sensor.is_pressed()
```

**Generated Java:**
```java
boolean pressed = touch_sensor.isPressed();
```

### get_heading()

Gets IMU heading.

**Returns:** Heading in degrees

**Example:**
```python
heading = imu.get_heading()
```

**Generated Java:**
```java
double heading = imu.get_heading();
```

### get_pitch()

Gets IMU pitch.

**Returns:** Pitch in degrees

**Example:**
```python
pitch = imu.get_pitch()
```

**Generated Java:**
```java
double pitch = imu.get_pitch();
```

### get_roll()

Gets IMU roll.

**Returns:** Roll in degrees

**Example:**
```python
roll = imu.get_roll()
```

**Generated Java:**
```java
double roll = imu.get_roll();
```

## Gamepad Input

### Analog Inputs

**Available analog inputs:**
- `gamepad1.left_stick_x`
- `gamepad1.left_stick_y`
- `gamepad1.right_stick_x`
- `gamepad1.right_stick_y`
- `gamepad1.left_trigger`
- `gamepad1.right_trigger`
- `gamepad2.left_stick_x`
- `gamepad2.left_stick_y`
- `gamepad2.right_stick_x`
- `gamepad2.right_stick_y`
- `gamepad2.left_trigger`
- `gamepad2.right_trigger`

**Example:**
```python
drive = -gamepad1.left_stick_y
turn = gamepad1.right_stick_x
```

**Generated Java:**
```java
double drive = -gamepad1.left_stick_y;
double turn = gamepad1.right_stick_x;
```

### Button Inputs

**Available button inputs:**
- `gamepad1.a_button` → `gamepad1.a`
- `gamepad1.b_button` → `gamepad1.b`
- `gamepad1.x_button` → `gamepad1.x`
- `gamepad1.y_button` → `gamepad1.y`
- `gamepad1.dpad_up`
- `gamepad1.dpad_down`
- `gamepad1.dpad_left`
- `gamepad1.dpad_right`
- `gamepad1.left_bumper`
- `gamepad1.right_bumper`
- `gamepad1.start`
- `gamepad1.back`

**Example:**
```python
if gamepad1.a_button:
    # A button pressed
if gamepad1.dpad_up:
    # D-pad up pressed
```

**Generated Java:**
```java
if (gamepad1.a) {
    // A button pressed
}
if (gamepad1.dpad_up) {
    // D-pad up pressed
}
```

## Telemetry

### telemetry_add(key, value)

Adds telemetry data.

**Parameters:**
- `key` (str): Data key/label
- `value`: Data value

**Example:**
```python
telemetry_add("Status", "Running")
telemetry_add("Power", motor_power)
```

**Generated Java:**
```java
telemetry.addData("Status", "Running");
telemetry.addData("Power", motor_power);
```

## Vision Processing

### webcam(name)

Declares a webcam.

**Parameters:**
- `name` (str): Webcam name

**Example:**
```python
self.camera = webcam("Webcam 1")
```

### apriltag_processor()

Creates AprilTag processor.

**Example:**
```python
self.apriltag = apriltag_processor()
```

### tensorflow_processor()

Creates TensorFlow processor.

**Example:**
```python
self.tensorflow = tensorflow_processor()
```

### vision_portal(camera, processor)

Creates vision portal.

**Parameters:**
- `camera`: Camera object
- `processor`: Vision processor

**Example:**
```python
self.portal = vision_portal(self.camera, self.apriltag)
```

## Dashboard Integration

### dashboard_register(key, default_value)

Registers dashboard variable.

**Parameters:**
- `key` (str): Variable name
- `default_value`: Default value

**Example:**
```python
dashboard_register("Drive Speed", 1.0)
```

### dashboard_get(key)

Gets dashboard variable value.

**Parameters:**
- `key` (str): Variable name

**Returns:** Variable value

**Example:**
```python
speed = dashboard_get("Drive Speed")
```

### dashboard_send_packet(data)

Sends data packet to dashboard.

**Parameters:**
- `data`: Data to send

**Example:**
```python
packet = {"speed": 0.5, "mode": "teleop"}
dashboard_send_packet(packet)
```

## Utility Functions

### sleep(milliseconds)

Pauses execution.

**Parameters:**
- `milliseconds` (int): Sleep duration in ms

**Example:**
```python
sleep(1000)  # Sleep for 1 second
```

**Generated Java:**
```java
sleep(1000);
```

### opmode_is_active()

Checks if OpMode is active.

**Returns:** True if active

**Example:**
```python
while opmode_is_active():
    # Main loop
```

**Generated Java:**
```java
while (opModeIsActive()) {
    // Main loop
}
```

## Class Structure

### Required Methods

#### init_hardware()

Hardware initialization method.

**Example:**
```python
def init_hardware(self):
    self.motor = motor("motor", "forward")
    self.servo = servo("servo")
```

#### run()

Main OpMode execution method.

**Example:**
```python
def run(self):
    self.loop()
```

#### loop()

Main control loop (called from run()).

**Example:**
```python
def loop(self):
    while opmode_is_active():
        # Control logic
        pass
```

### Optional Methods

You can define custom methods that will be transpiled to private Java methods:

**Example:**
```python
def calculate_power(self, input_value):
    return input_value * 0.8

def move_to_position(self, target):
    self.motor.set_target_position(target)
    self.motor.set_mode("run_to_position")
    self.motor.set_power(0.5)
```

**Generated Java:**
```java
private void calculate_power(double input_value) {
    return input_value * 0.8;
}

private void move_to_position(double target) {
    motor.setTargetPosition(target);
    motor.setMode(DcMotor.RunMode.RUN_TO_POSITION);
    motor.setPower(0.5);
}
```

## Error Handling

The transpiler includes error handling for common issues:

1. **Syntax Errors**: Invalid Python syntax will be reported
2. **Unknown Methods**: Unsupported method calls are preserved as comments
3. **Type Mismatches**: Basic type checking for hardware components
4. **Missing Decorators**: Classes without OpMode decorators still generate basic structure

## Limitations

Current limitations of the DSL:

1. **Complex Python Features**: Advanced Python features (list comprehensions, decorators other than OpMode, etc.) are not supported
2. **Custom Libraries**: Only FTC SDK libraries are supported
3. **Error Handling**: Python try/catch blocks are not yet supported
4. **Object-Oriented Features**: Inheritance and complex OOP features are limited
5. **Data Structures**: Complex data structures beyond basic variables are limited

## Best Practices

1. **Keep Methods Simple**: Use straightforward control flow
2. **Use Descriptive Names**: Hardware component names should match configuration
3. **Organize Code**: Group related functionality in separate methods
4. **Comment Complex Logic**: Add comments for complex calculations
5. **Test Incrementally**: Test simple features before adding complexity

## Future Enhancements

Planned features for future versions:

1. **Enhanced Error Handling**: Better error messages and recovery
2. **More Sensors**: Support for additional sensor types
3. **Advanced Vision**: Enhanced computer vision features
4. **Path Planning**: Built-in path planning utilities
5. **Multi-Robot**: Support for multi-robot coordination
6. **Simulation**: Integration with robot simulators
