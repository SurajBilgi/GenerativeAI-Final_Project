# Restaurant Chatbot

## Overview
This project is a restaurant chatbot designed using Langchain and GPT, with a frontend built in Streamlit and APIs managed by FastAPI. The chatbot interacts with customers to provide personalized food recommendations and resolve customer complaints. All data is stored in a SQLite database.

## Features
- Personalized food recommendations based on customer preferences
- Resolves customer complaints efficiently
- User-friendly interface built with Streamlit
- Robust backend APIs developed using FastAPI
- Data storage and management using SQLite

## Architecture
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Database:** SQLite
- **Chatbot Framework:** Langchain
- **Language Model:** GPT

## Prerequisites
- Python 3.11.5
- SQLite server
- Necessary Python packages (listed in `requirements.txt`)

## Installation

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/SurajBilgi/GenerativeAI-Final_Project
    cd GenerativeAI-Final_Project
    ```

2. **Set Up the Python Environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the FastAPI Backend:**
    ```sh
    fastapi dev api.py
    ```

2. **Start the Streamlit Frontend:**
    ```sh
    streamlit run frontend.py
    ```

## Usage
Once the application is running, open your browser and navigate to the Streamlit frontend URL (usually `http://localhost:8501`). Interact with the chatbot to get personalized food recommendations or to resolve any complaints you might have.


## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
