"""
Strait of Hormuz — Coordinated Maritime Blockade ABM
=====================================================
Agent-based model simulating a coordinated fast-attack-craft (FAC) swarm
blockade of commercial shipping in the Strait of Hormuz chokepoint.

Outputs:
  1. CoT Data Package (.zip) for iTAK visualization on iPad
  2. Landscape PDF/PNG dashboard report (matching blockade model style)

The model uses real-world coordinates for the Strait of Hormuz transit lanes
and generates TAK markers for each vessel and FAC at each simulation snapshot.

Scenario:
  - Commercial vessels (tankers, cargo, LNG) transit the strait via established
    Traffic Separation Scheme (TSS) lanes.
  - At a trigger step, a coordinated swarm of FACs deploys from Iranian coastal
    positions and converges on the chokepoint.
  - Vessels within the denial zone are forced to stop (primary blockade).
  - Trailing vessels queue up behind stopped traffic (cascade effect).
  - The model captures emergent queuing behavior and fits Poisson arrival rates.

Mesa 3.x compatible.
"""

import os
import time
import uuid
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.stats import poisson

from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

# ==========================================
# GEOGRAPHIC CONSTANTS — Strait of Hormuz
# ==========================================

# Bounding box for the simulation area (decimal degrees)
# Covers the narrowest part of the strait between Iran and Oman/UAE
HORMUZ_BOUNDS = {
    "lat_min": 26.20,   # Southern edge (Oman coast)
    "lat_max": 26.85,   # Northern edge (Iran coast)
    "lon_min": 56.00,   # Western entry (Persian Gulf side)
    "lon_max": 56.75,   # Eastern exit (Gulf of Oman side)
}

# Traffic Separation Scheme (TSS) — inbound and outbound lanes
# Inbound lane (westbound into Persian Gulf): southern lane
TSS_INBOUND_LAT = 26.38
# Outbound lane (eastbound out of Persian Gulf): northern lane
TSS_OUTBOUND_LAT = 26.52
# Lane width in degrees (~2 nautical miles)
LANE_WIDTH = 0.03

# Iranian coastal launch points for FACs
IRAN_LAUNCH_POINTS = [
    (26.75, 56.10),  # Bandar Abbas area
    (26.72, 56.25),  # Qeshm Island
    (26.68, 56.40),  # Larak Island
    (26.70, 56.55),  # Hengam Island
]

# Chokepoint center (narrowest passage)
CHOKEPOINT_CENTER = (26.45, 56.35)
DENIAL_RADIUS_DEG = 0.08  # ~8-9 km radius denial zone


# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def geo_distance(pos1, pos2):
    """Approximate distance in degrees between two (lat, lon) positions."""
    dlat = pos1[0] - pos2[0]
    dlon = pos1[1] - pos2[1]
    return np.sqrt(dlat**2 + dlon**2)


def lat_lon_from_grid(x, y, bounds):
    """Convert continuous space (x, y) back to (lat, lon)."""
    lat = bounds["lat_min"] + y * (bounds["lat_max"] - bounds["lat_min"])
    lon = bounds["lon_min"] + x * (bounds["lon_max"] - bounds["lon_min"])
    return (lat, lon)


def grid_from_lat_lon(lat, lon, bounds):
    """Convert (lat, lon) to continuous space (x, y) in [0, 1]."""
    x = (lon - bounds["lon_min"]) / (bounds["lon_max"] - bounds["lon_min"])
    y = (lat - bounds["lat_min"]) / (bounds["lat_max"] - bounds["lat_min"])
    return (x, y)


# ==========================================
# AGENTS
# ==========================================

class VesselAgent(Agent):
    """
    Commercial vessel transiting the Strait of Hormuz.
    Types: tanker, cargo, lng_carrier
    """
    STATE_TRANSITING = 0
    STATE_BLOCKED = 1       # Stopped by FAC denial zone
    STATE_QUEUED = 2        # Stopped behind blocked vessel
    STATE_DIVERTED = 3      # Turned around

    VESSEL_TYPES = ["tanker", "cargo", "lng_carrier"]

    def __init__(self, model, vessel_type, direction, start_pos):
        super().__init__(model)
        self.vessel_type = vessel_type
        self.direction = direction  # "inbound" or "outbound"
        self.state = VesselAgent.STATE_TRANSITING
        self.speed = self.random.uniform(0.005, 0.012)  # grid units per step
        self.pos_lat_lon = start_pos  # (lat, lon)
        # Convert to grid coords
        gx, gy = grid_from_lat_lon(start_pos[0], start_pos[1], HORMUZ_BOUNDS)
        self.gx = gx
        self.gy = gy

    def step(self):
        if self.state == VesselAgent.STATE_TRANSITING:
            self._move()
            self._check_denial_zone()
            self._check_queue()
        # Blocked/queued vessels don't move

    def _move(self):
        """Move vessel along its lane."""
        if self.direction == "inbound":
            self.gx -= self.speed  # westbound
        else:
            self.gx += self.speed  # eastbound
        # Clamp to bounds
        self.gx = max(0.0, min(1.0, self.gx))
        # Update lat/lon
        self.pos_lat_lon = lat_lon_from_grid(self.gx, self.gy, HORMUZ_BOUNDS)

    def _check_denial_zone(self):
        """Check if vessel has entered the FAC denial zone."""
        if not self.model.attack_active:
            return
        cp_x, cp_y = grid_from_lat_lon(
            CHOKEPOINT_CENTER[0], CHOKEPOINT_CENTER[1], HORMUZ_BOUNDS
        )
        dist = np.sqrt((self.gx - cp_x)**2 + (self.gy - cp_y)**2)
        denial_radius_grid = DENIAL_RADIUS_DEG / (HORMUZ_BOUNDS["lon_max"] - HORMUZ_BOUNDS["lon_min"])
        if dist < denial_radius_grid:
            if self.random.random() < 0.90:  # 90% compliance with armed threat
                self.state = VesselAgent.STATE_BLOCKED

    def _check_queue(self):
        """Check if vessel is behind a blocked vessel in the same lane."""
        if not self.model.attack_active:
            return
        for other in self.model.schedule.agents:
            if not isinstance(other, VesselAgent):
                continue
            if other is self:
                continue
            if other.direction != self.direction:
                continue
            if other.state not in (VesselAgent.STATE_BLOCKED, VesselAgent.STATE_QUEUED):
                continue
            # Check if we're close behind a stopped vessel
            dist = abs(self.gx - other.gx)
            lat_dist = abs(self.gy - other.gy)
            if dist < 0.025 and lat_dist < 0.02:
                self.state = VesselAgent.STATE_QUEUED
                return


class FACAgent(Agent):
    """
    Fast Attack Craft — Iranian IRGCN-style small boat.
    Deploys from coastal positions and converges on the chokepoint.
    """
    STATE_HOLDING = 0
    STATE_DEPLOYING = 1
    STATE_ON_STATION = 2

    def __init__(self, model, launch_point):
        super().__init__(model)
        self.state = FACAgent.STATE_HOLDING
        self.launch_lat_lon = launch_point
        self.pos_lat_lon = launch_point
        gx, gy = grid_from_lat_lon(launch_point[0], launch_point[1], HORMUZ_BOUNDS)
        self.gx = gx
        self.gy = gy
        self.speed = self.random.uniform(0.02, 0.035)  # FACs are fast

    def step(self):
        if self.state == FACAgent.STATE_HOLDING:
            if self.model.attack_active:
                self.state = FACAgent.STATE_DEPLOYING
        elif self.state == FACAgent.STATE_DEPLOYING:
            self._move_to_chokepoint()
        # On station: hold position (patrol small area)
        elif self.state == FACAgent.STATE_ON_STATION:
            self._patrol()

    def _move_to_chokepoint(self):
        """Move toward the chokepoint denial zone center."""
        cp_x, cp_y = grid_from_lat_lon(
            CHOKEPOINT_CENTER[0], CHOKEPOINT_CENTER[1], HORMUZ_BOUNDS
        )
        dx = cp_x - self.gx
        dy = cp_y - self.gy
        dist = np.sqrt(dx**2 + dy**2)
        if dist < 0.02:
            self.state = FACAgent.STATE_ON_STATION
            return
        # Normalize and move
        self.gx += (dx / dist) * self.speed
        self.gy += (dy / dist) * self.speed
        self.pos_lat_lon = lat_lon_from_grid(self.gx, self.gy, HORMUZ_BOUNDS)

    def _patrol(self):
        """Small random patrol movement around station."""
        self.gx += self.random.uniform(-0.005, 0.005)
        self.gy += self.random.uniform(-0.005, 0.005)
        self.pos_lat_lon = lat_lon_from_grid(self.gx, self.gy, HORMUZ_BOUNDS)


# ==========================================
# MODEL
# ==========================================

class HormuzBlockadeModel(Model):
    """
    Strait of Hormuz maritime blockade simulation.
    """
    def __init__(self, num_vessels=40, num_facs=16, attack_step=10, max_steps=50):
        super().__init__()
        self.num_vessels = num_vessels
        self.num_facs = num_facs
        self.attack_step = attack_step
        self.max_steps = max_steps
        self.attack_active = False
        self.current_step = 0
        self.schedule = RandomActivation(self)

        # Spawn vessels in both lanes
        for i in range(num_vessels):
            direction = "inbound" if i % 2 == 0 else "outbound"
            vessel_type = self.random.choice(VesselAgent.VESSEL_TYPES)

            if direction == "inbound":
                # Start from eastern side, move west
                start_lon = HORMUZ_BOUNDS["lon_max"] - self.random.random() * 0.6
                start_lat = TSS_INBOUND_LAT + self.random.uniform(-LANE_WIDTH, LANE_WIDTH)
            else:
                # Start from western side, move east
                start_lon = HORMUZ_BOUNDS["lon_min"] + self.random.random() * 0.6
                start_lat = TSS_OUTBOUND_LAT + self.random.uniform(-LANE_WIDTH, LANE_WIDTH)

            v = VesselAgent(self, vessel_type, direction, (start_lat, start_lon))
            self.schedule.add(v)

        # Spawn FACs at Iranian coastal launch points
        facs_per_point = num_facs // len(IRAN_LAUNCH_POINTS)
        for lp in IRAN_LAUNCH_POINTS:
            for j in range(facs_per_point):
                # Slight jitter around launch point
                jittered = (
                    lp[0] + self.random.uniform(-0.02, 0.02),
                    lp[1] + self.random.uniform(-0.02, 0.02),
                )
                fac = FACAgent(self, jittered)
                self.schedule.add(fac)

        # Data collection
        self.datacollector = DataCollector(
            model_reporters={
                "Vessels_Blocked": lambda m: sum(
                    1 for a in m.schedule.agents
                    if isinstance(a, VesselAgent) and a.state == VesselAgent.STATE_BLOCKED
                ),
                "Vessels_Queued": lambda m: sum(
                    1 for a in m.schedule.agents
                    if isinstance(a, VesselAgent) and a.state == VesselAgent.STATE_QUEUED
                ),
                "FACs_On_Station": lambda m: sum(
                    1 for a in m.schedule.agents
                    if isinstance(a, FACAgent) and a.state == FACAgent.STATE_ON_STATION
                ),
                "Total_Disrupted": lambda m: sum(
                    1 for a in m.schedule.agents
                    if isinstance(a, VesselAgent) and a.state in (
                        VesselAgent.STATE_BLOCKED, VesselAgent.STATE_QUEUED
                    )
                ),
            }
        )

    def step(self):
        if self.current_step == self.attack_step:
            self.attack_active = True
            print(f"[{time.strftime('%H:%M:%S')}] ATTACK: FAC swarm deploying to chokepoint.")
        self.datacollector.collect(self)
        self.schedule.step()
        self.current_step += 1


# ==========================================
# COT / TAK DATA EXPORT
# ==========================================

def _cot_timestamp(dt=None):
    """Format datetime as CoT timestamp."""
    if dt is None:
        dt = datetime.utcnow()
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _vessel_cot_type(vessel):
    """Map vessel state/type to CoT type code."""
    # Neutral shipping: a-n-S-C (neutral surface craft)
    if vessel.state == VesselAgent.STATE_TRANSITING:
        return "a-n-S-C-M"  # neutral surface commercial merchant
    else:
        return "a-n-S-C-M"  # same type, color will differentiate


def _vessel_color(vessel):
    """ARGB color for vessel marker based on state."""
    if vessel.state == VesselAgent.STATE_BLOCKED:
        return "-65536"       # Red
    elif vessel.state == VesselAgent.STATE_QUEUED:
        return "-33024"       # Orange
    elif vessel.state == VesselAgent.STATE_DIVERTED:
        return "-256"         # Yellow
    else:
        return "-16711936"    # Green (transiting normally)


def _fac_color(fac):
    """ARGB color for FAC marker."""
    if fac.state == FACAgent.STATE_ON_STATION:
        return "-65536"       # Red (hostile, on station)
    elif fac.state == FACAgent.STATE_DEPLOYING:
        return "-33024"       # Orange (deploying)
    else:
        return "-8355712"     # Gray (holding)


def _create_vessel_cot(vessel, sim_time):
    """Create a CoT event XML element for a vessel."""
    lat, lon = vessel.pos_lat_lon
    uid = f"hormuz-vessel-{vessel.unique_id}"
    cot_type = _vessel_cot_type(vessel)

    state_labels = {
        VesselAgent.STATE_TRANSITING: "TRANSITING",
        VesselAgent.STATE_BLOCKED: "BLOCKED (Primary)",
        VesselAgent.STATE_QUEUED: "QUEUED (Cascade)",
        VesselAgent.STATE_DIVERTED: "DIVERTED",
    }
    state_label = state_labels.get(vessel.state, "UNKNOWN")
    callsign = f"{vessel.vessel_type.upper()} - {vessel.direction.upper()} - {state_label}"

    stale_time = sim_time + timedelta(hours=1)

    event = ET.Element("event")
    event.set("version", "2.0")
    event.set("uid", uid)
    event.set("type", cot_type)
    event.set("how", "m-g")
    event.set("time", _cot_timestamp(sim_time))
    event.set("start", _cot_timestamp(sim_time))
    event.set("stale", _cot_timestamp(stale_time))

    point = ET.SubElement(event, "point")
    point.set("lat", str(round(lat, 6)))
    point.set("lon", str(round(lon, 6)))
    point.set("hae", "0")
    point.set("ce", "100")
    point.set("le", "100")

    detail = ET.SubElement(event, "detail")
    contact = ET.SubElement(detail, "contact")
    contact.set("callsign", callsign)

    remarks = ET.SubElement(detail, "remarks")
    remarks.text = (
        f"Vessel Type: {vessel.vessel_type.replace('_', ' ').title()}\n"
        f"Direction: {vessel.direction}\n"
        f"Status: {state_label}\n"
        f"Position: {lat:.4f}N, {abs(lon):.4f}E\n"
        f"Simulation Step: {vessel.model.current_step}"
    )

    color_elem = ET.SubElement(detail, "color")
    color_elem.set("argb", _vessel_color(vessel))

    return event


def _create_fac_cot(fac, sim_time):
    """Create a CoT event XML element for a FAC."""
    lat, lon = fac.pos_lat_lon
    uid = f"hormuz-fac-{fac.unique_id}"
    # Hostile surface small craft
    cot_type = "a-h-S-C-S"

    state_labels = {
        FACAgent.STATE_HOLDING: "HOLDING",
        FACAgent.STATE_DEPLOYING: "DEPLOYING",
        FACAgent.STATE_ON_STATION: "ON STATION",
    }
    state_label = state_labels.get(fac.state, "UNKNOWN")
    callsign = f"FAC-{fac.unique_id:03d} [{state_label}]"

    stale_time = sim_time + timedelta(hours=1)

    event = ET.Element("event")
    event.set("version", "2.0")
    event.set("uid", uid)
    event.set("type", cot_type)
    event.set("how", "m-g")
    event.set("time", _cot_timestamp(sim_time))
    event.set("start", _cot_timestamp(sim_time))
    event.set("stale", _cot_timestamp(stale_time))

    point = ET.SubElement(event, "point")
    point.set("lat", str(round(lat, 6)))
    point.set("lon", str(round(lon, 6)))
    point.set("hae", "0")
    point.set("ce", "50")
    point.set("le", "50")

    detail = ET.SubElement(event, "detail")
    contact = ET.SubElement(detail, "contact")
    contact.set("callsign", callsign)

    remarks = ET.SubElement(detail, "remarks")
    remarks.text = (
        f"IRGCN Fast Attack Craft\n"
        f"Status: {state_label}\n"
        f"Position: {lat:.4f}N, {abs(lon):.4f}E\n"
        f"Threat Level: HIGH\n"
        f"Simulation Step: {fac.model.current_step}"
    )

    color_elem = ET.SubElement(detail, "color")
    color_elem.set("argb", _fac_color(fac))

    return event


def generate_tak_data_package(model, output_path):
    """
    Generate a TAK Data Package (.zip) with CoT events for all agents
    at the final simulation state.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sim_time = datetime.utcnow()

    cot_events = []

    # Add vessel events
    for agent in model.schedule.agents:
        if isinstance(agent, VesselAgent):
            event = _create_vessel_cot(agent, sim_time)
            cot_events.append(event)
        elif isinstance(agent, FACAgent):
            event = _create_fac_cot(agent, sim_time)
            cot_events.append(event)

    # Add denial zone marker
    dz_event = _create_denial_zone_cot(sim_time)
    cot_events.append(dz_event)

    # Package into ZIP
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, event in enumerate(cot_events):
            event_xml = ET.tostring(event, encoding="unicode", xml_declaration=False)
            event_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + event_xml
            zf.writestr(f"cot/event_{i:03d}.cot", event_xml)

        manifest = _create_manifest(len(cot_events))
        zf.writestr("manifest.xml", manifest)
        zf.writestr("MANIFEST/manifest.xml", manifest)

    return output_path


def _create_denial_zone_cot(sim_time):
    """Create a CoT marker for the denial zone center."""
    lat, lon = CHOKEPOINT_CENTER
    uid = "hormuz-denial-zone"
    stale_time = sim_time + timedelta(hours=24)

    event = ET.Element("event")
    event.set("version", "2.0")
    event.set("uid", uid)
    event.set("type", "a-h-G")  # hostile ground
    event.set("how", "m-g")
    event.set("time", _cot_timestamp(sim_time))
    event.set("start", _cot_timestamp(sim_time))
    event.set("stale", _cot_timestamp(stale_time))

    point = ET.SubElement(event, "point")
    point.set("lat", str(round(lat, 6)))
    point.set("lon", str(round(lon, 6)))
    point.set("hae", "0")
    point.set("ce", str(int(DENIAL_RADIUS_DEG * 111000)))  # approx meters
    point.set("le", "0")

    detail = ET.SubElement(event, "detail")
    contact = ET.SubElement(detail, "contact")
    contact.set("callsign", "DENIAL ZONE — CHOKEPOINT")

    remarks = ET.SubElement(detail, "remarks")
    remarks.text = (
        "═══════════════════════════════════\n"
        "  MARITIME DENIAL ZONE\n"
        "  Strait of Hormuz Chokepoint\n"
        "═══════════════════════════════════\n\n"
        f"Center: {lat:.4f}N, {abs(lon):.4f}E\n"
        f"Radius: ~{DENIAL_RADIUS_DEG * 111:.1f} km\n\n"
        "Threat: Coordinated FAC swarm\n"
        "Effect: Commercial shipping halted\n"
        "Status: ACTIVE BLOCKADE\n\n"
        "═══════════════════════════════════\n"
        "  ABM Simulation | RiskRunners\n"
        "═══════════════════════════════════"
    )

    color_elem = ET.SubElement(detail, "color")
    color_elem.set("argb", "-65536")  # Red

    return event


def _create_manifest(event_count):
    """Create manifest.xml for the TAK data package."""
    pkg_uid = f"hormuz-sim-{uuid.uuid4().hex[:8]}"

    manifest = ET.Element("MissionPackageManifest")
    manifest.set("version", "2")

    config = ET.SubElement(manifest, "Configuration")
    p_uid = ET.SubElement(config, "Parameter")
    p_uid.set("name", "uid")
    p_uid.set("value", pkg_uid)

    p_name = ET.SubElement(config, "Parameter")
    p_name.set("name", "name")
    p_name.set("value", "Hormuz Blockade ABM — Final State")

    p_recv = ET.SubElement(config, "Parameter")
    p_recv.set("name", "onReceiveImport")
    p_recv.set("value", "true")

    contents = ET.SubElement(manifest, "Contents")
    for i in range(event_count):
        content = ET.SubElement(contents, "Content")
        content.set("ignore", "false")
        content.set("zipEntry", f"cot/event_{i:03d}.cot")
        param = ET.SubElement(content, "Parameter")
        param.set("name", "contentType")
        param.set("value", "CoT")

    xml_str = ET.tostring(manifest, encoding="unicode", xml_declaration=False)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str


# ==========================================
# DASHBOARD VISUALIZATION
# ==========================================

def generate_dashboard(model):
    """Generate a landscape dashboard figure with dark theme."""
    print(f"[{time.strftime('%H:%M:%S')}] Generating dashboard visualization...")

    data = model.datacollector.get_model_vars_dataframe()
    data["Total_Disrupted"] = data["Vessels_Blocked"] + data["Vessels_Queued"]

    # Style
    BG = '#0d1b2a'
    PANEL = '#1b2838'
    RED = '#e63946'
    ORANGE = '#f4a261'
    CYAN = '#2ec4b6'
    GREEN = '#06d6a0'
    TEXT = '#edf2f4'
    GRID = '#2d3561'

    plt.rcParams.update({
        'text.color': TEXT, 'axes.labelcolor': TEXT,
        'xtick.color': TEXT, 'ytick.color': TEXT,
        'axes.edgecolor': GRID, 'figure.facecolor': BG,
        'axes.facecolor': PANEL, 'font.family': 'sans-serif',
    })

    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(BG)

    # Title
    fig.text(0.5, 0.97, "STRAIT OF HORMUZ — COORDINATED MARITIME BLOCKADE",
             fontsize=15, fontweight='bold', color=TEXT, ha='center', va='top',
             fontfamily='monospace')
    fig.text(0.5, 0.94,
             "Agent-Based Model  |  FAC Swarm Denial  |  Queuing Theory Overlay  |  TAK Export",
             fontsize=9, color='#888888', ha='center', va='top')

    # --- 1. Geographic Map (Top Left, wide) ---
    ax_map = plt.subplot2grid((2, 3), (0, 0), colspan=2)
    ax_map.set_title("Strait of Hormuz — Agent Positions (Final State)",
                     fontsize=11, fontweight='bold', pad=8)

    # Draw coastlines (simplified polygons)
    # Iran coast (north)
    iran_lats = [26.75, 26.80, 26.85, 26.82, 26.78, 26.75]
    iran_lons = [56.0, 56.2, 56.4, 56.6, 56.75, 56.75]
    ax_map.fill(iran_lons, iran_lats, color='#2d3a2d', alpha=0.6, label='Iran')
    ax_map.plot(iran_lons, iran_lats, color='#4a7c59', linewidth=1.5)

    # Oman coast (south)
    oman_lats = [26.20, 26.20, 26.22, 26.25, 26.28, 26.30]
    oman_lons = [56.0, 56.75, 56.75, 56.6, 56.3, 56.0]
    ax_map.fill(oman_lons, oman_lats, color='#3d2d2d', alpha=0.6, label='Oman/UAE')
    ax_map.plot(oman_lons, oman_lats, color='#7c4a4a', linewidth=1.5)

    # TSS lanes
    ax_map.axhline(y=TSS_INBOUND_LAT, color=CYAN, linestyle='--', alpha=0.3, linewidth=0.8)
    ax_map.axhline(y=TSS_OUTBOUND_LAT, color=GREEN, linestyle='--', alpha=0.3, linewidth=0.8)
    ax_map.text(56.02, TSS_INBOUND_LAT + 0.01, "Inbound Lane (W)", fontsize=7, color=CYAN, alpha=0.6)
    ax_map.text(56.02, TSS_OUTBOUND_LAT + 0.01, "Outbound Lane (E)", fontsize=7, color=GREEN, alpha=0.6)

    # Denial zone circle
    dz_circle = patches.Circle(
        (CHOKEPOINT_CENTER[1], CHOKEPOINT_CENTER[0]),
        DENIAL_RADIUS_DEG, linewidth=1.5, edgecolor=RED,
        facecolor=RED, alpha=0.12, linestyle='-'
    )
    ax_map.add_patch(dz_circle)
    ax_map.text(CHOKEPOINT_CENTER[1], CHOKEPOINT_CENTER[0] - 0.01,
                "DENIAL\nZONE", fontsize=7, color=RED, ha='center', va='top', fontweight='bold')

    # Plot agents
    for agent in model.schedule.agents:
        if isinstance(agent, VesselAgent):
            lat, lon = agent.pos_lat_lon
            if agent.state == VesselAgent.STATE_BLOCKED:
                ax_map.plot(lon, lat, 's', color=RED, markersize=5, alpha=0.9)
            elif agent.state == VesselAgent.STATE_QUEUED:
                ax_map.plot(lon, lat, 's', color=ORANGE, markersize=4, alpha=0.7)
            else:
                ax_map.plot(lon, lat, 'o', color=GREEN, markersize=3, alpha=0.5)
        elif isinstance(agent, FACAgent):
            lat, lon = agent.pos_lat_lon
            if agent.state == FACAgent.STATE_ON_STATION:
                ax_map.plot(lon, lat, '^', color=RED, markersize=5, alpha=0.9)
            elif agent.state == FACAgent.STATE_DEPLOYING:
                ax_map.plot(lon, lat, '^', color=ORANGE, markersize=4, alpha=0.7)
            else:
                ax_map.plot(lon, lat, '^', color='#666666', markersize=3, alpha=0.4)

    ax_map.set_xlim(HORMUZ_BOUNDS["lon_min"], HORMUZ_BOUNDS["lon_max"])
    ax_map.set_ylim(HORMUZ_BOUNDS["lat_min"], HORMUZ_BOUNDS["lat_max"])
    ax_map.set_xlabel("Longitude (°E)", fontsize=8)
    ax_map.set_ylabel("Latitude (°N)", fontsize=8)
    ax_map.tick_params(labelsize=7)
    ax_map.set_aspect('equal')

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='s', color='w', markerfacecolor=RED, markersize=7, label='Vessel BLOCKED'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor=ORANGE, markersize=7, label='Vessel QUEUED'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=GREEN, markersize=7, label='Vessel Transiting'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor=RED, markersize=7, label='FAC On Station'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor=ORANGE, markersize=7, label='FAC Deploying'),
    ]
    ax_map.legend(handles=legend_elements, loc='lower right', fontsize=7, framealpha=0.4)

    # --- 2. Time Series (Top Right) ---
    ax_ts = plt.subplot2grid((2, 3), (0, 2))
    ax_ts.set_title("Disruption Over Time", fontsize=11, fontweight='bold', pad=8)
    ax_ts.plot(data['Vessels_Blocked'], color=RED, linewidth=2, label='Blocked (Primary)')
    ax_ts.plot(data['Vessels_Queued'], color=ORANGE, linewidth=2, label='Queued (Cascade)')
    ax_ts.plot(data['Total_Disrupted'], color=CYAN, linewidth=2, label='Total Disrupted')
    ax_ts.fill_between(data.index, data['Total_Disrupted'], alpha=0.1, color=CYAN)
    ax_ts.axvline(x=model.attack_step, color=RED, linestyle='--', alpha=0.6, label='Attack Trigger')
    ax_ts.set_xlabel("Step", fontsize=8)
    ax_ts.set_ylabel("Vessel Count", fontsize=8)
    ax_ts.grid(True, alpha=0.15, color=GRID)
    ax_ts.legend(fontsize=7, framealpha=0.3)
    ax_ts.tick_params(labelsize=7)

    # --- 3. Poisson Fit (Bottom Left) ---
    ax_poisson = plt.subplot2grid((2, 3), (1, 0))
    ax_poisson.set_title("Queuing Theory — Arrival Rate Fit", fontsize=11, fontweight='bold', pad=8)

    attack_window = data.iloc[model.attack_step:]
    mean_disrupted = attack_window['Total_Disrupted'].mean()

    ax_poisson.hist(attack_window['Total_Disrupted'],
                    bins=range(0, model.num_vessels + 1, 2),
                    density=True, alpha=0.5, color='#1d3557', edgecolor='#457b9d',
                    label='ABM Emergent Data')

    x_vals = np.arange(0, model.num_vessels, 2)
    poisson_fit = poisson.pmf(x_vals, mu=mean_disrupted)
    ax_poisson.plot(x_vals, poisson_fit, 'o-', color=CYAN, ms=4, linewidth=2,
                    label=f'Poisson (λ={mean_disrupted:.1f})')
    ax_poisson.set_xlabel("Vessels Disrupted", fontsize=8)
    ax_poisson.set_ylabel("Probability", fontsize=8)
    ax_poisson.legend(fontsize=7, framealpha=0.3)
    ax_poisson.grid(True, alpha=0.15, color=GRID)
    ax_poisson.tick_params(labelsize=7)

    # --- 4. FAC Deployment (Bottom Center) ---
    ax_fac = plt.subplot2grid((2, 3), (1, 1))
    ax_fac.set_title("FAC Swarm Deployment", fontsize=11, fontweight='bold', pad=8)
    ax_fac.plot(data['FACs_On_Station'], color=RED, linewidth=2, label='FACs On Station')
    ax_fac.fill_between(data.index, data['FACs_On_Station'], alpha=0.15, color=RED)
    ax_fac.axhline(y=model.num_facs, color='#666666', linestyle=':', alpha=0.5,
                   label=f'Total FACs ({model.num_facs})')
    ax_fac.axvline(x=model.attack_step, color=RED, linestyle='--', alpha=0.5)
    ax_fac.set_xlabel("Step", fontsize=8)
    ax_fac.set_ylabel("Count", fontsize=8)
    ax_fac.grid(True, alpha=0.15, color=GRID)
    ax_fac.legend(fontsize=7, framealpha=0.3)
    ax_fac.tick_params(labelsize=7)

    # --- 5. Risk Assessment Text (Bottom Right) ---
    ax_text = plt.subplot2grid((2, 3), (1, 2))
    ax_text.set_facecolor(PANEL)
    ax_text.axis('off')

    final_blocked = data['Vessels_Blocked'].iloc[-1]
    final_queued = data['Vessels_Queued'].iloc[-1]
    final_total = data['Total_Disrupted'].iloc[-1]
    pct_disrupted = (final_total / model.num_vessels) * 100
    facs_on = data['FACs_On_Station'].iloc[-1]

    ax_text.text(0.05, 0.95, "SITUATION ASSESSMENT", fontsize=11, fontweight='bold',
                 color=CYAN, va='top', fontfamily='monospace')
    ax_text.axhline(y=0.88, xmin=0.05, xmax=0.95, color=GRID, linewidth=0.8)

    assessment = (
        f"  Vessels Blocked:    {final_blocked:.0f}\n"
        f"  Vessels Queued:     {final_queued:.0f}\n"
        f"  Total Disrupted:    {final_total:.0f} / {model.num_vessels}\n"
        f"  Disruption Rate:    {pct_disrupted:.0f}%\n"
        f"  FACs On Station:    {facs_on:.0f} / {model.num_facs}\n\n"
        f"  Poisson λ:          {mean_disrupted:.1f} vessels/step\n"
        f"  Attack Trigger:     Step {model.attack_step}\n"
    )
    ax_text.text(0.05, 0.80, assessment, fontsize=9, color=TEXT, va='top',
                 fontfamily='monospace', linespacing=1.5)

    ax_text.text(0.05, 0.22, "IMPACT", fontsize=9, fontweight='bold', color=RED, va='top')
    impact = (
        "  ~20% of global oil transits\n"
        "  this chokepoint daily.\n"
        "  Full blockade = immediate\n"
        "  global energy supply shock."
    )
    ax_text.text(0.05, 0.14, impact, fontsize=8, color=TEXT, va='top',
                 fontfamily='monospace', linespacing=1.4)

    plt.tight_layout(rect=[0.01, 0.02, 0.99, 0.92])
    return fig


# ==========================================
# PDF / PNG EXPORT
# ==========================================

def export_report(fig, output_dir):
    """Export dashboard as landscape PDF and PNG."""
    from reportlab.lib.pagesizes import landscape, letter
    from reportlab.pdfgen import canvas as pdf_canvas
    from reportlab.lib.utils import ImageReader
    import io

    os.makedirs(output_dir, exist_ok=True)

    # PNG
    png_path = os.path.join(output_dir, "HormuzBlockadeReport.png")
    fig.savefig(png_path, format='png', dpi=200, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print(f"[{time.strftime('%H:%M:%S')}] PNG exported: {png_path}")

    # PDF (landscape)
    pdf_path = os.path.join(output_dir, "HormuzBlockadeReport.pdf")
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', dpi=200, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    img_buffer.seek(0)

    page_size = landscape(letter)
    c = pdf_canvas.Canvas(pdf_path, pagesize=page_size)
    page_w, page_h = page_size
    margin = 18
    image = ImageReader(img_buffer)
    c.drawImage(image, margin, margin,
                width=page_w - 2 * margin, height=page_h - 2 * margin,
                preserveAspectRatio=True, anchor='c')
    c.save()
    print(f"[{time.strftime('%H:%M:%S')}] PDF exported: {pdf_path}")


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    print("=" * 60)
    print("  STRAIT OF HORMUZ — MARITIME BLOCKADE ABM")
    print("  Agent-Based Model → TAK Data Package → iTAK")
    print("=" * 60)
    print()

    # 1. Run simulation
    print(f"[{time.strftime('%H:%M:%S')}] Initializing model...")
    model = HormuzBlockadeModel(
        num_vessels=40,
        num_facs=16,
        attack_step=10,
        max_steps=50,
    )

    print(f"[{time.strftime('%H:%M:%S')}] Running simulation ({model.max_steps} steps)...")
    for _ in range(model.max_steps):
        model.step()
    print(f"[{time.strftime('%H:%M:%S')}] Simulation complete.")

    # 2. Generate TAK data package
    tak_path = os.path.join(SCRIPT_DIR, "output", "hormuz_blockade.zip")
    generate_tak_data_package(model, tak_path)
    print(f"[{time.strftime('%H:%M:%S')}] TAK Data Package: {tak_path}")

    # 3. Generate dashboard
    fig = generate_dashboard(model)

    # 4. Export PDF + PNG
    export_report(fig, SCRIPT_DIR)

    print()
    print("=" * 60)
    print("  OUTPUT FILES:")
    print(f"    TAK:  {tak_path}")
    print(f"    PDF:  {os.path.join(SCRIPT_DIR, 'HormuzBlockadeReport.pdf')}")
    print(f"    PNG:  {os.path.join(SCRIPT_DIR, 'HormuzBlockadeReport.png')}")
    print()
    print("  TO LOAD IN iTAK:")
    print("    1. AirDrop hormuz_blockade.zip to iPad")
    print("    2. Open iTAK → Data Packages → Import")
    print("    3. Select the .zip file")
    print("    4. Markers appear: vessels (squares), FACs (triangles)")
    print("    5. Tap any marker for status details")
    print("=" * 60)
