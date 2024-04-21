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
    
    # 检查是否有错误信息
    if isinstance(repositories, dict) and repositories.get('message', ''):
        print(repositories['message'])
        return

    # 存储每个存储库的唯一视图数据
    all_unique_views_data = []

    for repo in repositories:
        if repo['name'] == exclude_repo:
            continue  # 跳过指定排除的存储库

        views_url = f"https://api.github.com/repos/{username}/{repo['name']}/traffic/views"
        views_response = requests.get(views_url, headers=headers)
        views_data = views_response.json()

        # 检查是否有错误信息
        if "message" in views_data:
            print(f"Error fetching views for {repo['name']}: {views_data['message']}")
            continue

        # 累加唯一视图数
        total_unique_views = sum(view['uniques'] for view in views_data.get('views', []))
        all_unique_views_data.append({'Repository': repo['name'], 'Total Unique Views': total_unique_views})

    # 转换成 DataFrame
    df = pd.DataFrame(all_unique_views_data)

    # 排序以显示最多唯一视图的存储库在前
    df = df.sort_values(by="Total Unique Views", ascending=False)

    # 绘制直条图
    plt.figure(figsize=(12, 8))
    plt.bar(df["Repository"], df["Total Unique Views"], color='purple')
    plt.xlabel('Repository')
    plt.ylabel('Total Unique Views')
    plt.title('Total Unique Views per Repository')
    plt.xticks(rotation=90)  # 旋转 x 轴标签以便阅读
    plt.tight_layout()  # 调整布局以避免挤压
    plt.savefig('github_visitor.png')

# 使用示例，需替换用户名、token及需要排除的仓库名称
get_all_repos_unique_views('username', api_key, exclude_repo='weitsunglin')
