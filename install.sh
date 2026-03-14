#!/bin/bash
# OdooProtect Installation Script

echo "🚀 Installing OdooProtect..."
echo "=========================="

# Check Python version
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is required but not found."
    exit 1
fi

# Make script executable
chmod +x odooprotect.py
echo "✅ Made odooprotect.py executable"

# Create symlink for global access
if [ -f "odooprotect.py" ]; then
    SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/odooprotect.py"

    # Try to create symlink in /usr/local/bin (requires sudo)
    if sudo ln -sf "$SCRIPT_PATH" /usr/local/bin/odooprotect 2>/dev/null; then
        echo "✅ Created global symlink: odooprotect"
        echo "   You can now use 'odooprotect' from anywhere!"
    else
        echo "⚠️  Could not create global symlink (need sudo permissions)"
        echo "   You can still use: $SCRIPT_PATH"
        echo ""
        echo "   To create global symlink manually:"
        echo "   sudo ln -sf $SCRIPT_PATH /usr/local/bin/odooprotect"
    fi
else
    echo "❌ odooprotect.py not found in current directory"
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
echo "  odooprotect -i file.py -b"
echo "  odooprotect -i project/ -b"
echo "  odooprotect -m  # Check machine ID"
echo "  odooprotect -c  # Check license status"
echo ""
echo "📖 Run 'odooprotect --help' for full documentation"
