import os
import requests

def is_healthy(domain):
    clean_domain = domain.split(' ')[-1].strip()
    if not clean_domain: return False
    url = f"https://{clean_domain}"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        if "Site not found" in r.text or r.status_code == 404:
            return False
        return r.status_code == 200
    except:
        return False

def update_track(current_file, active_file, failed_file):
    current = ""
    if os.path.exists(current_file):
        with open(current_file, "r") as f:
            current = f.read().strip()
    
    if not current or not is_healthy(current):
        if current:
            with open(failed_file, "a") as f:
                f.write(current + "\n")
        
        if os.path.exists(active_file):
            with open(active_file, "r") as f:
                pool = [l.strip() for l in f if l.strip()]
            
            new_found = False
            while pool:
                candidate = pool.pop(0)
                if is_healthy(candidate):
                    new_domain = candidate.split(' ')[-1].strip()
                    with open(current_file, "w") as f:
                        f.write(new_domain)
                    new_found = True
                    break
                else:
                    with open(failed_file, "a") as f:
                        f.write(candidate + "\n")
            
            with open(active_file, "w") as f:
                f.write("\n".join(pool))
            return new_found
    return False

def run():
    # Track 1: Original
    update_track("domain.txt", "active_domains.txt", "failed_domains.txt")
    
    # Track 2: New
    update_track("domain_new.txt", "active_domains_new.txt", "failed_domains_new.txt")

if __name__ == "__main__":
    run()
