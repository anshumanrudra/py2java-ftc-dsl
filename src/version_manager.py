#!/usr/bin/env python3
"""
Version Management Utility for FTC Python DSL Transpiler

Handles semantic versioning with proper validation and git integration.
Supports major.minor.patch versioning scheme.

Usage:
    python version_manager.py --bump major|minor|patch [--commit] [--tag]
    python version_manager.py --show
    python version_manager.py --set X.Y.Z
"""

import argparse
import re
import subprocess
import sys
import os
from pathlib import Path

class VersionManager:
    def __init__(self, version_file="VERSION"):
        self.version_file = Path(version_file)
        self.version_pattern = re.compile(r'^(\d+)\.(\d+)\.(\d+)$')
    
    def get_current_version(self):
        """Get the current version from VERSION file"""
        if not self.version_file.exists():
            return "0.0.0"
        
        with open(self.version_file, 'r') as f:
            version = f.read().strip()
        
        if not self.version_pattern.match(version):
            raise ValueError(f"Invalid version format in {self.version_file}: {version}")
        
        return version
    
    def parse_version(self, version_string):
        """Parse version string into major, minor, patch components"""
        match = self.version_pattern.match(version_string)
        if not match:
            raise ValueError(f"Invalid version format: {version_string}")
        
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    
    def format_version(self, major, minor, patch):
        """Format version components into version string"""
        return f"{major}.{minor}.{patch}"
    
    def set_version(self, new_version):
        """Set version to specific value"""
        # Validate format
        self.parse_version(new_version)
        
        with open(self.version_file, 'w') as f:
            f.write(new_version)
        
        return new_version
    
    def bump_version(self, bump_type):
        """Bump version by specified type (major, minor, patch)"""
        current_version = self.get_current_version()
        major, minor, patch = self.parse_version(current_version)
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        new_version = self.format_version(major, minor, patch)
        self.set_version(new_version)
        
        return current_version, new_version
    
    def is_git_repo(self):
        """Check if current directory is a git repository"""
        try:
            subprocess.run(['git', 'rev-parse', '--git-dir'], 
                         check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def git_commit_version(self, version):
        """Commit version change to git"""
        if not self.is_git_repo():
            print("Warning: Not in a git repository, skipping commit")
            return False
        
        try:
            subprocess.run(['git', 'add', str(self.version_file)], check=True)
            subprocess.run(['git', 'commit', '-m', f'Bump version to {version}'], check=True)
            print(f"✓ Committed version {version}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error committing version: {e}")
            return False
    
    def git_tag_version(self, version):
        """Create git tag for version"""
        if not self.is_git_repo():
            print("Warning: Not in a git repository, skipping tag")
            return False
        
        tag_name = f"v{version}"
        try:
            subprocess.run(['git', 'tag', tag_name], check=True)
            print(f"✓ Created tag {tag_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating tag: {e}")
            return False
    
    def get_git_status(self):
        """Get git status information"""
        if not self.is_git_repo():
            return None
        
        try:
            # Check if there are uncommitted changes
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, check=True)
            has_changes = bool(result.stdout.strip())
            
            # Get current branch
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, check=True)
            current_branch = result.stdout.strip()
            
            # Get latest commit
            result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], 
                                  capture_output=True, text=True, check=True)
            latest_commit = result.stdout.strip()
            
            return {
                'has_changes': has_changes,
                'current_branch': current_branch,
                'latest_commit': latest_commit
            }
        except subprocess.CalledProcessError:
            return None

def main():
    parser = argparse.ArgumentParser(description='FTC Python DSL Version Manager')
    parser.add_argument('--bump', choices=['major', 'minor', 'patch'], 
                       help='Bump version by specified type')
    parser.add_argument('--set', metavar='VERSION', 
                       help='Set version to specific value (e.g., 1.2.3)')
    parser.add_argument('--show', action='store_true', 
                       help='Show current version information')
    parser.add_argument('--commit', action='store_true', 
                       help='Commit version change to git')
    parser.add_argument('--tag', action='store_true', 
                       help='Create git tag for version')
    parser.add_argument('--version-file', default='VERSION', 
                       help='Path to version file (default: VERSION)')
    
    args = parser.parse_args()
    
    # Change to script directory to find VERSION file
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    
    vm = VersionManager(args.version_file)
    
    try:
        if args.show:
            current_version = vm.get_current_version()
            print(f"Current version: {current_version}")
            
            git_status = vm.get_git_status()
            if git_status:
                print(f"Git branch: {git_status['current_branch']}")
                print(f"Latest commit: {git_status['latest_commit']}")
                print(f"Uncommitted changes: {'Yes' if git_status['has_changes'] else 'No'}")
            else:
                print("Git status: Not a git repository")
        
        elif args.set:
            old_version = vm.get_current_version()
            new_version = vm.set_version(args.set)
            print(f"Version changed from {old_version} to {new_version}")
            
            if args.commit:
                vm.git_commit_version(new_version)
            
            if args.tag:
                vm.git_tag_version(new_version)
        
        elif args.bump:
            old_version, new_version = vm.bump_version(args.bump)
            print(f"Version bumped from {old_version} to {new_version}")
            
            if args.commit:
                vm.git_commit_version(new_version)
            
            if args.tag:
                vm.git_tag_version(new_version)
        
        else:
            parser.print_help()
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
