# 🚑 Smart Ambulance Routing System

**Smart Ambulance Routing System** is an intelligent web-based tool designed to assist ambulances in finding the nearest hospital with the fastest route, reducing response time and potentially saving lives. The system uses real-time geolocation, OpenStreetMap data, and OSRM routing, combined with a sleek UI and voice assistant for accessibility.



## 🌐 Live Demo
👉 [Visit Live App](https://smart-ambulance-routing-system.onrender.com/)

---

## 🚀 Features

- 📍 Get nearest hospital from current or entered location
- 🗺️ Display route on an interactive map (Leaflet.js + OpenStreetMap)
- ⏱️ Show estimated time of arrival (ETA) and distance
- 🔄 Refresh and restart new searches
- 🗣️ Voice Assistant that announces hospital info
- 📱 Fully responsive & mobile-friendly
- 💡 Clean and professional UI with animations

---

## 🛠️ Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Leaflet.js, Font Awesome
- **Backend**: Python, Flask
- **APIs**:
  - Nominatim (Geocoding)
  - Overpass API (Nearby hospitals)
  - OSRM (Routing)


##🔊 Voice Assistant Feature
Uses SpeechSynthesis API to read hospital name, distance & ETA aloud.

Automatically triggers after a successful route is displayed.
---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.x
- `pip` package manager

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/ArjunJayakrishnan-codes/Smart-Ambulance-Routing-System.git
cd Smart-Ambulance-Routing-System
