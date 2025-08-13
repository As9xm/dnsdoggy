import socket
import requests
from colorama import Fore, Style, init


init(autoreset=True)

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def is_hosting_provider(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/org", timeout=5)
        if response.status_code == 200:
            org = response.text
            # Basic heuristic: check for common hosting provider keywords
            hosting_keywords = ["Amazon", "Google", "Microsoft", "Cloudflare", "DigitalOcean", "Linode", "OVH"]
            for keyword in hosting_keywords:
                if keyword.lower() in org.lower():
                    return True, org
            return False, org
        else:
            return None, Fore.RED + "Unable to fetch organization info"
    except requests.RequestException:
        return None, Fore.RED + "Error while checking hosting provider"

def main():
    domain = input(Fore.BLACK + "Enter a domain name: ").strip()
    ip = get_ip(domain)
    if not ip:
        print(Fore.RED + "Could not resolve the domain name.")
        return

    print(f"IP address of {domain}: {ip}")
    is_hosting, org_info = is_hosting_provider(ip)
    if is_hosting is None:
        print(f"Could not determine hosting information: {org_info}")
    elif is_hosting:
        print(f"The IP belongs to a hosting provider: {org_info}")
    else:
        print(f"The IP appears to belong to a real server: {org_info}")

if __name__ == "__main__":
    main()