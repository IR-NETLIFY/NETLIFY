import os
import requests

TELEGRAM_WORKER_URL = "https://telegram-bot.ir-netlify.workers.dev/"

def is_healthy(domain):
    clean_domain = domain.split(' ')[-1].strip()
    if not clean_domain: return False
    try:
        r = requests.get(f"https://{clean_domain}", headers={'User-Agent': 'Mozilla/5.0'}, timeout=7)
        return r.status_code == 200 and "CONFIG GENERATOR" in r.text.upper()
    except: return False

def send_report(failed, new, list_name, remaining_list, failed_file):
    try:
        with open(failed_file, "r") as f:
            failed_content = f.read().strip()
        
        payload = {
            "failed_domain": failed,
            "new_domain": new,
            "list_name": list_name,
            "remaining_count": len(remaining_list),
            "failed_list": failed_content if failed_content else "Empty"
        }
        requests.post(TELEGRAM_WORKER_URL, json=payload, timeout=10)
    except: pass

def update_track(current_file, active_file, failed_file, list_label):
    current = ""
    if os.path.exists(current_file):
        with open(current_file, "r") as f:
            current = f.read().strip()

    if not current or not is_healthy(current):
        failed_target = current if current else "Unknown/Empty"
        
        if os.path.exists(active_file):
            with open(active_file, "r") as f:
                pool = [l.strip() for l in f if l.strip()]
            
            new_domain = None
            for candidate in pool[:]:
                if is_healthy(candidate):
                    new_domain = candidate.split(' ')[-1].strip()
                    pool.remove(candidate)
                    with open(current_file, "w") as f: f.write(new_domain)
                    break
                else:
                    with open(failed_file, "a") as f: f.write(candidate + "\n")
                    pool.remove(candidate)

            with open(active_file, "w") as f: f.write("\n".join(pool))
            
            if new_domain:
                if current:
                    with open(failed_file, "a") as f: f.write(current + "\n")
                send_report(failed_target, new_domain, list_label, pool, failed_file)
                return True
    return False

if __name__ == "__main__":
    update_track("domain.txt", "active_domains.txt", "failed_domains.txt", "Main Repository")
    update_track("domain_new.txt", "active_domains_new.txt", "failed_domains_new.txt", "New Repository")
