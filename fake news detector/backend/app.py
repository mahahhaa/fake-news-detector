from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import json

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key="",
    base_url="https://ellm.nrp-nautilus.io/v1",
    timeout=120,
)

SYSTEM_PROMPT = """
You are a media literacy expert and fact-checking assistant.
Analyze the following news headline or article snippet for credibility.

Return ONLY valid JSON in this exact format, no extra text:
{
  "credibility_score": <number from 0 to 100>,
  "verdict": "<one of: 'likely credible', 'uncertain', 'likely misleading'>",
  "flags": [
    {
      "type": "<one of: 'emotional language', 'logical fallacy', 'missing source', 'clickbait', 'exaggeration'>",
      "quote": "<the exact word or phrase from the headline that is problematic>",
      "explanation": "<one sentence explaining why this is flagged>"
    }
  ],
  "reasoning": "<2-3 sentence plain English summary of your overall assessment>",
  "suggested_search": "<a search query the user could Google to verify this claim>"
}
"""

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    if not data or "headline" not in data:
        return jsonify({"error": "Please provide a headline."}), 400

    headline = data["headline"].strip()

    if len(headline) < 10:
        return jsonify({"error": "Headline is too short."}), 400

    try:
        completion = client.chat.completions.create(
            model="qwen3-small",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this: {headline}"}
            ],
        )

        raw = completion.choices[0].message.content
        print("AI raw response:", raw)
        result = json.loads(raw)
        return jsonify(result)

    except json.JSONDecodeError:
        print("Failed to parse:", raw)
        return jsonify({"error": "AI returned unexpected format.", "raw": raw}), 500

    except Exception as e:
        print("EXCEPTION TYPE:", type(e).__name__)
        print("EXCEPTION DETAIL:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Fake News Detector API is running!"


if __name__ == "__main__":
    app.run(debug=True)