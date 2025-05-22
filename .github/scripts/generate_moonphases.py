import json
from datetime import datetime, timedelta

# Constants
LUNAR_CYCLE = 29.530588853  # average days between new moons
KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14)

# Moon phase offsets
PHASES = [
    ("New Moon", 0.0),
    ("First Quarter", 0.25),
    ("Full Moon", 0.5),
    ("Third Quarter", 0.75),
]

def days_since_known(date):
    return (date - KNOWN_NEW_MOON).total_seconds() / (86400)

def moon_phase_fraction(date):
    days = days_since_known(date)
    phase = (days % LUNAR_CYCLE) / LUNAR_CYCLE
    return phase if phase >= 0 else phase + 1

def find_next_phase(start, target_fraction):
    date = start
    for _ in range(40):
        phase = moon_phase_fraction(date)
        delta = abs(phase - target_fraction)
        delta = min(delta, 1 - delta)
        if delta < 0.02:
            return date
        date += timedelta(hours=6)
    return None

def generate_next_phases():
    now = datetime.utcnow()
    results = []
    date = now
    for i in range(4):
        name, target = PHASES[i % 4]
        next_date = find_next_phase(date, target)
        results.append({
            "name": name,
            "date": next_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        date = next_date + timedelta(hours=6)
    return results

if __name__ == "__main__":
    phases = generate_next_phases()
    with open("moonphases.json", "w") as f:
        json.dump(phases, f, indent=2)
