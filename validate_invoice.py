import json
from datetime import datetime

def validate_invoice_json(json_str):
    errors = []
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON format: {e}"]
    
    # 1. Required fields check
    required_fields = ["vendor", "invoice_no", "gstin", "amount", "due_date"]
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            errors.append(f"Missing required field: '{field}'")
            
    # 2. GSTIN 15-character check
    if "gstin" in data and data["gstin"]:
        gstin = str(data["gstin"]).strip()
        if len(gstin) != 15:
            errors.append(f"Invalid GSTIN length ({len(gstin)} chars): '{gstin}'. Must be exactly 15 characters.")
            
    # 3. Date format check (YYYY-MM-DD)
    if "due_date" in data and data["due_date"]:
        date_str = str(data["due_date"]).strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            errors.append(f"Invalid due_date format: '{date_str}'. Must be YYYY-MM-DD.")
            
    # 4. Amount numeric check
    if "amount" in data and data["amount"] is not None:
        try:
            amt = float(data["amount"])
            if amt < 0:
                errors.append(f"Amount cannot be negative: {amt}")
        except ValueError:
            errors.append(f"Invalid amount format: '{data['amount']}'. Must be a number.")
            
    return errors