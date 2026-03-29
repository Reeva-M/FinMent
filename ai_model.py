import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://go.fastrouter.ai/api/v1",
    api_key=os.getenv("FASTROUTER_API_KEY")
)

def generate_advice(data, sip, risk, gap, tax_bracket):
    prompt = f"""
    You are a financial advisor in India.

    STRICT RULES:
    - Monthly SIP = ₹{sip}
    - Do NOT suggest higher investments
    - Respect cashflow constraints

    User:
    Age: {data['age']}
    Income: {data['income']}
    Expenses: {data['expenses']}
    Savings: {data['savings']}
    Risk: {risk}
    Insurance Gap: ₹{gap}
    Tax Bracket: {tax_bracket}

    Provide:

    1. Investment Plan (aligned with ₹{sip})
    2. Emergency Fund (complete in 6 months)
    3. Insurance Plan (suggest term insurance for gap)
    4. Tax Advice (mention it depends on {tax_bracket})
    5. Action Steps

    Avoid unrealistic claims.
    Mention long-term wealth range (₹3–5 Cr, not 10Cr).
    """

    res = client.chat.completions.create(
        model="anthropic/claude-sonnet-4-20250514",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content