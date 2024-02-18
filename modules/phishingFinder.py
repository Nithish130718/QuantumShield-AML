import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_html_content(url):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Parse the HTML content
    # soup = BeautifulSoup(response.text, 'html.parser')

    # Extract text content
    text_content = response.text  # soup.get_text()

    # Print or do whatever you want with the text content
    print(text_content)


def validate_url(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ("http", "https"):
            return False
        return True
    except:
        return False


def check_encryption(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            if response.url.startswith("https"):
                return True
        return False
    except:
        return False


def is_safe_to_use(url):
    try:
        response = requests.head(url)
        if response.status_code == 200:
            if response.url.startswith("https"):
                # print("Website uses HTTPS and encryption.")
                return True
                # print("Website does not use HTTPS. Proceed with caution.")
        else:
            print("Error: Unable to access the website.")
    except Exception as e:
        print("Error:", e)
    return False


def check_ssl_certificate(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.url.startswith("https")
        else:
            print(
                "Error: Unable to access the website. Status code:",
                response.status_code,
            )
    except Exception as e:
        print("Error:", e)
    return False


# Example usage
url = input("Enter URL to be tested: ")

print("URL: ", url)
# get_html_content(url)

count = 0
flag = True
if validate_url(url):
    print("URL is valid.")
    count += 1
else:
    print("URL is not valid.")
    flag = False

if check_ssl_certificate(url):
    print("SSL certificate is valid.")
    count += 2
else:
    print("SSL certificate is invalid or missing.")
    flag = False

if check_encryption(url):
    print("Website uses HTTPS and encryption.")
    count += 1
else:
    print("Website does not use HTTPS or encryption.")
    flag = False

if is_safe_to_use(url):
    print("It appears safe to use.")
    count += 1
else:
    print("Exercise caution when using this website.")
    flag = False
print()
if flag:
    print("The website is completely safe to use!")
else:
    print("Please be cautious while using the website!!")

print("\nSafety Confidence: ", (count / 5) * 100, "%", sep="")
