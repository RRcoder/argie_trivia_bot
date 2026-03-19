# AGENTS.md - Argie Trivia Bot Development Guide

This document provides guidelines and commands for agents working on this codebase.

## Project Overview

A Telegram trivia bot built with Python and `python-telegram-bot`. Features quiz games with randomized questions, live scoring, and ranking displays.

## Project Structure

```
argie_trivia_bot/
├── bot_v2.py          # Main bot logic and handlers
├── quiz_data.py       # Quiz question database
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variables template
└── .env               # Environment variables (gitignored)
```

## Dependencies

- **python-telegram-bot>=20.0** - Telegram Bot API wrapper

## Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your TELEGRAM_BOT_TOKEN
```

## Running the Bot

```bash
# Standard run
python bot_v2.py

# Or with environment variables
TELEGRAM_BOT_TOKEN=your_token python bot_v2.py
```

## Code Quality Commands

```bash
# Install dev dependencies (if added)
pip install pytest pytest-asyncio ruff mypy

# Run linting with ruff
ruff check .

# Fix auto-fixable linting issues
ruff check --fix .

# Run type checking with mypy
mypy bot_v2.py quiz_data.py

# Run a single test
pytest tests/test_bot.py::test_function_name -v

# Run tests with coverage
pytest --cov=. --cov-report=term-missing
```

## Code Style Guidelines

### Python Version
- Target Python 3.8+ (as per README)
- Use modern Python features where appropriate (f-strings, type hints, etc.)

### Formatting
- **Indentation**: 4 spaces (no tabs)
- **Line length**: 88 characters (ruff default)
- **Blank lines**: Two blank lines between top-level definitions, one between class methods
- **Trailing whitespace**: Remove

### Imports
- Follow standard library → third-party → local application order
- Group imports with blank lines between groups
- Use absolute imports for local modules (`from quiz_data import QUIZ_QUESTIONS`)
- Sort imports alphabetically within each group

```python
# Correct
import logging
import random
import unicodedata

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    filters,
    MessageHandler,
)

from quiz_data import QUIZ_QUESTIONS

# Incorrect
from quiz_data import QUIZ_QUESTIONS
from telegram import Update
import logging, random
```

### Naming Conventions
- **Functions/variables**: `snake_case` (e.g., `normalize_text`, `user_id`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `QUESTIONS_PER_QUIZ`, `QUIZ_QUESTIONS`)
- **Classes**: `PascalCase` (e.g., `QuizGame`, `UserScore`)
- **Async functions**: Prefix with `async_` only if needed for disambiguation (not required)

### Type Annotations
- Add type hints for all function parameters and return values
- Use `typing` module for complex types (List, Dict, Optional, etc.)
- For Telegram bot handlers, use `ContextTypes.DEFAULT_TYPE` for context parameter

```python
# Good
async def handle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id: int = update.message.from_user.id
    scores: dict[int, dict[str, Any]] = {}

# Avoid
async def handle_guess(update, context):
```

### Docstrings and Comments
- Add docstrings for all public functions and classes
- Use Google-style or NumPy-style docstrings
- Keep comments focused on "why", not "what"

```python
def normalize(text: str) -> str:
    """Normalize text for case-insensitive comparison.
    
    Args:
        text: The raw input text from user.
        
    Returns:
        Lowercase, whitespace-stripped text with accents removed.
    """
    pass
```

### Error Handling
- Use specific exception types when possible
- Log errors with appropriate severity
- Don't silently swallow exceptions unless intentional
- Let exceptions propagate for truly unrecoverable errors

```python
# Good
try:
    await update.effective_chat.send_message(text)
except TelegramError as e:
    logging.error(f"Failed to send message: {e}")
    return

# Avoid
try:
    await update.effective_chat.send_message(text)
except:
    pass
```

### Async/Await Patterns
- Always `await` coroutines (never forget it)
- Use `async def` for all Telegram handler functions
- Don't mix sync and async code unnecessarily
- Use `asyncio` for async utilities when needed

### Telegram Bot Patterns
- Use `application.add_handler()` to register handlers
- Use `filters.TEXT & ~filters.COMMAND` for message handlers
- Access chat data via `context.chat_data` dictionary
- Use `update.effective_chat.send_message()` for replies
- Use `update.message.reply_text()` for direct replies to user messages

### Quiz Data Structure
Questions in `quiz_data.py` must follow this schema:

```python
{
    "question": "Question text here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_option_index": 0,  # 0-based index
    "category": "optional_category"  # optional field
}
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Commit with descriptive message
git commit -m "Add live ranking display to quiz"

# Push and create PR
git push -u origin feature/my-feature
```

## Common Issues and Solutions

### Bot not responding
- Verify `TELEGRAM_BOT_TOKEN` is set correctly in `.env`
- Check bot has been started via `/start` command in Telegram

### Import errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### Type errors with telegram.ext
- Some telegram.ext types require specific imports from the library
- Check `python-telegram-bot` documentation for correct types

## Testing Guidelines

When adding tests:
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use `pytest` and `pytest-asyncio` for async test functions
- Mock Telegram API calls using `unittest.mock` or `pytest-mock`
- Test handlers in isolation where possible

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_quiz_command():
    update = MagicMock()
    context = MagicMock()
    # ... set up mocks and test
```
