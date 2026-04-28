from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiProvider:
    def __init__(self, api_key=None):
        # Using the new Google GenAI SDK (google-genai)
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        self.last_error = None
        self.model_id = "gemini-3-flash-preview"
        
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                self.client = None
                self.last_error = str(e)
                print(f"Error configuring Gemini: {e}")

    def is_active(self):
        return self.client is not None

    def generate_explanation(self, action, sensors):
        if not self.is_active():
            return "Local Rule: Threshold matched sensor data."
        
        prompt = f"System decided: '{action}'. Sensors: {sensors}. 2-sentence explanation."
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text.strip()
        except:
            return f"{action} triggered by environmental conditions."

    def get_recommendations(self, history_summary):
        # AI Recommendations disabled to save free tier credits
        return [
            "Tip: Keep temperature above 24°C to save energy.",
            "Tip: Turn off lights when natural light intensity is high.",
            "Tip: Motion detection helps prevent unnecessary power usage."
        ]

    def get_chat_response(self, user_query, current_state, chat_history):
        if not self.is_active():
            return "I'm offline. Using local logic."
            
        system_instruction = f"You are the brain of the Sternritter Smart System. Current State: {current_state}."
        
        # Mapping chat history to the new SDK structure
        # The new SDK uses a different history structure for full chat sessions, 
        # but we can pass context in the prompt for simplicity or use the chat session.
        # For this logic, we use context in prompt.
        prompt = f"System Context: {system_instruction}\nHistory: {chat_history}\nUser: {user_query}. Answer concisely."
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"Brain Error: {str(e)}"
