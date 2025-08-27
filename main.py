from flask import Flask
import threading
import time
import requests
import random
import json

app = Flask(__name__)

# ========== إعدادات عامة ==========
CHANNEL_ID     = -1002752110921
INVITE_LINK    = "https://t.me/+YdnoVKBDrmAyY2Ex"
REQUEST_TIMEOUT = 0.5    # timeout لكل طلب HTTP
POLL_TIMEOUT    = 0.5    # timeout للـ getUpdates long polling
LOOP_DELAY      = 0.05   # تأخير حلقة البولينج

# قائمة توكنات البوتات الرئيسية
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

# توكنات البوتات الجانبي و Swap
SIDE_BOT_TOKEN = "8293938962:AAG0Rvs5FcLKdc_Una6iki3KZ9inkUXFfjw"
SWAPBOT_TOKEN  = "7445027136:AAE_xmaBcrtlUTauZEjagqXsvbGd3Vyng9w"

# قائمة الإيموجيات للتفاعل
EMOJIS       = ["❤️", "👍", "🤩", "🔥"]
# كل البوتات التي ستتفاعل
REACTOR_BOTS = BOT_TOKENS + [SIDE_BOT_TOKEN, SWAPBOT_TOKEN]


# ------------------ دوال مساعدة HTTP ------------------
def send_request(method, url, json_data=None, params=None):
    """ تنفّذ get أو post مع timeout ثابت وتُعيد JSON أو {} """
    try:
        if method == "get":
            return requests.get(url, params=params, timeout=REQUEST_TIMEOUT).json()
        else:  # post
            return requests.post(url, json=json_data, timeout=REQUEST_TIMEOUT).json()
    except:
        return {}

# ========== الجزء 1: بوتات رئيسية ==========
def run_bot(token):
    base = f"https://api.telegram.org/bot{token}"

    def is_subscribed(user_id):
        data = send_request("get", f"{base}/getChatMember",
                            params={"chat_id": CHANNEL_ID, "user_id": user_id})
        status = data.get("result", {}).get("status", "")
        return status in ("member", "administrator", "creator")

    def send_message(chat_id, text, reply_to=None, reply_markup=None):
        payload = {"chat_id": chat_id, "text": text}
        if reply_to:      payload["reply_to_message_id"] = reply_to
        if reply_markup:  payload["reply_markup"]       = reply_markup
        send_request("post", f"{base}/sendMessage", json_data=payload)

    def send_photo(chat_id, photo_url, caption, reply_markup=None):
        payload = {
            "chat_id":   chat_id,
            "photo":     photo_url,
            "caption":   caption,
            "parse_mode":"HTML"
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        send_request("post", f"{base}/sendPhoto", json_data=payload)

    def poll_updates():
        last_off = None
        print(f"✅ بوت رئيسي [{token[:8]}...] جاري العمل")
        while True:
            res = send_request("get", f"{base}/getUpdates",
                               params={"timeout": POLL_TIMEOUT, "offset": last_off})
            for upd in res.get("result", []):
                last_off = upd["update_id"] + 1
                msg = upd.get("message")
                if not msg or "text" not in msg:
                    continue

                chat_id = msg["chat"]["id"]
                text    = msg["text"]
                usr_id  = msg["from"]["id"]
                msg_id  = msg["message_id"]

                if text == "/start":
                    send_message(chat_id, "🔥", reply_to=msg_id)
                    if is_subscribed(usr_id):
                        photo = "https://i.postimg.cc/KvSKKLZW/E3-B52-A70-FBEA-47-BA-8615-B346-AABFBBDC.jpg"
                        cap = """
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
اقوى ثلاث روابــط ميـقا حصريات 🔞
__________________________

رابــط ميـقا 12 الف مقـطـع منوع 🔞🔞 2 تيـرا  
رابــط ميـقا مقاطع مشاهير 🔞🔞 40 قيقا  
رابـط ميـقا ورر3 ـان حصرري 🔞🔞 1 تيرا

((الروابـط مختصـرة)) 🔥🔥🔥
"""
                        kb = {
                            "inline_keyboard": [
                                [{"text":"🔗 رابط 2 تيرا","url":"https://en.shrinke.me/Megaio"}],
                                [{"text":"👑 مشاهير 40 قيقا","url":"https://shrinkme.ink/MeggaLink"}],
                                [{"text":"🎬 حصري 1 تيرا","url":"https://en.shrinke.me/Megaioapp"}]
                            ]
                        }
                        send_photo(chat_id, photo, cap, kb)
                    else:
                        kb = {"inline_keyboard":[[{"text":"🔔 اضغط للاشتراك بالقناة","url":INVITE_LINK}]]}
                        send_message(chat_id, "لازم تشترك في القناة لتستعمل البوت🫶🏻.", reply_markup=kb)
            time.sleep(LOOP_DELAY)

def start_main_bots():
    for tk in BOT_TOKENS:
        threading.Thread(target=run_bot, args=(tk,), daemon=True).start()


# ========== الجزء 2: البوت الجانبي ==========
def run_side_bot():
    base = f"https://api.telegram.org/bot{SIDE_BOT_TOKEN}"
    last_off = None
    print("✅ بوت جانبي جاري العمل")
    while True:
        res = send_request("get", f"{base}/getUpdates",
                           params={"timeout": POLL_TIMEOUT, "offset": last_off})
        for upd in res.get("result", []):
            last_off = upd["update_id"] + 1
            msg = upd.get("message")
            if not msg or "text" not in msg:
                continue

            cid = msg["chat"]["id"]
            text = """اهلًا بك 👋.

- هذا بوت فهرس قنوات وبوتات جاهل 🌟.

- كل يوم انشر روٌآبًطِ و مًقُآطِعٌ بالقناة 🔥‼️.

قناة جـاهـل | Jahil ☟
https://t.me/+YdnoVKBDrmAyY2Ex
"""
            send_request("post", f"{base}/sendMessage",
                         json_data={"chat_id":cid, "text":text, "parse_mode":"HTML"})
        time.sleep(LOOP_DELAY)


# ========== الجزء 3: بوت الـ Swap ==========
# (اضبط timeouts و polling سريع مماثل للأعلى)
def run_swap_bot():
    base    = f"https://api.telegram.org/bot{SWAPBOT_TOKEN}"
    last_off = None

    def is_sub_swap(uid):
        data = send_request("get", f"{base}/getChatMember",
                            params={"chat_id": CHANNEL_ID, "user_id": uid})
        st = data.get("result",{}).get("status","")
        return st in ("member","administrator","creator")

    def handle_message(msg):
        # مثال مبسط: يرد على /start فورياً
        cid  = msg["chat"]["id"]
        txt  = msg.get("text","")
        if txt == "/start":
            send_request("post", f"{base}/sendMessage",
                         json_data={"chat_id":cid,
                                    "text":"مرحبًا، SwapBot شغّال 🚀"})
    print("✅ بوت Swap جاري العمل")
    while True:
        res = send_request("get", f"{base}/getUpdates",
                           params={"timeout": POLL_TIMEOUT, "offset": last_off})
        for upd in res.get("result", []):
            last_off = upd["update_id"] + 1
            if "message" in upd:
                handle_message(upd["message"])
        time.sleep(LOOP_DELAY)


# ========== الجزء 4: تفاعلات البوتات ==========
def send_reaction(token, chat_id, message_id, emoji):
    base = f"https://api.telegram.org/bot{token}"
    send_request("post", f"{base}/sendReaction",
                 json_data={"chat_id":chat_id, "message_id":message_id, "emoji":emoji})

def reaction_worker():
    listener = BOT_TOKENS[0]
    base     = f"https://api.telegram.org/bot{listener}"
    last_off = None
    print("🔁 خدمة التفاعلات التلقائية بدأت")
    while True:
        res = send_request("get", f"{base}/getUpdates",
                           params={"timeout": POLL_TIMEOUT, "offset": last_off})
        for upd in res.get("result", []):
            last_off = upd["update_id"] + 1
            post = upd.get("channel_post")
            if not post:
                continue

            cid = post["chat"]["id"]
            mid = post["message_id"]
            # نختار 1-2-3 بوت عشوائياً
            k = random.choice([1,2,3])
            bots = random.sample(REACTOR_BOTS, k=k)
            for b in bots:
                emo = random.choice(EMOJIS)
                # كل بوت يتفاعل بمفرده في ثريد
                threading.Thread(target=send_reaction,
                                 args=(b, cid, mid, emo),
                                 daemon=True).start()
        time.sleep(LOOP_DELAY)


# ========== نقطة الإنطلاق ==========
@app.route('/')
def home():
    return "بوتاتك الآن تعمل بأقصى سرعة! 🚀"

if __name__ == "__main__":
    # تشغيل البوتات
    start_main_bots()
    threading.Thread(target=run_side_bot, daemon=True).start()
    threading.Thread(target=run_swap_bot, daemon=True).start()
    threading.Thread(target=reaction_worker, daemon=True).start()
    # ويب سيرفر لبقاء العملية حية
    app.run(host='0.0.0.0', port=8080)
