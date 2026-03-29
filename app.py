from flask import Flask, render_template, request, jsonify
from finance_engine import *
from ai_model import generate_advice

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json

    data['age'] = int(data['age'])
    data['income'] = float(data['income'])
    data['expenses'] = float(data['expenses'])
    data['savings'] = float(data['savings'])

    corpus, fire_sip = calculate_fire(data)
    goal = goal_sip(1000000, 5)
    recommended_sip = final_sip(fire_sip, goal)

    cashflow = plan_cashflow(data, recommended_sip)

    equity, debt = allocation(data['age'])
    gap = insurance_gap(data['income'])
    risk = risk_profile(data['age'])

    score, reasons = health_score(data)

    tax, bracket = tax_calculator(data['income'] * 12)

    advice = generate_advice(data, recommended_sip, risk, gap, bracket)

    return jsonify({
        "corpus": corpus,
        "recommended_sip": recommended_sip,
        "cashflow": cashflow,
        "equity": equity,
        "debt": debt,
        "insurance_gap": gap,
        "risk": risk,
        "score": score,
        "reasons": reasons,
        "tax": tax,
        "tax_bracket": bracket,
        "advice": advice
    })


if __name__ == "__main__":
    app.run(debug=True)