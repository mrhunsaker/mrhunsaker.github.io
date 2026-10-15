import os
import requests


def get_github_pages_sites(username):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    # RECOMMENDED: Run 'export GITHUB_TOKEN="your_token"' in your terminal before running
    # Or paste your token directly here if needed
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # Try regular user endpoint
    user_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    print(f"Checking user endpoint: {user_url}...")
    response = requests.get(user_url, headers=headers)

    # Fallback to org endpoint if 404
    if response.status_code == 404:
        org_url = f"https://api.github.com/orgs/{username}/repos?per_page=100"
        print(f"User not found. Trying organization endpoint: {org_url}...")
        response = requests.get(org_url, headers=headers)

    # Detailed Error Diagnosis
    if response.status_code != 200:
        print(f"\n--- API Failure Diagnosis ---")
        print(f"HTTP Status Code returned: {response.status_code}")
        try:
            print(f"GitHub Message: {response.json().get('message')}")
        except Exception:
            print(f"Raw Response: {response.text[:200]}")
        print(
            "\nTip: If the account is valid, try creating a classic Personal Access Token"
        )
        print(
            "on GitHub (no scopes needed for public data) and run: export GITHUB_TOKEN='your_token'"
        )
        return

    repos = response.json()
    pages_sites = []

    for repo in repos:
        if repo.get("has_pages"):
            repo_name = repo["name"]
            if repo_name.lower() == f"{username.lower()}.github.io":
                site_url = f"https://{username.lower()}.github.io/"
            else:
                site_url = f"https://{username.lower()}.github.io/{repo_name}/"
            pages_sites.append((repo_name, site_url))

    if pages_sites:
        print(
            f"\nSuccess! Found {len(pages_sites)} GitHub Pages site(s) for {username}:\n"
        )
        for name, link in pages_sites:
            print(f"- {name}: {link}")
    else:
        print(f"\nNo active GitHub Pages sites found for account: {username}")


if __name__ == "__main__":
    get_github_pages_sites("mrhunsaker")
