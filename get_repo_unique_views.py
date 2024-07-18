import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

api_key = os.getenv("API_KEY")

def get_all_repos_unique_views(username, token, exclude_repo=None):
    repos_url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {token}"}
    repos_response = requests.get(repos_url, headers=headers)
    repositories = repos_response.json()
    
    if isinstance(repositories, dict) and repositories.get('message', ''):
        print(repositories['message'])
        return

    all_unique_views_data = []

    for repo in repositories:
        if repo['name'] == exclude_repo:
            continue

        views_url = f"https://api.github.com/repos/{username}/{repo['name']}/traffic/views"
        views_response = requests.get(views_url, headers=headers)
        views_data = views_response.json()

        if "message" in views_data:
            print(f"Error fetching views for {repo['name']}: {views_data['message']}")
            continue

        total_unique_views = sum(view['uniques'] for view in views_data.get('views', []))
        all_unique_views_data.append({'Repository': repo['name'], 'Total Unique Views': total_unique_views})

    df = pd.DataFrame(all_unique_views_data)
    df = df.sort_values(by="Total Unique Views", ascending=False).head(10)

    plt.figure(figsize=(5, 8))
    bars = plt.bar(df["Repository"], df["Total Unique Views"], color='purple')
    plt.xlabel('Repository')
    plt.ylabel('Total Unique Views')
    plt.title('Last two week Top 10 Repositories by Total Unique Views')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # 設定y軸只有三個刻度
    max_views = df["Total Unique Views"].max()
    plt.ylim(0, max_views * 1.1)
    plt.yticks([0, max_views // 2, max_views])

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center')

    plt.savefig('github_visitor.png')

# Example usage, replace 'username', 'token', and the repository to exclude
get_all_repos_unique_views('weitsunglin', api_key, exclude_repo='weitsunglin')
