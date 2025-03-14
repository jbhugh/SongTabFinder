import requests

def main():
    print("Hello from SongTabFinder!")
    response = requests.get("https://www.google.com")
    print(f"Response: {response.status_code}")

if __name__ == "__main__":
    main()
