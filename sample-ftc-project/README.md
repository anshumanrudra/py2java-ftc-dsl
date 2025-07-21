# Sample FTC Team Project

This directory demonstrates how an FTC team would structure their project when using the Python DSL transpiler as a git submodule.

## Project Structure

```
sample-ftc-project/
├── py2java-ftc-dsl/           # Git submodule (this transpiler project)
├── robot/                     # Python robot code (version controlled)
│   ├── CompetitionRobot.py    # Main competition robot
│   ├── PracticeRobot.py       # Practice robot
│   ├── RedAutonomous.py       # Red alliance autonomous
│   └── BlueAutonomous.py      # Blue alliance autonomous
├── TeamCode/                  # Generated Java code (not version controlled)
│   └── src/main/java/org/firstinspires/ftc/teamcode/
├── logs/                      # Transpilation logs (not version controlled)
├── Makefile                   # Build commands (copied from submodule)
├── .gitignore                 # Ignores generated files
└── README.md                  # Team project documentation
```

## Setup Instructions

1. **Initialize as Git Repository**:
   ```bash
   git init
   git add README.md
   git commit -m "Initial commit"
   ```

2. **Add Transpiler Submodule**:
   ```bash
   git submodule add https://github.com/anshumanrudra/py2java-ftc-dsl.git
   git submodule update --init --recursive
   ```

3. **Copy Makefile**:
   ```bash
   cp py2java-ftc-dsl/Makefile .
   ```

4. **Set Up Project Structure**:
   ```bash
   make quickstart
   ```

5. **Start Coding**:
   - Edit Python files in `robot/` directory
   - Run `make transpile` to generate Java
   - Copy Java files to your FTC project

## Daily Workflow

1. **Edit Python Code**: Modify files in `robot/`
2. **Validate**: `make validate`
3. **Transpile**: `make transpile`
4. **Test**: Copy to FTC project and test on robot
5. **Commit**: Only commit Python files

## Version Control

- ✅ Commit: Python files, documentation, configuration
- ❌ Don't commit: Generated Java files, logs, temporary files

The `.gitignore` file is automatically configured to handle this.
