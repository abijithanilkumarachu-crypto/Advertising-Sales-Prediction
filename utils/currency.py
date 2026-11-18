"""
Currency conversion utilities and Indian Rupee (INR / ₹) configuration.
Provides conversion between INR advertising budgets and the original ML model's USD scale.
"""

# ==============================================================================
# CENTRALLY CONFIGURABLE EXCHANGE RATE
# ==============================================================================
# The original ML model was trained on the Advertising dataset where advertising
# budget values are expressed in thousands of US dollars ($k).
# Formula: Model input = INR amount / (USD_TO_INR_RATE * 1000)
# Example: At ₹90/USD, ₹1,35,00,000 -> 13,500,000 / (90 * 1000) = 150.0
# Update this exchange rate constant as needed.
# ==============================================================================
DEFAULT_USD_TO_INR = 90.0

TRANSPARENCY_NOTE = (
    "This application accepts advertising budgets in INR and converts them into "
    "the original dataset's USD-based scale before prediction. Currency conversion is "
    "approximate. The model was trained on historical US advertising data and has "
    "not been specifically calibrated for the Indian advertising market."
)


def inr_to_model_units(inr_amount: float, exchange_rate: float = DEFAULT_USD_TO_INR) -> float:
    """
    Converts an advertising budget amount in Indian Rupees (INR) to the original
    model's scale (thousands of USD).

    Formula: Model input = INR amount / (exchange_rate * 1000)
    """
    if inr_amount < 0:
        raise ValueError("Budget amount cannot be negative.")
    if exchange_rate <= 0:
        raise ValueError("Exchange rate must be positive.")
    return float(inr_amount) / (float(exchange_rate) * 1000.0)


def model_units_to_inr(model_units: float, exchange_rate: float = DEFAULT_USD_TO_INR) -> float:
    """
    Converts model units (thousands of USD) back to Indian Rupees (INR).

    Formula: INR amount = model units * exchange_rate * 1000
    """
    if exchange_rate <= 0:
        raise ValueError("Exchange rate must be positive.")
    return float(model_units) * float(exchange_rate) * 1000.0


def format_inr_currency(amount: float) -> str:
    """
    Formats a numeric amount into standard Indian currency string (₹x,xx,xxx).
    Example: 13500000 -> '₹1,35,00,000'
    """
    if amount < 0:
        return f"-{format_inr_currency(abs(amount))}"
    
    num_str = str(int(round(amount)))
    if len(num_str) <= 3:
        return f"₹{num_str}"
    
    last_three = num_str[-3:]
    remaining = num_str[:-3]
    parts = []
    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]
    if remaining:
        parts.insert(0, remaining)
    
    formatted_body = ",".join(parts)
    return f"₹{formatted_body},{last_three}"


def format_inr_readable(amount: float) -> str:
    """
    Formats an INR amount into readable Indian notation with Lakhs / Crores.
    Example: 13500000 -> '₹1.35 Cr (₹1,35,00,000)'
             2250000  -> '₹22.50 Lakh (₹22,50,000)'
             45000    -> '₹45,000'
    """
    full_inr = format_inr_currency(amount)
    if amount >= 10_000_000:
        crores = amount / 10_000_000
        return f"₹{crores:.2f} Cr ({full_inr})"
    elif amount >= 100_000:
        lakhs = amount / 100_000
        return f"₹{lakhs:.2f} Lakh ({full_inr})"
    else:
        return full_inr


def format_inr_short(amount: float) -> str:
    """
    Formats an INR amount into concise Indian notation.
    Example: 13500000 -> '₹1.35 Cr'
             2250000  -> '₹22.5 Lakh'
             45000    -> '₹45k'
    """
    if amount >= 10_000_000:
        return f"₹{amount / 10_000_000:.2f} Cr"
    elif amount >= 100_000:
        return f"₹{amount / 100_000:.2f} Lakh"
    elif amount >= 1_000:
        return f"₹{amount / 1_000:.1f}k"
    else:
        return f"₹{amount:,.0f}"


def get_inr_historical_bounds(exchange_rate: float = DEFAULT_USD_TO_INR) -> dict:
    """
    Returns historical dataset minimum and maximum bounds converted to INR.
    Original USD ranges:
      TV: [0.7, 296.4]
      radio: [0.0, 49.6]
      newspaper: [0.3, 114.0]
    """
    from utils.model_loader import HISTORICAL_BOUNDS
    inr_bounds = {}
    for channel, bounds in HISTORICAL_BOUNDS.items():
        inr_bounds[channel] = {
            "min_usd": bounds["min"],
            "max_usd": bounds["max"],
            "min_inr": model_units_to_inr(bounds["min"], exchange_rate),
            "max_inr": model_units_to_inr(bounds["max"], exchange_rate),
        }
    return inr_bounds
