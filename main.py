from flask import Flask
import threading
import time
import requests
import random
import json

app = Flask(__name__)

# ===================== البوتات الرئيسية =====================
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
    BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

    def is_subscribed(uid):
        try:
            r = requests.get(
                f"{BASE}/getChatMember",
                params={"chat_id": CHANNEL_ID, "user_id": uid},
                timeout=1
            ).json()
            st = r.get("result", {}).get("status", "")
            return st in ("member", "administrator", "creator")
        except:
            return False

    def send_message(cid, txt, markup=None, reply_to=None):
        payload = {"chat_id": cid, "text": txt}
        if markup: payload["reply_markup"] = markup
        if reply_to: payload["reply_to_message_id"] = reply_to
        requests.post(f"{BASE}/sendMessage", json=payload, timeout=1)

    def send_photo(cid, url, cap, markup=None):
        payload = {
            "chat_id": cid,
            "photo": url,
            "caption": cap,
            "parse_mode": "HTML"
        }
        if markup: payload["reply_markup"] = markup
        requests.post(f"{BASE}/sendPhoto", json=payload, timeout=1)

    def get_updates(offset=None):
        params = {"timeout": 1}
        if offset: params["offset"] = offset
        try:
            return requests.get(f"{BASE}/getUpdates", params=params, timeout=2).json()
        except:
            return {"ok": False}

    print(f"✅ بوت رئيسي شغّال: {BOT_TOKEN[:10]}...")
    last_id = None
    while True:
        upd = get_updates(last_id)
        if upd.get("ok"):
            for u in upd["result"]:
                last_id = u["update_id"] + 1
                msg = u.get("message")
                if not msg or "text" not in msg:
                    continue

                txt = msg["text"]
                cid = msg["chat"]["id"]
                uid = msg["from"]["id"]
                mid = msg["message_id"]

                if txt == "/start":
                    send_message(cid, "🔥", reply_to=mid)
                    if is_subscribed(uid):
                        photo = "https://i.postimg.cc/KvSKKLZW/E3-B52-A70-FBEA-47-BA-8615-B346-AABFBBDC.jpg"
                        caption = """
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
                                [{"text": "🔗 رابط 2 تيرا", "url": "https://en.shrinke.me/Megaio"}],
                                [{"text": "👑 مشاهير 40 قيقا", "url": "https://shrinkme.ink/MeggaLink"}],
                                [{"text": "🎬 حصري 1 تيرا", "url": "https://en.shrinke.me/Megaioapp"}]
                            ]
                        }
                        send_photo(cid, photo, caption, kb)
                    else:
                        kb = {
                            "inline_keyboard": [
                                [{"text": "🔔 اضغط للاشتراك بالقناة", "url": INVITE_LINK}]
                            ]
                        }
                        send_message(cid, "لازم تشترك في القناة لتستعمل البوت🫶🏻.", markup=kb)
        time.sleep(0.5)

def start_bots():
    for t in BOT_TOKENS:
        threading.Thread(target=run_bot, args=(t,), daemon=True).start()

@app.route('/')
def home():
    return "بوتاتك شغالة تمام! 🚀"

# ===================== البوت الجانبي =====================
SIDE_BOT_TOKEN = "8293938962:AAG0Rvs5FcLKdc_Una6iki3KZ9inkUXFfjw"

def run_side_bot():
    BASE = f"https://api.telegram.org/bot{SIDE_BOT_TOKEN}"

    def send_message(cid, txt, markup=None):
        payload = {"chat_id": cid, "text": txt, "parse_mode": "HTML"}
        if markup: payload["reply_markup"] = markup
        requests.post(f"{BASE}/sendMessage", json=payload, timeout=1)

    def get_updates(offset=None):
        params = {"timeout": 1}
        if offset: params["offset"] = offset
        try:
            return requests.get(f"{BASE}/getUpdates", params=params, timeout=2).json()
        except:
            return {"ok": False}

    last_id = None
    print("✅ بوت جانبي شغّال")
    while True:
        upd = get_updates(last_id)
        if upd.get("ok"):
            for u in upd["result"]:
                last_id = u["update_id"] + 1
                msg = u.get("message")
                if not msg or "text" not in msg:
                    continue
                cid = msg["chat"]["id"]
                text = """اهلًا بك 👋.

- هذا بوت فهرس قنوات وبوتات جاهل 🌟.

- كل يوم انشر روٌآبًطِ و مًقُآطِعٌ بالقناة 🔥‼️.

هنا ازرار //

قناة جـاهـل | Jahil
https://t.me/+YdnoVKBDrmAyY2Ex

بوت روٌآبًطِ مًيَيَقُآ
@JahilMegaBot

بوت تبادل مقاطع ، وسيط
@SwapJahil_Bot
"""
                kb = {
                    "inline_keyboard": [
                        [{"text": "قناة جـاهـل | Jahil", "url": "https://t.me/+YdnoVKBDrmAyY2Ex"}],
                        [{"text": "بوت روٌآبًطِ مًيَيَقُآ", "url": "https://t.me/JahilMegaBot"}],
                        [{"text": "بوت تبادل مقاطع ، وسيط", "url": "https://t.me/SwapJahil_Bot"}]
                    ]
                }
                send_message(cid, text, markup=kb)
        time.sleep(0.5)

# ===================== البوت swapbot =====================
SWAPBOT_TOKEN       = "7445027136:AAE_xmaBcrtlUTauZEjagqXsvbGd3Vyng9w"
API_URL_SWAP        = f"https://api.telegram.org/bot{SWAPBOT_TOKEN}"
SUB_CHANNEL_ID      = "-1002752110921"
CONTENT_CHANNEL_ID  = "-1003088252599"
SESSION_TIMEOUT     = 3600
GROUP_TIMEOUT       = 0.5
GET_UPDATES_TIMEOUT = 1

sessions    = {}
user_states = {}
known_users = {}
buffers     = {}

subscription_text = (
    "🚸| عذرًا عزيزي..\n"
    "🔰| عليك الاشتراك في قناة البوت لتتمكن من استخدامه\n\n"
    "- https://t.me/+SSmUDrm7HA5jNjgx\n\n"
    "‼️| اشترك ثم ارسل /start"
)

def is_subscribed_swap(uid):
    try:
        r = requests.get(
            f"{API_URL_SWAP}/getChatMember",
            params={"chat_id": SUB_CHANNEL_ID, "user_id": uid},
            timeout=1
        ).json()
        st = r.get("result", {}).get("status", "")
        return st in ("member", "administrator", "creator")
    except:
        return False

def get_updates_swap(offset=None):
    params = {"timeout": GET_UPDATES_TIMEOUT}
    if offset: params["offset"] = offset
    try:
        return requests.get(f"{API_URL_SWAP}/getUpdates", params=params, timeout=2).json().get("result", [])
    except:
        return []

def send_message_swap(cid, txt, parse_mode="Markdown", markup=None):
    data = {"chat_id": cid, "text": txt, "parse_mode": parse_mode}
    if markup: data["reply_markup"] = json.dumps(markup)
    requests.post(f"{API_URL_SWAP}/sendMessage", data=data, timeout=1)

def forward_message_swap(to_c, from_c, mid):
    d = {"chat_id": to_c, "from_chat_id": from_c, "message_id": mid}
    requests.post(f"{API_URL_SWAP}/forwardMessage", data=d, timeout=1)

def parse_message_content(msg):
    if "photo" in msg:
        p = msg["photo"][-1]
        return p["file_id"], "صورة", p.get("file_size", 0)
    if "video" in msg:
        v = msg["video"]
        return v["file_id"], "فيديو", v.get("file_size", 0)
    if "document" in msg:
        d = msg["document"]
        return d["file_id"], "ملف", d.get("file_size", 0)
    return None, None, 0

def format_size(b):
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.2f} KB"
    if b < 1024**3: return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

def generate_session_id():
    return "".join(str(random.randint(0,9)) for _ in range(8))

def cleanup_sessions_and_buffers():
    now = time.time()
    expired = [sid for sid, s in sessions.items() if now - s["created_at"] > SESSION_TIMEOUT]
    for sid in expired:
        sess = sessions.pop(sid)
        for side in ("user1", "user2"):
            if side in sess:
                send_message_swap(sess[side]["id"], f"⌛ انتهت صلاحية الجلسة {sid}.")
                user_states.pop(sess[side]["id"], None)
    to_proc = [k for k, buf in buffers.items() if now - buf["last_ts"] >= GROUP_TIMEOUT]
    for key in to_proc:
        buf = buffers.pop(key)
        cid, _ = key
        sid    = buf["session_id"]
        st     = user_states.get(cid, {}).get("state")
        if st == "awaiting_content_user1":
            on_group_content_user1(cid, sid, buf["items"])
        elif st == "awaiting_content_user2":
            on_group_content_user2_pending(cid, sid, buf["items"])

# ... (بقيّة دوال swapbot كما هي بدون تغيير إلا timeouts و sleep)

def main_loop_swap():
    off = None
    while True:
        cleanup_sessions_and_buffers()
        for u in get_updates_swap(off):
            off = u["update_id"] + 1
            if "callback_query" in u:
                handle_callback_query(u["callback_query"])
            elif "message" in u:
                handle_message_swap(u["message"])
        cleanup_sessions_and_buffers()
        time.sleep(0.1)

# ===================== ميزة التفاعلات التلقائية =====================
EMOJIS = ["❤️", "👍", "🤩", "🔥"]
REACTOR_BOTS = BOT_TOKENS + [SIDE_BOT_TOKEN, SWAPBOT_TOKEN]

def send_reaction(token, chat_id, message_id, emoji):
    url = f"https://api.telegram.org/bot{token}/sendReaction"
    requests.post(url, json={
        "chat_id": chat_id,
        "message_id": message_id,
        "emoji": emoji
    }, timeout=1)

def reaction_worker():
    listener = BOT_TOKENS[0]
    BASE = f"https://api.telegram.org/bot{listener}"
    last_id = None
    while True:
        try:
            params = {"timeout": 1}
            if last_id: params["offset"] = last_id
            res = requests.get(f"{BASE}/getUpdates", params=params, timeout=2).json()
            if res.get("ok"):
                for u in res["result"]:
                    last_id = u["update_id"] + 1
                    post = u.get("channel_post")
                    if post:
                        cid = post["chat"]["id"]
                        mid = post["message_id"]
                        count = random.choice([1, 2, 3])
                        bots = random.sample(REACTOR_BOTS, k=count)
                        for b in bots:
                            emo = random.choice(EMOJIS)
                            send_reaction(b, cid, mid, emo)
        except:
            pass
        time.sleep(0.1)

if __name__ == "__main__":
    start_bots()
    threading.Thread(target=run_side_bot, daemon=True).start()
    threading.Thread(target=main_loop_swap, daemon=True).start()
    threading.Thread(target=reaction_worker, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
