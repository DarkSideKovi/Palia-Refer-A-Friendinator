"""
Made with ♥ by DarkSideKovi

Do whatever the fuck you want with this code.
Usage examples and instructions available in the README file.
"""

import requests, random, time, threading

REGISTER_URL = "https://live.singularity6.com/acct-portal/api/v1/register"
REFRESH_URL = "https://web-auth.singularity6.com/api/jwt/refresh"
PROFILE_URL = "https://live.singularity6.com/acct-portal/api/v1/profile"
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
SMALL_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
DIGITS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
SPECIAL_CHARS = ['$', '%', ',', ':']

def main():
    code = input('Refer a friend code: ')
    T = time.time()
    threads: list[threading.Thread] = []
    print('Loading...')
    for i in range(5):
        thread: threading.Thread = threading.Thread(target = registerAccount, args = (code,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print(f'Operation completed in {time.time() - T:.4f} seconds.\n\nCheck your Refer-a-friend status on https://accounts.palia.com/account/referrals. If there are any missing, you can always re-run this script!:)')

def registerAccount(code: str) -> int:
    email: str = ''.join([i for i in random.choices(ALPHABET, k = 15)]) + "@akvy.ml"
    password: str = generatePassword()
    response: requests.Response = requests.post(
        url = REGISTER_URL,
        json = {
            "email": email,
            "needs_kws": False,
            "password": password,
            "preferred_languages": [ "en" ],
            "redemption_code": code,
            "subscribed": False
        }
    )
    if response.status_code != 200:
        print(f'Failed to register: {response.status_code}'); return -1
    
    regresp = response.json()
    try:
        access_token = regresp['access_token']
        refresh_token = regresp['refresh_token']
    except KeyError:
        print('Invalid response from registration API.'); return -1
    
    response: requests.Response = requests.post(
        url = REFRESH_URL,
        json = {
            "refreshToken": refresh_token,
            "token": f"Bearer {access_token}"
        }
    )

    if response.status_code != 200:
        print(f'Failed to refresh: {response.status_code}'); return -1

    refreshresp = response.json()
    try:
        access_token = refreshresp['token']
    except KeyError:
        print('Invalid response from refresh API.'); return -1
    
    response: requests.Response = requests.patch(
        url = PROFILE_URL,
        headers = {
            "Authorization": f"Bearer {access_token}"
        },
        json = {
            "account_name": email,
            "birth_date": "2000-09-03",
            "data": {
                "country": "AT"
            }
        }
    )
    if response.status_code != 200:
        print(f'Failed to update profile: {response.status_code}'); return -1
    print(f'Profile creation successful for {email}')
    return 0

def generatePassword() -> str:
    temp: str = str_concat_from(ALPHABET) + str_concat_from(SMALL_LETTERS) + str_concat_from(DIGITS, k = 2) + str_concat_from(SPECIAL_CHARS, k = 1)
    # Shuffle the characters
    password: str = ''.join(random.sample(temp, k = len(temp)))
    return password

def str_concat_from(L: list, k: int = 5) -> str:
    return ''.join([i for i in random.choices(L, k = k)])

if __name__ == '__main__':
    main()