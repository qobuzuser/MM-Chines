import json
import os

# အခြေအနေသိမ်းမည့် ဖိုင်အမည်
CONFIG_FILE = "bot_config.json"

def load_config():
    """Config file ကို ဖတ်ပါမယ်။ ဖိုင်မရှိသေးရင် အသစ်ဆောက်ပါမယ်။"""
    if not os.path.exists(CONFIG_FILE):
        # Default အနေနဲ့ Bot ကို On ထားပါမယ်
        default_config = {"is_public": True}
        save_config(default_config)
        return default_config
    
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        # ဖိုင်ဖတ်မရရင် Default ပြန်ပေးပါမယ်
        return {"is_public": True}

def save_config(config_data):
    """Config file ထဲသို့ သိမ်းပါမယ်။"""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f)
    except Exception as e:
        print(f"Error saving config: {e}")

def is_bot_active():
    """Bot ဖွင့်ထားသလား စစ်ဆေးရန်"""
    config = load_config()
    return config.get("is_public", True)

def set_bot_active(status: bool):
    """Bot ကို ပိတ်ရန်/ဖွင့်ရန်"""
    config = load_config()
    config["is_public"] = status
    save_config(config)
