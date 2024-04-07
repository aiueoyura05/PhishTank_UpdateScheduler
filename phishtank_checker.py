import requests
import pandas as pd
import schedule
import time

# CSVファイルのパス
csv_file_path = '1st_verify.csv'

def download_json_data():
    url = "http://data.phishtank.com/data/online-valid.json"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # JSONデータから'url'を抽出
        urls = [item['url'] for item in data][:200]
        return urls
    else:
        print(f"Failed to download JSON data. Status code: {response.status_code}, Response body: {response.text}")
        return None

def update_csv_file(urls):
    try:
        df_existing = pd.read_csv(csv_file_path)
        print("CSV file loaded successfully.")
    except FileNotFoundError:
        df_existing = pd.DataFrame()
        print("no exist")

    # 新しいデータをDataFrameに変換
    df_new = pd.DataFrame(urls, columns=['url'])
    
    # 既存のデータと新しいデータを結合
    df = pd.concat([df_existing, df_new], ignore_index=True)
    
    # 重複を削除
    df = df.drop_duplicates(subset='url')
    
    # 結合したデータをCSVファイルに保存
    df.to_csv(csv_file_path, index=False)
    print("CSV file updated successfully.")

def main():
    urls = download_json_data()
    print("URLs downloaded successfully")
    if urls is not None:
        update_csv_file(urls)

if __name__ == "__main__":
    main()
    schedule.every(1).hour.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)

