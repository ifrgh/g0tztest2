from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

# إعدادات القناة
CHANNEL_ID = -1002752110921
INVITE_LINK = "https://t.me/+YdnoVKBDrmAyY2Ex"

BOT_TOKENS = [
    "7571433385:AAFvadyJycOn5225XuQf8VKc2kmAqryE_-Q",
    "8441633566:AAEUkexMZu37xiabBWou1pbz01_sLTuWoOE",
    "8452340139:AAH01-D6sgPTSAmYOPaDzWFsfy7a0Le38nk",
    "8493548100:AAGnjxcWO5JibaKe4cyxYEvhcMHL3VxhghE",
    "7985937436:AAFCZi1aABdnteYg6O1zmAbK7IWxc6y69lM",
    "8218599803:AAFX-EYpZOvRM5eZPZtaK9OGsrjUDQM3W04",
    "7608840260:AAG6FaDpK4etvzGK3yTUQ053nlRq7uHmPNw",
    "8345480045:AAGanpCB_MJjnJtNJNmcZPvE-pNvPovwjPM",
    "8384924383:AAF_yAeKh_2z_kkmG7LzhNba40eTtg32mPY",
    "8160383787:AAE4xCU1O-rAi2KiboztmBGGkV8-1oPGKyw",
    "8112951576:AAEIJODtWhv8yelKJjYMcmPeXDVQFAo5xY",
    "8268966159:AAEkW7gLghP7I_9bFFm1n4OJhbItOEjKkcQ",
    "7929665367:AAHCindnzXmk-HEX6VXqlFavDVG_kScZB2s",
    "8369928062:AAGI4zg4yPMmUhDtNPuHwThVGhyKPrNpSfw",
    "8407391641:AAHZt_XeNfjQd1tyzlx21xQ29eF7Vht9ivQ",
    "8477718083:AAE7t_zyWsg_-m6paSawcmp-_uGiO0MAFZs"
]

def run_bot(BOT_TOKEN):
    BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

    def is_subscribed(user_id):
        url = f"{BASE_URL}/getChatMember"
        params = {"chat_id": CHANNEL_ID, "user_id": user_id}
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            if data.get("ok"):
                status = data["result"]["status"]
                return status in ["member", "administrator", "creator"]
            else:
                return False
        except Exception as e:
            print(f"[{BOT_TOKEN[:8]}...] خطأ بالتحقق من الاشتراك:", e)
            return False

    def send_message(chat_id, text, reply_markup=None, reply_to_message_id=None):
        url = f"{BASE_URL}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"[{BOT_TOKEN[:8]}...] خطأ بالإرسال:", e)

    def send_photo(chat_id, photo_url, caption, reply_markup=None):
        url = f"{BASE_URL}/sendPhoto"
        payload = {
            "chat_id": chat_id,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": "HTML"
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"[{BOT_TOKEN[:8]}...] خطأ بإرسال الصورة:", e)

    def get_updates(offset=None):
        url = f"{BASE_URL}/getUpdates"
        params = {"timeout": 5}
        if offset:
            params["offset"] = offset
        try:
            response = requests.get(url, params=params, timeout=10)
            return response.json()
        except Exception as e:
            print(f"[{BOT_TOKEN[:8]}...] خطأ بجلب التحديثات:", e)
            return {"ok": False}

    def main():
        print(f"✅ تم تشغيل البوت: {BOT_TOKEN[:10]}...")
        last_update_id = None

        while True:
            try:
                updates = get_updates(last_update_id)
                if not updates.get("ok"):
                    time.sleep(3)
                    continue

                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1

                    message = update.get("message")
                    if not message or "text" not in message:
                        continue

                    text = message.get("text")
                    chat_id = message["chat"]["id"]
                    user_id = message["from"]["id"]
                    message_id = message["message_id"]

                    if text == "/start":
                        send_message(chat_id, "🔥", reply_to_message_id=message_id)

                        if is_subscribed(user_id):
                            photo_url = "https://i.postimg.cc/KvSKKLZW/E3-B52-A70-FBEA-47-BA-8615-B346-AABFBBDC.jpg"
                            caption = """
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
اقوى ثلاث روابــط ميـقا حصريات 🔞
__________________________

رابــط ميـقا 12 الف مقـطـع منوع 🔞🔞 2 تيـرا  
رابــط ميـقا مقاطع مشاهير 🔞🔞 40 قيقا  
رابـط ميـقا ورر3 ـان حصرري 🔞🔞 1 تيرا

((الروابـط مختصـرة)) 🔥🔥🔥
"""
                            keyboard = {
                                "inline_keyboard": [
                                    [{"text": "🔗 رابط 2 تيرا", "url": "https://en.shrinke.me/Megaio"}],
                                    [{"text": "👑 مشاهير 40 قيقا", "url": "https://shrinkme.ink/MeggaLink"}],
                                    [{"text": "🎬 حصري 1 تيرا", "url": "https://en.shrinke.me/Megaioapp"}]
                                ]
                            }
                            send_photo(chat_id, photo_url, caption, keyboard)
                        else:
                            keyboard = {
                                "inline_keyboard": [
                                    [{"text": "🔔 اضغط للاشتراك بالقناة", "url": INVITE_LINK}]
                                ]
                            }
                            send_message(chat_id, "لازم تشترك في القناة لتستعمل البوت🫶🏻.", reply_markup=keyboard)

            except Exception as e:
                print(f"[{BOT_TOKEN[:8]}...] خطأ في الحلقة الرئيسية:", e)
                time.sleep(5)

    main()

def start_bots():
    for token in BOT_TOKENS:
        threading.Thread(target=run_bot, args=(token,), daemon=True).start()

@app.route('/')
def home():
    return "بوتاتك شغالة تمام! 🚀"

if __name__ == "__main__":
    start_bots()
    app.run(host='0.0.0.0', port=8080)
