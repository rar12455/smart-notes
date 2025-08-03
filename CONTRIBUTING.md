# Contributing to Smart Notes

Thank you for your interest in contributing to Smart Notes! We welcome contributions from developers of all skill levels.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Basic knowledge of tkinter (helpful but not required)

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/smart-notes.git
   cd smart-notes
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python smartnotes.py
   ```

## 🤝 How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Include detailed information**:
   - Operating system and version
   - Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

### Suggesting Features

1. **Check the roadmap** in CHANGELOG.md
2. **Open a feature request** with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Code Contributions

#### 1. Choose an Issue
- Look for issues labeled `good first issue` for beginners
- Check `help wanted` for priority contributions
- Comment on the issue to claim it

#### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

#### 3. Make Changes
- Follow the coding standards below
- Write clear, documented code
- Test your changes thoroughly

#### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add new feature description"
# or
git commit -m "fix: resolve bug description"
```

Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting changes
- `refactor:` for code restructuring
- `test:` for adding tests

#### 5. Push and Create Pull Request
```bash
git push origin your-branch-name
```

Then create a pull request with:
- Clear title and description
- Reference related issues
- List of changes made
- Screenshots for UI changes

## 📝 Coding Standards

### Python Style Guide

- Follow **PEP 8** style guidelines
- Use **4 spaces** for indentation
- **Maximum line length**: 88 characters
- Use **meaningful variable names**

### Code Structure

```python
# Good example
class NotesManager:
    """Manages note operations like create, read, update, delete."""
    
    def __init__(self):
        self.notes = []
    
    def add_note(self, title: str, content: str) -> int:
        """Add a new note and return its ID."""
        # Implementation here
        pass
```

### Documentation

- **Docstrings** for all classes and methods
- **Inline comments** for complex logic
- **Type hints** where appropriate
- **Clear variable names** that explain purpose

### UI Guidelines

- **Consistent theming** across all elements
- **Responsive design** that works on different screen sizes
- **Keyboard accessibility** for all features
- **Clear visual hierarchy** and spacing

## 🧪 Testing

### Manual Testing

1. **Test all features** after making changes
2. **Try both light and dark themes**
3. **Test with and without API key configured**
4. **Verify keyboard shortcuts work**
5. **Test error scenarios**

### Automated Testing (Future)

We're working on implementing automated tests. Contributions to testing infrastructure are welcome!

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Changes are well documented
- [ ] Manual testing completed
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages follow convention

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] Manual testing completed
- [ ] All features work as expected
- [ ] No regressions introduced

## Screenshots (if applicable)
Add screenshots for UI changes

## Related Issues
Closes #123
```

## 🎯 Areas for Contribution

### High Priority
- **Bug fixes** - Always welcome
- **Documentation improvements** - Help others understand the code
- **Performance optimizations** - Make the app faster
- **Accessibility improvements** - Make it usable for everyone

### Medium Priority
- **New features** from the roadmap
- **UI/UX enhancements** - Better user experience
- **Code refactoring** - Improve maintainability
- **Test coverage** - Automated testing

### Future Goals
- **Plugin system** - Extensibility framework
- **Cloud sync** - Multi-device support
- **Mobile app** - Companion application
- **Multiple AI providers** - Choice and redundancy

## 🏷️ Labeling System

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `documentation` - Improvements to docs
- `duplicate` - Issue already exists
- `wontfix` - Will not be worked on

## 💬 Communication

### Channels
- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and ideas
- **Pull Request Comments** - Code review discussions

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- **Be respectful** to all contributors
- **Use inclusive language**
- **Accept constructive criticism**
- **Focus on what's best for the community**
- **Show empathy** towards other community members

## 🎉 Recognition

Contributors will be:
- **Listed in CONTRIBUTORS.md**
- **Mentioned in release notes**
- **Credited in the About dialog**

## 📚 Resources

### Learning Resources
- [Python tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Google Generative AI Python SDK](https://github.com/google/generative-ai-python)
- [Material Design Guidelines](https://material.io/design)

### Development Tools
- **Code Editor**: VS Code, PyCharm, or your favorite editor
- **Git GUI**: GitKraken, Sourcetree, or command line
- **Python Environment**: virtualenv or conda

## ❓ Questions?

Don't hesitate to ask questions! You can:
- **Open an issue** for technical questions
- **Start a discussion** for general questions
- **Comment on existing issues** for clarification

---

**Happy Contributing! 🎉**

Thank you for helping make Smart Notes better for everyone!