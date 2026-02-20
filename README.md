# food-drive-api
A simple FastAPI application to **create and fetch food distribution drives** for specific cities.  
Uses **SQLite** as the database for simplicity (no installation required).

---

## Features

- **Create a food drive** (`POST /food-drives`)
- **Fetch drives by city** (`GET /food-drives?city=<city>`)

---

## Tech Stack

- Python 3.12.10
- FastAPI
- SQLAlchemy
- SQLite (file-based)
- Pydantic for data validation
- dotenv for environment variables

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone  https://github.com/roshnigith/food-drive-api
cd food_drive_api
