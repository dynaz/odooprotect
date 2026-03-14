# odooprotect

# OdooProtect - Advanced Python Code Obfuscator

![OdooProtect Logo](https://img.shields.io/badge/OdooProtect-Advanced%20Obfuscation-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.6+-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-%23FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/dynaz)

OdooProtect is a comprehensive Python code obfuscation tool with machine ID binding, designed to protect your Python applications from reverse engineering and unauthorized distribution.

## 🚀 Features

### Core Obfuscation
- **Variable Name Obfuscation**: Transforms readable variable names into obfuscated identifiers
- **String Encryption**: Encrypts string literals using base64 encoding
- **AST Transformation**: Advanced Abstract Syntax Tree manipulation
- **Import Protection**: Secures import statements and module loading

### Machine Binding & Licensing
- **Hardware Fingerprinting**: Generates unique machine identifiers based on CPU, MAC address, and disk serial
- **License Key Generation**: Creates signed license keys with expiration dates
- **Runtime Verification**: Validates licenses on every code execution
- **Tamper Detection**: Detects attempts to modify or bypass protection

### Project Protection
- **Directory Processing**: Obfuscates entire Python projects recursively
- **Package Structure Preservation**: Maintains original project structure
- **Unified Licensing**: Single license file for entire projects
- **Cross-Platform**: Works on Linux, Windows, and macOS

### Command Line Interface
- **Standalone Executable**: Run with `odooprotect` command after installation
- **Professional CLI**: Standard flag-based interface (`-i`, `-o`, `-m`, `-c`)
- **Easy Installation**: One-command setup with `./install.sh`
- **System Integration**: Available globally after installation

## 📋 Table of Contents

- [Installation](#installation)
  - [Quick Install (Recommended)](#quick-install-recommended)
  - [Manual Installation](#manual-installation)
  - [Docker Installation](#docker-installation)
  - [Development Installation](#development-installation)
  - [Advanced Installation](#advanced-installation)
  - [Post-Installation](#post-installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Command Line Options](#command-line-options)
- [Examples](#examples)
- [Security Features](#security-features)
- [Architecture](#architecture)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

Choose one of the installation methods below based on your needs.

### 📋 Prerequisites
- **Python 3.6 or higher** (3.9+ recommended for best performance)
- **pip package manager**
- **Git** (for cloning the repository)
- **sudo/admin privileges** (for system-wide installation)

---

## 🚀 Quick Install (Recommended)

### One-Command Installation
```bash
# Clone and install OdooProtect with standalone command
git clone https://github.com/dynaz/OdooProtect.git
cd OdooProtect
./install.sh
```

### Verify Installation
```bash
odooprotect --help
# Should display: OdooProtect - Python Obfuscator with Machine ID Binding
```

---

## 📦 Manual Installation

### Step 1: Download
```bash
# Clone the repository
git clone https://github.com/dynaz/OdooProtect.git
cd OdooProtect
```

### Step 2: Make Executable
```bash
# Make the script executable
chmod +x odooprotect.py
```

### Step 3: System Integration (Optional)
```bash
# Create global symlink (requires sudo)
sudo ln -sf "$(pwd)/odooprotect.py" /usr/local/bin/odooprotect

# Or add to your PATH
export PATH="$PATH:$(pwd)"
```

### Step 4: Verify
```bash
# Test direct execution
./odooprotect.py --help

# Test global command (if symlink created)
odooprotect --help
```

---

## 🐳 Docker Installation

### Build Docker Image
```bash
git clone https://github.com/dynaz/OdooProtect.git
cd OdooProtect

# Build the image
docker build -t odooprotect .

# Run OdooProtect in container
docker run -v $(pwd):/workspace odooprotect --help
```

### Use Pre-built Image
```bash
# Pull and run
docker run -it dynaz/odooprotect --help
```

---

## 🧪 Development Installation

### For Contributors
```bash
# Clone repository
git clone https://github.com/dynaz/OdooProtect.git
cd OdooProtect

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Make executable
chmod +x odooprotect.py
```

---

## 🔧 Advanced Installation

### Custom Installation Path
```bash
# Install to custom location
PYPROTECT_HOME="$HOME/.local/odooprotect"
mkdir -p "$PYPROTECT_HOME"
cp -r OdooProtect/* "$PYPROTECT_HOME/"
chmod +x "$PYPROTECT_HOME/odooprotect.py"

# Add to PATH in your shell profile
echo "export PATH=\"\$PATH:$PYPROTECT_HOME\"" >> ~/.bashrc
source ~/.bashrc
```

### Portable Installation (USB/External Drive)
```bash
# Copy to external drive
EXTERNAL_DRIVE="/mnt/external"
cp -r OdooProtect "$EXTERNAL_DRIVE/"
cd "$EXTERNAL_DRIVE/OdooProtect"

# Run directly
python3 odooprotect.py --help
```

---

## ✅ Post-Installation

### Test Your Installation
```bash
# Basic functionality test
odooprotect -m  # Should show your machine ID

# Obfuscation test
odooprotect -i examples/demo.py  # Should create /dist/demo.py

# License check test
odooprotect -c  # Should scan for license files
```

### Troubleshooting Installation
```bash
# If odooprotect command not found
which odooprotect  # Check if in PATH
ls -la /usr/local/bin/odooprotect  # Check symlink

# Test direct execution
./odooprotect.py --help

# Check permissions
ls -la odooprotect.py
```

### Upgrade OdooProtect
```bash
cd OdooProtect
git pull origin main
./install.sh  # Re-run installer
```

## 🚀 Quick Start

> **✅ NEW**: OdooProtect now supports **Odoo and framework obfuscation**! Public API names (functions and classes that don't start with `_`) are automatically preserved, allowing cross-module imports to work correctly.

### Protect a Single File
```bash
odooprotect -i my_script.py -b
# Output: /dist/my_script.py (machine-bound)
```

### Protect an Entire Project
```bash
odooprotect -i my_project/ -b -e 365
# Output: /dist/my_project/ (entire project protected)
# Note: Only use for self-contained projects without explicit cross-module imports
```

### Test Protection
```bash
# Test a protected script (after running odooprotect on it)
python3 -c "import sys; sys.path.insert(0, '.'); import my_protected_script"
# Should work on licensed machine, fail on others

# Or test the examples in this repository:
cd examples
python3 -c "import demo_bound; result = demo_bound.secret_function('super_secret_key_12345'); print('Protected script result:', result)"

# Test protected project modules:
cd protected_project
python3 -c "from models.user import User; u = User('Test', 25); print('User:', u.name)"
```

## 📖 Usage

### Basic Syntax
```bash
odooprotect -i INPUT [-o OUTPUT] [OPTIONS]
```

**Note**: After installation with `./install.sh`, you can use `odooprotect` from anywhere. Alternatively, use `python3 odooprotect.py` if running directly.

### ✅ Recommended Use Cases
- **Odoo Addons**: Custom Odoo modules and addons (✅ NEW: Fully supported!)
- **Django/Flask Apps**: Web applications with multiple modules (✅ NEW: Cross-module imports work!)
- **Standalone Scripts**: Single-file Python applications
- **Final Applications**: Complete apps with public APIs
- **Closed Systems**: Scripts running in controlled environments
- **CLI Tools**: Command-line utilities
- **Custom Business Logic**: Proprietary algorithms and business rules
- **Framework Plugins**: Plugins and extensions for existing frameworks

### ⚠️ Use With Caution For
- **Open-source Contributions**: Code that others need to read and maintain
- **Debugging Required**: Code still in active development (harder to debug obfuscated code)
- **Python Libraries**: Public packages on PyPI (users expect readable source code)

### Input Types
- **Single File**: `script.py`
- **Directory**: `myproject/` (processes all `.py` files recursively)

### Output Types
- **Single File**: `protected.py` (default: `/dist/filename.py`)
- **Directory**: `protected/` (default: `/dist/inputname/`, maintains input structure)

## ⚙️ Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input INPUT` | Input file or directory | Required |
| `-o, --output OUTPUT` | Output file or directory | `/dist/` |
| `-m, --machine-id` | Display current machine ID | - |
| `-c, --check-license DIR` | Check license validity in directory | Current dir |
| `-b` | Bind code to current machine hardware | Disabled |
| `-e DAYS` | License expiration in days | 365 |
| `--no-preserve-api` | ✨ **NEW**: Obfuscate all names including public API | Disabled (API preserved) |

### 🆕 Public API Preservation (Default)

By default, OdooProtect preserves public API names to allow cross-module imports:

- **Preserved**: Public functions/classes (no leading `_`)
- **Obfuscated**: Private functions/classes (leading `_`)
- **Preserved**: Odoo-specific attributes (`_name`, `_inherit`, `create`, etc.)
- **Compatible**: Works with Odoo, Django, Flask, and other frameworks

**Example**:
```bash
# Default: Preserves public API (Odoo/Framework compatible)
odooprotect -i my_odoo_addon/

# Full obfuscation: May break imports
odooprotect -i standalone_script.py --no-preserve-api
```

## 💡 Examples

### Example 1: Basic File Protection
```bash
# Protect a single Python file (output to /dist/filename.py)
odooprotect -i sensitive_code.py

# Or specify custom output
odooprotect -i sensitive_code.py -o protected.py
```

### Example 2: Machine-Bound Protection
```bash
# Protect and bind to current machine for 1 year
odooprotect -i app.py -o app_protected.py -b -e 365
```

### Example 3: Project Protection
```bash
# Protect entire Django/Flask project (output to /dist/)
odooprotect -i my_django_project/ -b

# Or specify custom output directory
odooprotect -i my_django_project/ -o protected_project/ -b
```

### Example 4: Check Machine ID
```bash
# Display current machine ID for licensing
odooprotect -m
# Output: Machine ID: 0a3a756bffd5fe563cb9b9ec3e5e17fb
```

### Example 5: Check License Status
```bash
# Check license validity in current directory
odooprotect -c

# Check license in specific directory
odooprotect -c /path/to/protected/app
# Shows: ✅ VALID - License valid, ✅ Machine ID matches
```

### Example 6: Trial Version (30 days)
```bash
# Create time-limited trial version
odooprotect -i software.py -o trial_version.py -b -e 30
```

### Example 7: Obfuscating Odoo Addons (✅ Now Supported!)
```bash
# ✅ NEW: Obfuscating Odoo addons now works correctly!
# Public API names are preserved, allowing cross-module imports

# Obfuscate a custom Odoo addon
odooprotect -i /path/to/custom_addon/ -o /dist/custom_addon/ -b

# Obfuscate entire Odoo server (if needed)
odooprotect -i /odoo18/odoo18-server/addons/my_custom_addon/ -b

# What gets preserved:
# ✅ Public functions: def my_function() → preserved
# ✅ Public classes: class MyClass → preserved  
# ✅ Public methods: def method() → preserved
# ✅ Odoo model attributes: _name, _inherit, create, write, etc.
# ⚙️ Private functions: def _helper() → obfuscated to _fn_0
# ⚙️ Variables: user_input → obfuscated to _obf_0

# Test after obfuscation:
cd /dist/custom_addon
python3 -m odoo  # Should work! ✅
```

## 🔒 Security Features

### Variable Obfuscation
```python
# Original
def process_data(user_input, api_key="secret123"):
    secret_token = "token_abc123"
    return user_input + secret_token

# Protected
def _obf_0(_obf_1, _obf_2=_decrypt_str('0')):
    _obf_3 = _decrypt_str('1')
    return _obf_1 + _obf_3
```

### String Encryption
```python
# Original strings are base64 encoded
_STRINGS = ['c2VjcmV0MTIz', 'dG9rZW5fYWJjMTIz']  # Encrypted strings
```

### Hardware Binding
- **Machine ID Generation**: Combines CPU, MAC, and disk serial
- **License Validation**: Runtime checks ensure code only runs on authorized machines
- **Expiration Control**: Time-based license expiration

### Runtime Protection
```python
# Automatic license check on import
_check_license()  # Validates machine and expiration
```

## 🏗️ Architecture

### Core Components

1. **AST Processor** (`Obfuscator` class)
   - Parses Python code into Abstract Syntax Tree
   - Transforms variable names and string literals
   - Applies obfuscation rules

2. **License Manager**
   - Generates hardware fingerprints
   - Creates signed license keys
   - Validates licenses at runtime

3. **Runtime Engine**
   - Decrypts strings on-demand
   - Verifies machine authorization
   - Handles tamper detection

### File Structure
```
OdooProtect/
├── odooprotect.py          # Main obfuscation tool
├── README.md            # This documentation
├── examples/            # Sample projects
│   ├── basic_script.py
│   └── sample_project/
└── tests/               # Test cases
    ├── test_obfuscation.py
    └── test_licensing.py
```

## ⚠️ Limitations

### Current Limitations
- **Complex Metaclasses**: Advanced Python patterns may need adjustment
- **Dynamic Imports**: `importlib` and dynamic imports may require special handling
- **Third-party Libraries**: Some libraries may not work with obfuscated code

### Public API Preservation (Default Behavior)
- **✅ Framework Compatible**: By default, OdooProtect preserves public API names (functions/classes not starting with `_`)
- **✅ Cross-Module Imports**: `from module import function_name` works correctly after obfuscation
- **✅ Odoo Compatible**: Tested and working with Odoo's module system
- **Option**: Use `--no-preserve-api` flag for full obfuscation (may break imports)

### Known Issues
- Very large files (>10MB) may be slow to process
- Some debugging tools may not work with obfuscated code

## 🔧 Troubleshooting

### Common Issues

#### "ImportError: cannot import name 'function_name' from 'module'" (FIXED!)
**Status**: ✅ **RESOLVED** - This issue is now fixed in the latest version!

**Solution**: OdooProtect now automatically preserves public API names (functions and classes that don't start with `_`), so cross-module imports work correctly by default.

**How it works**:
```python
# Public functions (no leading _) are preserved:
def strftime_format_to_spreadsheet_date_format(fmt):  # Name preserved ✅
    return _internal_helper(fmt)  # Private function obfuscated ✅

# After obfuscation, you can still import:
from module import strftime_format_to_spreadsheet_date_format  # Works! ✅
```

**Advanced Option**: If you need full obfuscation (which may break imports), use:
```bash
odooprotect -i mycode.py --no-preserve-api
```

**Best Practice**: Keep default behavior for Odoo/framework code. Only use `--no-preserve-api` for standalone scripts where no imports are needed.

#### "SyntaxError: invalid syntax"
**Cause**: F-strings or advanced Python syntax not supported
**Solution**: Convert f-strings to `.format()` or string concatenation

#### "ModuleNotFoundError"
**Cause**: Import paths changed after obfuscation
**Solution**: Use absolute imports or adjust PYTHONPATH

#### "Unauthorized use of script"
**Cause**: License validation failed
**Solutions**:
- Verify you're on the licensed machine
- Check license hasn't expired
- Regenerate license if hardware changed

#### "ast.Unparse not available"
**Cause**: Python version < 3.9
**Solution**: Upgrade Python or use string fallback mode

### Debug Mode
```bash
# Enable verbose output
odooprotect -i input.py -o output.py --verbose
```

### Recovery
```bash
# If obfuscation fails, restore from backup
cp original_file.py obfuscated_file.py.backup
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch
3. **Add** tests for new features
4. **Submit** a pull request

### Development Setup
```bash
git clone https://github.com/dynaz/OdooProtect
cd odooprotect
python3 -m pip install -r requirements-dev.txt
python3 -m pytest tests/
```

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation for changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Commercial Use
For commercial applications requiring advanced features:
- Enterprise licensing available
- Priority support
- Custom feature development
- Professional services

## 📞 Support

### Documentation
- [API Reference](api.md)
- [Security Guide](security.md)
- [Best Practices](best-practices.md)

### Community
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share experiences
- **Wiki**: Community guides and tutorials

### Professional Support
For enterprise deployments and custom requirements:
- Email: dynaz@mac.com
- Enterprise licensing: dynaz@mac.com

### Support the Project
If you find OdooProtect helpful, consider supporting the development:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-%23FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/dynaz)

Your support helps maintain and improve this open-source project! ☕

---

## 🎯 Quick Reference

### Most Common Commands
```bash
# Quick protection (output to /dist/)
odooprotect -i file.py -b

# Project protection (output to /dist/)
odooprotect -i project/ -b

# Trial version (30 days)
odooprotect -i app.py -o trial.py -b -e 30

# Check machine ID
odooprotect -m

# Check license status
odooprotect -c
```

### Verification
```bash
# Test protected file
python3 protected.py

# Test protected module (after creating one)
python3 -c "import my_protected_module; print('Module works!')"

# View machine ID (alternative method)
odooprotect -m

# Check license validity in current directory
odooprotect -c

# Check license in protected project
odooprotect -c /dist/base

# Test example protected scripts
cd examples
python3 -c "import demo_bound; result = demo_bound.secret_function('super_secret_key_12345'); print('Demo result:', result)"
python3 -c "import test_protected; result = test_protected.secret_function('super_secret_key_12345'); print('Test result:', result)"
```

---

**OdooProtect** - Secure your Python code with advanced obfuscation and hardware binding! 🔐✨
