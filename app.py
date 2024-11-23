import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Predefined historical characters
PREDEFINED_CHARACTERS = {
    "Albert Einstein": "a theoretical physicist explaining complex scientific ideas in simple terms.",
    "Cleopatra": "the Queen of Egypt discussing ancient Egyptian politics and culture.",
    "Abraham Lincoln": "the 16th President of the United States talking about leadership during the Civil War.",
    "Marie Curie": "a scientist explaining her groundbreaking research on radioactivity.",
    "Leonardo da Vinci": "a Renaissance polymath discussing his inventions, art, and philosophy."
}

# Function to interact with OpenAI
def chat_with_ai(character_name, character_description, user_input, custom_context=None):
    # Build the system prompt dynamically
    base_prompt = f"You are {character_name}. {character_description} "
    if custom_context:
        base_prompt += f"You are in the scenario: {custom_context}. "
    base_prompt += "Respond in character and provide educational, historically relevant answers."

    # Generate response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("🕰️ TimeTalk: Unified Historical Chat")
st.sidebar.header("Chat Options")

# Step 1: Choose Character Type
character_type = st.sidebar.radio(
    "How would you like to define the character?",
    ["Choose from Predefined Characters", "Create Custom Character"]
)

# Step 2: Character Details
if character_type == "Choose from Predefined Characters":
    character_name = st.sidebar.selectbox("Select a Historical Figure", list(PREDEFINED_CHARACTERS.keys()))
    character_description = PREDEFINED_CHARACTERS[character_name]
else:
    character_name = st.sidebar.text_input("Enter Character Name", placeholder="e.g., Napoleon Bonaparte")
    character_description = st.sidebar.text_area("Enter Character Description", placeholder="e.g., A military leader and emperor of France during the 19th century.")

# Step 3: Optional Custom Scenario
st.sidebar.header("Custom Scenario (Optional)")
custom_context = st.sidebar.text_area("Describe a hypothetical scenario:", placeholder="e.g., What if Napoleon had access to modern technology?")
use_custom_context = st.sidebar.checkbox("Use Custom Scenario", value=False)

# Chat Interface
if character_name and character_description:
    st.write(f"### Chatting with {character_name}")
    if use_custom_context and custom_context:
        st.markdown(f"**Scenario:** {custom_context}")

    # Initialize chat history
    history = st.session_state.get("history", [])
    user_input = st.text_input("Ask your question:", key="user_input")

    # Generate response
    if st.button("Send"):
        if user_input:
            try:
                context = custom_context if use_custom_context and custom_context else None
                response = chat_with_ai(character_name, character_description, user_input, context)
                history.append({"user": user_input, "character": response})
                st.session_state["history"] = history
            except Exception as e:
                st.error("An error occurred while processing your request.")
                st.error(str(e))

    # Display chat history
    for chat in history:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**{character_name}:** {chat['character']}")

    # Reset chat
    if st.sidebar.button("Reset Chat"):
        st.session_state["history"] = []
        st.experimental_rerun()
else:
    st.write("📝 Please define or select a character to begin chatting.")
