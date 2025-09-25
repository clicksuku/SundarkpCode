from fastmcp import FastMCP
import json
from datetime import datetime
from card_errors import get_random_error_code

mcp = FastMCP("Currency Validating Card Server")

def validateCardNumber(card_number_str: str) -> bool:
    card_number_str = card_number_str.replace(" ", "")  # Remove any spaces
    if not card_number_str.isdigit():
        return False  # Ensure all characters are digits

    digits = [int(d) for d in card_number_str]
    total_sum = 0

    # Iterate from right to left, doubling every second digit
    # and summing the results
    for i in range(len(digits) - 1, -1, -1):
        digit = digits[i]
        if (len(digits) - 1 - i) % 2 == 1:  # Every second digit from the right
            doubled_digit = digit * 2
            if doubled_digit > 9:
                total_sum += (doubled_digit - 9)  # Sum the digits (e.g., 12 -> 1+2=3)
            else:
                total_sum += doubled_digit
        else:
            total_sum += digit  # Add undoubled digits directly
    return total_sum % 10 == 0


@mcp.tool
def isValidCardNumber(cardNumber: str) -> bool:
    """
    Validates a card number using the Luhn algorithm.

    Args:
        card_number_str: A string representing the card number.

    Returns:
        True if the card number is valid, False otherwise.
    """
    return validateCardNumber(cardNumber)

@mcp.tool
def isCardActive(expiryDate: str) -> bool:
    """
    Checks if a credit card expiry date is valid (not expired).

    Args:
        expiry_month_year_str (str): The expiry date string in "MM/YY" format.

    Returns:
        bool: True if the expiry date is valid, False otherwise.
    """
    try:
        # Get the current date
        current_date = datetime.now()

        # Parse the expiry date string.
        # We assume the day is the first of the month for comparison.
        # Adding '01/' to create a full date string for parsing.
        expiry_date = datetime.strptime(f"01/{expiryDate}", "%d/%m/%y")

        # Compare the expiry date with the current date.
        # The card is valid if the expiry date is in the future or the current month/year.
        return expiry_date >= current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    except ValueError:
        # Handle cases where the input string is not in the expected format
        print("Invalid expiry date format. Please use MM/YY.")
        return False


@mcp.tool
async def checkCardErrorCode(cardNumber: str) -> str:
    """
    Checks if the card has any risk and compliance limitations

    Args:
        card_number_str (str): The card number string.

    Returns:
        int: returns a random error code
    """
    error = get_random_error_code()
    return error


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")