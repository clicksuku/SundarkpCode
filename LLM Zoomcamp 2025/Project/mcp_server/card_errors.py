import random

errorCodes = {
        "01": "Refer to issuer",
        "02": "Do not honor",
        "03": "Pick up card (no fraud)",
        "04": "Pick up card (fraud account)",
        "05": "Lost card – pick up",
        "06": "Stolen card – pick up",
        "07": "Transaction not permitted – card",
        "08": "Security violation (e.g., CVV/CID mismatch)",
        "09": "Violation – cannot complete",
        "10": "Restricted card",
        "11": "Transaction limit exceeded",
        "12": "Daily limit exceeded",
        "13": "Service/MCC not allowed",
        "14": "Country/region restricted",
        "15": "MCC restricted",
        "16": "Monthly limit exceeded",
        "17": "Weekly limit exceeded",
        "18": "Contactless limit exceeded",
        "19": "Below minimum amount",
        "20": "Above maximum amount",
    }
    
def get_random_error_code():
    # Choose a random error and return its human-readable text
    random_index = random.randint(0, 20)
    value = errorCodes.get(str(random_index))
    return value

