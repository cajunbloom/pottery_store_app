import qrcode
from flask import Flask, render_template, request
from escpos.network import Network
import socket

app = Flask(__name__)

# IP address and port of your Wi-Fi receipt printer
printer_ip = '192.168.1.100'  # Replace with your printer's IP address
printer_port = 9100  # Default port for most network printers

# Create a Network printer object
p = Network(socket.gethostname(), port=printer_port, address=printer_ip)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']

        # Generate QR code with prepopulated message
        message = f"Hello {first_name} {last_name}, this is That Paining Spot.Your pottery is available for pick up."

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Use a special URL scheme to prepopulate the SMS message
        sms_url = f'sms:{phone_number}?body={message}'
        qr.add_data(sms_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Print the QR code to the Wi-Fi printer
        p.text("Printing QR Code...\n")
        p.image(qr_img)
        p.text("Printing complete.\n")
        p.cut()

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
