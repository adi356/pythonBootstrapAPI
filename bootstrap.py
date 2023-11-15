import requests
import csv
import certifi

# Github API URL
url = "https://api.github.com/repos/twbs/bootstrap/releases"

# setting CA certificate path for SSL verification
ca_bundle_path = certifi.where()

# Create GET request
response = requests.get(url, verify=ca_bundle_path)

if response.status_code == 200:
    releases = response.json()
    
    # Add CSV file info
    fields = ['Created Date', 'Tag name', 'URL for the distribution zip file']
    filename = 'bootstrap_releases.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        
        for release in releases:
            created_date = release['created_at']
            tag_name = release['tag_name']
            
            assets = release['assets']
            zip_url = next((asset['browser_download_url'] for asset in assets if asset['name'].endswith('.zip')), None)
            
            writer.writerow({
                'Created Date': created_date,
                'Tag name': tag_name,
                'URL for the distribution zip file': zip_url
            })

    print(f"Successfully created '{filename}' with Bootstrap releases.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")