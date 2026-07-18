import os
import requests
import zipfile

def download_data():
    print("📥 Downloading GTD dataset...")
    
    try:
        # Try direct download
        url = "https://github.com/START-UMD/gtd/raw/master/gtd_71to18.csv.zip"
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open("data/data.zip", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print("📦 Extracting...")
            with zipfile.ZipFile("data/data.zip", 'r') as zip_ref:
                zip_ref.extractall("data/")
            os.remove("data/data.zip")
            print("✅ Dataset downloaded successfully!")
            return True
        else:
            print(f"❌ Download failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    download_data()