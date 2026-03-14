#!/bin/bash
# PyProtect Installation Script

echo "🚀 Installing PyProtect..."
echo "=========================="

# Check Python version
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is required but not found."
    exit 1
fi

# Make script executable
chmod +x pyprotect.py
echo "✅ Made pyprotect.py executable"

# Create symlink for global access
if [ -f "pyprotect.py" ]; then
    SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/pyprotect.py"

    # Try to create symlink in /usr/local/bin (requires sudo)
    if sudo ln -sf "$SCRIPT_PATH" /usr/local/bin/pyprotect 2>/dev/null; then
        echo "✅ Created global symlink: pyprotect"
        echo "   You can now use 'pyprotect' from anywhere!"
    else
        echo "⚠️  Could not create global symlink (need sudo permissions)"
        echo "   You can still use: $SCRIPT_PATH"
        echo ""
        echo "   To create global symlink manually:"
        echo "   sudo ln -sf $SCRIPT_PATH /usr/local/bin/pyprotect"
    fi
else
    echo "❌ pyprotect.py not found in current directory"
    exit 1
fi

# Install if running as pip package
if [ -f "setup.py" ]; then
    echo "📦 Installing as Python package..."
    pip3 install -e .
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📖 Usage Examples:"
echo "  pyprotect -i file.py -b"
echo "  pyprotect -i project/ -b"
echo "  pyprotect -m  # Check machine ID"
echo "  pyprotect -c  # Check license status"
echo ""
echo "📖 Run 'pyprotect --help' for full documentation"
