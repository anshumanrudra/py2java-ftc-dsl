# FTC Python-to-Java DSL Transpiler

A Domain-Specific Language (DSL) transpiler that converts Python-like syntax to FTC-compatible Java code for FIRST Tech Challenge robotics programming.

## 🚀 Features

- **Python-like Syntax**: Write robot code in familiar Python syntax
- **FTC API Integration**: Full support for FTC hardware and software APIs
- **Advanced Vision**: AprilTag detection and TensorFlow object recognition
- **Mobile Dashboard**: Custom mobile controller with real-time telemetry
- **Hardware Abstraction**: Simplified hardware configuration and control
- **Automatic Code Generation**: Transpiles to clean, readable Java code
- **Type Safety**: Maintains Java's type safety while providing Python's ease of use
- **Git Submodule Ready**: Easy integration into FTC team projects

## 📁 Project Structure

```
py2java-ftc-dsl/
├── src/
│   └── ftc_transpiler.py          # Main transpiler engine
├── examples/
│   ├── basic_teleop.py            # Basic TeleOp robot example
│   ├── apriltag_detection.py      # AprilTag vision example
│   ├── tensorflow_detection.py    # TensorFlow ML example
│   └── mobile_controller.py       # Advanced mobile dashboard
├── tests/
│   ├── test_transpiler.py         # Unit tests for transpiler
│   ├── test_examples.py           # Tests for example code
│   └── test_data/                 # Test input/output files
├── docs/
│   ├── API_REFERENCE.md           # Complete API documentation
│   ├── GETTING_STARTED.md         # Quick start guide
│   ├── FTC_TEAM_GUIDE.md          # Team integration guide
│   └── EXAMPLES.md                # Detailed examples
├── Makefile                       # Build automation
├── VERSION                        # Version information
└── README.md                      # This file
```

## 🛠️ Installation for FTC Teams

### As Git Submodule (Recommended)

This is the recommended approach for FTC teams:

```bash
# In your FTC project root
git submodule add https://github.com/anshumanrudra/py2java-ftc-dsl.git
git submodule update --init --recursive

# Set up project structure
make quickstart

# Start coding in Python!
```

See [FTC Team Guide](docs/FTC_TEAM_GUIDE.md) for complete team integration instructions.

### Standalone Installation

For individual development:

```bash
git clone https://github.com/anshumanrudra/py2java-ftc-dsl.git
cd py2java-ftc-dsl
pip install -r requirements.txt
chmod +x src/ftc_transpiler.py
```

## 🚀 Quick Start for FTC Teams

### 1. Add to Your Project

```bash
# Add as submodule
git submodule add https://github.com/anshumanrudra/py2java-ftc-dsl.git

# Set up project structure
make quickstart
```

### 2. Write Python Robot Code

Create `robot/MyRobot.py`:

```python
@teleop("My Team Robot", "Competition")
class MyTeamRobot:
    def init_hardware(self):
        self.left_drive = motor("left_drive", "forward")
        self.right_drive = motor("right_drive", "reverse")
        self.claw_servo = servo("claw_servo")

    def run(self):
        self.main_loop()

    def main_loop(self):
        # Tank drive
        left_power = -gamepad1.left_stick_y
        right_power = -gamepad1.right_stick_y
        
        self.left_drive.set_power(left_power)
        self.right_drive.set_power(right_power)
        
        # Claw control
        if gamepad1.a_button:
            self.claw_servo.set_position(0.0)  # Open
        elif gamepad1.b_button:
            self.claw_servo.set_position(1.0)  # Close
        
        telemetry_add("Left Power", left_power)
        telemetry_add("Right Power", right_power)
```

### 3. Transpile to Java

```bash
# Transpile all Python files
make transpile

# Or transpile specific file
make transpile-file FILE=robot/MyRobot.py
```

### 4. Use Generated Java

Copy the generated Java files from `TeamCode/` to your FTC project and deploy!

## 📚 Make Commands

```bash
make help              # Show all available commands
make quickstart        # Complete setup with sample robot
make transpile         # Transpile all Python files to Java
make transpile-file    # Transpile specific file
make validate          # Validate Python syntax
make clean             # Remove generated files
make test              # Run transpiler tests
make examples          # Transpile example files
make watch             # Auto-transpile on file changes
make version           # Show version information
```

## 🔍 Version Control Strategy

### What to Commit ✅
- Python robot files in `robot/`
- Project configuration
- Documentation
- Git submodule reference

### What NOT to Commit ❌
- Generated Java files in `TeamCode/`
- Log files
- Temporary files

The setup automatically creates a proper `.gitignore` file.

## 📖 DSL Syntax Examples

### Hardware Declaration
```python
def init_hardware(self):
    self.motor = motor("config_name", "direction")
    self.servo = servo("config_name")
    self.sensor = distance_sensor("config_name")
```

### Control Logic
```python
def main_loop(self):
    # Gamepad input
    drive = -gamepad1.left_stick_y
    turn = gamepad1.right_stick_x
    
    # Motor control
    self.left_motor.set_power(drive + turn)
    self.right_motor.set_power(drive - turn)
    
    # Conditional logic
    if gamepad1.a_button:
        self.servo.set_position(1.0)
    
    # Telemetry
    telemetry_add("Drive", drive)
```

### Advanced Features
```python
# AprilTag Detection
@autonomous("Vision Auto", "Advanced")
class VisionRobot:
    def init_hardware(self):
        self.camera = webcam("Webcam 1")
        self.apriltag = apriltag_processor()
        self.portal = vision_portal(self.camera, self.apriltag)
    
    def run(self):
        detections = self.apriltag.get_detections()
        for detection in detections:
            tag_id = detection.id
            distance = detection.ftc_pose.range
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test file
cd py2java-ftc-dsl && python -m pytest tests/test_transpiler.py -v

# Run with coverage
cd py2java-ftc-dsl && python -m pytest tests/ --cov=src --cov-report=html
```

## 📖 Documentation

- **[FTC Team Guide](docs/FTC_TEAM_GUIDE.md)**: Complete team integration guide
- **[Getting Started](docs/GETTING_STARTED.md)**: Quick start tutorial
- **[API Reference](docs/API_REFERENCE.md)**: Complete syntax reference
- **[Examples](examples/)**: Working robot examples

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `docs/` directory
- **Issues**: Report bugs on GitHub Issues
- **FTC Community**: Share on FTC Discord and forums

## 🔮 Roadmap

- [ ] Enhanced error handling and debugging
- [ ] Visual programming interface
- [ ] Real-time code preview
- [ ] Integration with FTC simulator
- [ ] Advanced path planning DSL
- [ ] Multi-robot coordination syntax

---

**Happy Coding! 🤖**

*Made with ❤️ for the FTC community*

## 📚 DSL Syntax Reference

### Hardware Declaration

```python
# Motors
self.motor_name = motor("config_name", "direction")  # direction: "forward" or "reverse"

# Servos
self.servo_name = servo("config_name")

# Sensors
self.distance_sensor = distance_sensor("config_name")
self.color_sensor = color_sensor("config_name")
self.touch_sensor = touch_sensor("config_name")
self.imu = imu("config_name")
```

### OpMode Types

```python
@teleop("OpMode Name", "Group Name")
class TeleOpRobot:
    # TeleOp implementation

@autonomous("OpMode Name", "Group Name")
class AutonomousRobot:
    # Autonomous implementation
```

### Motor Control

```python
# Basic power control
motor.set_power(0.5)  # 50% power

# Encoder modes
motor.set_mode("run_using_encoder")
motor.set_mode("run_without_encoder")
motor.set_mode("run_to_position")
motor.set_mode("stop_and_reset_encoder")

# Position control
motor.set_target_position(1000)
current_pos = motor.get_current_position()
```

### Sensor Reading

```python
# Distance sensor
distance = distance_sensor.get_distance()  # Returns distance in cm

# Color sensor
color = color_sensor.get_color()

# Touch sensor
is_pressed = touch_sensor.is_pressed()

# IMU
heading = imu.get_heading()
pitch = imu.get_pitch()
roll = imu.get_roll()
```

### Gamepad Input

```python
# Analog inputs
drive = gamepad1.left_stick_y
turn = gamepad1.right_stick_x

# Button inputs
if gamepad1.a_button:
    # A button pressed
if gamepad1.dpad_up:
    # D-pad up pressed

# Triggers and bumpers
if gamepad1.left_trigger > 0.5:
    # Left trigger pressed
if gamepad1.right_bumper:
    # Right bumper pressed
```

### Telemetry

```python
telemetry_add("Key", "Value")
telemetry_add("Motor Power", motor_power)
```

## 🔍 Advanced Features

### AprilTag Detection

```python
@autonomous("AprilTag Auto", "Vision")
class AprilTagRobot:
    def init_hardware(self):
        self.webcam = webcam("Webcam 1")
        self.apriltag_processor = apriltag_processor()
        self.vision_portal = vision_portal(self.webcam, self.apriltag_processor)
    
    def run(self):
        detections = self.apriltag_processor.get_detections()
        for detection in detections:
            tag_id = detection.id
            range_distance = detection.ftc_pose.range
            bearing = detection.ftc_pose.bearing
```

### TensorFlow Object Detection

```python
@autonomous("TensorFlow Auto", "Machine Learning")
class TensorFlowRobot:
    def init_hardware(self):
        self.webcam = webcam("Webcam 1")
        self.tensorflow_processor = tensorflow_processor()
        self.vision_portal = vision_portal(self.webcam, self.tensorflow_processor)
    
    def run(self):
        recognitions = self.tensorflow_processor.get_recognitions()
        for recognition in recognitions:
            label = recognition.label
            confidence = recognition.confidence
```

### Mobile Dashboard Integration

```python
@teleop("Dashboard Robot", "Advanced")
class DashboardRobot:
    def init_dashboard(self):
        dashboard_register("Drive Speed", 1.0)
        dashboard_register("Auto Align", True)
    
    def run(self):
        drive_speed = dashboard_get("Drive Speed")
        auto_align = dashboard_get("Auto Align")
        
        dashboard_packet = {"speed": drive_speed, "mode": "teleop"}
        dashboard_send_packet(dashboard_packet)
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_transpiler.py

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Structure

- `test_transpiler.py`: Core transpiler functionality
- `test_examples.py`: Example code transpilation
- `test_data/`: Input Python files and expected Java outputs

## 📖 Examples

### Basic TeleOp Robot
- Simple tank drive
- Servo control
- Basic telemetry

### AprilTag Detection
- Camera initialization
- Tag detection and tracking
- Autonomous navigation to tags

### TensorFlow Object Detection
- Machine learning model loading
- Object recognition and classification
- Autonomous object interaction

### Mobile Controller
- Advanced gamepad controls
- Custom dashboard integration
- Real-time telemetry and configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add unit tests for new features
- Update documentation for API changes
- Test transpilation with real FTC hardware when possible

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `docs/` directory for detailed guides
- **Issues**: Report bugs and request features on GitHub Issues
- **Discussions**: Join the GitHub Discussions for questions and community support
- **FTC Community**: Share your experience on the FTC Discord and forums

## 🙏 Acknowledgments

- FIRST Tech Challenge community for inspiration and feedback
- FTC SDK developers for the robust hardware abstraction layer
- Python AST documentation and examples
- Contributors and beta testers

## 🔮 Roadmap

- [ ] Enhanced error handling and debugging
- [ ] Support for custom sensor libraries
- [ ] Visual programming interface
- [ ] Real-time code preview
- [ ] Integration with FTC simulator
- [ ] Advanced path planning DSL
- [ ] Multi-robot coordination syntax

---

**Happy Coding! 🤖**

*Made with ❤️ for the FTC community*
