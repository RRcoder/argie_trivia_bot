# Argie-Trivia-Bot

Argie-Trivia- is an interactive and fun Telegram bot designed to run quizzes on various topics. Built using Python and the Telegram Bot API, this bot provides a seamless experience for users to test their knowledge, receive instant feedback, and view their quiz results.

## Features

- **Randomized Quiz Questions**: Users get a fresh set of randomized questions in each session.
- **Multiple-Choice Answers**: Inline keyboard buttons for easy and quick answer selection.
- **Instant Feedback**: Provides immediate feedback on whether the selected answer is correct or incorrect.
- **Score Tracking**: Tracks the number of correct answers and displays the final result at the end of the quiz.
- **Customizable Question Database**: Questions can be added or modified through a modular question file.

## Installation

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (create one via [BotFather](https://core.telegram.org/bots#botfather))

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/RRcoder/argie_trivia_bot.git
   cd argie_trivia_bot
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your Telegram Bot Token in the `bot.py` file:
   ```python
   application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
   ```
4. Run the bot:
   ```bash
   python bot_v2.py
   ```

## Usage

1. Start the bot on Telegram by sending the `/start` command.
2. Answer the multiple-choice questions by tapping the inline buttons.
3. View your score at the end of the quiz.

## File Structure

```
argie_trivia_bot/
├── bot_v2.py              # Main bot logic
├── quiz_data.py        # Question database
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Customizing Questions

The questions are stored in the `quiz_data.py` file. Each question is a dictionary with the following structure:
```python
{
    "question": "What is the purpose of machine learning?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_option_index": 2
    "category": "general"
}
```
- `question`: The text of the question.
- `options`: A list of possible answers.
- `correct_option_index`: The index of the correct answer in the `options` list (starting from 0).
- `category`: Indica a que categoria pertenece la pregunta

Add, modify, or remove questions as needed.

## Dependencies

- `python-telegram-bot`
- `random`
- `logging`

Install all dependencies with:
```bash
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have suggestions for improvement or additional features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments


