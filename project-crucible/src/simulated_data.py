"""
Project Crucible — Simulated Data Generator
Generates realistic Arizona fire incident data when NERIS API credentials
are not available. Allows the full pipeline to run in demo mode.
"""

import random
from datetime import datetime, timedelta


# Arizona city coordinates (lat, lon)
AZ_LOCATIONS = [
    {"name": "Phoenix", "lat": 33.4484, "lon": -112.0740},
    {"name": "Phoenix - South Mountain", "lat": 33.3456, "lon": -112.0600},
    {"name": "Phoenix - Ahwatukee", "lat": 33.3200, "lon": -111.9800},
    {"name": "Tucson", "lat": 32.2226, "lon": -110.9747},
    {"name": "Tucson - Catalina Foothills", "lat": 32.3300, "lon": -110.9200},
    {"name": "Flagstaff", "lat": 35.1983, "lon": -111.6513},
    {"name": "Prescott", "lat": 34.5400, "lon": -112.4685},
    {"name": "Sedona", "lat": 34.8697, "lon": -111.7610},
    {"name": "Mesa", "lat": 33.4152, "lon": -111.8315},
    {"name": "Tempe", "lat": 33.4255, "lon": -111.9400},
    {"name": "Scottsdale", "lat": 33.4942, "lon": -111.9261},
    {"name": "Scottsdale - North", "lat": 33.7200, "lon": -111.9000},
    {"name": "Yuma", "lat": 32.6927, "lon": -114.6277},
    {"name": "Sierra Vista", "lat": 31.5455, "lon": -110.3035},
    {"name": "Chandler", "lat": 33.3062, "lon": -111.8413},
    {"name": "Gilbert", "lat": 33.3528, "lon": -111.7890},
    {"name": "Glendale", "lat": 33.5387, "lon": -112.1860},
    {"name": "Peoria", "lat": 33.5806, "lon": -112.2374},
    {"name": "Surprise", "lat": 33.6292, "lon": -112.3680},
    {"name": "Payson", "lat": 34.2309, "lon": -111.3251},
    {"name": "Kingman", "lat": 35.1894, "lon": -114.0530},
    {"name": "Lake Havasu City", "lat": 34.4839, "lon": -114.3225},
    {"name": "Bullhead City", "lat": 35.1478, "lon": -114.5683},
    {"name": "Casa Grande", "lat": 32.8795, "lon": -111.7574},
    {"name": "Maricopa", "lat": 33.0581, "lon": -112.0476},
]

INCIDENT_TYPES = [
    "structure_fire",
    "wildfire",
    "vehicle_fire",
    "cooking_fire",
    "electrical_fire",
    "brush_fire",
    "dumpster_fire",
    "chimney_fire",
]

INCIDENT_TYPE_WEIGHTS = [30, 15, 20, 15, 10, 5, 3, 2]

PROPERTY_USE_TYPES = [
    "single_family_dwelling",
    "multi_family_dwelling",
    "commercial",
    "industrial",
    "wildland",
    "vehicle",
    "mixed_use",
]

SUPPRESSION_PERFORMANCE = ["operated_effectively", "failed", "not_present", "not_applicable"]

SMOKE_ALARM_STATUS = ["present_operated", "present_did_not_operate", "not_present", "undetermined"]

WEATHER_CONDITIONS = ["clear", "windy", "hot_dry", "monsoon", "overcast"]


def _random_timestamp(days_back: int = 90) -> str:
    """Generate a random ISO timestamp within the last N days."""
    base = datetime.now() - timedelta(days=random.randint(1, days_back))
    base = base.replace(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
    )
    return base.isoformat() + "Z"


def _jitter_coords(lat: float, lon: float, radius: float = 0.05) -> tuple:
    """Add small random offset to coordinates for variety."""
    return (
        lat + random.uniform(-radius, radius),
        lon + random.uniform(-radius, radius),
    )


def generate_simulated_incidents(count: int = 40) -> list:
    """
    Generate realistic simulated Arizona fire incident data.

    Returns a list of incident dicts matching the NERIS IncidentResponse schema.
    """
    incidents = []

    for i in range(count):
        location = random.choice(AZ_LOCATIONS)
        lat, lon = _jitter_coords(location["lat"], location["lon"])

        # Ensure coordinates stay within Arizona bounds
        lat = max(31.3, min(37.0, lat))
        lon = max(-114.8, min(-109.0, lon))

        incident_type = random.choices(INCIDENT_TYPES, weights=INCIDENT_TYPE_WEIGHTS, k=1)[0]

        # Generate dispatch timestamps
        dispatch_time = datetime.now() - timedelta(days=random.randint(1, 90))
        dispatch_time = dispatch_time.replace(
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
        )
        response_minutes = random.uniform(3.0, 18.0)
        arrival_time = dispatch_time + timedelta(minutes=response_minutes)
        controlled_time = arrival_time + timedelta(minutes=random.uniform(5.0, 120.0))

        # Suppression system data
        has_suppression = random.random() < 0.35
        suppression_data = None
        if has_suppression:
            perf = random.choices(
                SUPPRESSION_PERFORMANCE[:2],
                weights=[75, 25],
                k=1,
            )[0]
            suppression_data = {
                "type": random.choice(["wet_sprinkler", "dry_sprinkler", "standpipe"]),
                "performance": perf,
                "coverage": random.choice(["complete", "partial"]),
            }
        elif incident_type in ("structure_fire", "cooking_fire", "electrical_fire"):
            suppression_data = {
                "type": "none",
                "performance": "not_present",
                "coverage": "none",
            }

        # Smoke alarm data
        smoke_alarm = {
            "status": random.choices(
                SMOKE_ALARM_STATUS,
                weights=[50, 15, 30, 5],
                k=1,
            )[0],
            "type": random.choice(["ionization", "photoelectric", "combination", "unknown"]),
            "power_source": random.choice(["battery", "hardwired", "hardwired_with_battery", "unknown"]),
        }

        # Weather data (Arizona-specific)
        temp_f = random.randint(55, 115)
        humidity = random.randint(5, 45)
        wind_mph = random.uniform(0, 35)
        weather = {
            "temperature_f": temp_f,
            "humidity_pct": humidity,
            "wind_speed_mph": round(wind_mph, 1),
            "wind_direction": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"]),
            "conditions": random.choices(
                WEATHER_CONDITIONS,
                weights=[40, 20, 25, 10, 5],
                k=1,
            )[0],
        }

        # Property loss (simulated)
        if incident_type == "structure_fire":
            property_loss = random.randint(15000, 750000)
        elif incident_type == "wildfire":
            property_loss = random.randint(50000, 2000000)
        elif incident_type == "vehicle_fire":
            property_loss = random.randint(5000, 80000)
        else:
            property_loss = random.randint(1000, 150000)

        # Number of units responding
        units_count = random.randint(1, 8)

        incident = {
            "neris_id": f"AZ-{2024 + random.randint(0, 1)}-{random.randint(100000, 999999):06d}",
            "state": "AZ",
            "incident_types": [incident_type],
            "base": {
                "point": {
                    "crs": 4326,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [round(lon, 6), round(lat, 6)],
                    },
                },
                "property_use": random.choice(PROPERTY_USE_TYPES),
            },
            "dispatch": {
                "timestamp": dispatch_time.isoformat() + "Z",
                "arrival_timestamp": arrival_time.isoformat() + "Z",
                "controlled_timestamp": controlled_time.isoformat() + "Z",
                "response_time_minutes": round(response_minutes, 1),
                "location": {
                    "city": location["name"],
                    "state": "AZ",
                    "address": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Cactus', 'Camelback', 'Indian School', 'McDowell', 'Thomas', 'Van Buren', 'Broadway', 'Speedway', 'Grant', 'Ina'])} {random.choice(['St', 'Rd', 'Ave', 'Blvd', 'Dr', 'Way'])}",
                },
                "unit_responses": [
                    {
                        "unit_id": f"E-{random.randint(1, 50)}",
                        "unit_type": random.choice(["engine", "ladder", "rescue", "battalion_chief"]),
                        "response_time_minutes": round(response_minutes + random.uniform(-1, 3), 1),
                    }
                    for _ in range(units_count)
                ],
            },
            "fire_detail": {
                "area_of_origin": random.choice([
                    "kitchen", "bedroom", "living_room", "garage", "attic",
                    "electrical_panel", "exterior", "roof", "basement", "wildland",
                ]),
                "heat_source": random.choice([
                    "cooking_equipment", "electrical", "smoking_materials",
                    "heating_equipment", "open_flame", "natural", "unknown",
                ]),
                "item_first_ignited": random.choice([
                    "cooking_materials", "furniture", "structural_member",
                    "insulation", "vegetation", "vehicle", "appliance",
                ]),
                "fire_spread": random.choice([
                    "confined_to_room", "confined_to_floor", "confined_to_building",
                    "beyond_building", "confined_to_object",
                ]),
                "property_loss_dollars": property_loss,
            },
            "fire_suppression": suppression_data,
            "smoke_alarm": smoke_alarm,
            "fire_alarm": {
                "present": random.random() < 0.4,
                "operated": random.random() < 0.7,
                "type": random.choice(["local", "central_station", "proprietary", "none"]),
            },
            "weather": weather,
            "census_tract": f"04{random.randint(1, 15):03d}{random.randint(100000, 999999):06d}",
        }

        incidents.append(incident)

    return incidents
