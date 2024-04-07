import requests
import pandas as pd

csv = pd.read_csv('1st_verify_online.csv')

def download_json_data():
    url = "http://data.phishtank.com/data/online-valid.json"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # JSONデータから'url'を抽出
        urls = [item['url'] for item in data][:200]
        return urls
    else:
        print("Failed to download JSON data.")
        return None

# Call the function to get the list of URLs
urls = download_json_data()

# Check if the function returned a list of URLs
if urls is not None:
    # Convert the list of URLs into a DataFrame
    df = pd.DataFrame(urls, columns=['url'])
    
    # Save the DataFrame to a new CSV file
    df.to_csv('extracted_urls.csv', index=False)
    print("URLs saved to extracted_urls.csv")
else:
    print("No URLs were extracted.")
