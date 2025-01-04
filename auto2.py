import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import itertools
import time

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

# All site configurations
sites = {
    "takipcimx": {
        "base_url": "https://takipcimx.net",
        "login_url": "https://takipcimx.net/login",
        "action_page_url": "https://takipcimx.net/tools/send-follower",
    },
    "takipcizen": {
        "base_url": "https://takipcizen.com",
        "login_url": "https://takipcizen.com/login",
        "action_page_url": "https://takipcizen.com/tools/send-follower",
    },
    "takipcigir": {
        "base_url": "https://takipcigir.com",
        "login_url": "https://takipcigir.com/login",
        "action_page_url": "https://takipcigir.com/tools/send-follower",
    },
    "takipcikrali": {
        "base_url": "https://takipcikrali.com",
        "login_url": "https://takipcikrali.com/login",
        "action_page_url": "https://takipcikrali.com/tools/send-follower",
    },
    "takipcibase": {
        "base_url": "https://takipcibase.com",
        "login_url": "https://takipcibase.com/login",
        "action_page_url": "https://takipcibase.com/tools/send-follower",
    },
    "takipcitime": {
        "base_url": "https://takipcitime.com",
        "login_url": "https://takipcitime.com/login",
        "action_page_url": "https://takipcitime.com/tools/send-follower",
    },
    "takipcimax": {
        "base_url": "https://takipcimax.com",
        "login_url": "https://takipcimax.com/login",
        "action_page_url": "https://takipcimax.com/tools/send-follower",
    },
    "takipcivar": {
        "base_url": "https://www.takipcivar.net",
        "login_url": "https://www.takipcivar.net/login",
        "action_page_url": "https://www.takipcivar.net/tools/send-follower",
    },
    "takipcikrali_member": {
        "base_url": "https://www.takipcikrali.com",
        "login_url": "https://www.takipcikrali.com/login",
        "action_page_url": "https://www.takipcikrali.com/member",
    },
    "takipcimx_member": {
        "base_url": "https://takipcimx.com",
        "login_url": "https://takipcimx.com/member",
        "action_page_url": "https://takipcimx.com/tools/send-follower",
    },
    "takipciking_member": {
        "base_url": "https://takipciking.com",
        "login_url": "https://takipciking.com/member",
        "action_page_url": "https://takipciking.com/tools/send-follower",
    },
    "birtakipci_member": {
        "base_url": "https://birtakipci.com",
        "login_url": "https://birtakipci.com/member",
        "action_page_url": "https://birtakipci.com/tools/send-follower",
    },
    "instamoda": {
        "base_url": "https://www.instamoda.org",
        "login_url": "https://www.instamoda.org/login",
        "action_page_url": "https://www.instamoda.org/tools/send-follower",
    },
    "followersize": {
        "base_url": "https://followersize.com",
        "login_url": "https://followersize.com/member",
        "action_page_url": "https://followersize.com/tools/send-follower",
    },
    "platintakipci": {
        "base_url": "https://platintakipci.com",
        "login_url": "https://platintakipci.com/member",
        "action_page_url": "https://platintakipci.com/tools/send-follower",
    },
    "takipcifox": {
        "base_url": "https://takipcifox.com",
        "login_url": "https://takipcifox.com/member",
        "action_page_url": "https://takipcifox.com/tools/send-follower",
    },
    "takipciking_net": {
        "base_url": "https://takipciking.net",
        "login_url": "https://takipciking.net/login",
        "action_page_url": "https://takipciking.net/tools/send-follower",
    },
    "takipcigen": {
        "base_url": "https://takipcigen.com",
        "login_url": "https://takipcigen.com/login",
        "action_page_url": "https://takipcigen.com/tools/send-follower",
    },
    "instavevo": {
        "base_url": "https://instavevo.com",
        "login_url": "https://instavevo.com/member",
        "action_page_url": "https://instavevo.com/tools/send-follower",
    },
    "seritakipci": {
        "base_url": "https://seritakipci.com",
        "login_url": "https://seritakipci.com/member",
        "action_page_url": "https://seritakipci.com/tools/send-follower",
    },
    "takipstar": {
        "base_url": "https://takipstar.net",
        "login_url": "https://takipstar.net/login/login.php",
        "action_page_url": "https://takipstar.net/tools/send-follower",
    },
    "birtakipci_net": {
        "base_url": "https://birtakipci.net",
        "login_url": "https://birtakipci.net/login",
        "action_page_url": "https://birtakipci.net/tools/send-follower",
    },
    "anatakip": {
        "base_url": "https://anatakip.com",
        "login_url": "https://anatakip.com/login",
        "action_page_url": "https://anatakip.com/tools/send-follower",
    },
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def load_credentials(file_path):
    credentials = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                username, password = line.strip().split(":")
                credentials.append({"username": username, "password": password})
    except FileNotFoundError:
        pass
    return credentials

def resilient_request(request_func, *args, **kwargs):
    try:
        response = request_func(*args, **kwargs)
        return response
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}Error: {e}. Skipping to next site...{Colors.RESET}")
        return None

def process_site(session, site_name, credentials, target_username):
    config = sites[site_name]
    login_payload = {"username": credentials["username"], "password": credentials["password"], "userid": ""}
    login_response = resilient_request(session.post, config["login_url"], headers=headers, data=login_payload)

    if not login_response or "success" not in login_response.text.lower():
        print(f"{Colors.RED}Login failed on {site_name.upper()} for {credentials['username']}{Colors.RESET}")
        return

    print(f"{Colors.GREEN}Login successful on {site_name.upper()} for {credentials['username']}{Colors.RESET}")
    action_page_response = resilient_request(session.get, config["action_page_url"], headers=headers)

    if not action_page_response:
        return

    soup = BeautifulSoup(action_page_response.text, "html.parser")
    form = soup.find("form", {"action": "?formType=findUserID"})

    if not form:
        print(f"{Colors.RED}Form not found on {site_name.upper()}. Skipping...{Colors.RESET}")
        return

    form_action = urljoin(config["action_page_url"], form["action"])
    fields = {input_tag.get("name"): input_tag.get("value", "") for input_tag in form.find_all("input") if input_tag.get("name")}
    fields["username"] = target_username
    form_response = resilient_request(session.post, form_action, headers=headers, data=fields, allow_redirects=False)

    if not form_response or "Location" not in form_response.headers:
        print(f"{Colors.RED}No redirection found on {site_name.upper()}. Skipping...{Colors.RESET}")
        return

    redirected_url = urljoin(config["action_page_url"], form_response.headers["Location"])
    redirected_response = resilient_request(session.get, redirected_url, headers=headers)

    if not redirected_response:
        return

    soup = BeautifulSoup(redirected_response.text, "html.parser")
    form = soup.find("form", {"id": "formTakip"})

    if not form:
        print(f"{Colors.RED}Form 'formTakip' not found on {site_name.upper()}. Skipping...{Colors.RESET}")
        return

    form_action = urljoin(redirected_url, form.get("action", "?formType=send"))
    fields = {input_tag.get("name"): input_tag.get("value", "") for input_tag in form.find_all("input") if input_tag.get("name")}
    fields["adet"] = "100"

    send_response = resilient_request(session.post, form_action, headers=headers, data=fields)

    if send_response and "success" in send_response.text.lower():
        print(f"{Colors.CYAN}Followers sent successfully on {site_name.upper()} for {target_username}{Colors.RESET}")
    else:
        print(f"{Colors.RED}Error sending followers on {site_name.upper()} for {target_username}{Colors.RESET}")

def main():
    while True:
        credentials = load_credentials("credentials.txt")
        if not credentials:
            print(f"{Colors.YELLOW}No credentials found. Retrying in 10 seconds...{Colors.RESET}")
            time.sleep(10)
            continue

        target_username = input(f"{Colors.YELLOW}\nEnter the target username: {Colors.RESET}")
        session = requests.Session()

        for cred in itertools.cycle(credentials):
            for site in sites:
                process_site(session, site, cred, target_username)

main()