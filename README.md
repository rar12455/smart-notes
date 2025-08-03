# Smart Notes

A modern, elegant note-taking application with AI assistance powered by Google Gemini.

![Smart Notes](https://img.shields.io/badge/version-3.0-blue.svg)
![License](https://img.shields.io/badge/license-GPL%20v3-green.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)

## 🌟 Features

### 📝 **Core Note-Taking**
- Create, edit, and manage notes with a clean interface
- Automatic saving and loading of notes
- Search functionality to quickly find your notes
- Export notes to text files
- Intuitive sidebar for note navigation

### 🤖 **AI Assistant Integration**
- Powered by Google Gemini AI
- Get AI assistance for writing, brainstorming, and content enhancement
- Secure API key management with local storage
- Test API functionality before saving

### 🎨 **Modern Design**
- Elegant Material Design-inspired dark theme (default)
- Light theme option available
- Clean, distraction-free interface
- No scrollbars for a minimal look
- Professional typography with optimized font sizes

### ⚡ **User Experience**
- Keyboard shortcuts for power users
- Fast search across all notes
- Visual separation between different text areas
- Responsive layout that adapts to your workflow

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually comes with Python)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rar12455/smart-notes.git
   cd smart-notes
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python smartnotes.py
   ```

### Optional: AI Features Setup

To use AI assistance features:

1. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Launch Smart Notes
3. Click "Assign API" in the toolbar
4. Enter your API key and test it
5. Save and start using AI features!

## 📖 Usage

### Basic Operations
- **New Note**: Click "New Note" or press `Ctrl+N`
- **Save Note**: Click "Save" or press `Ctrl+S`
- **Delete Note**: Click "Delete" or press `Ctrl+Delete`
- **Search**: Type in the search box to filter notes

### AI Assistant
1. Type your prompt in the "AI Assistant Input" area
2. Click "AI" button to get AI-powered assistance
3. View responses in the "AI Response" area
4. Use AI for writing help, brainstorming, or content enhancement

### Keyboard Shortcuts
- `Ctrl+N` - Create new note
- `Ctrl+S` - Save current note
- `Ctrl+Delete` - Delete current note
- `Ctrl+E` - Export current note

### Themes
- Toggle between dark and light themes using the "Theme" button
- Settings are automatically saved and restored

## 🛠️ Configuration

Smart Notes automatically creates a configuration file (`smartnotes_config.json`) to store:
- Your API key (encrypted locally)
- Theme preferences
- Window settings

## 📁 File Structure

```
smart-notes/
├── smartnotes.py          # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── LICENSE               # GPL v3 license
└── smart_notes.json      # Notes database (created automatically)
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. Clone your fork
2. Install dependencies: `pip install -r requirements.txt`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🐛 Bug Reports

Found a bug? Please open an issue with:
- Your operating system
- Python version
- Steps to reproduce the bug
- Expected vs actual behavior

## 📋 Roadmap

- [ ] Plugin system for extensions
- [ ] Cloud synchronization
- [ ] Markdown preview
- [ ] Note categories and tags
- [ ] Import from other note-taking apps
- [ ] Multiple AI provider support
- [ ] Mobile companion app

## 🔧 Troubleshooting

### Common Issues

**App won't start:**
- Ensure Python 3.7+ is installed
- Check that tkinter is available: `python -c "import tkinter"`

**AI features not working:**
- Verify your API key in "Assign API"
- Check internet connection
- Ensure Google Generative AI library is installed

**Notes not saving:**
- Check write permissions in the app directory
- Ensure sufficient disk space

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**RAR**

## 🙏 Acknowledgments

- Google for the Gemini AI API
- The Python community for excellent libraries
- Material Design for inspiration
- All contributors and users

## 📞 Support

If you find this project helpful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🤝 Contributing code

---

*Made with ❤️ for productivity enthusiasts*
