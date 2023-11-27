from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import requests
import io
from PIL import Image, ImageOps
import base64


app = Flask(__name__)

API_URL = "https://xdwvg9no7pefghrn.us-east-1.aws.endpoints.huggingface.cloud"
API_KEY = "VknySbLLTUjbxXAXCjyfaFIPwUTCeRXbFSOjwRiCxsxFyhbnGjSFalPKrpvvDAaPVzWEevPljilLVDBiTzfIbWFdxOkYJxnOPoHhkkVGzAknaOulWggusSFewzpqsNWM"

headers = {
    "Accept": "image/png",
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()

        # Replace the placeholders with your email server details
        smtp_server = 'smtp.gmail.com'
        smtp_port = 465 
        smtp_username = 'xyz.bank.35@gmail.com' #change email address
        smtp_password = ''#update deive specific password for your email address

        from_address = smtp_username
        to_address = data['email']

        subject = 'Comic Strip'
        body = 'Check out this awesome comic!'

        # Create the MIME object
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach the image
        image_data = data['image'].split(',')[1]  # Remove the data:image/png;base64, prefix
        image_attachment = MIMEImage(base64.b64decode(image_data), name='comic.png')
        msg.attach(image_attachment)

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(from_address, to_address, msg.as_string())

        return jsonify({'message': 'Email sent successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_comic', methods=['POST'])
def generate_comic():
    try:
        #reading text from web page
        text_inputs = [request.form[f'text_{i+1}'] for i in range(10)]
        
        images = []
        #adding images to the list
        for i, text_input in enumerate(text_inputs):
            image_bytes = query({"inputs": text_input})
            image = Image.open(io.BytesIO(image_bytes))
            image = ImageOps.expand(image, border=(4, 4), fill='black')#adding border to the image
            images.append(image)


        # Get the dimensions of the images
        width, height = images[0].size

        # Create a blank image for the comic strip
        comic_strip = Image.new('RGB', (width * 5, height * 2))

        # Paste the first 5 images in the first row
        for i in range(5):
            comic_strip.paste(images[i], (width * i, 0))

        # Paste the next 5 images in the second row
        for i in range(5):
            comic_strip.paste(images[i + 5], (width * i, height))

        # Save the final comic strip
        comic_strip = ImageOps.expand(comic_strip, border=(4, 4), fill='black')
        data = io.BytesIO()
        comic_strip.save(data, "PNG")
        encoded_img_data = base64.b64encode(data.getvalue())
        # Optionally, you can redirect to a success page
        return render_template("results.html", img_data=encoded_img_data.decode('utf-8'))
        
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "An error occurred while generating the comic.", 500

if __name__ == "__main__":
    app.run(debug=True)
