# Insurance Price Calculator API

A FastAPI-based application that calculates insurance prices based on area, plan, travel duration, and optional COVID-19 coverage addon.

## Features

- Calculates insurance prices for two areas (area1 and area2) with three plans each
- Supports variable pricing based on trip duration
- Optional COVID-19 coverage addon
- Applies stamp duty for totals ≥ $150
- Includes SST (6%) for area1
- RESTful API endpoints
- Error handling for invalid inputs

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies.
```bash
pip install -r requirements.txt
```

4. Running the Application
Start the server with:
```bash
fastapi dev main.py
```

Visit http://localhost:8000 for application, http://127.0.0.1:8000/docs for Documentation.

## Additional Notes
* The assessment is simple, so static file serving is not implemented by default
* Fetching with the API is intended to be implemented in the HTML frontend