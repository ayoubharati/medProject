import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# Generate realistic pharmaceutical data
def generate_amm_data(num_records):
    data = []
    manufacturers = ["PharmaCorp", "HealthGen", "MediVita", "CureAll", "BioPharm Solutions"]
    products = {
        "MediSafeX": {"type": "antibiotic", "normal_dosage": "500mg", "suspicious_dosage": "2000mg"},
        "QuickHeal": {"type": "painkiller", "normal_dosage": "400mg", "suspicious_dosage": "800mg"},
        "PainAway": {"type": "analgesic", "normal_dosage": "200mg", "suspicious_dosage": "1000mg"},
        "FlexiJoint": {"type": "anti-inflammatory", "normal_dosage": "100mg", "suspicious_dosage": "500mg"},
        "CardioPlus": {"type": "cardiovascular", "normal_dosage": "50mg", "suspicious_dosage": "200mg"}
    }

    for i in range(1, num_records + 1):
        amm_number = f"AMM-2023-{i:03d}"
        product_name = random.choice(list(products.keys()))
        manufacturer = random.choice(manufacturers)

        # Generate realistic dates
        submission_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 180))

        # 25% fraud rate
        is_fraud = random.random() < 0.25

        if is_fraud:
            # --- Fraudulent characteristics (moderate overlap with legit) ---
            approval_days   = random.randint(20, 150)     # overlaps legit at 45–60
            participants    = random.randint(500, 1200)   # overlaps legit at 700–900
            side_effects    = int(participants * random.uniform(0.10, 0.25))  # overlaps legit
            batch_size      = random.choice([30000, 50000, 75000, 100000])   # overlaps legit
            production_cost = round(random.uniform(3.0, 9.0), 2)             # overlaps legit
            price           = round(production_cost * random.uniform(10.0, 22.0), 2)  # overlaps legit

        else:
            # --- Normal characteristics (moderate overlap with fraud) ---
            approval_days   = random.randint(45, 180)    # overlaps fraud at 45–60
            participants    = random.randint(700, 2000)  # overlaps fraud at 700–900
            side_effects    = random.randint(5, int(participants * 0.12))    # overlaps fraud
            batch_size      = random.choice([75000, 100000, 150000, 200000]) # overlaps fraud
            production_cost = round(random.uniform(5.0, 15.0), 2)
            price           = round(production_cost * random.uniform(3.0, 9.0), 2)  # overlaps fraud

        # --- Add realistic noise to all records ---
        approval_days   = max(1, approval_days + random.randint(-7, 7))
        participants    = max(100, participants + random.randint(-50, 50))
        side_effects    = max(0, side_effects + random.randint(-3, 3))
        production_cost = max(0.5, round(production_cost + random.uniform(-0.5, 0.5), 2))
        price           = max(0.1, round(price + random.uniform(-1.0, 1.0), 2))

        approval_date = submission_date + timedelta(days=approval_days)

        # Additional fraud indicators (kept from original)
        suspicious_patterns = []
        if is_fraud:
            if approval_days < 30:
                suspicious_patterns.append("fast_approval")
            if price / production_cost > 10:
                suspicious_patterns.append("high_markup")
            if participants > 0 and side_effects / participants > 0.15:
                suspicious_patterns.append("high_side_effects")
            if batch_size < 50000:
                suspicious_patterns.append("small_batch")
            if participants < 500:
                suspicious_patterns.append("small_trial")

        data.append([
            amm_number,
            product_name,
            manufacturer,
            submission_date.strftime("%Y-%m-%d"),
            approval_date.strftime("%Y-%m-%d"),
            participants,
            side_effects,
            batch_size,
            f"{price:.2f}",
            f"{production_cost:.2f}",
            int(is_fraud),
            ",".join(suspicious_patterns) if suspicious_patterns else "none"
        ])

    # --- Add 5% label noise (flip some labels) ---
    noise_rate = 0.05
    for row in data:
        if random.random() < noise_rate:
            row[10] = 1 - row[10]  # flip 0→1 or 1→0

    return data


# Write to CSV
def write_to_csv(filename, data):
    headers = [
        "amm_number", "product_name", "manufacturer", "submission_date", "approval_date",
        "clinical_trial_participants", "reported_side_effects", "batch_size",
        "price_per_unit", "production_cost", "is_fraud", "suspicious_patterns"
    ]

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Generated {filename} with {len(data)} records")
    print(f"Fraud rate: {sum(1 for row in data if row[10] == 1) / len(data):.1%}")


# Generate and save data
pharma_data = generate_amm_data(1000)
write_to_csv("pharma_amm_data.csv", pharma_data)