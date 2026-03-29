def calculate_sip(target, current, rate, years):
    r = rate / 12
    n = years * 12

    future_current = current * (1 + rate) ** years

    sip = (target - future_current) * r / ((1 + r) ** n - 1)
    return round(max(sip, 0), 2)


# FIRE
def calculate_fire(data):
    annual_expenses = data['expenses'] * 12
    target_corpus = annual_expenses * 25
    years_left = 60 - data['age']

    sip = calculate_sip(target_corpus, data['savings'], 0.12, years_left)
    return target_corpus, sip


# Goal SIP
def goal_sip(goal, years):
    return calculate_sip(goal, 0, 0.10, years)


# FINAL SIP
def final_sip(fire_sip, goal_sip):
    MIN_INVEST = 3000
    return round(max(fire_sip, goal_sip, MIN_INVEST), 2)


# ✅ CLEAN CASHFLOW (NO CONFUSION)
def plan_cashflow(data, sip):
    capacity = data['income'] - data['expenses']
    emergency_total = data['expenses'] * 6
    current_savings = data['savings']

    emergency_needed = max(emergency_total - current_savings, 0)

    monthly_emergency = round(emergency_needed / 6, 2)

    # Ensure we don't exceed capacity
    if monthly_emergency > capacity:
        monthly_emergency = capacity
        initial_sip = 0
    else:
        initial_sip = capacity - monthly_emergency

    return {
        "phase1": {
            "duration": "Months 1-6",
            "emergency": monthly_emergency,
            "sip": round(initial_sip, 2)
        },
        "phase2": {
            "duration": "After Month 6",
            "sip": sip
        }
    }


# ✅ CONSISTENT ALLOCATION
def allocation(age):
    equity = 90 if age < 30 else min(80, 100 - age)
    debt = 100 - equity
    return equity, debt


# Insurance Gap
def insurance_gap(income, current=0):
    ideal = income * 12 * 10
    gap = max(ideal - current, 0)
    return gap


# Risk
def risk_profile(age):
    return "Aggressive" if age < 30 else "Moderate"


# Health Score
def health_score(data):
    score = 0
    reasons = []

    if data['savings'] >= data['expenses'] * 6:
        score += 40
    else:
        reasons.append("Low emergency savings")

    if data['savings'] < data['income'] * 2:
        reasons.append("Limited investments")

    if data['income'] * 12 * 10 > data.get("insurance", 0):
        reasons.append("High insurance gap")

    ratio = data['savings'] / max(data['income'], 1)
    score += min(ratio * 60, 60)

    return int(score), reasons


# ✅ TAX (CLEAR OUTPUT)
def tax_calculator(income):
    if income <= 250000:
        return 0, "0%"
    elif income <= 500000:
        return income * 0.05, "5%"
    elif income <= 1000000:
        return income * 0.2, "20%"
    else:
        return income * 0.3, "30%"