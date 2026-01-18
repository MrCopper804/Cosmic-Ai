import google.generativeai as genai
import requests
import base64

# --- CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyCPFq6h-wYpFwkDWq4Do4B9AroKm72earA"
GITHUB_TOKEN = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN" # Yahan apna GitHub Token dalein
REPO_NAME = "your-username/cosmic-ai-project"
FILE_PATH = "cosmic_ai_logic.py"

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def cosmic_ai_chat(prompt):
    # System Instruction for "Cosmic AI"
    full_prompt = f"System: You are Cosmic AI, a brilliant and helpful assistant. User: {prompt}"
    response = model.generate_content(full_prompt)
    return response.text

def save_to_github(content):
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Encode content to Base64
    encoded_content = base64.b64encode(content.encode()).decode()
    
    data = {
        "message": "Update Cosmic AI Logic",
        "content": encoded_content
    }
    
    # Pehle check karte hain file exist karti hai ya nahi (SHA lene ke liye)
    get_res = requests.get(url, headers=headers)
    if get_res.status_code == 200:
        data["sha"] = get_res.json()["sha"]

    res = requests.put(url, headers=headers, json=data)
    if res.status_code in [200, 201]:
        print("✅ Cosmic AI logic successfully saved to GitHub!")
    else:
        print(f"❌ Error saving to GitHub: {res.text}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("Welcome to Cosmic AI 🌌")
    user_msg = input("Aapka sawal: ")
    
    # 1. Get AI Response
    ai_reply = cosmic_ai_chat(user_msg)
    print(f"\nCosmic AI: {ai_reply}")
    
    # 2. Save this interaction or logic to GitHub
    log_content = f"# Cosmic AI Interaction\n# User: {user_msg}\n# AI: {ai_reply}\n"
    save_to_github(log_content)
