import os

def generate_configs():
    if not os.path.exists("domain.txt"):
        return

    with open("domain.txt", "r") as f:
        host = f.read().strip()

    direct_snis = [
        "kubernetes.io", "letsencrypt.org", "kwok.sigs.k8s.io", "kind.sigs.k8s.io",
        "krew.sigs.k8s.io", "kueue.sigs.k8s.io", "jobset.sigs.k8s.io", "minikube.sigs.k8s.io",
        "kustomize.sigs.k8s.io", "cluster-api.sigs.k8s.io", "gateway-api.sigs.k8s.io",
        "image-builder.sigs.k8s.io", "kubectl.docs.kubernetes.io", "scheduler-plugins.sigs.k8s.io",
        "secrets-store-csi-driver.sigs.k8s.io"
    ]

    combo_snis = [
        "kubernetes.io", "letsencrypt.org", "jobset.sigs.k8s.io",
        "gateway-api.sigs.k8s.io", "cluster-api.sigs.k8s.io"
    ]

    ips = [
        "50.7.87.4", "144.76.1.88", "85.10.207.48", "95.216.69.37",
        "94.130.13.19", "94.130.50.12", "94.130.33.41", "204.12.196.34"
    ]

    results = []

    for sni in direct_snis:
        conf = f"vless://Telegram-Parsashonam@{sni}:443?encryption=none&security=tls&sni={sni}&alpn=h2%2Chttp%2F1.1&insecure=1&allowInsecure=1&type=xhttp&host={host}&path=%2Fp4r34m&mode=auto#%F0%9F%8C%90%20%40IR_NETLIFY%20%20%20{sni}"
        results.append(conf)

    for sni in combo_snis:
        for ip in ips:
            conf = f"vless://Telegram-Parsashonam@{ip}:443?encryption=none&security=tls&sni={sni}&alpn=h2%2Chttp%2F1.1&insecure=1&allowInsecure=1&type=xhttp&host={host}&path=%2Fp4r34m&mode=auto#%F0%9F%8C%90%20%40IR_NETLIFY%20%20{sni}%20%20{ip}"
            results.append(conf)

    with open("IR_NETLIFY_SUB.txt", "w") as f:
        f.write("\n".join(results))

if __name__ == "__main__":
    generate_configs()
