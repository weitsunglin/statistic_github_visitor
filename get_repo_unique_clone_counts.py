import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
api_key = os.getenv("API_KEY")

def get_all_repos_unique_clones(username, token, exclude_repo=None):
    repos_url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {token}"}
    repos_response = requests.get(repos_url, headers=headers)
    repositories = repos_response.json()
    
    if isinstance(repositories, dict) and repositories.get('message', ''):
        print(repositories['message'])
        return

    all_clones_data = []

    for repo in repositories:
        if repo['name'] == exclude_repo:
            continue

        clones_url = f"https://api.github.com/repos/{username}/{repo['name']}/traffic/clones"
        clones_response = requests.get(clones_url, headers=headers)
        clones_data = clones_response.json()

        if "message" in clones_data:
            print(f"Error fetching clones for {repo['name']}: {clones_data['message']}")
            continue

        total_unique_clones = sum(clone['uniques'] for clone in clones_data.get('clones', []))
        all_clones_data.append({'Repository': repo['name'], 'Unique Clones': total_unique_clones})

    df = pd.DataFrame(all_clones_data)

    # 排序並取前10個有最多Unique Clones的repositories
    df = df.sort_values(by="Unique Clones", ascending=False).head(10)

    plt.figure(figsize=(6, 8))
    bars = plt.bar(df["Repository"], df["Unique Clones"], color='blue')
    plt.xlabel('Repository')
    plt.ylabel('Unique Clones')
    plt.title('Top 10 Repositories by Unique Clones')
    plt.xticks(rotation=90)
    plt.tight_layout()

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom')  # va: vertical alignment
            
    plt.savefig('github_clone_counts.png')

# Example usage with a placeholder token and username
# Replace 'username' and 'token' with your actual GitHub username and token
# Replace 'weitsunglin' with the repository you want to exclude
get_all_repos_unique_clones('weitsunglin', api_key, exclude_repo='weitsunglin')
