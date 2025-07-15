from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, function_tool, RunConfig
from duckduckgo_search import DDGS  # ✅ DuckDuckGo search tool
from twilio.rest import Client

load_dotenv()

# ✅ Tool 1: User Data Filter
@function_tool
def get_user_data(min_age: int) -> list[dict]:
    "Retrieve user data based on a minimum age"
    users = [
        {"name": "Muneeb", "age": 2},
        {"name": "Zainscity", "age": 25},
        {"name": "Azan", "age": 19},
    ]
    return [user for user in users if user["age"] >= min_age]

# ✅ Tool 2: DuckDuckGo Search
@function_tool
def search_duckduckgo(query: str) -> list[dict]:
    "Search the web using DuckDuckGo"
    with DDGS() as ddgs:
        results = ddgs.text(query)
        return [
            {"title": r["title"], "href": r["href"], "body": r["body"]}
            for r in results[:5]
        ]

# ✅ Main function with agent
def main():
    MODEL_NAME = "gemini-2.0-flash"
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model=MODEL_NAME,
        openai_client=external_client
    )

    config  = RunConfig(
        model= model,
        model_provider=external_client,
        tracing_disabled=True
    )

    rishtey_wali_agent = Agent(
        name="Auntie",
        model=model,
        instructions="You are a warm and wise 'Rishtey Wali Auntie' who helps people find matches.",
        tools=[get_user_data, search_duckduckgo]
    )



    result = Runner.run_sync(
        starting_agent=rishtey_wali_agent,
        input="Find a match of 20 minimum age and tell me the details about the match from LinkedIn, Instagram, Facebook, Tiktok.",
        run_config=config
    )

    print(result.final_output)
    send_whatsapp_message(result.final_output)  # ✅ Sends result to your WhatsApp



def send_whatsapp_message(message: str):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_whatsapp = os.getenv("TWILIO_WHATSAPP_NUMBER")
    to_whatsapp = os.getenv("MY_WHATSAPP_NUMBER")

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=from_whatsapp,
        to=to_whatsapp
    )




if __name__ == "__main__":
    main()
