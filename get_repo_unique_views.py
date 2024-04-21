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
    
    # Check for error messages
    if isinstance(repositories, dict) and repositories.get('message', ''):
        print(repositories['message'])
        return

    # Store unique view data for each repository
    all_unique_views_data = []

    for repo in repositories:
        if repo['name'] == exclude_repo:
            continue  # Skip the specified repository

        views_url = f"https://api.github.com/repos/{username}/{repo['name']}/traffic/views"
        views_response = requests.get(views_url, headers=headers)
        views_data = views_response.json()

        # Check for error messages
        if "message" in views_data:
            print(f"Error fetching views for {repo['name']}: {views_data['message']}")
            continue

        # Sum up unique view counts
        total_unique_views = sum(view['uniques'] for view in views_data.get('views', []))
        all_unique_views_data.append({'Repository': repo['name'], 'Total Unique Views': total_unique_views})

    # Convert to DataFrame
    df = pd.DataFrame(all_unique_views_data)

    # Sort to display repositories with most unique views at the top
    df = df.sort_values(by="Total Unique Views", ascending=False)

    # Plot the bar chart
    plt.figure(figsize=(12, 8))
    bars = plt.bar(df["Repository"], df["Total Unique Views"], color='purple')
    plt.xlabel('Repository')
    plt.ylabel('Total Unique Views')
    plt.title('Total Unique Views per Repository')
    plt.xticks(rotation=90)  # Rotate x-axis labels for readability
    plt.tight_layout()  # Adjust layout to avoid squeezing

    # Add text annotations on each bar for the specific view counts
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center')  # Vertical and horizontal alignment

    plt.savefig('github_visitor.png')

# Example usage, replace 'username', 'token', and the repository to exclude
get_all_repos_unique_views('weitsunglin', api_key, exclude_repo='weitsunglin')
