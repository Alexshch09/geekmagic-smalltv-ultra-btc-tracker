import requests
import time
from PIL import Image, ImageDraw, ImageFont

# Function to download and open the Bitcoin image
def download_bitcoin_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open('bitcoin_logo.png', 'wb') as file:
            file.write(response.content)
        return Image.open('bitcoin_logo.png')
    else:
        print("Error downloading the Bitcoin image.")
        return None

# Function to get the current Bitcoin price without decimal part
def get_bitcoin_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        bitcoin_price = data['bpi']['USD']['rate']
        # Remove decimal part
        bitcoin_price = bitcoin_price.split('.')[0]
        return bitcoin_price
    else:
        print("Error fetching Bitcoin price.")
        return None

# Function to create an image with a blue background and Bitcoin price text
def create_blue_image(width, height, text, logo):
    image = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
    
    # Combine logo with text
    image.paste(logo, (60, 20))
    draw.text((45, 170), text, fill="white", font=font)
    return image

# Function to save the image to disk
def save_image(image, filename):
    image.save(filename)

# Function to upload the image to the device
def upload_image_to_device(filename):
    url = "http://192.168.0.123/doUpload?dir=/image/"
    with open(filename, 'rb') as file:
        files = {'file': ('image.jpg', file, 'image/jpeg')}
        response = requests.post(url, files=files)
    if response.status_code == 200:
        print("Image successfully uploaded to the device.")
    else:
        print("Error uploading the image to the device.")
        print(response.status_code)

# Function to set the image on the device
def set_image_on_device(image_name):
    url = f"http://192.168.0.123/set?img=%2Fimage%2F{image_name}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Image successfully set on the device.")
    else:
        print("Error setting the image on the device.")

def main():
    # Image parameters
    image_width = 240
    image_height = 240
    image_filename = "image.jpg"
    bitcoin_logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/128px-Bitcoin.svg.png"

    # Download Bitcoin logo
    bitcoin_logo = download_bitcoin_image(bitcoin_logo_url)
    if bitcoin_logo is None:
        return

    while True:
        # Get the current Bitcoin price
        bitcoin_price = get_bitcoin_price()
        if bitcoin_price is None:
            time.sleep(10)
            continue

        # Create an image with the Bitcoin price
        text = f"${bitcoin_price}"
        blue_image = create_blue_image(image_width, image_height, text, bitcoin_logo)

        # Save the image to disk
        save_image(blue_image, image_filename)

        # Upload the image to the device
        upload_image_to_device(image_filename)

        # Set the image on the device
        set_image_on_device(image_filename)

        # Wait for a while before updating the image
        time.sleep(10)

if __name__ == "__main__":
    main()
