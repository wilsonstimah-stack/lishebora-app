import hashlib
import random
from datetime import datetime

# --- Constants ---
ROLE_CLIENT = "client"
ROLE_DEVELOPER = "developer/nutritionist"

MOH_AGE_BRACKETS = {
    "0-6m": "Infant (0-6 months)",
    "6-23m": "Young Child (6-23 months)",
    "2-5y": "Child (2-5 years)",
    "5-9y": "Child (5-9 years)",
    "10-14y": "Adolescent (10-14 years)",
    "15-19y": "Late Adolescent (15-19 years)",
    "20-59y": "Adult (20-59 years)",
    "60+y": "Elderly (60+ years)",
    "pregnant": "Pregnant Woman",
    "lactating": "Lactating Mother"
}

CONDITIONS = [
    "None", "Diabetes (Type 1)", "Diabetes (Type 2)", "Hypertension", 
    "Pregnancy", "Lactation", "Anemia", "Gout", "Chronic Kidney Disease", 
    "Peptic Ulcers", "Lactose Intolerance", "Celiac Disease", 
    "Hypercholesterolemia", "Rheumatoid Arthritis", "Food Allergies",
    "GERD", "PCOS", "Osteoporosis", "Hypothyroidism", "Hyperthyroidism",
    "IBS", "HIV/AIDS", "Tuberculosis", "Malaria Recovery"
]

HEALTH_TIPS = [
    "Nutrition Health Fact: Did you know that Avocado is rich in healthy monounsaturated fats that support heart health?",
    "Nutrition Health Fact: Did you know that drinking 8 glasses of water daily significantly improves digestion and energy levels?",
    "Nutrition Health Fact: Did you know that traditional vegetables like Managu and Terere are packed with Iron and Calcium?",
    "Nutrition Health Fact: Did you know that reducing salt intake is one of the most effective ways to manage blood pressure?",
    "Nutrition Health Fact: Did you know that Sweet Potatoes (Ngwaci) are a superior source of Vitamin A compared to white potatoes?",
    "Nutrition Health Fact: Did you know that eating slowly allows your brain to register fullness, preventing overeating?",
    "Nutrition Health Fact: Did you know that frequent sugary drinks are a leading cause of tooth decay and metabolic issues?",
    "Nutrition Health Fact: Did you know that Omena (silver fish) is one of the richest sources of Calcium and Omega-3 in Kenya?",
    "Nutrition Health Fact: Did you know that green leafy vegetables can reduce your risk of heart disease by up to 25%?"
]

# --- Kenyan Food Composition Database ---
KENYAN_FOOD_DB = {
    "starch": [
        {"name": "Ugali (Maize)", "cal": 150, "fiber": "low", "macros": "carb"},
        {"name": "Ugali (Sorghum/Millet)", "cal": 140, "fiber": "high", "macros": "carb"},
        {"name": "Sweet Potatoes (Ngwaci)", "cal": 90, "fiber": "high", "macros": "carb"},
        {"name": "Arrowroots (Nduma)", "cal": 100, "fiber": "high", "macros": "carb"},
        {"name": "Chapati", "cal": 300, "fiber": "medium", "macros": "carb/fat"},
        {"name": "Rice", "cal": 130, "fiber": "low", "macros": "carb"},
        {"name": "Green Bananas (Matoke)", "cal": 90, "fiber": "high", "macros": "carb"},
        {"name": "Cassava (Mhogo)", "cal": 160, "fiber": "medium", "macros": "carb"},
        {"name": "Irish Potatoes", "cal": 80, "fiber": "medium", "macros": "carb"},
        {"name": "Githeri", "cal": 180, "fiber": "high", "macros": "carb/protein"}
    ],
    "protein": [
        {"name": "Beans (Maharagwe)", "cal": 110, "fiber": "high", "macros": "protein/carb"},
        {"name": "Green Grams (Ndengu)", "cal": 105, "fiber": "high", "macros": "protein/carb"},
        {"name": "Omena", "cal": 200, "fiber": "low", "macros": "protein/fat"},
        {"name": "Beef", "cal": 250, "fiber": "0", "macros": "protein/fat"},
        {"name": "Chicken (Kienyeji)", "cal": 150, "fiber": "0", "macros": "protein"},
        {"name": "Eggs", "cal": 140, "fiber": "0", "macros": "protein/fat"},
        {"name": "Milk (Maziwa)", "cal": 60, "fiber": "0", "macros": "protein/fat"},
        {"name": "Yoghurt (Mala)", "cal": 100, "fiber": "0", "macros": "protein/carb"},
        {"name": "Fish (Tilapia)", "cal": 120, "fiber": "0", "macros": "protein"},
        {"name": "Lentils (Kamande)", "cal": 115, "fiber": "high", "macros": "protein/carb"}
    ],
    "veg": [
        {"name": "Sukuma Wiki (Kale)", "cal": 30, "vitamins": "A, C, K"},
        {"name": "Spinach", "cal": 25, "vitamins": "A, C, K"},
        {"name": "Managu (African Nightshade)", "cal": 35, "vitamins": "A, C, Iron"},
        {"name": "Terere (Amaranth)", "cal": 30, "vitamins": "A, C, Iron"},
        {"name": "Kunde (Cowpea leaves)", "cal": 35, "vitamins": "A, C"},
        {"name": "Cabbage", "cal": 25, "vitamins": "C, K"},
        {"name": "Pumpkin Leaves (Malenge)", "cal": 30, "vitamins": "A, C"},
        {"name": "Mrenda (Jute Mallow)", "cal": 28, "vitamins": "A, C, Iron"},
        {"name": "Sagaa (Spider Plant)", "cal": 32, "vitamins": "A, C"}
    ],
    "fruit": [
        {"name": "Mango", "cal": 60, "vitamins": "A, C"},
        {"name": "Avocado", "cal": 160, "vitamins": "E, K, Fat"},
        {"name": "Orange", "cal": 45, "vitamins": "C"},
        {"name": "Watermelon", "cal": 30, "vitamins": "A, C"},
        {"name": "Pawpaw (Papaya)", "cal": 40, "vitamins": "A, C"},
        {"name": "Banana", "cal": 90, "vitamins": "Potassium"},
        {"name": "Passion Fruit", "cal": 35, "vitamins": "A, C"},
        {"name": "Pineapple", "cal": 50, "vitamins": "C, B6"}
    ]
}

# --- Anthropometric Standards (WHO/MOH Kenya) ---

# MUAC cutoffs (mm) for different age groups
MUAC_CUTOFFS = {
    "6-59m": {"SAM": 115, "MAM": 125, "Normal": 999},  # Children 6-59 months
    "5-9y": {"SAM": 135, "MAM": 145, "Normal": 999},
    "10-14y": {"SAM": 160, "MAM": 185, "Normal": 999},
    "15-19y": {"SAM": 185, "MAM": 210, "Normal": 999},
    "adult": {"SAM": 190, "MAM": 210, "Normal": 999},
    "pregnant": {"SAM": 190, "MAM": 230, "Normal": 999}  # Special for pregnant women
}

def calculate_age_years(dob_str):
    """Calculate age in years from date of birth string (YYYY-MM-DD)"""
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except:
        return None

def get_age_bracket_from_age(age_years, is_pregnant=False, is_lactating=False):
    """Determine age bracket from numerical age"""
    if is_pregnant:
        return "pregnant"
    if is_lactating:
        return "lactating"
    if age_years < 0.5:
        return "0-6m"
    elif age_years < 2:
        return "6-23m"
    elif age_years < 5:
        return "2-5y"
    elif age_years < 10:
        return "5-9y"
    elif age_years < 15:
        return "10-14y"
    elif age_years < 20:
        return "15-19y"
    elif age_years < 60:
        return "20-59y"
    else:
        return "60+y"

def calculate_bmi(weight_kg, height_cm):
    """Calculate Body Mass Index"""
    try:
        if not weight_kg or not height_cm or height_cm == 0:
            return 0
        height_m = height_cm / 100
        return round(weight_kg / (height_m * height_m), 1)
    except:
        return 0

def get_muac_status(muac_mm, age_bracket):
    """
    Determine nutritional status based on MUAC (Mid-Upper Arm Circumference)
    Returns: SAM (Severe Acute Malnutrition), MAM (Moderate), or Normal
    """
    if not muac_mm:
        return "Not Assessed"
    
    # Map age bracket to MUAC category
    if age_bracket in ["6-23m", "2-5y"]:
        category = "6-59m"
    elif age_bracket in ["5-9y"]:
        category = "5-9y"
    elif age_bracket in ["10-14y"]:
        category = "10-14y"
    elif age_bracket in ["15-19y"]:
        category = "15-19y"
    elif age_bracket == "pregnant":
        category = "pregnant"
    else:
        category = "adult"
    
    cutoffs = MUAC_CUTOFFS.get(category, MUAC_CUTOFFS["adult"])
    
    if muac_mm < cutoffs["SAM"]:
        return "SAM (Severe Acute Malnutrition)"
    elif muac_mm < cutoffs["MAM"]:
        return "MAM (Moderate Acute Malnutrition)"
    else:
        return "Normal"

def get_bmi_status(bmi, age_bracket):
    """Get nutritional status based on BMI for adults"""
    if age_bracket in ["20-59y", "60+y"]:
        if bmi < 16.0:
            return "Severe Underweight"
        elif bmi < 17.0:
            return "Moderate Underweight"
        elif bmi < 18.5:
            return "Mild Underweight"
        elif bmi < 25.0:
            return "Normal Weight"
        elif bmi < 30.0:
            return "Overweight"
        elif bmi < 35.0:
            return "Obese Class I"
        elif bmi < 40.0:
            return "Obese Class II"
        else:
            return "Obese Class III"
    elif age_bracket == "pregnant":
        # Simplified for pregnancy
        if bmi < 18.5:
            return "Underweight (Risk)"
        elif bmi < 25.0:
            return "Healthy Weight"
        elif bmi < 30.0:
            return "Overweight (Monitor)"
        else:
            return "Obese (High Risk)"
    else:
        # Children - simplified, normally use Z-scores
        return "Use MUAC/Z-Score"

def get_comprehensive_status(weight_kg, height_cm, muac_mm, age_bracket):
    """
    Get comprehensive nutritional assessment using multiple indicators
    """
    bmi = calculate_bmi(weight_kg, height_cm)
    bmi_status = get_bmi_status(bmi, age_bracket)
    muac_status = get_muac_status(muac_mm, age_bracket)
    
    # Priority: MUAC for acute malnutrition, BMI for chronic
    if "SAM" in muac_status:
        priority_status = muac_status
        action = "URGENT: Refer to health facility immediately"
    elif "MAM" in muac_status:
        priority_status = muac_status
        action = "ATTENTION: Nutrition supplementation recommended"
    elif "Underweight" in bmi_status:
        priority_status = bmi_status
        action = "Monitor closely, increase nutrient-dense foods"
    elif "Obese" in bmi_status or "Overweight" in bmi_status:
        priority_status = bmi_status
        action = "Lifestyle modification recommended"
    else:
        priority_status = "Normal"
        action = "Maintain healthy eating habits"
    
    return {
        "bmi": bmi,
        "bmi_status": bmi_status,
        "muac_status": muac_status,
        "priority_status": priority_status,
        "action": action
    }

def get_random_food(category, count=1, exclude=None):
    items = [x['name'] for x in KENYAN_FOOD_DB[category]]
    if exclude:
        items = [x for x in items if x not in exclude]
    return random.sample(items, min(count, len(items)))

def generate_diet_plan(condition, age_bracket, status):
    """
    Returns a dictionary structured by meal time with Kenyan foods.
    """
    plan = {}
    
    # 1. Breakfast
    main_starch = get_random_food("starch", 1)[0]
    subs_starch = get_random_food("starch", 2, exclude=[main_starch])
    bf_main = f"{main_starch} + Tea (Low Sugar)"
    
    plan["Breakfast"] = {
        "main": bf_main,
        "subs": subs_starch,
        "goal": "Energy Start"
    }

    # 2. Snack AM
    main_fruit = get_random_food("fruit", 1)[0]
    subs_fruit = get_random_food("fruit", 2, exclude=[main_fruit])
    plan["Snack (10am)"] = {
        "main": f"1 Serving of {main_fruit}",
        "subs": subs_fruit,
        "goal": "Vitamin Boost"
    }

    # 3. Lunch
    l_starch = get_random_food("starch", 1)[0]
    l_prot = get_random_food("protein", 1)[0]
    l_veg = get_random_food("veg", 1)[0]
    
    l_subs = []
    for _ in range(2):
        s = get_random_food("starch", 1)[0]
        p = get_random_food("protein", 1)[0]
        v = get_random_food("veg", 1)[0]
        l_subs.append(f"{s} + {p} + {v}")
    
    plan["Lunch"] = {
        "main": f"{l_starch} + {l_prot} + {l_veg}",
        "subs": l_subs,
        "goal": "Balanced Meal"
    }

    # 4. Snack PM
    plan["Snack (4pm)"] = {
        "main": "Yoghurt (Mala) or Groundnuts",
        "subs": ["Fresh Juice", "Boiled Egg", "Fruit Salad"],
        "goal": "Sustain Energy"
    }

    # 5. Supper
    s_starch = get_random_food("starch", 1, exclude=[l_starch])[0]
    s_prot = get_random_food("protein", 1, exclude=[l_prot])[0]
    s_veg = get_random_food("veg", 1, exclude=[l_veg])[0]
    
    ss_starch = get_random_food("starch", 1, exclude=[l_starch, s_starch])[0]
    
    plan["Supper"] = {
        "main": f"{s_starch} + {s_prot} + {s_veg}",
        "subs": [f"{ss_starch} + {s_prot} + {s_veg}"],  
        "goal": "Recovery & Rest"
    }

    return plan

def analyze_intake(food_log_text, condition):
    text = food_log_text.lower()
    
    found_starch = any(f['name'].split()[0].lower() in text for f in KENYAN_FOOD_DB['starch'])
    found_protein = any(f['name'].split()[0].lower() in text for f in KENYAN_FOOD_DB['protein'])
    found_veg = any(f['name'].split()[0].lower() in text for f in KENYAN_FOOD_DB['veg'])
    found_fruit = any(f['name'].split()[0].lower() in text for f in KENYAN_FOOD_DB['fruit'])
    
    analysis = "Daily Intake Assessment:\n"
    missing = []
    
    if found_starch: analysis += "✓ Energy Foods (Starch) - Present\n"
    else: missing.append("Starch/Energy Foods")
    
    if found_protein: analysis += "✓ Body Building Foods (Protein) - Present\n"
    else: missing.append("Protein/Body Building Foods")
    
    if found_veg: analysis += "✓ Protective Foods (Vegetables) - Present\n"
    else: missing.append("Vegetables/Protective Foods")
    
    if found_fruit: analysis += "✓ Vitamin-Rich Foods (Fruits) - Present\n"
    else: missing.append("Fruits")
    
    recommendation = ""
    if missing:
        recommendation = f"Nutritional Goal:\nYour intake is missing: {', '.join(missing)}.\nPlease include these food groups in your next meal for optimal health."
    else:
        recommendation = "Excellent! You have achieved dietary diversity today. Continue maintaining this balanced intake."
        
    return analysis, recommendation

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_hash, password):
    return stored_hash == hashlib.sha256(password.encode()).hexdigest()

# Consent Text (Professional)
CONSENT_TEXT = """
INFORMED CONSENT FOR NUTRITION SERVICES

Purpose: This application collects health and dietary information to provide personalized nutrition guidance aligned with Kenya Ministry of Health guidelines.

Data Usage:
• Your information will be used solely for nutrition assessment and personalized recommendations
• Data may be anonymized for research to improve nutrition interventions in Kenya
• Your personal identifiers will remain confidential and protected

Your Rights:
• You may withdraw consent at any time
• You may request access to or deletion of your data
• You may decline to answer any questions

By proceeding, I confirm that:
1. I understand the purpose of this nutrition service
2. I consent to the collection and use of my health data as described
3. I will provide accurate information to the best of my knowledge
4. I understand this is not a substitute for professional medical advice

This consent is in accordance with the Kenya Data Protection Act, 2019.
"""
