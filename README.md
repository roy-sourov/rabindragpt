# 🎵 RabindraGPT

**Open Source Bengali Poetry and Music Generator**

A beautiful Streamlit application that generates Bengali poetry and music using AI, inspired by the works of Rabindranath Tagore and Bengali cultural heritage.

## 🌟 Features

- **📝 Poetry Generation**: Create beautiful Bengali poetry in various styles (Sonnet, Ghazal, Free Verse, Haiku)
- **🎼 Music Generation**: Compose Rabindra Sangeet and other Bengali music styles
- **🎭 Fusion Mode**: Generate poetry and music together for complete artistic experiences
- **⚙️ Customizable Settings**: Adjust creativity levels and generation parameters
- **📊 Analytics**: Track your generation history and statistics
- **🎨 Beautiful UI**: Modern, responsive interface with Bengali cultural elements

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/rabindragpt.git
   cd rabindragpt
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501` to access the application.

## 📖 Usage Guide

### Poetry Generation
1. Select "Poetry Generation" from the sidebar
2. Choose your preferred poetry type (Sonnet, Ghazal, etc.)
3. Optionally enter a theme or topic
4. Adjust the poem length using the slider
5. Click "Generate Poetry" to create your masterpiece

### Music Generation
1. Select "Music Generation" from the sidebar
2. Choose your preferred music style (Rabindra Sangeet, Folk, etc.)
3. Set the desired duration
4. Click "Generate Music" to compose your piece

### Fusion Mode
1. Select "Poetry + Music" for a complete artistic experience
2. The app will generate both poetry and accompanying music
3. Enjoy the harmonious combination of words and melody

## 🛠️ Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4
TEMPERATURE=0.8
MAX_TOKENS=500
```

### Settings Panel
- **Creativity Level**: Adjust the AI's creativity (0.1 - 2.0)
- **Max Tokens**: Control the length of generated content
- **Language Preference**: Choose between Bengali, English, or both
- **History**: Enable/disable generation history saving

## 🏗️ Project Structure

```
rabindragpt/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore           # Git ignore rules
├── .env                 # Environment variables (create this)
├── venv/                # Virtual environment (created during setup)
└── assets/              # Static assets (images, audio samples)
    ├── images/
    └── audio/
```

## 🧪 Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
```

### Linting
```bash
flake8 .
```

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Contributing Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the works of Rabindranath Tagore
- Built with Streamlit for beautiful web interfaces
- Powered by modern AI and machine learning technologies
- Bengali cultural heritage and literature

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Check the documentation
- Join our community discussions

## 🔮 Roadmap

- [ ] Integration with advanced language models
- [ ] Real-time music generation
- [ ] Voice synthesis for poetry recitation
- [ ] Mobile app version
- [ ] Community sharing features
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] API endpoints for developers

---

**Made with ❤️ for Bengali culture and literature**

*"Where the mind is without fear and the head is held high..."* - Rabindranath Tagore
