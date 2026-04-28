# Sternritter Smart System: AI-Powered Smart Home Controller

Sternritter Control is a dynamic smart home automation simulator built with Python and Streamlit. It intelligently manages home environment sensors by combining classical utility-based decision making with an on-demand Google Gemini LLM backend.

## ✨ Features

- **Automated & Manual Modes**: Run the simulation automatically with randomized sensor data, or manually override temperature, light, time, and motion to test specific scenarios.
- **Utility-Based Agent Logic**: Makes smart decisions about Heating/Cooling, Lighting, and Power based on weighted comfort and energy efficiency algorithms.
- **Credit-Safe AI Brain**: Connects to the Google Gemini API to explain the agent's decisions in plain English. Operates strictly "On-Demand" to conserve your API credits.
- **Integrated Chatbot**: Ask the Sternritter AI questions about your home status directly within the dashboard.
- **Activity Logging**: Automatically logs all sensor data, agent decisions, and AI explanations to a local CSV file. Export and archive capabilities built-in.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/munafsolanki/SmartHome-AI.git
   cd SmartHome-AI
   ```

2. **Install the required dependencies:**
   Make sure you have Python installed. Then, install the required packages using pip:
   ```bash
   pip install streamlit pandas plotly google-genai
   ```

3. **Set up Environment Variables (Optional but Recommended):**
   Create a `.env` file in the root directory and add your Google Gemini API Key. Alternatively, you can input this directly in the dashboard UI.
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

## 🚀 How to Run

Start the Streamlit application by running the following command in your terminal:

```bash
streamlit run main.py
```

The dashboard will open automatically in your default web browser (usually at `http://localhost:8501`).

## 📁 Project Structure

- `main.py`: The core Streamlit application and UI dashboard.
- `agent.py`: The utility-based logic defining how the system reacts to different sensor inputs.
- `ai_module.py`: Handles the connection to Google's Gemini API for on-demand explanations and chatbot features.
- `sensors.py`: Generates simulated data and handles manual override inputs.
- `logger.py`: Manages data logging, history retrieval, and CSV archiving.

---
*Built for intelligent home management simulation.*
