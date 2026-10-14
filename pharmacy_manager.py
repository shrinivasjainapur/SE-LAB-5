"""Manage pharmacy medicines, stock, billing, and prescriptions."""
import hashlib
import json
import os
import re
import secrets
from datetime import date, datetime

# Global pharmacy state
medicines = {}
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")


# Add medicine stock
def add_medicine(
    name,
    qty=0,
    price=0.0,
    expiry="2099-12-31",
    audit=None,
):
    """Record medicine stock and update the audit log."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Medicine name must be a non-empty string.")
    if (
        not isinstance(qty, int)
        or isinstance(qty, bool)
        or qty < 0
    ):
        raise ValueError("Quantity must be a non-negative integer.")
    if (
        not isinstance(price, (int, float))
        or isinstance(price, bool)
        or price < 0
    ):
        raise ValueError("Price must be a non-negative number.")
    datetime.strptime(expiry, "%Y-%m-%d")
    if audit is None:
        audit = []
    if name not in medicines:
        medicines[name] = {
            "qty": 0,
            "price": price,
            "expiry": expiry,
        }
    else:
        medicines[name]["price"] = price
        medicines[name]["expiry"] = expiry
    medicines[name]["qty"] += qty
    audit.append(f"{datetime.now()}: Stocked {qty} units of {name}")
    return audit


# Dispense available medicine stock
def dispense_medicine(name, qty):
    """Reduce stock after validating the requested quantity."""
    if (
        not isinstance(qty, int)
        or isinstance(qty, bool)
        or qty <= 0
    ):
        raise ValueError("Quantity must be a positive integer.")
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    if medicines[name]["qty"] < qty:
        raise ValueError(f"Insufficient stock for {name}.")
    medicines[name]["qty"] -= qty


# Return the available medicine quantity
def get_quantity(name):
    """Return the current stock quantity for a medicine."""
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    return medicines[name]["qty"]


# Check whether a medicine has expired
def is_expired(name):
    """Return whether the medicine's expiry date has passed."""
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    expiry = datetime.strptime(
        medicines[name]["expiry"], "%Y-%m-%d"
    ).date()
    return expiry < date.today()


# Calculate the total prescription bill
def bill_amount(prescription):
    """Calculate the total cost of the prescribed medicines."""
    total = 0.0
    for name, qty in prescription:
        if name not in medicines:
            raise KeyError(f"Medicine not found: {name}")
        if (
            not isinstance(qty, int)
            or isinstance(qty, bool)
            or qty < 0
        ):
            raise ValueError("Billing quantity must be non-negative.")
        total += medicines[name]["price"] * qty
    return total


# Calculate dosage from a multiplication formula
def calculate_dosage(formula):
    """Calculate dosage from a multiplication formula."""
    if not isinstance(formula, str):
        raise ValueError("Dosage formula must be a string.")
    match = re.fullmatch(
        r"\s*(\d+(?:\.\d+)?)\s*\*\s*(\d+(?:\.\d+)?)\s*",
        formula.strip(),
    )
    if not match:
        raise ValueError("Invalid dosage formula.")
    first = float(match.group(1))
    second = float(match.group(2))
    if first <= 0 or second <= 0:
        raise ValueError("Dosage values must be positive.")
    return first * second


# Generate a SHA-256 patient identifier
def patient_id(name, phone):
    """Generate a SHA-256 hash from patient details."""
    patient_data = f"{name}{phone}".encode("utf-8")
    return hashlib.sha256(patient_data).hexdigest()


# Generate a prescription number securely
def generate_rx_number():
    """Generate a prescription number using secure randomness."""
    return f"RX-{secrets.randbelow(900000) + 100000}"


# Save medicine stock to a JSON file
def save_stock(file="pharmacy.json"):
    """Save the current medicine stock to a JSON file."""
    with open(file, "w", encoding="utf-8") as stock_file:
        json.dump(medicines, stock_file, indent=4)


# Load medicine stock from a JSON file
def load_stock(file="pharmacy.json"):
    """Load medicine stock from a JSON file."""
    if not os.path.exists(file):
        medicines.clear()
        return
    with open(file, "r", encoding="utf-8") as stock_file:
        stock_data = json.load(stock_file)
    if not isinstance(stock_data, dict):
        raise ValueError("Stock file must contain a JSON object.")
    medicines.clear()
    medicines.update(stock_data)


# Print a medicine dispensing label
def print_label(name):
    """Print the dispensing label for a medicine."""
    print(f"Dispensing label: {name}")


# Find medicines nearing their expiry date
def expiring_soon(days=30):
    """Return medicines expiring within the specified number of days."""
    if not isinstance(days, int) or isinstance(days, bool) or days < 0:
        raise ValueError("Days must be a non-negative integer.")
    result = []
    today = date.today()
    for name, details in medicines.items():
        expiry = datetime.strptime(
            details["expiry"], "%Y-%m-%d"
        ).date()
        remaining_days = (expiry - today).days
        if 0 <= remaining_days <= days:
            result.append(name)
    return result


# Validate the pharmacist password
def pharmacist_login(password):
    """Check the supplied password against the configured password."""
    return bool(DB_PASSWORD) and secrets.compare_digest(
        str(password), DB_PASSWORD
    )


# Display the current pharmacy stock report
def print_stock():
    """Print the current medicine stock report."""
    print("===== Pharmacy Stock Report =====")
    for name, details in medicines.items():
        print(
            f"{name} -> {details['qty']} units, "
            f"Rs. {details['price']} exp {details['expiry']}"
        )


# Run the pharmacy manager demonstration
def main():
    """Run the pharmacy manager demonstration."""
    medicines.clear()
    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2027-01-15")
    add_medicine("Cetirizine 10mg", 10, 2.0, "2027-03-31")
    add_medicine("Vitamin C 500mg", 25)
    dispense_medicine("Paracetamol 500mg", 30)
    try:
        dispense_medicine("Insulin", 2)
    except (KeyError, ValueError) as error:
        print(f"Dispensing failed: {error}")
    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    prescription = [
        ("Paracetamol 500mg", 10),
        ("Amoxicillin 250mg", 5),
    ]
    print("Bill:", bill_amount(prescription))
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print("Login:", pharmacist_login("pharma@123"))
    print_label("Paracetamol 500mg")
    save_stock()
    load_stock()
    print_stock()


if __name__ == "__main__":
    main()
