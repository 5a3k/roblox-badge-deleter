import requests
import json

with open("config.json", "r") as file:
    data = json.load(file)

cookies = {
    ".ROBLOSECURITY": data.get("cookie"),
}

csrf_token = requests.post("https://auth.roblox.com/v2/logout", cookies=cookies).headers['X-CSRF-TOKEN']

headers = {
    "x-csrf-token": csrf_token,
}

def get_user_id():
    response = requests.get("https://users.roblox.com/v1/users/authenticated", cookies=cookies, headers=headers)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        raise Exception("Failed to retrieve user ID. Check your .ROBLOSECURITY cookie.")

def get_badges(user_id):
    badges = []
    next_page_cursor = ""
    while True:
        response = requests.get(
            f"https://badges.roblox.com/v1/users/{user_id}/badges",
            params={"limit": 100, "sortOrder": "Asc", "cursor": next_page_cursor},
            cookies=cookies,
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            badges.extend(data["data"])
            next_page_cursor = data.get("nextPageCursor", "")
            if not next_page_cursor:
                break
        else:
            raise Exception("Failed to fetch badges.")
    return badges

def delete_badge(badge_id):
    response = requests.delete(f"https://badges.roblox.com/v1/user/badges/{badge_id}", cookies=cookies, headers=headers)
    if response.status_code == 200:
        print(f"Deleted badge {badge_id}")
    else:
        print(f"Failed to delete badge {badge_id}: {response.status_code}")

def delete_all_badges():
    try:
        user_id = get_user_id()
        print(f"User ID: {user_id}")
        
        badges = get_badges(user_id)
        print(f"Found {len(badges)} badges.")

        for badge in badges:
            badge_id = badge["id"]
            delete_badge(badge_id)
        
        print("All badges deleted.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

delete_all_badges()
