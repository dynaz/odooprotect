# Contributing to OdooProtect

Thank you for your interest in contributing to OdooProtect! 🎉

We welcome contributions from everyone. This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Reporting Issues](#reporting-issues)
- [Submitting Pull Requests](#submitting-pull-requests)

## 🤝 Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- Git
- Basic understanding of Python AST manipulation

### Quick Setup
```bash
# Fork and clone the repository
git clone https://github.com/dynaz/OdooProtect.git
cd OdooProtect

# Set up development environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🛠️ Development Setup

### Installing Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_license.py -v

# Run with coverage
python -m pytest --cov=odooprotect tests/
```

### Code Quality
```bash
# Format code
black odooprotect.py tests/

# Lint code
flake8 odooprotect.py tests/

# Type checking (if applicable)
mypy odooprotect.py
```

## 💡 How to Contribute

### Types of Contributions
- 🐛 **Bug fixes** - Fix existing issues
- ✨ **Features** - Add new functionality
- 📚 **Documentation** - Improve docs or examples
- 🧪 **Tests** - Add or improve test coverage
- 🎨 **UI/UX** - Improve user experience

### Development Workflow

1. **Choose an issue** or **create a new one** describing what you want to work on
2. **Fork the repository** on GitHub
3. **Create a feature branch**: `git checkout -b feature/your-feature-name`
4. **Make your changes** following our coding standards
5. **Write tests** for new functionality
6. **Run the test suite** to ensure everything works
7. **Update documentation** if needed
8. **Commit your changes** with clear, descriptive messages
9. **Push to your fork** and **create a pull request**

### Coding Standards

#### Python Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions small and focused (single responsibility)

#### Commit Messages
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

Examples:
```
feat(license): add hardware fingerprinting support
fix(obfuscator): handle f-string syntax errors
docs(readme): update installation instructions
```

## 🐛 Reporting Issues

### Bug Reports
When reporting bugs, please include:

1. **Clear title** describing the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs. **actual behavior**
4. **Environment details**:
   - Python version
   - Operating system
   - OdooProtect version
5. **Code samples** or **error messages**
6. **Screenshots** if applicable

### Feature Requests
For feature requests, please include:

1. **Clear description** of the proposed feature
2. **Use case** - why is this feature needed?
3. **Implementation ideas** if you have any
4. **Mockups** or **examples** if applicable

## 🔄 Submitting Pull Requests

### Before Submitting
- ✅ All tests pass
- ✅ Code follows style guidelines
- ✅ Documentation is updated
- ✅ No new linting errors
- ✅ Commit messages are clear and descriptive

### Pull Request Template
Please use this template when creating pull requests:

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update
- [ ] Code style update

## How Has This Been Tested?
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] All existing tests pass

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
```

### Review Process
1. **Automated checks** run (tests, linting, etc.)
2. **Code review** by maintainers
3. **Feedback** and requested changes
4. **Approval** and merge

## 🎯 Areas for Contribution

### High Priority
- **F-string support** in obfuscator
- **Advanced AST transformations**
- **Performance optimizations**
- **Cross-platform testing**

### Medium Priority
- **GUI interface** (web or desktop)
- **Plugin system** for custom transformations
- **Configuration file support**
- **Docker integration**

### Good for Beginners
- **Documentation improvements**
- **Test coverage expansion**
- **Example projects**
- **Error message improvements**

## 📞 Getting Help

If you need help or have questions:

1. **Check existing issues** on GitHub
2. **Read the documentation** thoroughly
3. **Search the codebase** for similar implementations
4. **Ask in discussions** or create an issue

## 🙏 Recognition

Contributors will be recognized in:
- Repository contributors list
- CHANGELOG.md for significant contributions
- Release notes
- Social media mentions

Thank you for contributing to OdooProtect! 🚀✨
