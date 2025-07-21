# Version Management Guide

This guide explains how to manage versions of the FTC Python DSL Transpiler using semantic versioning.

## Semantic Versioning

The project follows [Semantic Versioning](https://semver.org/) with the format `MAJOR.MINOR.PATCH`:

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backwards compatible manner  
- **PATCH**: Backwards compatible bug fixes

## Version Management Commands

### Show Current Version

```bash
# Show detailed version information
make version
```

Output example:
```
Current version: 1.2.3
Git branch: main
Latest commit: abc1234
Uncommitted changes: No
```

### Bump Version

#### Patch Version (Bug Fixes)
```bash
# Bump patch version: 1.2.3 → 1.2.4
make bump-patch
```

#### Minor Version (New Features)
```bash
# Bump minor version: 1.2.3 → 1.3.0
make bump-minor
```

#### Major Version (Breaking Changes)
```bash
# Bump major version: 1.2.3 → 2.0.0
make bump-major
```

### Set Specific Version

```bash
# Set to specific version
make set-version VERSION=1.5.0
```

### Create Releases

Release commands automatically bump version, commit changes, and create git tags:

```bash
# Create patch release
make release-patch

# Create minor release  
make release-minor

# Create major release
make release-major
```

## Release Workflow

### For Maintainers

1. **Prepare Release**:
   ```bash
   # Ensure clean working directory
   git status
   
   # Pull latest changes
   git pull origin main
   ```

2. **Create Release**:
   ```bash
   # For bug fixes
   make release-patch
   
   # For new features
   make release-minor
   
   # For breaking changes
   make release-major
   ```

3. **Push Release**:
   ```bash
   # Push commits and tags
   git push origin main --tags
   ```

### For FTC Teams Using Submodules

1. **Update to Latest Release**:
   ```bash
   # Update submodule to latest tag
   cd py2java-ftc-dsl
   git fetch --tags
   git checkout $(git describe --tags --abbrev=0)
   cd ..
   
   # Commit submodule update
   git add py2java-ftc-dsl
   git commit -m "Update transpiler to $(cd py2java-ftc-dsl && git describe --tags --abbrev=0)"
   ```

2. **Use Specific Version**:
   ```bash
   # Update to specific version
   cd py2java-ftc-dsl
   git checkout v1.2.3
   cd ..
   
   # Commit specific version
   git add py2java-ftc-dsl
   git commit -m "Pin transpiler to v1.2.3"
   ```

## Version History

### Version 1.x.x
- Initial release with basic transpilation
- Support for TeleOp and Autonomous modes
- Hardware abstraction layer

### Planned Versions

#### v1.1.0 (Minor)
- Enhanced error handling
- Additional sensor support
- Improved telemetry features

#### v1.2.0 (Minor)
- Vision processing improvements
- TensorFlow integration enhancements
- Mobile dashboard features

#### v2.0.0 (Major)
- Breaking API changes
- New DSL syntax features
- Performance improvements

## Advanced Version Management

### Using the Version Manager Script Directly

The version manager script provides more advanced options:

```bash
# Show version with git status
python src/version_manager.py --show

# Bump version without Make
python src/version_manager.py --bump patch

# Bump and commit in one step
python src/version_manager.py --bump minor --commit

# Bump, commit, and tag
python src/version_manager.py --bump major --commit --tag

# Set specific version
python src/version_manager.py --set 2.0.0-beta.1
```

### Pre-release Versions

For pre-release versions, use the script directly:

```bash
# Create beta version
python src/version_manager.py --set 1.3.0-beta.1

# Create release candidate
python src/version_manager.py --set 1.3.0-rc.1
```

### Version Validation

The version manager validates version formats:

- ✅ Valid: `1.0.0`, `2.5.10`, `10.0.1`
- ❌ Invalid: `1.0`, `v1.0.0`, `1.0.0-SNAPSHOT`

## Git Integration

### Automatic Git Operations

Release commands automatically:
1. Add VERSION file to git
2. Create commit with version message
3. Create annotated git tag

### Manual Git Operations

If you prefer manual control:

```bash
# Bump version only
make bump-patch

# Then manually commit and tag
git add VERSION
git commit -m "Bump version to $(cat py2java-ftc-dsl/VERSION)"
git tag "v$(cat py2java-ftc-dsl/VERSION)"
```

### Tag Format

Git tags follow the format `vX.Y.Z`:
- `v1.0.0` - Major release
- `v1.1.0` - Minor release  
- `v1.1.1` - Patch release

## Best Practices

### When to Bump Versions

#### Patch Version (1.0.0 → 1.0.1)
- Bug fixes
- Documentation updates
- Internal refactoring
- Performance improvements (no API changes)

#### Minor Version (1.0.0 → 1.1.0)
- New DSL features
- New hardware support
- New examples
- Backwards compatible API additions

#### Major Version (1.0.0 → 2.0.0)
- Breaking DSL syntax changes
- Removed deprecated features
- Major architecture changes
- Incompatible API changes

### Release Checklist

Before creating a release:

- [ ] All tests pass: `make test`
- [ ] Documentation is updated
- [ ] Examples work with new version
- [ ] CHANGELOG.md is updated
- [ ] No uncommitted changes
- [ ] On main/master branch

### FTC Team Guidelines

#### For Competition Season
- Use stable releases (avoid pre-releases)
- Pin to specific versions: `git checkout v1.2.3`
- Test thoroughly before updating

#### For Off-Season Development
- Can use latest releases
- Help test pre-release versions
- Provide feedback on new features

## Troubleshooting

### Common Issues

**Issue**: `Version file not found`
**Solution**: Ensure you're in the transpiler directory or submodule

**Issue**: `Not a git repository`
**Solution**: Version bumping works, but git operations are skipped

**Issue**: `Uncommitted changes`
**Solution**: Commit or stash changes before creating releases

### Recovery

If version gets corrupted:

```bash
# Reset to last known good version
git checkout HEAD -- VERSION

# Or set manually
make set-version VERSION=1.2.3
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Release
on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Create Release
        run: |
          VERSION=${GITHUB_REF#refs/tags/v}
          echo "Creating release for version $VERSION"
          # Add release automation here
```

### Automated Version Bumping

```yaml
name: Auto Version Bump
on:
  push:
    branches: [main]

jobs:
  bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Bump Version
        run: |
          if [[ ${{ github.event.head_commit.message }} == *"[major]"* ]]; then
            make release-major
          elif [[ ${{ github.event.head_commit.message }} == *"[minor]"* ]]; then
            make release-minor
          else
            make release-patch
          fi
```

This allows version bumping based on commit messages:
- `fix: bug fix [patch]` → patch version
- `feat: new feature [minor]` → minor version  
- `feat!: breaking change [major]` → major version
