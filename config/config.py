import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(BASE_DIR, "archive", "foodDemand_train")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

TRAIN_CSV = os.path.join(RAW_DATA_DIR, "train.csv")
MEAL_INFO_CSV = os.path.join(RAW_DATA_DIR, "meal_info.csv")
CENTER_INFO_CSV = os.path.join(RAW_DATA_DIR, "fulfilment_center_info.csv")
TEST_CSV = os.path.join(BASE_DIR, "archive", "food_Demand_test.csv")
PROCESSED_CSV = os.path.join(PROCESSED_DATA_DIR, "smartcanteen_processed.csv")

MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "random_forest_demand.pkl")

# Mapping all 51 Kaggle meal_ids to distinct, realistic canteen dish names
FULL_MEAL_NAMES = {
    1885: "Thai Iced Tea",
    1993: "Thai Green Tea",
    2539: "Lemongrass Cooler",
    1248: "Masala Chai",
    2631: "Filter Coffee",
    1311: "Thai Peanut Chips",
    1062: "Italian Soda",
    1778: "Espresso Tonic",
    1803: "Steamed Rice Side",
    1198: "Crispy Spring Roll Dippers",
    2707: "Iced Cappuccino",
    1847: "Tom Yum Soup",
    1438: "Tom Kha Coconut Soup",
    2494: "Clear Noodle Soup",
    2760: "Crispy Noodle Basket",
    2490: "Caesar Salad",
    1109: "Paneer Rice Bowl",
    2290: "Rajma Chawal Bowl",
    1525: "Thai Fish Cake Bites",
    2704: "Sesame Toast Snacks",
    1878: "Chicken Satay Skewers",
    2640: "Veg Money Bags",
    2577: "Crispy Tofu Bites",
    1754: "Panini Grilled Sandwich",
    1971: "Pesto Veggie Sandwich",
    2306: "Arrabbiata Penne",
    2139: "Mango Lassi",
    2826: "Cheese Toastie Sandwich",
    2664: "Caprese Salad",
    2569: "Mediterranean Pasta Salad",
    1230: "Cold Brew Coffee",
    1207: "Chocolate Milkshake",
    2322: "Vanilla Smoothie",
    2492: "Gulab Jamun",
    1216: "Creamy Alfredo Pasta",
    1727: "Chole Rice Bowl",
    1902: "Hyderabadi Dum Biryani",
    1247: "Lucknowi Veg Biryani",
    2304: "Rasgulla",
    1543: "Kheer Pudding",
    1770: "Special Paneer Biryani",
    2126: "Basil Spaghetti",
    1558: "Margherita Pizza",
    2581: "Farmhouse Veggie Pizza",
    1962: "Pepperoni Delight Pizza",
    1571: "Grilled Lemon Fish",
    2956: "Crispy Fish Fillet",
    2104: "Baked Herb Fish",
    2444: "Butter Garlic Prawns",
    2867: "Crispy Calamari Rings",
    1445: "Seafood Chowder Platter"
}

CENTER_MAPPING = {
    55: "Main Campus Canteen (Center 55)",
    24: "Hostel Block A Canteen (Center 24)",
    11: "Engineering Block Canteen (Center 11)",
    52: "Management Block Canteen (Center 52)",
    86: "Medical Campus Canteen (Center 86)",
}
