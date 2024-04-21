import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
api_key = os.getenv("API_KEY")

def get_all_repos_unique_clones(username, token):
    repos_url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {token}"}
    repos_response = requests.get(repos_url, headers=headers)
    repositories = repos_response.json()
    
    # Check for error messages
    if isinstance(repositories, dict) and repositories.get('message', ''):
        print(repositories['message'])
        return

    # Store clone data for each repository
    all_clones_data = []

    for repo in repositories:
        clones_url = f"https://api.github.com/repos/{username}/{repo['name']}/traffic/clones"
        clones_response = requests.get(clones_url, headers=headers)
        clones_data = clones_response.json()

        # Check for error messages
        if "message" in clones_data:
            print(f"Error fetching clones for {repo['name']}: {clones_data['message']}")
            continue

        # Sum up the unique clone counts
        total_unique_clones = sum(clone['uniques'] for clone in clones_data.get('clones', []))
        all_clones_data.append({'Repository': repo['name'], 'Unique Clones': total_unique_clones})

    # Convert to DataFrame
    df = pd.DataFrame(all_clones_data)

    # Sort to show the repositories with the most unique clones at the top
    df = df.sort_values(by="Unique Clones", ascending=False)

    # Plot the bar chart
    plt.figure(figsize=(5, 3))
    plt.bar(df["Repository"], df["Unique Clones"], color='blue')
    plt.xlabel('Repository')
    plt.ylabel('Unique Clones')
    plt.title('Unique Clones per Repository')
    plt.xticks(rotation=90)  # Rotate x-axis labels for readability
    plt.tight_layout()  # Adjust layout to avoid squeezing
    plt.savefig('github_clone_counts.png')


# Example usage with a placeholder token and username
# Replace 'username' and 'token' with your actual GitHub username and token
get_all_repos_unique_clones('weitsunglin', api_key)
