import os
import uuid
import qrcode
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.get_json()
    seller_id = data.get("seller_id")

    # UUID生成
    ticket_id = str(uuid.uuid4())

    # QRコード生成（Pillow不要）
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(ticket_id)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # static フォルダに保存
    img_path = f"static/{ticket_id}.png"
    img.save(img_path)

    return jsonify({
        "ticket_id": ticket_id,
        "seller_id": seller_id,
        "qr_url": img_path
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
