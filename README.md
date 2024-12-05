# AI Tour Guide 🌍 🎙️

An intelligent, interactive tour guide application that provides personalized, voice-enabled historical information about various locations. Built with Python and Streamlit, this application combines the power of AI with an intuitive user interface to create engaging, educational experiences.

## Features ✨

- 🗣️ **Voice-Enabled Narration**: Uses ElevenLabs for natural-sounding, multilingual text-to-speech
- 🧠 **Intelligent Context Understanding**: Powered by LangChain for smart, context-aware responses
- 💾 **Efficient Data Storage**: ChromaDB for vector storage and quick information retrieval
- 🔍 **Smart Search**: Semantic search capabilities for finding relevant historical information
- 🌐 **Multilingual Support**: Content available in multiple languages
- 📊 **Performance Monitoring**: Integrated with Arize for AI performance tracking
- 🎯 **Personalization**: Customized experiences based on user preferences

## Installation 🚀

1. Clone the repository:
```bash
git clone [repository-url]
cd ai_tour_guide
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

## Required API Keys 🔑

- **ElevenLabs API Key**: For text-to-speech conversion
- **OpenAI API Key**: For AI language model capabilities
- **Arize API Key**: For monitoring (optional)

## Usage 🎯

1. Start the application:
```bash
streamlit run app/main.py
``

2. Features available:
   - Browse historical sites and landmarks
   - Listen to AI-generated narrations
   - Customize language preferences
   - Save favorite locations
   - Get personalized recommendations



## Dependencies 📚

Key dependencies include:
- Streamlit (>= 1.29.0)
- LangChain (>= 0.0.350)
- ChromaDB (>= 0.4.22)
- ElevenLabs (>= 0.3.0)
- OpenAI (>= 1.6.1)
- And more (see requirements.txt)

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License 📄

[Your License Here]

## Support 💬

For support, please open an issue in the GitHub repository or contact [Your Contact Information].

---
Built with ❤️ using Python and Streamlit
