# LisheBora Nutrition System - Setup & User Guide

## Overview
This project contains two premium Desktop Applications for managing nutrition in the Kenyan context.
1. **Client App (`client_app.py`)**: For patients to track health, view diets, and chat with AI/Nutritionists.
2. **Professional App (`developer_app.py`)**: For Nutritionists to monitor patient stats and answer queries.

## Prerequisites
- Python 3.x installed.
- Tkinter (usually comes with Python).
- `sqlite3` (standard library).

## How to Run
### 1. Start the Client App
Open a terminal and run:
```bash
python client_app.py
```
- **Login**: Use any simulated credentials or Register a new account.
- **Features**: 
    - Go to "My Health" to calculate BMI.
    - Go to "My Diet" to generate a plan.
    - Go to "Chat" to ask questions (Try asking about "water" or "ugali").
    - **Sync**: Click "Sync Data to Cloud" to simulate sending data to the server.

### 2. Start the Professional App
Open another terminal (or split view) and run:
```bash
python developer_app.py
```
- **Login**: Use simulated credentials (or register as a Professional).
- **Dashboard**: View total clients and pending questions.
- **Questions**: Go to "Pending Questions" to see what the Client sent. You can reply, and the Client will see it after they Sync again.

## Design Highlights
- **Architecture**: Disconnected/Offline-First. The Client App works offline and syncs when requested.
- **UI/UX**: Custom styled Tkinter widgets to mimic a modern, clean web-like aesthetic.
- **Data**: Uses SQLite (`client_data.db` and `server_data.db`) to simulate the two separate environments.

## File Structure
- `backend_manager.py`: Handles all database and sync logic.
- `common_utils.py`: Contains Shared Logic, MOH Standards, and Food Database.
- `client_app.py`: The End-User Application.
- `developer_app.py`: The Nutritionist Dashboard.
