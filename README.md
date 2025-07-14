💍 Rishtey Wali Auntie - AI Matchmaking Agent
An AI-powered matchmaking agent built with OpenAI-compatible Gemini models, DuckDuckGo web search, and Twilio WhatsApp API to deliver matches straight to your WhatsApp. 🤖📱

📌 Features
🤝 AI Matchmaking Assistant ("Auntie") helps find suitable matches based on age.

🌐 Web Search Tool using DuckDuckGo to fetch LinkedIn, Instagram, Facebook, and TikTok profiles.

💬 WhatsApp Integration via Twilio to send results directly to your phone.

🧠 Powered by Gemini model using OpenAI-compatible interfaces.

⚙️ Modular, tool-based agent built with the agents framework.

🏗️ Project Structure
bash
Copy
Edit
📁 match-making/
├── main.py              # Main agent logic
├── .env                 # API keys and credentials
├── search_tools.py      # DDGS search wrapper
├── requirements.txt     # Dependencies
🔧 Setup Instructions
✅ 1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/your-username/rishtey-wali-auntie.git
cd rishtey-wali-auntie
✅ 2. Create and Activate Virtual Environment (optional)
bash
Copy
Edit
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
✅ 3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Include these packages in requirements.txt:

Copy
Edit
python-dotenv
agents
ddgs
twilio
✅ 4. Setup .env File
Create a .env file in the project root:

env
Copy
Edit
# Gemini
GEMINI_API_KEY=your_gemini_api_key

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
MY_WHATSAPP_NUMBER=whatsapp:+92xxxxxxxxxx
🚀 Run the App
bash
Copy
Edit
uv run main.py
Or if using plain Python:

bash
Copy
Edit
python main.py
🤖 How It Works
get_user_data(min_age) filters predefined users based on age.

search_duckduckgo(query) searches LinkedIn, Facebook, etc. for relevant matches.

Agent is initialized with:

Gemini model

Instructions to behave like a matchmaking "Auntie"

Both tools registered

Result is sent to your WhatsApp number using Twilio's API.

🛠️ Example Query
"Find a match of 20 minimum age and tell me the details about the match from LinkedIn, Instagram, Facebook, Tiktok."

Output:

Filtered user data

Top 5 DuckDuckGo search results

Result printed in terminal & sent via WhatsApp ✅

📸 Screenshot (Optional)
You can add a screenshot showing a WhatsApp message or terminal output here.

🧠 Tech Stack
Component	Library
AI Agent	agents
LLM Backend	Gemini (AsyncOpenAI wrapper)
Web Search	ddgs
Messaging	twilio
Env Handling	python-dotenv

📬 Contact
Made with ❤️ by @zainscity

If you have any issues or suggestions, feel free to open an issue or pull request.