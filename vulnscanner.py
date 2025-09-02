import requests
import sys

# === Function 1: get headers ===
def get_headers(url):
    try:
        response = requests.get(url)
        print(f"\n[+] Scanning: {url}")
        print("[+] Status Code:", response.status_code)
        return response.headers
    except requests.exceptions.RequestException as e:
        print("[-] Error:", e)
        sys.exit(1)

# === Function 2: check for missing security headers ===
def check_missing_headers(headers):
    recommended = ["X-Frame-Options", "X-Content-Type-Options", "Content-Security-Policy"]
    print("\n[+] Checking Security Headers...")
    for h in recommended:
        if h not in headers:
            print(f"[-] Missing: {h}")
        else:
            print(f"[+] Found: {h}")

# === Function 3: check for sensitive files ===
def check_sensitive_files(url):
    sensitive_files = ["/robots.txt", "/.git/", "/.env"]
    print("\n[+] Checking Sensitive Files...")
    for f in sensitive_files:
        try:
            r = requests.get(url + f)
            if r.status_code == 200:
                print(f"[!] Accessible: {url}{f}")
            else:
                print(f"[-] Not Found: {url}{f}")
        except requests.exceptions.RequestException:
            print(f"[-] Error checking {f}")

# === Main block ===
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vulnscanner.py <URL>")
        sys.exit(1)

    target_url = sys.argv[1]

    # Call your functions here 👇
    headers = get_headers(target_url)          # 1. Grab headers
    check_missing_headers(headers)             # 2. Check security headers
    check_sensitive_files(target_url)          # 3. Look for sensitive files
