from flask import Flask, request, jsonify
import qrcode
import uuid
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "MatchPoint API is running"

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.get_json()
    seller_id = data.get("seller_id")

    ticket_id = str(uuid.uuid4())

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(ticket_id)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # static の絶対パスで保存（Render でも確実に動く）
    save_path = os.path.join(app.static_folder, f"{ticket_id}.png")
    img.save(save_path)

    return jsonify({
        "ticket_id": ticket_id,
        "seller_id": seller_id,
        "qr_url": f"static/{ticket_id}.png"
    })

if __name__ == "__main__":
    app.run()
