from openai import OpenAI
import json

client = OpenAI(
    api_key="",
    base_url="https://ellm.nrp-nautilus.io/v1",
    timeout=30,
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

def analyze_headline(headline):
    completion = client.chat.completions.create(
        model="gpt-oss",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analyze this: {headline}"}
        ],
    )

    raw = completion.choices[0].message.content

    try:
        result = json.loads(raw)
        print("\n--- RESULTS ---")
        print(f"Credibility Score : {result['credibility_score']}/100")
        print(f"Verdict           : {result['verdict']}")
        print(f"Reasoning         : {result['reasoning']}")
        print(f"Suggested Search  : {result['suggested_search']}")
        print("\nFlags:")
        for flag in result['flags']:
            print(f"  - [{flag['type']}] \"{flag['quote']}\" → {flag['explanation']}")
    except json.JSONDecodeError:
        print("Raw response (not JSON):", raw)

# Test it with a headline
analyze_headline("BREAKING: Scientists confirm chocolate cures cancer, big pharma doesn't want you to know")