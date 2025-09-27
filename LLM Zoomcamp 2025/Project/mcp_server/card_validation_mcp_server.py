from fastmcp import FastMCP
import json
from datetime import datetime
import random

mcp = FastMCP("Currency Validating Card Server")

decline_codes = {
    "01": {
        "Reason": "Refer to issuer - The issuing bank prevented the transaction without a specific reason",
        "Description": "The issuing bank prevented the transaction."
    },
    "02": {
        "Reason": "Refer to issuer (special condition) - The customer's bank prevented the transaction",
        "Description": "The customer’s bank prevented the transaction."
    },
    "03": {
        "Reason": "Invalid merchant - Merchant not recognized or invalid",
        "Description": "Invalid merchant."
    },
    "04": {
        "Reason": "Pick up card (no fraud) - Bank wants merchant to hold the card (overdrawn/expired)",
        "Description": "The customer’s bank prevented the transaction and is also telling the merchant to hold the card. This doesn’t imply fraud, but rather overdrawn cards or expired ones."
    },
    "05": {
        "Reason": "Do not honor - Bank told merchant not to accept the card",
        "Description": "The customer’s bank stopped the transaction and told the merchant to 'not honor' the card."
    },
    "06": {
        "Reason": "Error - Unspecified transaction error",
        "Description": "The issuing bank can’t specify the error, but something went wrong with the transaction."
    },
    "07": {
        "Reason": "Pick up card (fraud) - Card flagged as fraudulent",
        "Description": "The customer’s bank stopped the transaction because the card or bank account has been flagged as fraudulent."
    },
    "08": {
        "Reason": "Pick up card (fraud) - Card flagged as fraudulent",
        "Description": ""
    },
    "09": {
        "Reason": "Pick up card (fraud) - Card flagged as fraudulent",
        "Description": ""
    },
    "10": {
        "Reason": "Partial approval - Bank accepts partial payment but blocks the rest",
        "Description": "The issuing bank accepts a part of the payment but blocks the rest, typically due to exceeding the credit limit or funds in the account."
    },
    "12": {
        "Reason": "Invalid transaction - Transaction type is invalid",
        "Description": "The transaction attempted is invalid."
    },
    "13": {
        "Reason": "Invalid amount - Invalid transaction amount entered",
        "Description": "The amount you entered for the transaction was invalid."
    },
    "14": {
        "Reason": "Invalid account number - Card number is invalid",
        "Description": "The card number is invalid."
    },
    "15": {
        "Reason": "No such issuer - First digit identifies wrong issuing bank",
        "Description": "The first digit, which identifies the card’s issuing bank, was incorrect."
    },
    "19": {
        "Reason": "Re-enter transaction - Unknown error occurred",
        "Description": "An unknown error occurred."
    },
    "21": {
        "Reason": "No action taken",
        "Description": ""
    },
    "25": {
        "Reason": "Unable to locate record in file",
        "Description": ""
    },
    "28": {
        "Reason": "File temporarily unavailable",
        "Description": "An error occurred during the transaction without the reason specified."
    },
    "30": {
        "Reason": "Format error",
        "Description": ""
    },
    "41": {
        "Reason": "Lost card, pick up - Card reported lost",
        "Description": "The card's legitimate owner has reported it lost or stolen, so the card issuer has denied the transaction."
    },
    "43": {
        "Reason": "Stolen card, pick up - Card reported stolen",
        "Description": "The legitimate owner has reported the card as stolen, so the card issuer denied the transaction."
    },
    "51": {
        "Reason": "Insufficient funds/over credit limit",
        "Description": "The card issuer is blocking the transaction because the account has already exceeded the credit limit, or the pending transaction would put the card over."
    },
    "52": {
        "Reason": "No current account",
        "Description": ""
    },
    "53": {
        "Reason": "No savings account",
        "Description": ""
    },
    "54": {
        "Reason": "Expired card",
        "Description": "The expiration date has already passed."
    },
    "55": {
        "Reason": "Incorrect PIN",
        "Description": ""
    },
    "57": {
        "Reason": "Transaction not permitted - card",
        "Description": "This code shows up when you're trying to use a card for a transaction that's specifically not allowed."
    },
    "58": {
        "Reason": "Transaction not permitted - terminal",
        "Description": "If the merchant account connected to the terminal or payment processor is not properly configured, you’ll see this error."
    },
    "59": {
        "Reason": "Suspected fraud",
        "Description": ""
    },
    "61": {
        "Reason": "Exceeds approval amount limit",
        "Description": ""
    },
    "62": {
        "Reason": "Invalid/restricted service code",
        "Description": "The invalid service code can refer to two specific situations.1: You’re trying to process an American Express or Discover card, but the system doesn’t support those card issuers. 2: You tried to pay for online purchase with a card that doesn’t support online payments."
    },
    "63": {
        "Reason": "Security violation - Incorrect CVV/CVC/CID",
        "Description": "The three-digit CVV2 or CVC or the four-digit CID security code was incorrect or wasn’t read properly."
    },
    "64": {
        "Reason": "Transaction does not fulfil AML requirement",
        "Description": ""
    },
    "65": {
        "Reason": "Exceeds withdrawal limit",
        "Description": "The credit card user has exceeded the credit limit."
    },
    "70": {
        "Reason": "PIN data required",
        "Description": ""
    },
    "71": {
        "Reason": "PIN Not Changed",
        "Description": ""
    },
    "75": {
        "Reason": "Allowable number of PIN entry attempts exceeded",
        "Description": "Allowable number of PIN tries exceeded."
    },
    "76": {
        "Reason": "Invalid/nonexistent 'To Account' specified",
        "Description": "Invalid/nonexistent 'To Account' specified"
    },
    "77": {
        "Reason": "Invalid/nonexistent 'From Account' specified",
        "Description": "Invalid/nonexistent 'From Account' specified"
    },
    "78": {
        "Reason": "Blocked, first use",
        "Description": "Blocked, first use"
    },
    "79": {
        "Reason": "Already reversed",
        "Description": "Already reversed"
    },
    "82": {
        "Reason": "Negative CAM, dCVV, iCVV or CVV results",
        "Description": "Negative CAM, dCVV, iCVV or CVV results"
    },
    "85": {
        "Reason": "No reason to decline",
        "Description": "The issuing bank can’t identify a specific problem, but the transaction still didn’t go through."
    },
    "86": {
        "Reason": "Cannot verify PIN",
        "Description": "Cannot verify PIN"
    },
    "87": {
        "Reason": "Purchase Amount Only, No Cash Back Allowed",
        "Description": ""
    },
    "88": {
        "Reason": "Cryptographic failure",
        "Description": ""
    },
    "89": {
        "Reason": "Unacceptable PIN - Retry",
        "Description": ""
    },
    "90": {
        "Reason": "Cutoff is in progress",
        "Description": ""
    },
    "91": {
        "Reason": "Issuer or switch unavailable",
        "Description": "The terminal or payment processor was unable to complete the payment authorization."
    },
    "92": {
        "Reason": "Unable to route transaction",
        "Description": "The terminal cannot reach the card issuer to process the transaction."
    },
    "93": {
        "Reason": "Transaction can't be completed - legal violation",
        "Description": "The issuing bank has recognized (or has been informed of) a legal violation on the part of the credit card user, and assets have been frozen."
    },
    "94": {
        "Reason": "Duplicate transaction detected",
        "Description": "Duplicate transaction detected"
    },
    "96": {
        "Reason": "System error",
        "Description": "There’s a temporary issue with the payment processor."
    },
    "97": {
        "Reason": "Invalid CVV",
        "Description": "Invalid CVV"
    },
    "1A": {
        "Reason": "Additional customer authentication required",
        "Description": ""
    },
    "R0": {
        "Reason": "Recurring charge stopped at customer request",
        "Description": "Customer asked to stop the recurring payment."
    },
    "R1": {
        "Reason": "Recurring charge stopped at customer request",
        "Description": "Customer asked to stop the recurring payment."
    },
    "CV": {
        "Reason": "Card type verification error (chip/magnetic strip issue)",
        "Description": "The card reader had a problem verifying the card. This could be an issue with the microchip or the magnet strip."
    },
    "W1": {
        "Reason": "Error connecting to bank",
        "Description": "This can happen because of a power or service outage."
    },
    "W2": {
        "Reason": "Error connecting to bank",
        "Description": "This can happen because of a power or service outage."
    },
    "W9": {
        "Reason": "Error connecting to bank",
        "Description": "This can happen because of a power or service outage."
    },
    "00": {
        "Reason": "Approved or completed successfully (included for reference)",
        "Description": "(Included for reference)"
    },
    "08": {
        "Reason": "Honor with ID",
        "Description": ""
    },
    "1Z": {
        "Reason": "Authorization system or issuer system inoperative",
        "Description": ""
    },
    "215": {
        "Reason": "Lost/stolen card",
        "Description": "The real cardholder has reported the card as lost or stolen, and the card issuer blocks the transaction."
    },
    "534": {
        "Reason": "Do not honor, high fraud",
        "Description": "The transaction failed PayPal or Google Checkout risk modeling."
    },
    "596": {
        "Reason": "Suspected fraud",
        "Description": "Again, the card issuer suspects fraud and has blocked the transaction."
    }
}
    
async def get_random_error_code():
    # Choose a random error and return its human-readable text
    number = random.randint(1, 100)
    code = str(number).zfill(2)
    reason_desc = decline_codes.get(code)
    if reason_desc is None:
        number = random.randint(1, 10)
        code = str(number).zfill(2)
        reason_desc = decline_codes.get(code)
    
    reason = reason_desc.get("Reason")
    description = reason_desc.get("Description")
    value = f"{code}: {reason}: {description}"
    return value

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
        str: Returns a string with the random error code and description, e.g. "05: Lost card – pick up"
    """
    result = await get_random_error_code()
    return result


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")