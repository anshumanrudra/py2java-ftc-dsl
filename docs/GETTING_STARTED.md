# Getting Started with FTC Python DSL

This guide will help you get up and running with the FTC Python-to-Java DSL transpiler quickly.

## Prerequisites

Before you begin, make sure you have:

1. **Python 3.7+** installed on your system
2. **FTC Robot Controller SDK** set up
3. **Android Studio** for Java compilation and deployment
4. **Basic understanding** of FTC programming concepts
5. **Python programming knowledge** (basic to intermediate)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/anshumanrudra/py2java-ftc-dsl.git
cd py2java-ftc-dsl
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Make Scripts Executable

```bash
chmod +x src/ftc_transpiler.py
```

### Step 4: Verify Installation

```bash
python src/ftc_transpiler.py --help
```

If you see the usage message, you're ready to go!

## Your First Robot

Let's create a simple robot that can drive around and control a claw.

### Step 1: Create Your Python Robot

Create a file called `my_first_robot.py`:

```python
@teleop("My First Robot", "Learning")
class MyFirstRobot:
    def init_hardware(self):
        # Drive motors
        self.left_drive = motor("left_drive", "forward")
        self.right_drive = motor("right_drive", "reverse")
        
        # Claw servo
        self.claw_servo = servo("claw_servo")
        
        # Distance sensor for safety
        self.distance_sensor = distance_sensor("distance")

    def run(self):
        # Main execution starts here
        self.main_loop()

    def main_loop(self):
        # Tank drive controls
        left_power = -gamepad1.left_stick_y
        right_power = -gamepad1.right_stick_y
        
        # Apply power to motors
        self.left_drive.set_power(left_power)
        self.right_drive.set_power(right_power)
        
        # Claw control
        if gamepad1.a_button:
            self.claw_servo.set_position(0.0)  # Open claw
        elif gamepad1.b_button:
            self.claw_servo.set_position(1.0)  # Close claw
        
        # Safety: stop if obstacle detected
        distance = self.distance_sensor.get_distance()
        if distance < 15:  # 15 cm
            self.left_drive.set_power(0)
            self.right_drive.set_power(0)
            telemetry_add("Warning", "OBSTACLE!")
        
        # Display telemetry
        telemetry_add("Left Power", left_power)
        telemetry_add("Right Power", right_power)
        telemetry_add("Distance", distance)
```

### Step 2: Transpile to Java

```bash
python src/ftc_transpiler.py my_first_robot.py MyFirstRobot.java
```

### Step 3: Review Generated Java

Open `MyFirstRobot.java` to see the generated code:

```java
import com.qualcomm.robotcore.eventloop.opmode.LinearOpMode;
import com.qualcomm.robotcore.eventloop.opmode.TeleOp;
import com.qualcomm.robotcore.hardware.DcMotor;
import com.qualcomm.robotcore.hardware.Servo;
import com.qualcomm.robotcore.hardware.DistanceSensor;
import org.firstinspires.ftc.robotcore.external.navigation.DistanceUnit;

@TeleOp(name="My First Robot", group="Learning")
public class MyFirstRobot extends LinearOpMode {
    // Hardware components
    private DcMotor left_drive = null;
    private DcMotor right_drive = null;
    private Servo claw_servo = null;
    private DistanceSensor distance_sensor = null;

    private void initHardware() {
        left_drive = hardwareMap.get(DcMotor.class, "left_drive");
        left_drive.setDirection(DcMotor.Direction.FORWARD);
        right_drive = hardwareMap.get(DcMotor.class, "right_drive");
        right_drive.setDirection(DcMotor.Direction.REVERSE);
        claw_servo = hardwareMap.get(Servo.class, "claw_servo");
        distance_sensor = hardwareMap.get(DistanceSensor.class, "distance");
    }

    @Override
    public void runOpMode() {
        initHardware();
        
        telemetry.addData("Status", "Initialized");
        telemetry.update();
        
        waitForStart();
        
        main_loop();
    }

    private void main_loop() {
        while (opModeIsActive()) {
            double left_power = -gamepad1.left_stick_y;
            double right_power = -gamepad1.right_stick_y;
            
            left_drive.setPower(left_power);
            right_drive.setPower(right_power);
            
            if (gamepad1.a) {
                claw_servo.setPosition(0.0);
            } else if (gamepad1.b) {
                claw_servo.setPosition(1.0);
            }
            
            double distance = distance_sensor.getDistance(DistanceUnit.CM);
            if (distance < 15) {
                left_drive.setPower(0);
                right_drive.setPower(0);
                telemetry.addData("Warning", "OBSTACLE!");
            }
            
            telemetry.addData("Left Power", left_power);
            telemetry.addData("Right Power", right_power);
            telemetry.addData("Distance", distance);
            telemetry.update();
        }
    }
}
```

### Step 4: Deploy to Robot

1. Copy `MyFirstRobot.java` to your FTC project's `TeamCode` directory
2. Build and deploy using Android Studio
3. Configure hardware names in the Robot Controller app
4. Test your robot!

## Key Concepts

### OpMode Types

Use decorators to specify OpMode type:

```python
@teleop("TeleOp Name", "Group")     # For driver-controlled
@autonomous("Auto Name", "Group")   # For autonomous
```

### Hardware Declaration

Declare hardware in `init_hardware()`:

```python
def init_hardware(self):
    self.motor_name = motor("config_name", "direction")
    self.servo_name = servo("config_name")
    self.sensor_name = distance_sensor("config_name")
```

### Control Flow

Structure your robot logic:

```python
def run(self):
    # Called once when OpMode starts
    self.main_loop()

def main_loop(self):
    # Main control loop - runs continuously
    while opmode_is_active():
        # Your robot logic here
        pass
```

### Gamepad Input

Access gamepad controls:

```python
# Analog inputs (joysticks, triggers)
drive = gamepad1.left_stick_y
turn = gamepad1.right_stick_x
trigger = gamepad1.left_trigger

# Button inputs
if gamepad1.a_button:
    # A button pressed
if gamepad1.dpad_up:
    # D-pad up pressed
```

### Telemetry

Display information on Driver Station:

```python
telemetry_add("Label", value)
telemetry_add("Motor Power", motor_power)
telemetry_add("Status", "Running")
```

## Common Patterns

### Tank Drive

```python
def tank_drive(self):
    left_power = -gamepad1.left_stick_y
    right_power = -gamepad1.right_stick_y
    
    self.left_motor.set_power(left_power)
    self.right_motor.set_power(right_power)
```

### Arcade Drive

```python
def arcade_drive(self):
    drive = -gamepad1.left_stick_y
    turn = gamepad1.right_stick_x
    
    left_power = drive + turn
    right_power = drive - turn
    
    self.left_motor.set_power(left_power)
    self.right_motor.set_power(right_power)
```

### Mecanum Drive

```python
def mecanum_drive(self):
    drive = -gamepad1.left_stick_y
    strafe = gamepad1.left_stick_x
    turn = gamepad1.right_stick_x
    
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
    
    self.front_left.set_power(front_left_power)
    self.front_right.set_power(front_right_power)
    self.back_left.set_power(back_left_power)
    self.back_right.set_power(back_right_power)
```

### Servo Control

```python
def servo_control(self):
    if gamepad2.a_button:
        self.servo.set_position(0.0)    # Minimum position
    elif gamepad2.b_button:
        self.servo.set_position(0.5)    # Middle position
    elif gamepad2.y_button:
        self.servo.set_position(1.0)    # Maximum position
```

### Encoder-Based Movement

```python
def move_to_position(self, target_position):
    self.motor.set_mode("stop_and_reset_encoder")
    self.motor.set_target_position(target_position)
    self.motor.set_mode("run_to_position")
    self.motor.set_power(0.5)
    
    # Wait for movement to complete
    while self.motor.get_current_position() != target_position:
        telemetry_add("Position", self.motor.get_current_position())
        telemetry_add("Target", target_position)
```

## Autonomous Programming

Create autonomous OpModes:

```python
@autonomous("Simple Auto", "Competition")
class SimpleAuto:
    def init_hardware(self):
        self.drive_motor = motor("drive", "forward")
        self.distance_sensor = distance_sensor("distance")

    def run(self):
        # Drive forward until obstacle
        while opmode_is_active():
            distance = self.distance_sensor.get_distance()
            
            if distance > 20:  # 20 cm clearance
                self.drive_motor.set_power(0.3)
            else:
                self.drive_motor.set_power(0)
                break
            
            telemetry_add("Distance", distance)
            sleep(50)  # Small delay
```

## Testing Your Code

### Unit Testing

Run the included tests:

```bash
python -m pytest tests/
```

### Syntax Validation

Check if your Python code will transpile correctly:

```bash
python src/ftc_transpiler.py --validate my_robot.py
```

### Step-by-Step Testing

1. **Start Simple**: Begin with basic motor control
2. **Add Features Gradually**: Add sensors, servos, etc. one at a time
3. **Test Each Addition**: Transpile and test after each new feature
4. **Use Telemetry**: Add telemetry to debug issues

## Troubleshooting

### Common Issues

**Issue**: "Hardware not found" error
**Solution**: Check hardware configuration names match your Python code

**Issue**: Motor runs in wrong direction
**Solution**: Change direction parameter: "forward" ↔ "reverse"

**Issue**: Gamepad not responding
**Solution**: Check gamepad number (gamepad1 vs gamepad2) and button names

**Issue**: Transpilation errors
**Solution**: Check Python syntax, ensure proper indentation

### Getting Help

1. **Check Examples**: Look at the examples in the `examples/` directory
2. **Read API Reference**: See `docs/API_REFERENCE.md` for complete syntax
3. **Run Tests**: Use `pytest tests/` to verify your installation
4. **Check Issues**: Look at GitHub issues for known problems

## Next Steps

Once you're comfortable with the basics:

1. **Explore Examples**: Check out the advanced examples:
   - `examples/apriltag_detection.py` - Computer vision
   - `examples/tensorflow_detection.py` - Machine learning
   - `examples/mobile_controller.py` - Advanced controls

2. **Learn Advanced Features**:
   - Vision processing with AprilTags
   - TensorFlow object detection
   - Mobile dashboard integration
   - Custom sensor integration

3. **Contribute**: Help improve the DSL by contributing features or reporting bugs

4. **Share**: Share your robots and experiences with the FTC community

## Best Practices

1. **Use Meaningful Names**: Choose descriptive names for hardware and variables
2. **Keep Methods Short**: Break complex logic into smaller methods
3. **Add Comments**: Document complex calculations and logic
4. **Test Incrementally**: Test each feature as you add it
5. **Follow FTC Guidelines**: Ensure your code follows FTC programming guidelines
6. **Version Control**: Use Git to track changes to your robot code

Happy coding! 🤖
