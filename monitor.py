import os
import requests

ACTIVE_F = "active_domains.txt"
FAILED_F = "failed_domains.txt"
CURRENT_F = "domain.txt"

def is_healthy(domain):
    domain = domain.strip()
    if not domain or domain.startswith("[source"): # نادیده گرفتن خطوط توضیحی
        return False
    try:
        # پاکسازی آدرس برای اطمینان
        url = domain if domain.startswith("http") else f"https://{domain}"
        r = requests.get(url, timeout=10, allow_redirects=True)
        print(f"Checking {domain}... Status: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"Error checking {domain}: {e}")
        return False

def run():
    current = ""
    if os.path.exists(CURRENT_F):
        with open(CURRENT_F, "r") as f:
            current = f.read().strip()

    # اگر دامنه فعلی خراب است یا اصلاً وجود ندارد
    if not current or not is_healthy(current):
        print(f"⚠️ Domain '{current}' is down or missing!")
        
        if current:
            with open(FAILED_F, "a") as f:
                f.write(current + "\n")

        if os.path.exists(ACTIVE_F):
            with open(ACTIVE_F, "r") as f:
                pool = [l.strip() for l in f if l.strip() and not l.startswith("[")]
            
            new_found = False
            while pool:
                candidate = pool.pop(0)
                if is_healthy(candidate):
                    with open(CURRENT_F, "w") as f:
                        f.write(candidate)
                    print(f"✅ Switched to NEW healthy domain: {candidate}")
                    new_found = True
                    break
                else:
                    print(f"❌ {candidate} is also down.")
                    with open(FAILED_F, "a") as f:
                        f.write(candidate + "\n")
            
            # بروزرسانی لیست دامنه‌های فعال باقی‌مانده
            with open(ACTIVE_F, "w") as f:
                f.write("\n".join(pool))
            
            if not new_found:
                print("🚨 CRITICAL: No healthy domains left in active_domains.txt!")
    else:
        print(f"☀️ Current domain {current} is still healthy.")

if __name__ == "__main__":
    run()
