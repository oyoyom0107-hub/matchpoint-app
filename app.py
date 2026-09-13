from flask import Flask, request, jsonify, send_file
import qrcode
import uuid
import os

# .env を読み込む
from dotenv import load_dotenv
load_dotenv()

# Supabase クライアント（Anon Key を使う）
from supabase import create_client

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_ANON_KEY")   # ← ここだけでOK
)

app = Flask(__name__)

# Supabase 接続テスト
print(supabase.table("tickets").select("*").execute())

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

    # Render 本番環境で唯一書き込み可能な /tmp に保存
    save_path = f"/tmp/{ticket_id}.png"
    img.save(save_path)

    return jsonify({
        "ticket_id": ticket_id,
        "seller_id": seller_id,
        "qr_url": f"/qr/{ticket_id}.png"
    })

@app.route("/qr/<filename>")
def get_qr(filename):
    return send_file(f"/tmp/{filename}", mimetype="image/png")

if __name__ == "__main__":
    app.run()
