# FTC Python DSL Transpiler Makefile
# Provides commands for transpiling Python robot code to Java using ftc_transpiler.py

# Configuration
PYTHON := python3
TRANSPILER_DIR := py2java-ftc-dsl
TRANSPILER := $(TRANSPILER_DIR)/src/ftc_transpiler.py
SRC_DIR := robot
JAVA_DIR := TeamCode/src/main/java/org/firstinspires/ftc/teamcode
EXAMPLES_DIR := $(TRANSPILER_DIR)/examples

# Default target
.PHONY: help
help:
	@echo "FTC Python DSL Transpiler"
	@echo "========================="
	@echo ""
	@echo "Available commands:"
	@echo "  make transpile          - Transpile all Python files to Java"
	@echo "  make transpile-file FILE=<file.py> - Transpile specific file"
	@echo "  make clean              - Remove generated Java files"
	@echo "  make setup              - Set up project structure"
	@echo "  make test               - Run transpiler tests"
	@echo "  make validate           - Validate Python syntax"
	@echo "  make examples           - Transpile example files"
	@echo "  make watch              - Watch for changes and auto-transpile"
	@echo "  make install            - Install dependencies"
	@echo "  make version            - Show version information"
	@echo "  make sample             - Create sample robot file"
	@echo "  make quickstart         - Complete setup with sample"
	@echo ""
	@echo "Version Management:"
	@echo "  make bump-major         - Bump major version (X.0.0)"
	@echo "  make bump-minor         - Bump minor version (x.X.0)"
	@echo "  make bump-patch         - Bump patch version (x.x.X)"
	@echo "  make release-major      - Bump major version, commit and create git tag"
	@echo "  make release-minor      - Bump minor version, commit and create git tag"
	@echo "  make release-patch      - Bump patch version, commit and create git tag"
	@echo "  make set-version VERSION=X.Y.Z - Set specific version"
	@echo ""
	@echo "Project structure:"
	@echo "  robot/                  - Your Python robot code (version controlled)"
	@echo "  TeamCode/               - Generated Java code (not version controlled)"
	@echo "  py2java-ftc-dsl/        - Transpiler submodule"

# Check if transpiler exists
check-transpiler:
	@if [ ! -f "$(TRANSPILER)" ]; then \
		echo "Error: Transpiler not found at $(TRANSPILER)"; \
		echo "Make sure py2java-ftc-dsl is added as a git submodule"; \
		echo "Run: git submodule add https://github.com/anshumanrudra/py2java-ftc-dsl.git"; \
		echo "Then: git submodule update --init --recursive"; \
		exit 1; \
	fi

# Install dependencies
.PHONY: install
install: check-transpiler
	@echo "Installing dependencies..."
	@if [ -f "$(TRANSPILER_DIR)/requirements.txt" ]; then \
		pip install -r $(TRANSPILER_DIR)/requirements.txt; \
	fi
	@echo "Dependencies installed successfully!"

# Set up project structure
.PHONY: setup
setup: check-transpiler
	@echo "Setting up project structure..."
	@mkdir -p $(SRC_DIR)
	@mkdir -p $(JAVA_DIR)
	@mkdir -p logs
	@if [ ! -f $(SRC_DIR)/README.md ]; then \
		echo "# Robot Python Code" > $(SRC_DIR)/README.md; \
		echo "" >> $(SRC_DIR)/README.md; \
		echo "Place your Python robot files here." >> $(SRC_DIR)/README.md; \
		echo "Use \`make transpile\` to generate Java code." >> $(SRC_DIR)/README.md; \
	fi
	@if [ ! -f .gitignore ]; then \
		echo "# Generated Java files" > .gitignore; \
		echo "TeamCode/" >> .gitignore; \
		echo "*.java" >> .gitignore; \
		echo "" >> .gitignore; \
		echo "# Logs and temporary files" >> .gitignore; \
		echo "logs/" >> .gitignore; \
		echo "*.log" >> .gitignore; \
		echo "*.tmp" >> .gitignore; \
		echo "" >> .gitignore; \
		echo "# Python cache" >> .gitignore; \
		echo "__pycache__/" >> .gitignore; \
		echo "*.pyc" >> .gitignore; \
		echo "*.pyo" >> .gitignore; \
		echo "" >> .gitignore; \
		echo "# IDE files" >> .gitignore; \
		echo ".vscode/" >> .gitignore; \
		echo ".idea/" >> .gitignore; \
		echo "*.swp" >> .gitignore; \
		echo "*.swo" >> .gitignore; \
	fi
# Validate Python syntax
.PHONY: validate
validate: check-transpiler
	@echo "Validating Python syntax..."
	@error_count=0; \
	for file in $(SRC_DIR)/*.py; do \
		if [ -f "$$file" ]; then \
			echo "Checking $$file..."; \
			$(PYTHON) -m py_compile "$$file" 2>/dev/null; \
			if [ $$? -ne 0 ]; then \
				echo "✗ Syntax error in $$file"; \
				$(PYTHON) -m py_compile "$$file"; \
				error_count=$$((error_count + 1)); \
			else \
				echo "✓ $$file syntax OK"; \
			fi; \
		fi; \
	done; \
	if [ $$error_count -gt 0 ]; then \
		echo "Found $$error_count syntax errors. Please fix before transpiling."; \
		exit 1; \
	fi
	@echo "All Python files have valid syntax!"

# Transpile all Python files using ftc_transpiler.py
.PHONY: transpile
transpile: check-transpiler validate
	@echo "Transpiling Python files to Java using ftc_transpiler.py..."
	@mkdir -p $(JAVA_DIR)
	@mkdir -p logs
	@echo "Transpilation started at $$(date)" > logs/transpile.log
	@count=0; \
	for file in $(SRC_DIR)/*.py; do \
		if [ -f "$$file" ]; then \
			basename=$$(basename "$$file" .py); \
			java_file="$(JAVA_DIR)/$${basename}.java"; \
			echo "Transpiling $$file -> $$java_file"; \
			echo "Command: $(PYTHON) $(TRANSPILER) $$file $$java_file" >> logs/transpile.log; \
			$(PYTHON) $(TRANSPILER) "$$file" "$$java_file" 2>&1 | tee -a logs/transpile.log; \
			if [ $$? -eq 0 ]; then \
				echo "✓ Successfully transpiled $$file" | tee -a logs/transpile.log; \
				count=$$((count + 1)); \
			else \
				echo "✗ Failed to transpile $$file" | tee -a logs/transpile.log; \
			fi; \
		fi; \
	done; \
	echo "Transpilation completed: $$count files processed" | tee -a logs/transpile.log
	@echo "Java files generated in $(JAVA_DIR)/"

# Transpile specific file using ftc_transpiler.py
.PHONY: transpile-file
transpile-file: check-transpiler
	@if [ -z "$(FILE)" ]; then \
		echo "Error: Please specify FILE=<filename.py>"; \
		echo "Example: make transpile-file FILE=robot/MyRobot.py"; \
		exit 1; \
	fi
	@if [ ! -f "$(FILE)" ]; then \
		echo "Error: File $(FILE) not found"; \
		exit 1; \
	fi
	@echo "Transpiling $(FILE) using ftc_transpiler.py..."
	@mkdir -p $(JAVA_DIR)
	@mkdir -p logs
	@basename=$$(basename "$(FILE)" .py)
	@java_file="$(JAVA_DIR)/$${basename}.java"
	@echo "Output: $$java_file"
	@echo "Command: $(PYTHON) $(TRANSPILER) $(FILE) $$java_file" | tee logs/transpile-file.log
	@$(PYTHON) $(TRANSPILER) "$(FILE)" "$$java_file" 2>&1 | tee -a logs/transpile-file.log
	@if [ $$? -eq 0 ]; then \
		echo "✓ Successfully transpiled $(FILE)"; \
	else \
		echo "✗ Failed to transpile $(FILE)"; \
		exit 1; \
	fi

# Clean generated files
.PHONY: clean
clean:
	@echo "Cleaning generated Java files..."
	@rm -rf $(JAVA_DIR)/*.java
	@rm -rf logs/*.log
	@echo "Clean completed!"

# Run tests
.PHONY: test
test: check-transpiler
	@echo "Running transpiler tests..."
	@cd $(TRANSPILER_DIR) && $(PYTHON) -m pytest tests/ -v
	@echo "Tests completed!"

# Transpile examples using ftc_transpiler.py
.PHONY: examples
examples: check-transpiler
	@echo "Transpiling example files using ftc_transpiler.py..."
	@mkdir -p examples-java
	@for file in $(EXAMPLES_DIR)/*.py; do \
		if [ -f "$$file" ]; then \
			basename=$$(basename "$$file" .py); \
			java_file="examples-java/$${basename}.java"; \
			echo "Transpiling $$file -> $$java_file"; \
			$(PYTHON) $(TRANSPILER) "$$file" "$$java_file"; \
		fi; \
	done
	@echo "Example Java files generated in examples-java/"

# Watch for changes and auto-transpile
.PHONY: watch
watch: check-transpiler
	@echo "Watching for changes in $(SRC_DIR)/ ..."
	@echo "Press Ctrl+C to stop"
	@touch .last_transpile
	@while true; do \
		find $(SRC_DIR) -name "*.py" -newer .last_transpile 2>/dev/null | head -1 | grep -q . && { \
			echo "Changes detected, transpiling..."; \
			make transpile; \
			touch .last_transpile; \
		}; \
		sleep 2; \
	done

# Show version information
.PHONY: version
version: check-transpiler
	@cd $(TRANSPILER_DIR) && $(PYTHON) src/version_manager.py --show

# Version bumping commands using version manager script
.PHONY: bump-version-major
bump-version-major: check-transpiler
	@echo "Bumping major version..."
	@cd $(TRANSPILER_DIR) && $(PYTHON) src/version_manager.py --bump major
	@echo "Major version bump complete!"
	@echo "To commit and tag: make release-major"

.PHONY: bump-version-minor
bump-version-minor: check-transpiler
	@echo "Bumping minor version..."
	@cd $(TRANSPILER_DIR) && $(PYTHON) src/version_manager.py --bump minor
	@echo "Minor version bump complete!"
	@echo "To commit and tag: make release-minor"

.PHONY: bump-version-patch
bump-version-patch: check-transpiler
	@echo "Bumping patch version..."
	@cd $(TRANSPILER_DIR) && $(PYTHON) src/version_manager.py --bump patch
	@echo "Patch version bump complete!"
	@echo "To commit and tag: make release-patch"

# Convenience aliases for version bumping
.PHONY: bump-major bump-minor bump-patch
bump-major: bump-version-major
bump-minor: bump-version-minor  
bump-patch: bump-version-patch

# Release workflow - bump version, commit, and tag using version manager
.PHONY: release-major release-minor release-patch
release-major: check-transpiler
	@echo "Creating major release..."
	@cd $(TRANSPILER_DIR) && $(PYTHON) src/version_manager.py --bump major --commit --tag
	@echo "Major release complete! 🚀"

release-minor: check-transpiler
	@echo "Creating minor release..."
	@cd $(TRANSPILER_DIR) && $(PYTHON) src/version_manager.py --bump minor --commit --tag
	@echo "Minor release complete! 🚀"

release-patch: check-transpiler
	@echo "Creating patch release..."
	@cd $(TRANSPILER_DIR) && $(PYTHON) src/version_manager.py --bump patch --commit --tag
	@echo "Patch release complete! 🚀"

# Set specific version
.PHONY: set-version
set-version: check-transpiler
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: Please specify VERSION=X.Y.Z"; \
		echo "Example: make set-version VERSION=1.2.3"; \
		exit 1; \
	fi
	@echo "Setting version to $(VERSION)..."
	@cd $(TRANSPILER_DIR) && $(PYTHON) src/version_manager.py --set $(VERSION)
	@echo "Version set to $(VERSION)"

# Create a sample robot file
.PHONY: sample
sample: setup
	@if [ ! -f $(SRC_DIR)/SampleRobot.py ]; then \
		echo "Creating sample robot file..."; \
		cat > $(SRC_DIR)/SampleRobot.py << 'EOF'; \
# Sample FTC Robot using Python DSL\
# This file demonstrates basic robot functionality\
\
@teleop("Sample Robot", "Learning")\
class SampleRobot:\
    def init_hardware(self):\
        # Drive motors\
        self.left_drive = motor("left_drive", "forward")\
        self.right_drive = motor("right_drive", "reverse")\
        \
        # Manipulator\
        self.arm_motor = motor("arm_motor", "forward")\
        self.claw_servo = servo("claw_servo")\
        \
        # Sensors\
        self.distance_sensor = distance_sensor("distance")\
    \
    def run(self):\
        self.main_loop()\
    \
    def main_loop(self):\
        # Tank drive\
        left_power = -gamepad1.left_stick_y\
        right_power = -gamepad1.right_stick_y\
        \
        self.left_drive.set_power(left_power)\
        self.right_drive.set_power(right_power)\
        \
        # Arm control\
        arm_power = -gamepad2.left_stick_y\
        self.arm_motor.set_power(arm_power)\
        \
        # Claw control\
        if gamepad1.a_button:\
            self.claw_servo.set_position(0.0)  # Open\
        elif gamepad1.b_button:\
            self.claw_servo.set_position(1.0)  # Close\
        \
        # Safety check\
        distance = self.distance_sensor.get_distance()\
        if distance < 10:\
            self.left_drive.set_power(0)\
            self.right_drive.set_power(0)\
            telemetry_add("Warning", "OBSTACLE!")\
        \
        # Telemetry\
        telemetry_add("Left Power", left_power)\
        telemetry_add("Right Power", right_power)\
        telemetry_add("Distance", distance)\
EOF\
		echo "Sample robot created: $(SRC_DIR)/SampleRobot.py"; \
		echo "Run 'make transpile' to generate Java code"; \
	else \
		echo "Sample robot already exists: $(SRC_DIR)/SampleRobot.py"; \
	fi

# Quick start - set up everything and create sample
.PHONY: quickstart
quickstart: setup sample
	@echo ""
	@echo "🚀 Quick Start Complete!"
	@echo "======================="
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit robot/SampleRobot.py or create your own Python files"
	@echo "2. Run 'make transpile' to generate Java code"
	@echo "3. Copy generated Java files from TeamCode/ to your FTC project"
	@echo ""
	@echo "Useful commands:"
	@echo "  make transpile      - Convert Python to Java"
	@echo "  make validate       - Check Python syntax"
	@echo "  make clean          - Remove generated files"
	@echo "  make help           - Show all commands"
