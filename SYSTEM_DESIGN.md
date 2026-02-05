# LisheBora Nutrition System Design

## Overview
A dual-application system consisting of a **Client Nutrition App** (Patient) and a **Developer/Nutritionist App** (Professional).

## Architecture
- **Client App**: Local SQLite database for offline capability. Syncs with central server when online.
- **Developer App**: Connects directly to the Central Server (simulated or real).
- **Central Server/API**: Handles data synchronization, secure channels, and AI routing.

## Modules

### 1. Shared / Common (`common.py`)
- MOH Growth Standards (functions for Z-score calc).
- Kenyan Food Composition Database (JSON/Dict).
- Condition-based logic (Rules engine).
- Security Utilities (Hashing, Encryption).

### 2. Client App (`client_app.py`)
- **Auth**: Registration, Login, **Informed Consent (Research/Privacy)**.
- **UI**: Modern Ttk/Tkinter interface with **Emoji-enhanced User Experience**.
- **Features**:
    - Profile & Anthropometrics Input.
    - Diet Generator (based on local foods).
    - Daily Intake Log.
    - Help & AI Chat Interface.
    - Offline/Online Sync Manager.

### 3. Developer App (`developer_app.py`)
- **UI**: Dashboard view.
- **Features**:
    - Patient List (Grouped by risk/age).
    - Review Incoming Data.
    - AI Triage Approval Queue.
    - Notification/Content Push.

### 4. Server/Backend (`server.py`)
- Flask or Simulated Backend class.
- Endpoints for Snyc, Auth, Messaging.

## Data Schema (Conceptual)
- **Users**: id, email, password_hash, role, age_bracket, **consent_given**.

- **Profiles**: user_id, weight, height, condition, nutritional_status.
- **Logs**: user_id, date, food_items, analysis_result.
- **Messages**: id, user_id, question, ai_draft, status (pending/approved), response.

## Implementation Steps
1.  **Setup**: Create `common.py` with MOH standards and Food DB. [COMPLETED]
2.  **Database**: Create `database_manager.py` to handle Local vs Central DB. [COMPLETED]
3.  **Client UI**: Build the Auth and Main Dashboard for Clients. [COMPLETED - Premium UI Implemented]
4.  **Developer UI**: Build the Dashboard for Nutritionists. [COMPLETED - Premium UI Implemented]
5.  **Integration**: Ensure data flows between Client -> (Sync) -> Server -> Developer. [COMPLETED]
