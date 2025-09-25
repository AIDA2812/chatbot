from flask import Flask, request, jsonify, render_template
from nlp_parser import CommandParser
from email_sender import EmailSender
from config import Config

app = Flask(__name__)
command_parser = CommandParser()
email_sender = EmailSender()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/send", methods=["POST"])
def api_send():
    try:
        data = request.get_json(silent=True) or {}
        text = data.get("text", "").strip()
        attachments = data.get("attachments", [])
        
        if not text:
            return jsonify({"ok": False, "error": "No text provided", "parsed": None}), 400
        
        parsed = command_parser.parse_command(text)
        
        if parsed["intent"] != "send_email":
            return jsonify({"ok": False, "error": "No email sending intent detected", "parsed": parsed}), 400
        if not parsed["to"]:
            return jsonify({"ok": False, "error": "No recipient email found", "parsed": parsed}), 400
        
        email_sender.send_email(parsed["to"], parsed["subject"], parsed["body"], attachments)
        return jsonify({"ok": True, "message": "Email sent successfully", "parsed": parsed})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "parsed": parsed if 'parsed' in locals() else None}), 500

if __name__ == "__main__":
    app.run(debug=Config.FLASK_DEBUG, host='0.0.0.0', port=5000)
