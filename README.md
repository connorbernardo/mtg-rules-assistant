# MTG Rules Assistant

A command-line tool that answers Magic: The Gathering Commander rules questions using Claude AI. Ask it anything about Commander damage, color identity, deck building, mulligans, and more.

## How It Works

1. Loads local rules documentation from the `docs/` folder
2. Finds the most relevant doc based on your question
3. Sends your question + the relevant rules to Claude
4. Prints the answer

## Requirements

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

1. Clone the repo
   ```bash
   git clone https://github.com/your-username/mtg-rules-assistant.git
   cd mtg-rules-assistant
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

```bash
cd src
python main.py
```

Then type your question when prompted:
```
I am the MTG rules assistant, please ask me a MTG commander-related question.

> How much commander damage does it take to eliminate a player?
```

## Project Structure

```
mtg-rules-assistant/
+-- docs/               # MTG Commander rules reference files
+-- src/
¦   +-- main.py         # Main application
+-- tests/
¦   +-- test_api.py     # API connection test
+-- requirements.txt
+-- .env                # Not committed — create this yourself
```
