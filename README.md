# Calebstone

## Project Background

Calebstone is a personal project developed to deepen understanding of Python, GitHub, object-oriented programming, and game development using Pygame. This project, inspired by Blizzard's Hearthstone, began as a learning tool and has evolved into a unique game with its own features and mechanics. The first line of code was written on May 13, 2020. The initial goal was to replicate Hearthstone's gameplay but the project has since taken its own direction.

## Installation

To run this program in a terminal on a mac
Install python if not already
cd /path/to/Calebstone
python3 -m venv calebstone
source calebstone/bin/activate
pip install -r requirements.txt
python3 GameManager
deactivate (to exit venv when you're done)

---

This guide explains how to set up and launch the Calebstone game server locally. The server is powered by Flask and provides RESTful API endpoints for managing game sessions and gameplay.

Requirements 1. Python 3.8 or higher installed on your machine. 2. pip, the Python package manager. 3. (Optional) virtualenv for creating a virtual environment.

Setup Instructions

1. Clone the Repository

If you haven’t already, clone the repository to your local machine:

git clone <repository-url>
cd <repository-directory>

2. Create a Virtual Environment (Recommended)

Set up a virtual environment to keep dependencies isolated:

python3 -m venv calebstone_env
source calebstone_env/bin/activate # For Linux/Mac
calebstone_env\Scripts\activate # For Windows

3. Install Dependencies

Install the required Python packages using pip:

pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file in the game_server directory to specify environment variables (optional). For example:

FLASK_ENV=development
FLASK_APP=run.py

If no .env file is created, the server defaults to development mode.

5. Start the Game Server

Navigate to the game_server directory and run the server:

cd game_server
python run.py

By default, the server will run on http://localhost:5000.

6. Using the API

Endpoints Overview

Using the API with Environment Variables

## 1. Create a New Game Session

Endpoint: POST /api/new_game
Example curl Command:

export GAME_SESSION_ID=$(curl -X POST http://localhost:5000/api/new_game | jq -r '.session_id')

    •	This command uses jq (a lightweight JSON processor) to extract the session_id from the response and stores it in an environment variable named GAME_SESSION_ID.
    •	Make sure you have jq installed. Install it using your package manager if needed (e.g., sudo apt-get install jq on Ubuntu).

Verify the Environment Variable:

echo $GAME_SESSION_ID

## 2. Get the Current Game State

Endpoint: GET /api/game_state/<session_id>
Example curl Command:

curl -X GET http://localhost:5000/api/game_state/$GAME_SESSION_ID

This command uses the $GAME_SESSION_ID variable set earlier to fetch the game state.

## 3. Send an Action

Endpoint: POST /api/action/<session_id>

Example curl Commands:
• Play a Card:
curl -X POST http://localhost:5000/api/action/$GAME_SESSION_ID -H "Content-Type: application/json" -d '{"type": "play_card", "card_index": 0}'

    •	Attack:

curl -X POST http://localhost:5000/api/action/$GAME_SESSION_ID -H "Content-Type: application/json" -d '{"type": "attack", "attacker_index": 1, "target_index": 2}'

    •	End Turn:

curl -X POST http://localhost:5000/api/action/$GAME_SESSION_ID -H "Content-Type: application/json" -d '{"type": "end_turn"}'

These commands reuse the $GAME_SESSION_ID environment variable for convenience.

## 4. Fetch Available Cards

Endpoint: GET /api/cards
Example curl Command:

curl -X GET http://localhost:5000/api/cards

This endpoint does not require a session ID.

    •	If you start a new game session, make sure to update the $GAME_SESSION_ID variable:
        export GAME_SESSION_ID=$(curl -X POST http://localhost:5000/api/new_game | jq -r '.session_id')

Stopping the Server

To stop the server, press Ctrl+C in the terminal.

If you used a virtual environment, deactivate it:

deactivate

Troubleshooting 1. Port Already in Use:
If the default port 5000 is busy, you can specify a different port:

python run.py --port=8000

    2.	Missing Dependencies:

Ensure all dependencies are installed with:

pip install -r requirements.txt

    3.	Permission Issues:

Use sudo (Linux/Mac) or run as administrator (Windows) if you encounter permission errors.

Next Steps

Once the server is running:
• Connect it to the Calebstone frontend or other clients.
• Explore the API using provided endpoints.
• Add more functionality or extend the game logic as needed.

Happy coding! 🚀
