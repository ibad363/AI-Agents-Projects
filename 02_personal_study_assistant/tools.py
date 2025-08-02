import os
import requests
import google.generativeai as genai
from agents import function_tool

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
# print("SERPER_API_KEY:", SERPER_API_KEY)

@function_tool()
async def web_search(query: str) -> str:
    try:
        print("🔎 Using Serper API for:", query)

        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"q": query}

        # ✅ MUST use POST, not GET
        res = requests.post("https://google.serper.dev/news", headers=headers, json=payload)

        if res.status_code != 200:
            return f"❌ Serper API failed with status code: {res.status_code}"

        data = res.json()
        articles = data.get("news", [])[:3]

        if not articles:
            return "❌ No news found."

        # 🧠 Summarize with Gemini
        content = "Summarize this news:\n" + "\n".join(f"{a['title']} - {a['link']}" for a in articles)

        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(content)

        return response.text.strip()

    except Exception as e:
        print (f"Error in web_search: {str(e)}")
        return f"❌ Error: {str(e)}"