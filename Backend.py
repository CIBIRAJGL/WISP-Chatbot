# Backend.py

import os
from dotenv import load_dotenv  # To load variables from a .env file
from groq import Groq  # Groq API client

# STEP 1: Load environment variables from the .env file

load_dotenv()  # This will read the GROQ_API_KEY stored in the .env file

# STEP 2: Function to get AI response from Groq

def ask_groq(prompt):
    """
    Takes a user prompt as input and returns the AI response using the Groq API.
    """
    try:
        # Get the API key from the environment variable
        api_key = os.getenv("GROQ_API_KEY")

        # Initialize the Groq client
        client = Groq(api_key=api_key)

        # Send the user's message to the model
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-70b-8192",  # Make sure this matches your model from Groq
            stream=False,
        )

        # Return the model's response
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"[Error] {str(e)}"

# STEP 3: Main loop to interact with the user

if __name__ == "__main__":
    print("🧠 Chatbot ready! Type 'exit' or 'quit' to end the session.")
    while True:
        user_input = input("You: ")

        # Check if user wants to quit
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Exiting chatbot. Goodbye!")
            break

        # Get AI response and print it
        response = ask_groq(user_input)
        print("Bot:", response)
