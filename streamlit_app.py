import streamlit as st
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, function_tool, RunConfig
from search_tools import DDGS
from twilio.rest import Client
import asyncio

# It's a good practice to run async functions in a running event loop
# Streamlit runs in a thread that might not have one, so we ensure one is available.
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


# --- Agent Tools ---

@function_tool
def get_user_data(min_age: int) -> list[dict]:
    """Retrieve user data based on a minimum age."""
    # In a real app, this would query a database.
    users = [
        {"name": "Muneeb", "age": 22},
        {"name": "Zainscity", "age": 25},
        {"name": "Azan", "age": 19},
        {"name": "Ayesha", "age": 28},
    ]
    return [user for user in users if user["age"] >= min_age]


@function_tool
def search_duckduckgo(query: str) -> list[dict]:
    """Search the web using DuckDuckGo to find information."""
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=5)]
        return [{"title": r["title"], "href": r["href"], "body": r["body"]} for r in results]


# --- Twilio WhatsApp Function ---

def send_whatsapp_message(message: str, twilio_config: dict):
    """Sends a message via Twilio WhatsApp."""
    try:
        client = Client(twilio_config["account_sid"], twilio_config["auth_token"])
        client.messages.create(
            body=message,
            from_=twilio_config["from_whatsapp"],
            to=twilio_config["to_whatsapp"]
        )
        return True
    except Exception as e:
        st.error(f"Failed to send WhatsApp message: {e}")
        return False


# --- Main Agent Runner ---

def run_matchmaking_agent(prompt: str, gemini_api_key: str):
    """Initializes and runs the matchmaking agent."""
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash", # Using the latest flash model
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    rishtey_wali_agent = Agent(
        name="Auntie",
        model=model,
        instructions="You are a warm, friendly, and wise 'Rishtey Wali Auntie' who helps people find matches. Be personable and encouraging in your response.",
        tools=[get_user_data, search_duckduckgo]
    )

    runner = Runner() # Initialize with no arguments
    result = asyncio.run(runner.run(
        input=prompt,
        starting_agent=rishtey_wali_agent,
        run_config=config
    ))

    return result.final_output

# --- Streamlit UI ---

st.set_page_config(page_title="AI Matchmaking Auntie", page_icon="🤖", layout="centered")

st.title("AI Matchmaking Auntie 🤖")
st.markdown("Let Auntie help you find a suitable match and gather some initial details!")

# --- Sidebar for Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("Your API Keys are loaded securely from Streamlit Secrets.")

    st.subheader("Twilio WhatsApp Notification")
    st.markdown("Enter your personal WhatsApp number to receive the results. It must be in the format `whatsapp:+1234567890`.")
    user_whatsapp_number = st.text_input(
        "Your WhatsApp Number",
        placeholder="whatsapp:+1234567890",
        help="Include 'whatsapp:' prefix and your country code."
    )

# --- Main App Logic ---
default_prompt = "Find a suitable match for me who is at least 24 years old. Then, tell me a little about them based on what you can find on their LinkedIn or other public profiles."
user_prompt = st.text_area("Your Request to Auntie:", value=default_prompt, height=150)

if st.button("✨ Find a Match"):
    # Input validation
    if not user_prompt:
        st.warning("Please enter your request in the text box.")
    elif not user_whatsapp_number:
        st.warning("Please enter your WhatsApp number in the sidebar to receive notifications.")
    else:
        try:
            # Load secrets
            gemini_key = st.secrets["GEMINI_API_KEY"]
            twilio_sid = st.secrets["TWILIO_ACCOUNT_SID"]
            twilio_token = st.secrets["TWILIO_AUTH_TOKEN"]
            twilio_from_num = st.secrets["TWILIO_WHATSAPP_NUMBER"]

            with st.spinner("Auntie is searching for the perfect match... 🕵️‍♀️"):
                # Run the agent
                final_result = run_matchmaking_agent(user_prompt, gemini_key)

                # Display result in the app
                st.balloons()
                st.subheader("💌 Here's what Auntie found:")
                st.markdown(final_result)

                # Send WhatsApp notification
                st.info("Sending the result to your WhatsApp...")
                twilio_config = {
                    "account_sid": twilio_sid,
                    "auth_token": twilio_token,
                    "from_whatsapp": twilio_from_num,
                    "to_whatsapp": user_whatsapp_number
                }
                if send_whatsapp_message(final_result, twilio_config):
                    st.success("Message sent successfully to your WhatsApp! ✅")

        except KeyError as e:
            st.error(f"Configuration Error: Please make sure the secret '{e.name}' is set in your Streamlit Secrets.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")