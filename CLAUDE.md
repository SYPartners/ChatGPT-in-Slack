# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Slack bot that integrates OpenAI's ChatGPT models (GPT-3.5, GPT-4, GPT-4o) and DALL-E for image generation into Slack workspaces. The bot operates via Socket Mode (WebSocket connection) and provides AI-powered conversations, document generation, proofreading, and image creation capabilities.

## Development Commands

### Setup and Running
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application locally
python main.py

# For production deployment on Render (with health check server)
gunicorn --worker-class gevent --workers 1 --bind 0.0.0.0:$PORT render_app:health_app
```

### Code Quality and Testing
```bash
# Run complete validation (formatting, linting, type checking, tests)
./validate.sh

# Individual commands:
black ./*.py ./app/*.py ./tests/*.py  # Format code
pytest .                                # Run all tests
pytest tests/markdown_conversion_test.py::test_markdown_to_slack  # Run specific test
flake8 ./*.py ./app/*.py ./tests/*.py  # Lint code
pytype ./*.py ./app/*.py ./tests/*.py  # Type checking
```

## Architecture

### Core Components

1. **main.py**: Entry point for Socket Mode operation. Initializes Slack Bolt app, registers event listeners, and starts SocketModeHandler.

2. **render_app.py**: Production wrapper for Render.com deployment. Provides Flask health check endpoint at `/healthz` while running the Socket Mode app in a background thread.

3. **app/bolt_listeners.py**: Contains all Slack event handlers and command processors. Handles messages, app mentions, shortcuts, and modal interactions.

4. **app/openai_ops.py**: OpenAI API integration layer. Manages streaming responses, context windows, model selection, and function calling. Supports both standard OpenAI and Azure OpenAI endpoints.

5. **app/slack_ops.py**: Slack API utilities for message posting, thread management, and file operations.

6. **app/openai_constants.py**: Model definitions, aliases, and validation. Maintains supported model lists and their configurations.

### Key Design Patterns

- **Streaming Responses**: Uses OpenAI streaming API to provide real-time updates in Slack threads
- **Context Management**: Tracks conversation history within threads, managing token limits per model
- **Async Processing**: Uses threading for long-running operations to avoid Slack's 3-second timeout
- **State Management**: Redis cache for user preferences and conversation state (when available)
- **Error Recovery**: Comprehensive error handling with user-friendly messages and retry logic

## Environment Variables

Required for operation:
- `SLACK_APP_TOKEN`: xapp-1-... (Socket Mode connection)
- `SLACK_BOT_TOKEN`: xoxb-... (Bot authentication)
- `OPENAI_API_KEY`: sk-... (OpenAI API access)

Optional configuration:
- `OPENAI_MODEL`: Model selection (default: gpt-3.5-turbo)
- `OPENAI_TEMPERATURE`: Response creativity 0-2 (default: 1.0)
- `OPENAI_TIMEOUT_SECONDS`: API timeout (default: 30)
- `OPENAI_IMAGE_GENERATION_MODEL`: Image model (default: dall-e-3)
- `USE_SLACK_LANGUAGE`: Auto-translate to user's language (default: true)
- `TRANSLATE_MARKDOWN`: Convert between OpenAI markdown and Slack mrkdwn (default: false)
- `REDACTION_ENABLED`: Redact sensitive info before sending to OpenAI (default: false)
- `IMAGE_FILE_ACCESS_ENABLED`: Process image files in conversations (default: false)

## Slack Integration Points

1. **Event Subscriptions**: `app_mention`, `message.channels`, `message.groups`, `message.im`, `app_home_opened`
2. **Shortcuts**: Message shortcuts for summarization and translation
3. **Interactivity**: Modal submissions for proofreading and image generation
4. **Socket Mode**: Maintains WebSocket connection for real-time events

## Deployment Notes

- **Primary**: Render.com with auto-deploy from main branch
- **Health Check**: Flask server provides `/healthz` endpoint for Render monitoring
- **Concurrency**: Uses gunicorn with gevent workers for production
- **Git Remotes**: 
  - `origin`: SYPartners fork
  - `upstream`: Original seratch repository (sync regularly)