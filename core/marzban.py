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
        return "خطا در لاگین به مرزبان"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # تنظیمات کاربری که می‌خوایم بسازیم (حجم به بایت محاسبه میشه)
    payload = {
        "username": username,
        "data_limit":int(data_limit_gb) * 1073741824, # تبدیل گیگابایت به بایت
        "proxies":{ "vmess": {},
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
    
    if response.status_code == 200:
        new_user = response.json()
        # لینک اشتراک (سابسکریپشن) کاربر رو استخراج می‌کنیم
        sub_link = new_user.get("subscription_url")
        return f"  لینک ساب :  {MARZBAN_URL}{sub_link}"
    elif response.status_code== 409 or "User already exists" in response.text:

        requests.post(f"{MARZBAN_URL}/api/user/{username}/reset", headers=headers)

        update_payload = {
            "data_limit": int(data_limit_gb) * 1073741824,
            "status": "active"
        }
        update_res = requests.put(f"{MARZBAN_URL}/api/user/{username}", headers=headers, json=update_payload)
        
        # برگرداندن اطلاعات کاربرِ تمدید شده
        return update_res.text 
        
    # اگر اروری نبود و کاربر جدید با موفقیت ساخته شد، نتیجه را برگردان
    return response.text
       


