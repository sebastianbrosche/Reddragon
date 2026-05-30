# Hestia Foundation — Sensor Network Specification
# Prototype Monitoring System

**Version:** 1.0  
**Date:** 2026-05-29  
**Location:** Shell A (37.5m²) prototype, Lagos, Algarve  
**Duration:** 12 months continuous  
**License:** CC BY-SA 4.0

---

## Monitoring Objectives

1. **Thermal performance:** Verify passive cooling, cross-ventilation, and insulation effectiveness
2. **Energy performance:** Quantify off-grid system adequacy and efficiency
3. **Structural performance:** Monitor deflection, settlement, and material degradation
4. **Indoor air quality:** Ensure healthy living environment
5. **Water performance:** Track consumption and solar hot water efficiency
6. **Occupant comfort:** Correlate objective data with subjective experience

---

## Sensor Network Architecture

### Data Logger
- **Primary:** Raspberry Pi 4 (4GB RAM) with 256GB SSD
- **Backup:** Raspberry Pi Zero 2 W with 64GB microSD (redundant logging)
- **Power:** 12V DC from main battery system, with UPS backup
- **Connectivity:** 4G/LTE modem (unlimited data SIM) + WiFi fallback
- **Software:** InfluxDB (time-series database) + Grafana (dashboard) + Node-RED (automation)
- **Publishing:** Public Grafana dashboard + daily CSV export to GitHub

### Sensor Layout (Shell A — 37.5m²)

```
Plan view (7.5m × 5m):

    [EXT-1]        [EXT-2]        [EXT-3]
       |              |              |
    ┌─────────────────────────────────────┐
    │  [IN-1]      [IN-2]      [IN-3]   │  ← North wall
    │                                     │
    │  [IN-4]              [IN-5]         │
    │           [OCC-1]                   │  ← Occupancy zone
    │                                     │
    │  [IN-6]      [IN-7]      [IN-8]   │  ← South wall
    └─────────────────────────────────────┘
       |              |              |
    [EXT-4]        [EXT-5]        [EXT-6]

Roof section:
    [ROOF-1] — attic/roof cavity
    [ROOF-2] — exterior roof surface (solar panel back)

Wall cavities:
    [CAV-1] — North wall cavity
    [CAV-2] — South wall cavity
    [CAV-3] — East wall cavity
    [CAV-4] — West wall cavity

Foundation:
    [FOUND-1] — underfloor (crawl space)
```

---

## Sensors by Category

### 1. Temperature and Humidity (22 sensors)

| ID | Location | Type | Purpose | Accuracy | Cost (€) |
|----|----------|------|---------|----------|----------|
| IN-1 | Interior, north wall, 1.5m height | SHT30 | Indoor thermal comfort | ±0.2°C, ±2% RH | 8 |
| IN-2 | Interior, centre, 1.5m height | SHT30 | Reference indoor | ±0.2°C, ±2% RH | 8 |
| IN-3 | Interior, south wall, 1.5m height | SHT30 | Indoor thermal comfort | ±0.2°C, ±2% RH | 8 |
| IN-4 | Interior, west wall, 1.5m height | SHT30 | Indoor thermal comfort | ±0.2°C, ±2% RH | 8 |
| IN-5 | Interior, east wall, 1.5m height | SHT30 | Indoor thermal comfort | ±0.2°C, ±2% RH | 8 |
| IN-6 | Interior, kitchen zone | SHT30 | Cooking heat/moisture | ±0.2°C, ±2% RH | 8 |
| IN-7 | Interior, sleeping zone | SHT30 | Night comfort | ±0.2°C, ±2% RH | 8 |
| IN-8 | Interior, near door | SHT30 | Air infiltration | ±0.2°C, ±2% RH | 8 |
| EXT-1 | Exterior, north, shaded | SHT30 | Outdoor reference | ±0.2°C, ±2% RH | 8 |
| EXT-2 | Exterior, south, sun-exposed | SHT30 | Solar gain | ±0.2°C, ±2% RH | 8 |
| EXT-3 | Exterior, east, morning sun | SHT30 | Morning heat | ±0.2°C, ±2% RH | 8 |
| EXT-4 | Exterior, west, afternoon sun | SHT30 | Afternoon heat | ±0.2°C, ±2% RH | 8 |
| EXT-5 | Exterior, roof level | SHT30 | Roof temperature | ±0.2°C, ±2% RH | 8 |
| EXT-6 | Exterior, 2m underground | DS18B20 | Ground temperature | ±0.5°C | 3 |
| CAV-1 | North wall cavity, mid-height | SHT30 | Wall thermal performance | ±0.2°C, ±2% RH | 8 |
| CAV-2 | South wall cavity, mid-height | SHT30 | Wall thermal performance | ±0.2°C, ±2% RH | 8 |
| CAV-3 | East wall cavity, mid-height | SHT30 | Wall thermal performance | ±0.2°C, ±2% RH | 8 |
| CAV-4 | West wall cavity, mid-height | SHT30 | Wall thermal performance | ±0.2°C, ±2% RH | 8 |
| ROOF-1 | Roof cavity, centre | SHT30 | Attic temperature | ±0.2°C, ±2% RH | 8 |
| ROOF-2 | Roof exterior, near PV | SHT30 | Solar panel temperature | ±0.2°C, ±2% RH | 8 |
| FOUND-1 | Underfloor, centre | DS18B20 + soil moisture | Ground conditions | ±0.5°C | 6 |
| OCC-1 | Occupancy zone, mobile | SHT30 | Portable comfort check | ±0.2°C, ±2% RH | 8 |

**Subtotal:** 22 sensors × ~€8 = **€176**

### 2. Energy Monitoring (5 sensors)

| ID | Location | Type | Purpose | Accuracy | Cost (€) |
|----|----------|------|---------|----------|----------|
| EN-1 | Solar PV output | Peacefair PZEM-017 + shunt | DC power generation | ±1% | 25 |
| EN-2 | Battery state | Victron SmartShunt | SOC, voltage, current | ±0.1% | 120 |
| EN-3 | Inverter output | Peacefair PZEM-004T | AC power consumption | ±1% | 20 |
| EN-4 | Solar hot water | DS18B20 (tank top/middle/bottom) | Temperature stratification | ±0.5°C | 15 |
| EN-5 | Overall house | Smart meter (Shelly EM) | Total import/export | ±1% | 50 |

**Subtotal:** **€230**

### 3. Structural Monitoring (4 sensors)

| ID | Location | Type | Purpose | Accuracy | Cost (€) |
|----|----------|------|---------|----------|----------|
| STR-1 | North wall, mid-height | Inclinometer (MEMS) | Wall plumb deviation | ±0.1° | 45 |
| STR-2 | South wall, mid-height | Inclinometer (MEMS) | Wall plumb deviation | ±0.1° | 45 |
| STR-3 | Floor, centre | Load cell (50kg) | Floor deflection under load | ±0.5% | 60 |
| STR-4 | Roof, centre | LVDT or laser distance | Roof deflection | ±1mm | 80 |

**Subtotal:** **€230**

### 4. Indoor Air Quality (3 sensors)

| ID | Location | Type | Purpose | Accuracy | Cost (€) |
|----|----------|------|---------|----------|----------|
| IAQ-1 | Interior, centre | Sensirion SGP30 | TVOC (volatile organic compounds) | ±10% | 25 |
| IAQ-2 | Interior, centre | Sensirion SCD40 | CO₂ concentration | ±50ppm | 35 |
| IAQ-3 | Interior, kitchen | PMS5003 | PM2.5 / PM10 (particles) | ±10% | 20 |

**Subtotal:** **€80**

### 5. Water Monitoring (2 sensors)

| ID | Location | Type | Purpose | Accuracy | Cost (€) |
|----|----------|------|---------|----------|----------|
| WAT-1 | Main water inlet | YF-S201 flow meter | Total water consumption | ±10% | 10 |
| WAT-2 | Hot water outlet | DS18B20 | Hot water delivery temperature | ±0.5°C | 3 |

**Subtotal:** **€13**

### 6. Weather Station (1 unit)

| ID | Location | Type | Purpose | Accuracy | Cost (€) |
|----|----------|------|---------|----------|----------|
| WX-1 | Exterior, 2m height | BME680 + anemometer + rain gauge | Barometric pressure, wind, rainfall | ±1hPa, ±0.5m/s | 80 |

**Subtotal:** **€80**

---

## Data Logger and Infrastructure

| Item | Specification | Cost (€) |
|------|-------------|----------|
| Raspberry Pi 4 (4GB) + case + PSU | Primary data logger | 120 |
| Raspberry Pi Zero 2 W + case | Backup logger | 40 |
| 256GB SSD (USB) | Primary storage | 35 |
| 64GB microSD | Backup storage | 15 |
| 4G/LTE modem (Quectel EC25) + antenna | Connectivity | 60 |
| UPS HAT (PiJuice) | Power backup | 50 |
| PoE splitter or 12V-5V converter | Power from battery | 15 |
| Enclosure (IP65, ventilated) | Weather protection | 40 |
| Breadboard, wires, resistors, etc. | Prototyping | 25 |
| **Subtotal infrastructure** | | **€400** |

---

## Total Sensor Network Cost

| Category | Cost (€) |
|----------|----------|
| Temperature/Humidity (22 sensors) | 176 |
| Energy (5 sensors) | 230 |
| Structural (4 sensors) | 230 |
| Air Quality (3 sensors) | 80 |
| Water (2 sensors) | 13 |
| Weather (1 station) | 80 |
| Infrastructure | 400 |
| Cables, connectors, installation | 200 |
| Contingency (15%) | 210 |
| **TOTAL** | **~€1,620** |

---

## Data Acquisition Protocol

### Sampling Rates
- Temperature/Humidity: every 60 seconds
- Energy: every 10 seconds (PV, battery), every 60 seconds (consumption)
- Structural: every 5 minutes (or on-demand after seismic events)
- Air Quality: every 60 seconds
- Water: every 60 seconds (flow), every 10 seconds (temperature)
- Weather: every 60 seconds

### Data Storage
- Raw data: retained indefinitely in InfluxDB
- Daily averages: computed and published
- Monthly summaries: computed and published
- Annual report: compiled at Month 12

### Public Dashboard
- URL: https://hestiafoundation.org/dashboard (or similar)
- Real-time: all sensors, 5-minute refresh
- Historical: zoomable time series, date range selector
- Export: CSV download for any date range
- Mobile-responsive: works on phones and tablets

### Data Privacy
- All data is anonymised (no occupant names or personal information)
- Occupant comfort surveys are voluntary and separately stored
- Data is published under CC BY-SA 4.0

---

## Installation Schedule

| Phase | Timing | Activities |
|-------|--------|------------|
| Pre-install | Day -7 | Order all sensors and infrastructure |
| Day 0 | Build Day 6 | Install conduit and sensor positions during services installation |
| Day 1 | Build Day 7 | Install temperature/humidity sensors in walls and roof |
| Day 2 | Build Day 8 | Install energy monitoring (PV, battery, inverter) |
| Day 3 | Build Day 9 | Install structural sensors, air quality sensors, weather station |
| Day 4 | Build Day 10 | Configure data logger, test all sensors, verify data flow |
| Week 1 | Post-build | Calibrate sensors, establish baselines, debug issues |
| Week 2 | Post-build | Launch public dashboard, announce monitoring programme |

---

## Maintenance Schedule

| Frequency | Activity |
|-----------|----------|
| Weekly | Check data logger uptime, verify all sensors reporting |
| Monthly | Clean dust from sensors, check cable connections, download backup |
| Quarterly | Calibrate temperature sensors against reference, inspect structural sensors |
| Annually | Full system review, replace degraded sensors, publish annual report |

---

## Alert Thresholds

| Parameter | Normal Range | Alert Threshold | Action |
|-----------|-------------|-----------------|--------|
| Indoor temperature | 18–26°C | <16°C or >30°C | Check heating/cooling systems |
| Indoor humidity | 40–60% RH | <30% or >70% | Check ventilation, condensation |
| CO₂ | <1000ppm | >1500ppm | Increase ventilation |
| Battery SOC | 20–100% | <15% | Check PV output, reduce loads |
| Wall inclination | ±0.5° | ±1.0° | Structural inspection |
| Roof deflection | <5mm | >10mm | Structural inspection |

---

## Deliverables

1. **Public dashboard** — live from Day 10
2. **Daily data files** — CSV, published to GitHub
3. **Monthly summary reports** — PDF, published on website
4. **Annual performance report** — comprehensive analysis at Month 12
5. **Peer-reviewed dataset** — formatted for academic publication
6. **Sensor network documentation** — this document, open-source

---

**License:** Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0)

**Last updated:** 2026-05-29  
**Version:** 1.0  
**Next version:** After installation and calibration
