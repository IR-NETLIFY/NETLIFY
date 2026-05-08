import os, requests

ACTIVE_F = "active_domains.txt"
FAILED_F = "failed_domains.txt"
CURRENT_F = "domain.txt"

def is_healthy(domain):
    # پاکسازی نام دامنه از کاراکترهای اضافه
    clean_domain = domain.split(' ')[-1].strip()
    if not clean_domain: return False
    try:
        r = requests.get(f"https://{clean_domain}", timeout=10)
        return r.status_code == 200
    except: return False

def run():
    current = ""
    if os.path.exists(CURRENT_F):
        with open(CURRENT_F, "r") as f: current = f.read().strip()
    
    # اگر دامنه فعلی خراب بود یا خالی بود
    if not current or not is_healthy(current):
        print(f"Domain {current} is down!")
        if current:
            with open(FAILED_F, "a") as f: f.write(current + "\n")
        
        if os.path.exists(ACTIVE_F):
            with open(ACTIVE_F, "r") as f:
                pool = [l.strip() for l in f if l.strip()]
            
            new_found = False
            while pool:
                candidate = pool.pop(0)
                if is_healthy(candidate):
                    with open(CURRENT_F, "w") as f: f.write(candidate.split(' ')[-1].strip())
                    print(f"Switched to {candidate}")
                    new_found = True
                    break
                else:
                    with open(FAILED_F, "a") as f: f.write(candidate + "\n")
            
            with open(ACTIVE_F, "w") as f: f.write("\n".join(pool))

if __name__ == "__main__":
    run()
