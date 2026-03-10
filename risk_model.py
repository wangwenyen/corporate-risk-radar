import math

def calculate_survival_months(liquidity, burn_rate):

    if burn_rate == 0:
        return 0

    survival = liquidity / burn_rate
    return round(survival,2)


def bankruptcy_probability(survival_months):

    # logistic risk model
    alpha = 2.5
    beta = -0.35

    z = alpha + beta * survival_months

    probability = 1 / (1 + math.exp(-z))

    return round(probability * 100,2)