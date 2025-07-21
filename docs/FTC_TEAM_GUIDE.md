# FTC Team Integration Guide

This guide shows how FTC teams can integrate the Python DSL transpiler into their workflow using git submodules.

## Quick Setup for FTC Teams

### Step 1: Add as Git Submodule

In your FTC project root directory:

```bash
# Add the transpiler as a submodule
git submodule add https://github.com/anshumanrudra/py2java-ftc-dsl.git

# Initialize and update the submodule
git submodule update --init --recursive

# Commit the submodule addition
git add .gitmodules py2java-ftc-dsl
git commit -m "Add Python DSL transpiler submodule"
```

### Step 2: Set Up Project Structure

```bash
# Set up the project structure and create sample files
make quickstart
```

This creates:
- `robot/` - Directory for your Python robot code (version controlled)
- `TeamCode/` - Generated Java code (not version controlled)
- `.gitignore` - Configured to ignore generated Java files
- `robot/SampleRobot.py` - Sample robot to get started

### Step 3: Write Your Robot in Python

Edit `robot/SampleRobot.py` or create new Python files in the `robot/` directory:

```python
@teleop("My Team Robot", "Competition")
class MyTeamRobot:
    def init_hardware(self):
        # Define your robot's hardware
        self.left_drive = motor("left_drive", "forward")
        self.right_drive = motor("right_drive", "reverse")
        self.arm_motor = motor("arm_motor", "forward")
        self.claw_servo = servo("claw_servo")
        
    def run(self):
        self.main_loop()
        
    def main_loop(self):
        # Your robot control logic
        drive = -gamepad1.left_stick_y
        turn = gamepad1.right_stick_x
        
        self.left_drive.set_power(drive + turn)
        self.right_drive.set_power(drive - turn)
        
        # Add more robot logic here
```

### Step 4: Transpile to Java

```bash
# Transpile all Python files to Java
make transpile

# Or transpile a specific file
make transpile-file FILE=robot/MyTeamRobot.py
```

### Step 5: Copy to FTC Project

The generated Java files are in `TeamCode/src/main/java/org/firstinspires/ftc/teamcode/`. Copy these to your actual FTC project's TeamCode directory.

## Daily Workflow

### Development Cycle

1. **Edit Python Code**: Modify files in `robot/` directory
2. **Validate Syntax**: `make validate`
3. **Transpile**: `make transpile`
4. **Test**: Copy Java files to FTC project and test
5. **Commit**: Only commit Python files, not generated Java

### Useful Commands

```bash
# Show all available commands
make help

# Validate Python syntax before transpiling
make validate

# Transpile all Python files
make transpile

# Transpile specific file
make transpile-file FILE=robot/MyRobot.py

# Clean generated files
make clean

# Watch for changes and auto-transpile
make watch

# Run transpiler tests
make test

# Show version information
make version
```

## Version Control Strategy

### What to Commit

✅ **DO commit:**
- Python robot files in `robot/`
- Project configuration files
- Documentation and README files
- Git submodule reference

❌ **DON'T commit:**
- Generated Java files in `TeamCode/`
- Log files in `logs/`
- Temporary files

### .gitignore Configuration

The setup automatically creates a `.gitignore` file:

```gitignore
# Generated Java files
TeamCode/
*.java

# Logs and temporary files
logs/
*.log
*.tmp

# Python cache
__pycache__/
*.pyc
*.pyo

# IDE files
.vscode/
.idea/
*.swp
*.swo
```

## Team Collaboration

### Setting Up for New Team Members

When a new team member clones the repository:

```bash
# Clone the main repository
git clone <your-team-repo>
cd <your-team-repo>

# Initialize submodules
git submodule update --init --recursive

# Set up project structure
make setup

# Install dependencies (if needed)
make install
```

### Updating the Transpiler

To update to a newer version of the transpiler:

```bash
# Update submodule to latest version
cd py2java-ftc-dsl
git pull origin main
cd ..

# Commit the submodule update
git add py2java-ftc-dsl
git commit -m "Update Python DSL transpiler to latest version"
```

### Using Tagged Releases

To use a specific tagged release:

```bash
# Update submodule to specific tag
cd py2java-ftc-dsl
git checkout v1.0.0  # Replace with desired version
cd ..

# Commit the specific version
git add py2java-ftc-dsl
git commit -m "Pin Python DSL transpiler to v1.0.0"
```

## Project Structure

```
your-ftc-project/
├── py2java-ftc-dsl/           # Git submodule (transpiler)
│   ├── src/ftc_transpiler.py  # Main transpiler
│   ├── examples/              # Example Python robots
│   ├── tests/                 # Transpiler tests
│   └── docs/                  # Documentation
├── robot/                     # Your Python robot code (version controlled)
│   ├── SampleRobot.py
│   ├── AutonomousRobot.py
│   └── TeleOpRobot.py
├── TeamCode/                  # Generated Java code (not version controlled)
│   └── src/main/java/org/firstinspires/ftc/teamcode/
├── logs/                      # Transpilation logs (not version controlled)
├── Makefile                   # Build commands
├── .gitignore                 # Git ignore rules
└── README.md                  # Your project documentation
```

## Advanced Usage

### Custom Hardware Configurations

Create Python files for different robot configurations:

```python
# robot/CompetitionRobot.py
@teleop("Competition Robot", "Competition")
class CompetitionRobot:
    def init_hardware(self):
        # Competition robot hardware
        pass

# robot/PracticeRobot.py  
@teleop("Practice Robot", "Practice")
class PracticeRobot:
    def init_hardware(self):
        # Practice robot hardware
        pass
```

### Autonomous Programs

```python
# robot/RedAutonomous.py
@autonomous("Red Alliance Auto", "Competition")
class RedAutonomous:
    def init_hardware(self):
        # Hardware setup
        pass
        
    def run(self):
        # Autonomous logic
        pass
```

### Vision and Advanced Features

```python
# robot/VisionRobot.py
@autonomous("Vision Auto", "Advanced")
class VisionRobot:
    def init_hardware(self):
        self.webcam = webcam("Webcam 1")
        self.apriltag_processor = apriltag_processor()
        self.vision_portal = vision_portal(self.webcam, self.apriltag_processor)
        
    def run(self):
        # Vision-based autonomous
        detections = self.apriltag_processor.get_detections()
        # Process detections...
```

## Troubleshooting

### Common Issues

**Issue**: `make: command not found`
**Solution**: Install make utility or use commands directly:
```bash
python3 py2java-ftc-dsl/src/ftc_transpiler.py robot/MyRobot.py TeamCode/src/main/java/org/firstinspires/ftc/teamcode/MyRobot.java
```

**Issue**: Submodule not found
**Solution**: Initialize submodules:
```bash
git submodule update --init --recursive
```

**Issue**: Python syntax errors
**Solution**: Run validation:
```bash
make validate
```

**Issue**: Transpilation fails
**Solution**: Check logs:
```bash
cat logs/transpile.log
```

### Getting Help

1. **Check Documentation**: Read the full API reference in `py2java-ftc-dsl/docs/`
2. **Run Examples**: Try transpiling examples: `make examples`
3. **Test Installation**: Run tests: `make test`
4. **Check Issues**: Look at GitHub issues for known problems

## Best Practices

### Code Organization

1. **One Robot Per File**: Keep each robot class in its own Python file
2. **Descriptive Names**: Use clear, descriptive names for hardware and methods
3. **Consistent Structure**: Follow the same pattern across all robot files
4. **Comments**: Document complex logic and hardware configurations

### Testing Strategy

1. **Incremental Development**: Start simple and add features gradually
2. **Validate Early**: Run `make validate` frequently
3. **Test Transpilation**: Transpile and check generated Java regularly
4. **Hardware Testing**: Test on actual robot hardware frequently

### Team Workflow

1. **Code Reviews**: Review Python code before transpiling
2. **Shared Standards**: Establish team coding standards
3. **Documentation**: Document robot configurations and special procedures
4. **Backup Strategy**: Keep backups of working robot configurations

## Support and Community

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Complete API reference and examples
- **FTC Community**: Share experiences on FTC forums and Discord
- **Contributing**: Help improve the transpiler by contributing code or documentation

Happy coding! 🤖
