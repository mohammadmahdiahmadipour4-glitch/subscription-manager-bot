import requests

# اطلاعات سرور مرزبان شما
MARZBAN_URL = "https://vip.chapar.us"
ADMIN_USER = "Mhmmdahp"
ADMIN_PASS = "Mohammad.5831@ahp"

# ۱. تابع برای گرفتن توکن ورود
def get_token():
    data = {"username": ADMIN_USER, "password": ADMIN_PASS}
    # مرزبان برای لاگین دیتا رو به صورت فرم می‌گیره (نه جیسون)
    response = requests.post(f"{MARZBAN_URL}/api/admin/token", data=data)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None

# ۲. تابع برای ساخت کاربر جدید
def create_vpn_user(username, data_limit_gb):
    token = get_token()
    if not token:
        return "❌ خطا در لاگین به مرزبان"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    if int(float(data_limit_gb)) == 0.1 : 
        bytes_limit = 104857600
    else : 
        bytes_limit = int(float(data_limit_gb) * 1073741824)

    payload = {
        "username": username,
        "data_limit": bytes_limit, 
        "proxies": { 
            "vmess": {},
            "trojan": {},
            "shadowsocks": {}
        }, 
       "inbounds": {
            "vmess": ["VMess Websocket"],
            "trojan": ["TROJAN GRPC NOTLS"],
            "shadowsocks": ["Shadowsocks TCP"]
        }
    }
    
    response = requests.post(f"{MARZBAN_URL}/api/user", headers=headers, json=payload)
    
    # --- حالت اول: ساخت موفقیت‌آمیز کاربر جدید ---
    if response.status_code == 200:
        new_user = response.json()
        sub_link = new_user.get("subscription_url", "")
        # فقط لینک ساب رو برمی‌گردونیم (کانفیگ‌های خام حذف میشن)
        return f"{MARZBAN_URL}{sub_link}"
        
    # --- حالت دوم: کاربر از قبل وجود دارد (شارژ و تمدید) ---
    elif response.status_code == 409 or "User already exists" in response.text:

        if username.endswith("test"):
            return "❌ شما قبلاً یک بار اکانت تست دریافت کرده‌اید و امکان دریافت مجدد وجود ندارد."
        # صفر کردن مصرف
        requests.post(f"{MARZBAN_URL}/api/user/{username}/reset", headers=headers)
        
        # شارژ مجدد
        update_payload = {
            "data_limit": bytes_limit,
            "status": "active"
        }
        update_res = requests.put(f"{MARZBAN_URL}/api/user/{username}", headers=headers, json=update_payload)
        
        if update_res.status_code == 200:
            updated_user = update_res.json()
            sub_link = updated_user.get("subscription_url", "")
            # فقط لینک ساب رو برمی‌گردونیم
            return f"{MARZBAN_URL}{sub_link}"
        else:
            return "❌ خطای سرور در زمان تمدید"
            
    # به جای متنِ "خطای ناشناخته"، دقیقاً دلیل ارور رو از مرزبان می‌گیریم!
    return f"❌ ارور دقیق از مرزبان:\nکد: {response.status_code}\nدلیل: {response.text}"

