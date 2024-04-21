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
    
    # 检查是否有错误信息
    if isinstance(repositories, dict) and repositories.get('message', ''):
        print(repositories['message'])
        return

    # 存储每个存储库的唯一克隆数据
    all_clones_data = []

    for repo in repositories:
        if repo['name'] == exclude_repo:
            continue  # 跳过指定排除的存储库

        clones_url = f"https://api.github.com/repos/{username}/{repo['name']}/traffic/clones"
        clones_response = requests.get(clones_url, headers=headers)
        clones_data = clones_response.json()

        # 检查是否有错误信息
        if "message" in clones_data:
            print(f"Error fetching clones for {repo['name']}: {clones_data['message']}")
            continue

        # 累加唯一克隆计数
        total_unique_clones = sum(clone['uniques'] for clone in clones_data.get('clones', []))
        all_clones_data.append({'Repository': repo['name'], 'Unique Clones': total_unique_clones})

    # 转换成 DataFrame
    df = pd.DataFrame(all_clones_data)

    # 排序以显示最多唯一克隆的存储库在前
    df = df.sort_values(by="Unique Clones", ascending=False)

    # 绘制直条图
    plt.figure(figsize=(12, 8))
    bars = plt.bar(df["Repository"], df["Unique Clones"], color='blue')
    plt.xlabel('Repository')
    plt.ylabel('Unique Clones')
    plt.title('Unique Clones per Repository')
    plt.xticks(rotation=90)  # 旋转 x 轴标签以便阅读
    plt.tight_layout()  # 调整布局以避免挤压

    # 在每个条形上添加文本注释显示具体克隆数
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom')  # va: vertical alignment

    plt.savefig('github_clone_counts.png')

# Example usage with a placeholder token and username
# Replace 'username' and 'token' with your actual GitHub username and token
# Replace 'weitsunglin' with the repository you want to exclude
get_all_repos_unique_clones('username', api_key, exclude_repo='weitsunglin')
