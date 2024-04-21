import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
api_key = os.getenv("API_KEY")

def get_all_repos_unique_views(username, token):
    repos_url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {token}"}
    repos_response = requests.get(repos_url, headers=headers)
    repositories = repos_response.json()
    
    # 檢查是否有錯誤信息
    if isinstance(repositories, dict) and repositories.get('message', ''):
        print(repositories['message'])
        return

    # 存儲每個存儲庫的唯一視圖數據
    all_unique_views_data = []

    for repo in repositories:
        views_url = f"https://api.github.com/repos/{username}/{repo['name']}/traffic/views"
        views_response = requests.get(views_url, headers=headers)
        views_data = views_response.json()

        # 檢查是否有錯誤信息
        if "message" in views_data:
            print(f"Error fetching views for {repo['name']}: {views_data['message']}")
            continue

        # 累加唯一視圖數
        total_unique_views = sum(view['uniques'] for view in views_data.get('views', []))
        all_unique_views_data.append({'Repository': repo['name'], 'Total Unique Views': total_unique_views})

    # 轉換成 DataFrame
    df = pd.DataFrame(all_unique_views_data)

    # 排序以顯示最多唯一視圖的存儲庫在前
    df = df.sort_values(by="Total Unique Views", ascending=False)

    # 繪製直條圖
    plt.figure(figsize=(5, 3))
    plt.bar(df["Repository"], df["Total Unique Views"], color='purple')
    plt.xlabel('Repository')
    plt.ylabel('Total Unique Views')
    plt.title('Total Unique Views per Repository')
    plt.xticks(rotation=90)  # 旋轉 x 軸標籤以便閱讀
    plt.tight_layout()  # 調整布局以避免擠壓
    plt.savefig('github_visitor.png')

# 使用範例，請替換以下資訊
get_all_repos_unique_views('weitsunglin', api_key)
