import os
import uuid
import qrcode
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- トップページ ---
@app.route("/")
def index():
    return render_template("index.html")

# --- QR発行API ---
@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.get_json()
    seller_id = data.get("seller_id")

    # UUID生成
    ticket_id = str(uuid.uuid4())

    # QRコード生成
    img = qrcode.make(ticket_id)
    img_path = f"static/{ticket_id}.png"
    img.save(img_path)

    return jsonify({
        "ticket_id": ticket_id,
        "seller_id": seller_id,
        "qr_url": img_path
    })

# --- Render用起動設定 ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
