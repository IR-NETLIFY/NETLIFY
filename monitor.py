import os
import requests

def is_healthy(domain):
    clean_domain = domain.split(' ')[-1].strip()
    if not clean_domain:
        return False
    url = f"https://{clean_domain}"
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=7)
        return r.status_code == 200 and "CONFIG GENERATOR" in r.text.upper()
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

            new_domain_found = False
            failed_candidates = []

            for candidate in pool:
                if is_healthy(candidate):
                    new_domain = candidate.split(' ')[-1].strip()
                    with open(current_file, "w") as f:
                        f.write(new_domain)
                    
                    new_domain_found = True
                    pool.remove(candidate)
                    break
                else:
                    failed_candidates.append(candidate)

            if failed_candidates:
                with open(failed_file, "a") as f:
                    f.write("\n".join(failed_candidates) + "\n")
                for fc in failed_candidates:
                    if fc in pool:
                        pool.remove(fc)

            with open(active_file, "w") as f:
                f.write("\n".join(pool))
            
            return new_domain_found
    return False

def run():
    update_track("domain.txt", "active_domains.txt", "failed_domains.txt")
    update_track("domain_new.txt", "active_domains_new.txt", "failed_domains_new.txt")

if __name__ == "__main__":
    run()
