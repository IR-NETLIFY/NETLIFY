import os, requests

ACTIVE_F = "active_domains.txt"
FAILED_F = "failed_domains.txt"
CURRENT_F = "domain.txt"

def is_healthy(domain):
    try:
        # چک کردن با تایم‌اوت کوتاه برای سرعت بیشتر
        r = requests.get(f"https://{domain.strip()}", timeout=10)
        return r.status_code == 200
    except: return False

if os.path.exists(CURRENT_F):
    with open(CURRENT_F, "r") as f: current = f.read().strip()
    
    if not current or not is_healthy(current):
        print(f"Domain {current} is down!")
        if current:
            with open(FAILED_F, "a") as f: f.write(current + "\n")
        
        if os.path.exists(ACTIVE_F):
            with open(ACTIVE_F, "r") as f:
                pool = [l.strip() for l in f if l.strip()]
            
            while pool:
                candidate = pool.pop(0)
                if is_healthy(candidate):
                    with open(CURRENT_F, "w") as f: f.write(candidate)
                    print(f"Switched to {candidate}")
                    break
                else:
                    with open(FAILED_F, "a") as f: f.write(candidate + "\n")
            
            with open(ACTIVE_F, "w") as f: f.write("\n".join(pool))
