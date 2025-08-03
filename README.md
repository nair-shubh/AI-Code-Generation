# Intelligent Code Automation Engine

A sophisticated AI-powered code generation and deployment system that leverages E2B cloud execution for safe, isolated code processing. This system provides both command-line and web interfaces for automated code modifications with GitHub integration.

## 🚀 Key Features

- **🤖 AI-Powered Code Generation**: Uses OpenAI GPT-4 for intelligent code modifications
- **☁️ E2B Cloud Execution**: Safe, isolated code execution in cloud environments
- **🔐 GitHub Integration**: Direct repository access and automated deployments
- **📊 Real-time Progress Tracking**: Live streaming of execution progress
- **🧪 Automated Testing**: Built-in test execution and validation
- **🔄 Branch Management**: Automatic branch creation and deployment
- **🎯 User Token Management**: Secure handling of user-provided tokens

## 🏗️ Architecture

The system consists of two main components:

1. **IntelligentCodeEngine** (`code_automation_engine.py`): Core automation engine
2. **Web Interface** (`web_interface.py`): Modern web UI for user interaction

### Core Engine Features

- **E2B Integration**: Cloud-based code execution with fallback to local workspace
- **GitHub API**: Repository management and deployment
- **OpenAI Integration**: AI-powered code generation
- **Async Processing**: Non-blocking operations with real-time updates
- **Error Handling**: Comprehensive error management and recovery

## 📦 Installation

### Prerequisites

- Python 3.8+
- Git
- OpenAI API key
- GitHub personal access token
- E2B API key (optional, for cloud execution)

### Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements_new.txt
   ```

2. **Set environment variables** (optional):
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export E2B_API_KEY="your-e2b-api-key"
   ```

## 🚀 Usage

### Command Line Interface

Run the standalone engine:

```bash
python code_automation_engine.py
```

The CLI will prompt for:
- GitHub token
- Repository selection
- Code modification description

### Web Interface

Start the web server:

```bash
python web_interface.py
```

Then open your browser to: http://localhost:8000/ui

## 🔧 API Endpoints

### Web Interface Endpoints

- `GET /` - Application information
- `GET /ui` - Web interface
- `GET /health` - Health check
- `GET /docs` - API documentation

### Core API Endpoints

- `POST /api/repositories` - Fetch user repositories
- `POST /api/generate` - Start code generation
- `GET /api/stream/{session_id}` - Real-time progress streaming

## 🔐 Security Features

- **Token Isolation**: User tokens stored only in session memory
- **E2B Sandboxing**: Isolated code execution environment
- **No Persistent Storage**: Sensitive data not stored permanently
- **Input Validation**: Comprehensive input sanitization
- **Error Handling**: Secure error reporting without data leakage

## 🏖️ E2B Integration

The system leverages E2B for secure cloud code execution:

### Features
- **Cloud Workspace**: Isolated execution environment
- **File System Access**: Direct file manipulation
- **Process Execution**: Command-line operations
- **Automatic Cleanup**: Resource management

### Fallback
If E2B is unavailable, the system falls back to local execution with the same functionality.

## 📊 Workflow

1. **User Input**: GitHub token, OpenAI key, and modification description
2. **Repository Selection**: Browse and select target repository
3. **Workspace Initialization**: E2B cloud environment setup
4. **Code Analysis**: Repository structure analysis
5. **AI Generation**: Code modification generation using GPT-4
6. **Modification Application**: Safe application of changes
7. **Testing**: Automated test execution
8. **Deployment**: GitHub branch creation and push

## 🔄 Real-time Updates

The system provides live progress updates via Server-Sent Events (SSE):

- **Progress Tracking**: Visual progress bar
- **Status Updates**: Real-time status messages
- **Error Reporting**: Immediate error notifications
- **Completion Events**: Success/failure notifications

## 🧪 Testing

### Automated Testing
- **Test Execution**: Runs existing tests in the repository
- **Validation**: Ensures code changes don't break existing functionality
- **Reporting**: Provides test results and coverage information

### Manual Testing
```bash
# Test the engine
python -c "from code_automation_engine import IntelligentCodeEngine; print('✅ Engine imports successfully')"

# Test the web interface
python -c "from web_interface import app; print('✅ Web interface imports successfully')"
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `E2B_API_KEY` | E2B API key (for cloud execution) | No |
| `GITHUB_TOKEN` | GitHub personal access token | User-provided |

### GitHub Token Permissions

Your GitHub token needs these permissions:
- `repo` (Full control of private repositories)
- `workflow` (Update GitHub Action workflows)

## 🚀 Deployment

### Local Development
```bash
# Start web interface
python web_interface.py

# Or run engine directly
python code_automation_engine.py
```

### Production Considerations
- **Reverse Proxy**: Use nginx for SSL termination
- **Load Balancing**: Deploy multiple instances
- **Monitoring**: Add health checks and metrics
- **Security**: Implement rate limiting and authentication

## 📁 Project Structure

```
.
├── code_automation_engine.py    # Core automation engine
├── web_interface.py            # Web interface and API
├── requirements_new.txt        # Dependencies
├── README_new.md              # This file
└── .env                       # Environment variables (optional)
```

## 🔍 Troubleshooting

### Common Issues

1. **E2B Not Available**
   - System will fall back to local execution
   - Check E2B API key configuration

2. **GitHub Token Issues**
   - Verify token has correct permissions
   - Check token expiration

3. **OpenAI API Errors**
   - Verify API key is valid
   - Check account balance and rate limits

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **E2B**: Cloud execution environment
- **OpenAI**: AI code generation capabilities
- **FastAPI**: Modern web framework
- **PyGithub**: GitHub API integration

## 🔮 Future Enhancements

- **Multi-language Support**: Additional programming languages
- **Advanced Testing**: Integration with CI/CD pipelines
- **Collaboration Features**: Multi-user support
- **Template System**: Pre-built modification templates
- **Analytics**: Usage tracking and insights 