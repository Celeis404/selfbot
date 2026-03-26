import discord
import asyncio
import random
from discord.ext import tasks
from discord import Message
from discord.ext.commands import Bot
from discord import Client
from random import choice
import datetime

client = discord.Client()
token = input("TOKEN:")

# Features state
mimic_targets = set()
autoreact_targets = {}
self_autoreact = None
spam_task = None
spam_text = None
bold_enabled = False
large_enabled = False
caps_enabled = False
owoify_enabled = False
mock_enabled = False
clap_enabled = False
ascii_enabled = False
reverse_enabled = False
zalog_enabled = False
emoji_enabled = False
autoreply_targets = {}
ladder_target = None
ladder_task = None
start_time = datetime.datetime.now()
user_menu_pages = {}  # Track page per user
afk_data = {'is_afk': False, 'start_time': None}  # AFK state

default_autoreply_messages = [
    " "
]

ladder_msgs = [
    "DUMB ASS BITCH NIGGA",
    "SLUTTY ASS WHORE",
    "FAGGOT ASS NIGGA GET BACK",
    "IM ENDING U WITHOUT TRYNG MY BEST UR A FUCKING LIGHTWORK",
    "REMINDER= SH0T HOED U",
    "DUMB ASS FUCK",
    "SAD ASS NIGGA",
    "MAD ASS DIRTY ASS BITCH",
    "COME AT ME",
    "UR NEVER GOOD",
    "U CANT SURVIVE THE BITCHING",
    "FAT ASS BITCH",
    "LITTLE ASS POOR PORON",
    "NASTY ASS PEDO",
    "NIGGA U BECAME EGOLESS AFTER THIS HORRIBLE BITCHING",
    "TERRIBLE ASS NIGGA",
    "ANGRY ASS SCAMMER",
    "# STEP TO SH0T THOT",
    "EGOLESS ASS INDIAN NIGGA",
    "WEAK ASS BITCH",
    "SLOW ASS NIGGA",
    "LITTLE DUMB ASS TRANNY",
    "SHITTY ASS RETARDED ASS NIGGA",
    "THOTTY ASS NIGGA COME TO ME",
    "WANNABE CHATPACKER UR NEVER GOING ABOVE",
    "CREEPY ASS NIGGA",
    "FAILED ASS BROKE ASS NIGGA",
    "WHY DID U DIE",
    "GETCHO HEAD UP DUMB ASS NIGGA",
    "U CANT WIN AND YK THAT",
    "SASSY ASS FUCK NIGGA",
    "UR A FUCKING WITCH",
    "UGLY ASS NIGGA",
    "LITTLE ASS JUNIOR",
    "DOGSHIT TIER HAVING ASS NIGGA",
    "UR MY BITCH FOREVER AND ITS MERCHED",
    "BITCH ASS FAGGOT END UR SELF",
    "LAME ASS NIGGA",
    "WEAK ASS CLONE",
    "UR FORCED TO OBEY UR GODS",
    "U DUMB AS SHIT NIGGA",
    "WHOREY ASS BITCH",
    "FAT ASS FUCK",
    "UR NEVER GOOD UR BELOW ME DUMB ASS BITCH"
]

rizz_lines = [
    "Are you French? Because Eiffel for you.",
    "Are you a magician? Because whenever I look at you, everyone else disappears.",
    "Is your name Google? Because you got everything I'm searching for.",
    "you must be made of dopamine ‘cause every time I’m around you, I’m high as hell",
    "forget Netflix, let’s skip to the part where you're moaning my name like a broken record",
    "are you WiFi? because I’m feeling a strong connection… in more than just my phone",
    "you look like the type to ruin my life—and baby, I want it wrecked",
    "the way you walk should be illegal, but I’d happily serve time for touching what’s mine",
    "you say you're a night owl, good—because I don’t plan on letting you sleep tonight",
    "let’s make some bad decisions and blame it on how good you look with no clothes on",
    "you’ve got me thinking about things I’d only confess at 3am with my hands all over you",
    "don’t tempt me unless you plan on finishing what that look just started",
    "you bring the sin, I’ll bring the stamina—let’s make heaven jealous tonight",
    "the things I wanna do to you aren’t even legal in most time zones",
    "you’re not just in my head—you’ve got front-row seats to my dirtiest thoughts",
    "if I had a dollar for every time I imagined you on top of me, I’d own your soul by now",
    "don’t tell me you’re shy—I’ve already undressed you in my mind a hundred times",
    "your body’s got more curves than my moral compass after 2am",
    "I wanna treat your moans like a playlist—repeat, shuffle, then slow it down",
    "your voice is cute, but I wanna hear what it sounds like when you're begging",
    "baby, I’m not trying to waste your time—I’m trying to ruin your bed",
    "you look like you taste better than my self-control",
    "my hands are bored and your body’s the only thing on their to-do list",
    "Are you the spoon i use to eat my bday cake? cuz i love licking off that cream from you.",
    "Ykw, i am a single seater car, wanna drive?",
    "Are you a magician? Because every time I see you, I magically grow a 207th bone.",
    "are you my phone’s screen time? because I know I should stop, but I just can’t look away",
    "are you Bluetooth? because we connected once and now I can’t function without you",
    "are you a bad habit? because I know you’ll ruin me, and I still want more",
    "are you a pillow? cuz i always wondered why you are so soft and squishy",
    "Are you a lava cake? 'Cause the moment I open you up wide, you start dripping tht hot and sweet chocolate."
]

flirt_lines = [
    "If beauty were a crime, you'd be serving a life sentence.",
    "Do you have a name, or can I call you mine?",
    "Are you a parking ticket? Because you've got FINE written all over you.",
    "if you keep smiling like that, I might fall for you on accident",
    "you’re dangerously close to becoming my favorite distraction",
    "are you this charming with everyone, or am I just lucky?",
    "careful, you’re making it really hard to focus on anything else",
    "you’ve got that look that makes people text back fast",
    "I don’t know what’s more attractive—your face or the vibe you give off",
    "we’d look pretty cute in each other’s lives, don’t you think?",
    "if I had a star for every time you crossed my mind, I’d be holding a galaxy",
    "you give me a reason to check my phone with a smile",
    "whatever you’re doing, don’t stop—it's working on me",
    "talking to you feels like the highlight of my day—every single time",
    "you make it really hard to play it cool when you're this cute",
    "so… when are we pretending to run into each other again?",
    "you make me wish I was the reason you’re smiling right now",
    "you’re lowkey my type, highkey my crush",
    "I was gonna play hard to get, but damn, you’re making it difficult",
    "I’m not saying I’m flirting, but if I were—you’d definitely be enjoying it",
    "can we skip the small talk and get to the part where we hold hands in public?",
    "if being charming was a sport, you'd be undefeated",
    "I swear you’ve got some kind of magnetic field around you, because I keep coming back"
]

def format_bold(text):
    return f"**{text}**"

def format_large(text):
    return f"# {text}"

def format_caps(text):
    return text.upper()

def format_mock(text):
    return ''.join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text))

def format_clap(text):
    return ' 👏 '.join(text.split())

def owoify(text):
    faces = ['(・`ω´・)', ';;w;;', 'owo', 'UwU', '>w<', '^w^', 'rawr~', 'nya~', '~uwu~']
    substitutions = {
        'r': 'w', 'l': 'w',
        'I': 'W', 'L': 'W',
        'no': 'nu', 'has': 'haz', 'have': 'haz',
        'you': 'uu', 'the': 'da', 'love': 'wuv',
        'this': 'dis', 'that': 'dat', 'is': 'ish'
    }

    for orig, sub in substitutions.items():
        text = text.replace(orig, sub)

    # Add stutters
    def stutter(word):
        return word if len(word) < 3 or random.random() > 0.3 else f"{word[0]}-{word}"

    text = ' '.join(stutter(word) for word in text.split())
    text += ' ' + random.choice(faces)
    if random.random() > 0.5:
        text += ' ~'
    return text

def format_zalog(text):
    zalgo_chars = ['̽','̾','̄','̅','̿','͑','̆','̐','͒','͗','͑','̇','̈','̊','̂','̓','̈','͊','͋','͌','̃','̂','̌','͐','̀','́','̋','̏','̒','̓','̔','̽','̉','ͣ','ͤ','ͥ','ͦ','ͧ','ͨ','ͩ','ͪ','ͫ','ͬ','ͭ','ͮ','ͯ','̾','͛','͆','̚']
    return ''.join(char + ''.join(random.choices(zalgo_chars, k=random.randint(1, 3))) if char.isalpha() else char for char in text)

def format_emoji(text):
    return ' '.join(f":regional_indicator_{char.lower()}:" if char.isalpha() else char for char in text)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    global spam_task, spam_text, bold_enabled, large_enabled, caps_enabled, self_autoreact, ladder_target, ladder_task, owoify_enabled, mock_enabled, clap_enabled, ascii_enabled, reverse_enabled, zalog_enabled, emoji_enabled

    # AFK functionality
    if message.author != client.user:
        if afk_data['is_afk'] and client.user in message.mentions:
            await message.channel.send("```SH0T/WAIT UNTIL IM HERE```")
        # Process other users' messages as before
        if message.author.id in mimic_targets:
            await message.channel.send(message.content)
        if message.author.id in autoreact_targets:
            await message.add_reaction(autoreact_targets[message.author.id])
        if message.author.id in autoreply_targets:
            response = random.choice(default_autoreply_messages)
            await message.channel.send(response)
        return

    # Handle our own messages
    content = message.content.lower()

    if self_autoreact:
        try:
            await message.add_reaction(self_autoreact)
        except discord.HTTPException:
            pass

    # AFK command
    if content == '?afk':
        if not afk_data['is_afk']:
            afk_data['is_afk'] = True
            afk_data['start_time'] = datetime.datetime.now()
            await message.channel.send("```SH0T/AFK```")
        return

    # AFK removal
    if (afk_data['is_afk'] 
        and content != '?afk' 
        and content != '```sh0t/afk```' 
        and content != '```sh0t/wait until im here```'):
        afk_end = datetime.datetime.now()
        afk_duration = afk_end - afk_data['start_time']
        
        total_seconds = int(afk_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        duration_str = []
        if hours > 0:
            duration_str.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0:
            duration_str.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if seconds > 0 or (hours == 0 and minutes == 0):
            duration_str.append(f"{seconds} second{'s' if seconds != 1 else ''}")
        
        duration_text = ", ".join(duration_str)
        
        afk_data['is_afk'] = False
        afk_data['start_time'] = None
        
        await message.channel.send(f"```SH0T/WENT AFK FOR: {duration_text}```")

    # Original script functionality
    content = message.content.strip()

    # Interaction GIFs block
    gif_links = {
        "kill": [
            "https://tenor.com/view/mikey-tokyo-revengers-kazutora-killing-gif-22612903",
            "https://tenor.com/view/me-friends-smash-anime-crash-gif-16153256",
            "https://tenor.com/view/die-kill-kills-you-anime-gif-23910501",
            "https://tenor.com/view/2s-gif-23585902",
            "https://tenor.com/view/anime-gif-21901093",
        ],
        "hug": [
            "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif",
            "https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",
            "https://tenor.com/view/syno-i-love-you-syno-synowithazero-gif-2023483407273504018",
            "https://tenor.com/view/anime-anime-hug-anime-boy-anime-girl-gif-17749921123084786510",
            "https://tenor.com/view/cuddle-anime-hug-love-hug-happy-hug-loving-embrace-gif-24485164",
            "https://tenor.com/view/me-ana-gif-24686698",
            "https://tenor.com/view/hug-happy-hugging-friends-cute-gif-7898446808540296103",
            "https://tenor.com/view/hugs-gif-25241863",
            "https://tenor.com/view/anime-cheeks-hugs-gif-14106856",
            "https://tenor.com/view/anime-sevendeadlysins-hug-cutie-cuddle-gif-12712189657208313855",
            "https://tenor.com/view/anime-anime-hug-anime-girl-horimiya-hori-gif-12008257000506444611",
            "https://tenor.com/view/excited-hug-gif-6617609971298839541",
            "https://tenor.com/view/hug-gif-26359154",
            "https://tenor.com/view/cuddle-anime-gif-13420799227594028113",
            "https://tenor.com/view/cute-anime-hug-gif-5188990491482568848",
            "https://tenor.com/view/hug-anime-cute-gif-23990109",
            "https://tenor.com/view/hugs-cute-yuri-anime0-royalmale-gif-25253467",
            "https://tenor.com/view/hug-anime-gif-11460631102424457741",
            "https://tenor.com/view/yukon-child-form-embracing-ulquiorra-gif-15599442819011505520"
        ],
        "kiss": [
            "https://media.giphy.com/media/G3va31oEEnIkM/giphy.gif",
            "https://media.giphy.com/media/bGm9FuBCGg4SY/giphy.gif",
            "https://tenor.com/view/shirayuki-zen-kiss-anime-kiss-anime-couple-gif-gif-27520373",
            "https://tenor.com/view/megumi-kato-kiss-saekano-aki-tomoya-gif-26277378",
            "https://tenor.com/view/kiss-anime-kiss-anime-gif-27284749",
            "https://tenor.com/view/cute-kawai-kiss-anime-gif-16371489",
            "https://tenor.com/view/kiss-kisses-anime-love-gif-22389490",
            "https://tenor.com/view/anime-couple-kiss-gif-27081985",
            "https://tenor.com/view/anime-couple-val-ally-kiss-gif-24860682",
            "https://tenor.com/view/ichigo-hiro-anime-kiss-anime-gif-8146116001988818857",
            "https://tenor.com/view/surprise-kiss-sleeping-anime-kiss-anime-kiss-gif-11050339424267066801",
            "https://tenor.com/view/anime-kiss-hot-ground-gif-6403364776724165906",
            "https://tenor.com/view/anime-cry-anime-anime-kiss-anime-sad-gif-23131290",
            "https://tenor.com/view/kiss-anime-anime-kiss-gif-3450693716425841973",
            "https://tenor.com/view/misaki-kamiigusa-sakurasou-the-pet-girl-of-sakurasou-sakurasou-no-pet-na-kanojo-gif-7408509529161103833",
            "https://tenor.com/view/horimiya-izumi-miyamura-kyouko-hori-kiss-anime-gif-3861010441824361602",
            "https://media.tenor.com/YHxJ9NvLYKsAAAAM/anime-kiss.gif",
            "https://tenor.com/view/kiss-anime-couple-saekano-gif-27089907",
            "https://tenor.com/view/berranın-opucugu-gif-15362018629727623154",
            "https://tenor.com/view/anime-kiss-adolpha-geodolpha-gif-1416991736383803745",
            "https://tenor.com/view/kiss-gif-kiss-gif-couple-couple-kiss-gif-kiss-gif-couple-miss-you-lover-hug-gif-13554905650404903841"
        ],
        "pat": [
            "https://media.giphy.com/media/ARSp9T7wwxNcs/giphy.gif",
            "https://media.giphy.com/media/109ltuoSQT212w/giphy.gif",
            "https://tenor.com/view/tsumiki-anime-waifu-miia-neko-gif-27055340",
            "https://tenor.com/view/pat-pat-pat-anime-girl-pat-anime-girl-gif-gif-9912105134255577569",
            "https://tenor.com/view/cat-girl-head-pat-headpat-anime-gif-15491115994804690187",
            "https://tenor.com/view/pat-gif-19836593",
            "https://tenor.com/view/aharen-aharen-san-anime-aharen-san-anime-anime-pat-gif-10523722640399508139",
            "https://tenor.com/view/hugtrip-gif-9131675680678653389",
            "https://tenor.com/view/rika-higurashi-furude-kawaiiso-pat-gif-26128254",
            "https://tenor.com/view/pat-pat-gif-27638431",
            "https://tenor.com/view/anime-pat-gif-22001971",
            "https://tenor.com/view/love2-acetil-gif-27020683",
            "https://tenor.com/view/pat-anime-bear-headpat-gif-20785072",
            "https://media.tenor.com/Wrr4rxTqrrkAAAAM/futeki-fearless.gif",
            "https://media.tenor.com/xvwMZvxTQAQAAAAM/pat.gif",
            "https://tenor.com/view/pat-anime-cute-tail-wagging-gif-17904486",
            "https://tenor.com/view/anime-pet-cat-gif-19596945",
            "https://tenor.com/view/aharen-san-aharen-san-anime-aharen-aharen-anime-anime-gif-25554875",
        ],
        "slap": [
            "https://media.giphy.com/media/Zau0yrl17uzdK/giphy.gif",
            "https://tenor.com/view/slap-handa-seishuu-naru-kotoishi-barakamon-anime-barakamon-gif-5509136",
            "https://tenor.com/view/slap-jjk-nicevagg-anime-gif-22368283",
            "https://tenor.com/view/uma-musume-uma-musume-kitasan-kitasan-black-gif-6941681486235993768",
            "https://tenor.com/view/yuuri-gif-17416729081201359957",
            "https://tenor.com/view/chikku-neesan-girl-hit-wall-stfu-anime-girl-smack-gif-17078255",
            "https://tenor.com/view/no-angry-anime-slap-gif-7355956",
            "https://tenor.com/view/slap-gif-20126850",
            "https://tenor.com/view/anime-slap-slap-anime-gif-23297969",
            "https://tenor.com/view/anime-girl-anime-girl-kawai-pink-gif-20052983",
            "https://tenor.com/view/anime-nagatoro-anpan-gif-21427460",
            "https://tenor.com/view/dekiru-neko-slap-cat-giant-cat-anime-gif-1778586976017166950",
            "https://tenor.com/view/anime-kaguya-sama-kaguya-shinomiya-slap-slapping-gif-8212906941276691404",
            "https://tenor.com/view/slap-anime-girl-anime-gif-16992074182247359639",
        ],
        "kick": [
            "https://tenor.com/view/kid-goku-yajirobe-dragon-ball-goku-fight-gif-16931749225272277129",
            "https://tenor.com/view/mad-angry-rage-funa-kick-gif-17536300",
            "https://tenor.com/view/kick-anime-gif-18816835",
            "https://tenor.com/view/bleach-anime-ichigo-kick-fight-gif-18957478",
            "https://tenor.com/view/toradora-taiga-kick-ryuji-anime-gif-21310698",
            "https://tenor.com/view/charlotte-window-kick-anime-nao-tomori-gif-17562884",
            "https://tenor.com/view/the-god-of-highschool-anime-jin-mori-kick-ultimate-kick-gif-17805599",
            "https://tenor.com/view/gifdapumpkin-pumpkinama-danganronpa-anime-kick-gif-17730026",
            "https://tenor.com/view/taiga-aisaka-starling-bg-waifu-ryuuji-takasu-kick-anime-calcium-chloride-kick-gif-19132197",
            "https://tenor.com/view/anime-love-after-world-domination-kick-kicking-kick-out-gif-25869776",
            "https://tenor.com/view/taro-sakamoto-sakamoto-days-anime-kashima-kick-gif-1529081702233971101",
            "https://tenor.com/view/okabe-rintaro-rintaro-okabe-moeka-steins-gate-punch-gif-27572724",
            "https://tenor.com/view/the-god-of-highschool-anime-jin-mori-kick-ultimate-kick-gif-17805519",
            "https://tenor.com/view/clannad-kick-beat-up-kyou-fujibayashi-anime-gif-17887440",
        ],
        "punch": [
            "https://tenor.com/view/naru-punch-love-hina-anime-naru-punch-gif-15189240312390226244",
            "https://tenor.com/view/anya-forger-damian-spy-x-family-damian-desmond-anya-damian-spy-x-family-gif-25682493",
            "https://tenor.com/view/hxh-hunter-x-hunter-hxh1999-hunter-x-hunter1999-gon-gif-26633516",
            "https://tenor.com/view/anime-punch-anime-touma-accelerator-a-certain-scientific-railgun-gif-20976942",
            "https://tenor.com/view/anime-jujutsu-kaisen-anime-punch-yuji-itadori-gif-24156663",
            "https://tenor.com/view/punch-anime-flip-over-hit-strike-gif-16346949",
            "https://tenor.com/view/weliton-amogos-arzkeir-jujutsu-kaisen-panda-gif-20161414",
            "https://tenor.com/view/naruto-narutothelast-punch-anime-gif-18105611",
            "https://tenor.com/view/anime-naruto-punch-fight-gif-12911685",
            "https://tenor.com/view/anime-punch-mad-angry-gif-15580060",
            "https://tenor.com/view/anime-punching-gif-10194781",
            "https://tenor.com/view/killua-hxh-hunter-x-hunter-anime-fight-sucker-punch-gif-24326086",
            "https://tenor.com/view/rimuru-rimuru-punch-anime-punch-one-punch-slime-gif-23181170",
            "https://tenor.com/search/blue-exorcist-gifs",
            "https://tenor.com/view/shiki-granbell-shiki-punch-powerful-punch-anime-gif-22445425",
            "https://tenor.com/view/kofune-ushio-ushio-kofune-str-shinpei-gif-25615437",
        ],
        "cuddle": [
            "https://tenor.com/view/anime-drawing-couple-love-cuddle-gif-17338067475279154697",
            "https://tenor.com/view/anime-drawing-love-cuddle-hug-gif-7068602029394070952",
            "https://tenor.com/view/cuddle-anime-gif-26206284",
            "https://tenor.com/view/kuzu-no-honkai-hug-anime-gif-4584142524367836953",
            "https://media.tenor.com/c2SMIhi33DMAAAAM/cuddle-bed-hug.gif",
            "https://media.tenor.com/08vDStcjoGAAAAAM/cuddle-anime-hug-anime.gif",
            "https://media.tenor.com/MApGHq5Kvj0AAAAM/anime-hug.gif",
            "https://tenor.com/view/hug-gif-13392052862017604721",
            "https://tenor.com/view/myonigirl-my-oni-girl-myonigirl-tsumugi-myonigirl-sorry-myonigirl-apologize-gif-669997682499439860",
            "https://tenor.com/view/no-gif-26780550",
            "https://tenor.com/view/himeno-himeno-csm-himeno-chainsaw-man-kobeni-himeno-and-kobeni-gif-27068090"
        ],
        "highfive": [
            "https://tenor.com/view/anime-high-five-love-gif-10559431",
            "https://tenor.com/view/high-five-high5-up-top-take-five-give-five-gif-26900519",
            "https://tenor.com/view/kirito-anime-gif-26015428",
            "https://tenor.com/view/fairy-tail-nalu-natsu-lucy-anime-gif-9443275",
            "https://tenor.com/view/hunter-x-hunter-high-five-killua-zoldyck-gon-freecss-anime-gif-16129960",
            "https://tenor.com/view/black-star-soul-evans-soul-eater-high-five-bros-gif-1943483747726346285",
            "https://tenor.com/view/isagi-yoichi-nagi-seishiro-blue-lock-anime-soccer-gif-27518930",
            "https://tenor.com/view/no-game-no-life-ngnl-anime-gif-5121370209982387308",
            "https://tenor.com/view/renora-rwby-flower-power-team-sloth-sloth-gif-26967805",
            "https://tenor.com/view/high-five-anime-highspeed-etoile-gif-13092404470867486758",
            "https://tenor.com/view/ai-miyashita-jennifer-high-five-leo-happy-gif-2623841894286359422",
            "https://tenor.com/view/inazuma-eleven-inazuma-eleven-ares-inazuma-eleven-ares-no-tenbin-anime-inamori-asuto-gif-26073050",
        ],
        "poke": [
            "https://tenor.com/view/poking-anime-madoka-magica-madoka-magica-gif-13003129460001111615",
            "https://tenor.com/view/my-deer-friend-nokotan-noko-gif-13644573839223951462",
            "https://tenor.com/view/anime-poke-wake-up-gif-12396068",
            "https://tenor.com/view/nekone-utawarerumono-poke-anime-gif-26470052",
            "https://tenor.com/view/boop-rascal-does-not-dream-of-bunny-girl-senpai-anime-touch-nose-poke-gif-17682170",
            "https://tenor.com/view/poke-gif-19326797",
            "https://tenor.com/view/saikava-dragon-maid-kanna-kobayashi-gif-21755515",
            "https://tenor.com/view/sick-anime-gif-6004309",
        ],
        "bite": [
            "https://tenor.com/view/anime-bite-gif-25923605",
            "https://tenor.com/view/anime-sticker-hand-hand-kiss-gif-8149740244619239425",
            "https://tenor.com/view/anime-bite-gif-25923541",
            "https://tenor.com/view/cuddle-him-anime-love-in-gif-22592342",
            "https://tenor.com/view/holo-wise-wolf-holo-the-wise-wolf-spice-and-wolf-ookami-to-koushinryou-gif-12146569274942598106",
            "https://tenor.com/view/anime-bite-gif-25923608",
            "https://tenor.com/view/nom-nom-anime-love-anime-bite-anime-red-gif-27700246",
            "https://tenor.com/view/princess-connect-anime-bite-carmina-gif-24959954",
            "https://tenor.com/view/no-blood-neck-bite-vampire-fangs-anime-gif-17722210",
            "https://tenor.com/view/zero-no-tsukaima-bite-neck-bite-anime-gif-15992229",
            "https://tenor.com/view/anime-bite-gif-25923542",
            "https://tenor.com/view/omamori-himari-manga-lick-neck-kiss-gif-16854581",
        ],
        "fuck": [
            "https://tenor.com/view/anime-bed-sex-love-feet-gif-9474558",
            "https://tenor.com/view/anime-girl-moan-blush-pleasure-gif-25368829",
            "https://tenor.com/view/couple-anime-kiss-kissing-sexual-gif-10989995",
            "https://tenor.com/view/chobits-kiss-kisses-xoxo-make-out-gif-5612596",
            "https://tenor.com/view/laito-anime-sexual-vampire-bite-gif-5160295",
            "https://tenor.com/view/nagatoro-anime-love-anime-lf_cp9-girlfriend-gif-21111356",
            "https://tenor.com/view/anime-sex-sign-gif-18516379",
            "https://tenor.com/view/anime-salia-tereshkova-cross-ange-spank-blushing-gif-15788982",
            "https://tenor.com/view/vicbiz-gif-9049751501072135628",
            "https://tenor.com/view/kiss-gif-11018467039470229030",
            "https://tenor.com/view/marrochi-evil-smile-gif-5525527275077070847",
            "https://tenor.com/view/amanesuou-grisaianokajitsu-moan-gif-20122061",
            "https://tenor.com/view/anime-moan-no-game-no-life-anime-moan-gif-3855741872945793906",
            "https://tenor.com/view/anime-sad-emotional-frown-problematic-gif-16049354",
            "https://tenor.com/view/hizuru-minakata-anime-sad-girl-anime-str-summertimerendering-gif-26210718",
            "https://tenor.com/view/anime-crying-sad-upset-tears-gif-5974033",
            "https://tenor.com/view/anime-girl-gif-20775292",
        ],
        "lick": [
            "https://tenor.com/view/lick-framp-gif-2140410627496331849",
            "https://tenor.com/view/lick-gif-20726730",
            "https://tenor.com/view/lick-licky-anime-gif-17549074",
            "https://tenor.com/view/lick-gif-18767419",
        ],
        "spank": [
            "https://tenor.com/view/rikka-takanashi-chunibyo-spanking-spank-anime-gif-18249073",
            "https://tenor.com/view/spank-slap-butt-anime-gif-17784858",
            "https://tenor.com/view/anime-anime-girl-uzaki-chan-uzaki-chan-wa-sobitai-gif-21553622",
            "https://tenor.com/view/lol-funny-gif-27575230",
            "https://tenor.com/view/spank-rank-anime-gif-22745814",
            "https://tenor.com/view/anime-spanking-bad-girl-gif-14106854",
            "https://tenor.com/view/chika-fujiwara-angry-anime-spank-gif-13585603"
        ],
        "boop": [
            "https://tenor.com/view/boop-rascal-does-not-dream-of-bunny-girl-senpai-anime-touch-nose-poke-gif-17682170",
            "https://tenor.com/view/boop-nose-anime-gif-6287077",
            "https://tenor.com/view/anime-hello-hey-there-blush-gif-1485114834257298286",
            "https://tenor.com/view/boop-anime-gif-26396569",
            "https://tenor.com/view/anime-poke-poke-face-gif-12011027",
            "https://tenor.com/view/anime-boop-anime-boop-cute-cute-boop-gif-9097019291277682019",
            "https://tenor.com/view/nana-osaki-nana-nana-anime-gif-7432168892065809516",
            "https://tenor.com/view/poke-trick-hi-hello-annoy-gif-14134415"
        ],
        "eat": [
            "https://tenor.com/view/kobayashi-dragon-maid-kanna-kobayashi-anime-cute-gif-24018128",
            "https://tenor.com/view/meme-anime-cute-gif-21692179",
            "https://tenor.com/view/wataten-watashi-ni-tenshi-ga-maiorita-nom-nom-hana-food-gif-16566741",
            "https://tenor.com/view/fairy-tail-eating-nom-nom-natsu-gif-15995731",
            "https://tenor.com/view/anime-girl-loli-cute-nom-gif-24760926",
            "https://tenor.com/view/the-quintessential-quintuplets-nanako-itsuki-nakano-5toubun-hanayome-itsuki-eating-gif-23969622",
            "https://tenor.com/view/bocchi-the-rock-ryo-yamada-eating-eat-nom-nom-gif-14706351339254788083",
            "https://tenor.com/view/nom-nom-gif-14060451299149945321",
            "https://tenor.com/view/meme-nom-nom-gif-19244594",
            "https://tenor.com/view/megumin-konosuba-anime-cute-eat-gif-7762724657521975974"
        ],
        "tickle": [
            "https://tenor.com/view/date-a-live-date-a-live-iv-kotori-tickle-tickling-gif-25856492",
            "https://tenor.com/view/classroom-of-the-elite-youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-ayanokoji-tickle-horikita-gif-5774122175989684200",
            "https://tenor.com/view/tickle-laugh-gif-19915995",
            "https://tenor.com/view/onimai-momiji-hozuki-tickling-mahiro-oyama-anime-gif-8371425587834572630",
            "https://tenor.com/view/nezuko-mitsuri-tickle-anime-laugh-gif-5590774283571697252",
            "https://tenor.com/view/laugh-droll-tickle-smiles-gif-19915987",
            "https://tenor.com/view/tickle-anime-gif-11379130",
            "https://tenor.com/view/anime-id-invaded-tickles-playfighting-wholesome-gif-25800740",
            "https://tenor.com/view/chika-love-is-war-anime-fujiwara-tickle-gif-25934959",
            "https://tenor.com/view/okayu-nekomata-hololive-cat-girl-cute-gif-13718027099192082751",
            "https://tenor.com/view/bang-dream-bandori-anime-hikawa-hina-wakamiya-eve-gif-20748825"
        ],
        "smack": [
            "https://tenor.com/view/chainsaw-man-csm-csm-anime-chainsaw-man-anime-denji-gif-26957270",
            "https://tenor.com/view/smack-gif-21292724",
            "https://tenor.com/view/slap-handa-seishuu-naru-kotoishi-barakamon-anime-barakamon-gif-1776266652663386652",
            "https://tenor.com/view/chikku-neesan-girl-hit-wall-stfu-anime-girl-smack-gif-17078255",
            "https://tenor.com/view/bleach-anime-hiyori-shinji-hirako-gif-3815255846540858967",
        ]
    }
    for action in gif_links:
        if content.startswith(f".{action}"):
            if message.mentions:
                target = message.mentions[0].mention
                gif = random.choice(gif_links[action])
                await message.channel.send(f"*{client.user.mention} {action}s {target}* 💥\n{gif}")
            else:
                await message.channel.send(f"Usage: .{action} @user")

    # Roast / 8ball / Rate / Driprate block
    roasts = [
        "You're as useless as the 'ueue' in 'queue'.",
        "You bring everyone so much joy… when you leave the room.",
        "If I had a dollar for every smart thing you say, I'd be broke.",
        "You're the reason the gene pool needs a lifeguard."
    ]
    magic_8ball = [
        "It is certain.",
        "Without a doubt.",
        "You may rely on it.",
        "Yes – definitely.",
        "Ask again later.",
        "Better not tell you now.",
        "Don't count on it.",
        "My reply is no.",
        "Very doubtful."
    ]

    if content.startswith(".roast"):
        if message.mentions:
            target = message.mentions[0].mention
            await message.channel.send(f"{target}, {random.choice(roasts)}")
        else:
            await message.channel.send("Usage: .roast @user")

    if content.startswith(".8ball"):
        question = content[6:].strip()
        if question:
            await message.channel.send(f"🎱 {random.choice(magic_8ball)}")
        else:
            await message.channel.send("Ask a question like `.8ball will I win?`")

    if content.startswith(".rate"):
        if message.mentions:
            target = message.mentions[0].mention
            await message.channel.send(f"I rate {target} a solid {random.randint(1, 10)}/10.")
        else:
            await message.channel.send("Usage: .rate @user")

    if content.startswith(".driprate"):
        if message.mentions:
            target = message.mentions[0].mention
            await message.channel.send(f"{target}'s drip is at {random.randint(1, 100)}% 🧢")
        else:
            await message.channel.send("Usage: .driprate @user")

    pages = [
"""```ini
[SH0T/TOOLS]
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⠿⢿⡀⠀⠀⠀⠀⣠⣶⣿⣷⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣦⣴⣿⡋⠀⠀⠈⢳⡄⠀⢠⣾⣿⠁⠈⣿⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⠿⠛⠉⠉⠁⠀⠀⠀⠹⡄⣿⣿⣿⠀⠀⢹⡇⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣾⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣰⣏⢻⣿⣿⡆⠀⠸⣿⠀⠀⠀
⠀⠀⠀⢀⣴⠟⠁SH0TONTOP⢠⣾⣿⣿⣆⠹⣿⣷⠀⢘⣿⠀⠀⠀
⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⠋⠉⠛⠂⠹⠿⣲⣿⣿⣧⠀⠀
⠀⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣿⣿⣷⣾⣿⡇⢀⠀⣼⣿⣿⣿⣧⠀CREDITS TO:
⠰⠃0MATRIXO⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⡘⢿⣿⣿⣿⠀0KILER
⠁0SOUL⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣷⡈⠿⢿⣿⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠁⢙⠛⣿⣿⣿⣿⡟⠀⡿⠀⠀⢀⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣶⣤⣉⣛⠻⠇⢠⣿⣾⣿⡄⢻⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣦⣤⣾⣿⣿⣿⣿⣆⠁

- .autokill {user} → kills the user
- .react {emoji} → react to yourself
- .react {user} {emoji} → react on an another user
- .reply {user} →  autoreplies the user
- .mimics {user} → repeats whatever he says
- ?afk → goes afk
- .spam {message} → spams msgs
- .repeat {number} {message} → repeats that msg
- .purge {number} → deletes msgs
```""",

""" ```ansi
SH0T/TEXT FILTERS
.autobold - bolds your texts (toggle on/off)                     
.autolarge - makes your texts large (toggle on/off)     
.autocaps - auto capitalizes your texts (toggle on/off)
.clap on/off - text clap text clap text whatever             
.mock on/off - MoCkiNg TexT                                             
.owoify on/off - uwu your texts                                          
.zalog on/off - makes your text glitchy                            
.ascii on/off - turns your text into ASCII art                     
.reverse on/off - reverses your text                                          
.emoji on/off - turns your texts into emoji                      ```
""", 
""" 
```ansi
SH0T/COMMANDS
.pp @user - exposes that person's pp size
.gay @user - you know who to use this on
.simp @user - blah blah blah
.iq @user - blah blah blah
.rate @user - rates someone
.driprate @user - rates someone's drip
.8ball - ask any question about someone
.roast @user - roasts that guy
.flirt @user - flirts with someone
.rizz @user - rizzes someone
.hack @user - hacks that person
.coinflip - chooses heads or tails```
"""
,
""" 
```ansi
SH0T/COMMANDS
.kill @user - kills someone
.kick @user - kicks someone
.slap @user - slaps someone
.punch @user - punches someone
.bite @user - bites someone
.highfive @user - highfives someone
.poke @user - pokes someone
.cuddle @user - cuddles someone
.pat @user - pats someone
.kiss @user - kisses someone
.hug @user - hugs someone
.tickle @user - tickles someone
.smack @user - smacks someone
.fuck @user - fucks someone
.lick @user - licks someone
.spank @user - spanks someone
.boop @user - boops someone
.eat - eats anything or someone```
""",
"""
```SH0T/TOOLS
.uptime - uptime of the bot
.stream on/off - streams your text
.countdown - starts a countdown```
"""
]
    if content.startswith(".help") or content.startswith(".menu"):
        user_menu_pages[message.author.id] = 0
        await message.channel.send(pages[0])

    elif content.startswith(".next"):
        current = user_menu_pages.get(message.author.id, 0)
        current = (current + 1) % len(pages)
        user_menu_pages[message.author.id] = current
        await message.channel.send(pages[current])

    elif content.startswith(".prev"):
        current = user_menu_pages.get(message.author.id, 0)
        current = (current - 1) % len(pages)
        user_menu_pages[message.author.id] = current
        await message.channel.send(pages[current])

    # Auto text formatting
    if bold_enabled or large_enabled or caps_enabled or owoify_enabled or mock_enabled or clap_enabled or ascii_enabled or reverse_enabled or zalog_enabled or emoji_enabled:
        new_content = content
        if bold_enabled:
            new_content = format_bold(new_content)
        if large_enabled:
            new_content = format_large(new_content)
        if caps_enabled:
            new_content = format_caps(new_content)
        if owoify_enabled:
            new_content = owoify(new_content)
        if mock_enabled:
            new_content = format_mock(new_content)
        if clap_enabled:
            new_content = format_clap(new_content)
        if ascii_enabled:
            new_content = f"```\n{new_content.upper()}\n```"
        if reverse_enabled:
            new_content = new_content[::-1]
        if zalog_enabled:
            new_content = format_zalog(new_content)
        if emoji_enabled:
            new_content = format_emoji(new_content)

        if new_content != content:
            try:
                await message.edit(content=new_content)
            except:
                pass

    if content.startswith(".owoify") and not content.startswith(".owoify on") and not content.startswith(".owoify off"):
        to_owoify = content[8:].strip()
        if to_owoify:
            await message.channel.send(owoify(to_owoify))
        else:
            await message.channel.send("Usage: .owoify <text>")

    if content.startswith(".owoify on"):
        owoify_enabled = True
        await message.channel.send("owoify mode enabled")
    elif content.startswith(".owoify off"):
        owoify_enabled = False
        await message.channel.send("owoify mode disabled")

    if content.startswith(".mock on"):
        mock_enabled = True
        await message.channel.send("mock mode enabled")
    elif content.startswith(".mock off"):
        mock_enabled = False
        await message.channel.send("mock mode disabled")

    if content.startswith(".clap on"):
        clap_enabled = True
        await message.channel.send("clap mode enabled")
    elif content.startswith(".clap off"):
        clap_enabled = False
        await message.channel.send("clap mode disabled")

    if content.startswith(".ascii on"):
        ascii_enabled = True
        await message.channel.send("ascii mode enabled")
    elif content.startswith(".ascii off"):
        ascii_enabled = False
        await message.channel.send("ascii mode disabled")

    if content.startswith(".reverse on"):
        reverse_enabled = True
        await message.channel.send("reverse mode enabled")
    elif content.startswith(".reverse off"):
        reverse_enabled = False
        await message.channel.send("reverse mode disabled")

    if content.startswith(".zalog on"):
        zalog_enabled = True
        await message.channel.send("zalog mode enabled")
    elif content.startswith(".zalog off"):
        zalog_enabled = False
        await message.channel.send("zalog mode disabled")

    if content.startswith(".emoji on"):
        emoji_enabled = True
        await message.channel.send("emoji mode enabled")
    elif content.startswith(".emoji off"):
        emoji_enabled = False
        await message.channel.send("emoji mode disabled")

    if content.startswith(".countdown"):
        parts = content.split()
        if len(parts) == 2 and parts[1].isdigit():
            seconds = int(parts[1])
            await message.channel.send(f"Countdown starting from {seconds}s")
            for i in range(seconds, 0, -1):
                await message.channel.send(f"{i}...")
                await asyncio.sleep(1)
            await message.channel.send("⏰ Time's up!")
        else:
            await message.channel.send("Usage: .countdown <seconds>")

    if content.startswith(".uptime"):
        uptime = datetime.now() - start_time
        await message.channel.send(f"Uptime: {str(uptime).split('.')[0]}")

    if content.startswith(".rizz"):
        await message.channel.send(random.choice(rizz_lines))

    if content.startswith(".flirt"):
        await message.channel.send(random.choice(flirt_lines))

    if content.startswith(".reverse "):
        text = content[9:].strip()
        await message.channel.send(text[::-1])

    if content.startswith(".ascii "):
        text = content[7:].strip()
        await message.channel.send(f"```\n{text.upper()}\n```")

    if content.startswith(".repeat"):
        parts = content.split(maxsplit=2)
        if len(parts) == 3 and parts[1].isdigit():
            times = int(parts[1])
            await message.channel.send((parts[2] + ' ') * times)

    if content.startswith(".time"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await message.channel.send(f"Current time: {now}")

    if content.startswith(".coinflip"):
        result = random.choice(["heads", "tails"])
        await message.channel.send(f"The coin landed on: **{result}**")

    if content.startswith(".mimic "):
        if "off" in content.lower():
            mimic_targets.clear()
            await message.channel.send("```SH0T/MIMICKING IS OFF```")
        else:
            for mention in message.mentions:
                mimic_targets.add(mention.id)
            await message.channel.send("```SH0T/MIMICKING IS ON```")

    elif content.startswith(".react"):
        parts = content.split()
        if content.lower().strip() == ".react off":
            autoreact_targets.clear()
            self_autoreact = None
            await message.channel.send("```SH0T/kill is done```")
        elif len(message.mentions) == 1 and len(parts) >= 3:
            target_user = message.mentions[0].id
            emoji = parts[-1]
            autoreact_targets[target_user] = emoji
            await message.channel.send(f"```SH0T/ REACTING TO <@{target_user}> with {emoji}.```")
        elif len(message.mentions) == 0 and len(parts) == 2:
            self_autoreact = parts[1]
            await message.channel.send(f"```SH0T/claiming weapon {self_autoreact}.```")
        else:
            await message.channel.send("Usage:\n.autoreact @user ☠️\n.autoreact ☠️\n.autoreact off")

    elif content.startswith(".reply"):
        if content.lower().strip() == ".reply off":
            autoreply_targets.clear()
            await message.channel.send("```SH0T/AUTOREPLY IS OFF```")
        elif len(message.mentions) == 1:
            target_user = message.mentions[0].id
            autoreply_targets[target_user] = True
            await message.channel.send(f"```SH0T/AUTOREPLYING TO <@{target_user}>```")
        else:
            await message.channel.send("Usage:\n.reply @user\n.reply off")

    elif content.startswith(".autokill"):
        if "off" in content.lower():
            if ladder_task:
                ladder_task.cancel()
                ladder_task = None
                ladder_target = None
                await message.channel.send("```SH0T/AUTOKILL IS OFF```")
        elif len(message.mentions) == 1:
            ladder_target = message.mentions[0].id
            await message.channel.send(f"```SH0T/KILLING <@{ladder_target}>```")
            async def ladder_loop():
                while True:
                    text = random.choice(ladder_msgs)
                    await message.channel.send(f"{text} <@{ladder_target}>")
                    await asyncio.sleep(0.1)
            ladder_task = asyncio.create_task(ladder_loop())
        else:
            await message.channel.send("Usage:\n.autokill @user\n.autokill off")

    elif content.startswith(".purge"):
        try:
            count = int(content.split()[1])
            deleted = await message.channel.purge(limit=count + 1, check=lambda m: m.author == client.user)
            await message.channel.send(f"Deleted {len(deleted)-1} messages.")
        except (IndexError, ValueError):
            await message.channel.send("Usage: `.purge <number>`")
        except discord.Forbidden:
            await message.channel.send("I don't have permission to delete messages.")

    elif content.startswith(".spam "):
        if "stop" in content:
            spam_text = None
            if spam_task:
                spam_task.cancel()
            await message.channel.send("```SH0T/SPAM IS OFF```")
        else:
            spam_text = content[6:]
            await message.channel.send(f"```SH0T/STARTED SPAMMING: {spam_text}```")
            async def spam_loop():
                while True:
                    await message.channel.send(spam_text)
                    await asyncio.sleep(1.5)
            spam_task = asyncio.create_task(spam_loop())

    elif content == ".autobold":
        bold_enabled = not bold_enabled
        await message.channel.send(f"Auto bold {'enabled' if bold_enabled else 'disabled'}.")

    elif content == ".autolarge":
        large_enabled = not large_enabled
        await message.channel.send(f"Auto large {'enabled' if large_enabled else 'disabled'}.")

    elif content == ".autocaps":
        caps_enabled = not caps_enabled
        await message.channel.send(f"Auto capital {'enabled' if caps_enabled else 'disabled'}.")

    elif content.startswith(".stream"):
        if content.lower().strip() == ".stream off":
            await client.change_presence(activity=None)
            await message.channel.send("Streaming status removed.")
        else:
            stream_text = content[8:].strip()
            await client.change_presence(activity=discord.Streaming(name=stream_text, url="https://twitch.tv/yourchannel"))
            await message.channel.send(f"Now streaming: {stream_text}")

    elif content.startswith(".pp"):
        target = message.mentions[0].display_name if message.mentions else "You"
        size = "=" * random.randint(1, 5)
        await message.channel.send(f"{target}'s PP size: 8{size}D")

    elif content.startswith(".gay"):
        target = message.mentions[0].display_name if message.mentions else "You"
        percent = random.randint(0, 100)
        await message.channel.send(f"{target} is {percent}% gay 🌈")

    elif content.startswith(".simp"):
        target = message.mentions[0].display_name if message.mentions else "You"
        percent = random.randint(0, 100)
        await message.channel.send(f"{target} is {percent}% simp 🪢")

    elif content.startswith(".iq"):
        target = message.mentions[0].display_name if message.mentions else "You"
        iq = random.randint(30, 150)
        await message.channel.send(f"{target}'s IQ is {iq} 🧠")

    elif content.startswith(".hack") and message.mentions:
        victim = message.mentions[0]
        msg = await message.channel.send(f"Hacking {victim.display_name}...")
        await asyncio.sleep(1)
        for dots in [".", "..", "...", ".", "..", "..."]:
            await msg.edit(content=f"Hacking {victim.display_name}{dots}")
            await asyncio.sleep(0.6)

        joined = "Unknown"
        if isinstance(victim, discord.Member) and victim.joined_at:
            joined = victim.joined_at.strftime("%Y-%m-%d")

        info = (
            f"**Public Info:**\n"
            f"Username: {victim.name}\n"
            f"Display Name: {victim.display_name}\n"
            f"ID: {victim.id}\n"
            f"Account Created: {victim.created_at.strftime('%Y-%m-%d')}\n"
            f"Joined Server: {joined}\n"
            f"Avatar: {victim.avatar.url if victim.avatar else 'None'}\n"
        )
        await msg.edit(content=info)

        await asyncio.sleep(1)
        msg = await message.channel.send("Getting personal details...")
        for dots in [".", "..", "...", ".", "..", "..."]:
            await msg.edit(content=f"Getting personal details{dots}")
            await asyncio.sleep(0.6)

        funny_pics = [
            "https://cdn.discordapp.com/attachments/1315306124202737766/1358862825719861489/Screenshot_20250407_232016_Instagram.png?ex=67f56320&is=67f411a0&hm=ab719844875805c9200fad0072bc4881fa8a679c3fee792540dc785f3276479f&",
            "https://cdn.discordapp.com/attachments/1315306124202737766/1358862826784948394/Screenshot_20250407_232049_Instagram.png?ex=67f56320&is=67f411a0&hm=e28070d04fd122a442ecdd68c5247287fb69a32fe6ed027e656c2eb60ebf427e&",
            "https://cdn.trendhunterstatic.com/thumbs/72/weird-beards.jpeg",
            "https://i.pinimg.com/736x/c2/df/a5/c2dfa579caaa86f7251a16f811b42518.jpg",
            "https://i.pinimg.com/564x/6c/ca/54/6cca54de714fa29be9635927826525c1.jpg",
            "https://i.pinimg.com/474x/ce/8f/ab/ce8fabce2a938bc83baa729321c6a604.jpg",
            "https://img.mensxp.com/media/content/2020/Nov/Epic-and-Hilarious-Haircut-Fails-That-Are-A-Cautionary-Tale-To-Every-Man-Going-To-The-Salon-500-2_5fc0f80ea18a2.jpeg?w=780&h=997&cc=1"
        ]

        fake_infos = [
            f"**Real Info Leaked:**\n"
            f"Name: {random.choice(['Dr. Monkey Banana', 'Rick Sanchez', 'Elon Dusk', 'Captain Noodle'])}\n"
            f"Gender: {random.choice(['Apache Helicopter', 'Mystery', 'Cyborg', 'Banana'])}\n"
            f"Age: {random.randint(10, 99)}\n"
            f"Email: {random.choice(['bananas@apeplanet.com', 'rick@multiverse.net', 'elon@teslatree.com'])}\n"
            f"Phone: +{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}\n"
            f"Address: {random.choice(['69 Jungle Tree Blvd, Planet of Apes', '101 Spaceway, Galaxy', '1 Meme Street, Internet'])}\n"
            f"Occupation: {random.choice(['Banana Quality Inspector', 'Memelord', 'Sauce Dealer', 'Quantum Farmer'])}\n"
            f"Crimes: {random.choice(['Stealing mangoes', 'Time travel without license', 'Wearing socks in sandals', 'Illegal meme distribution'])}\n"
            f"Last Seen: {random.choice(['In the banana aisle 🐒', 'riding a flying pig 🐷', 'coding in the matrix 💻', 'chilling in Area 51 👽'])}\n"
            f"Profile Pic: {random.choice(funny_pics)}"
        ]

        await msg.edit(content=random.choice(fake_infos))

client.run("ODI5MzE0MDA3MTU2MTI5ODEz.GckTiT.akWh8k8dj-YgM9SEAFAeb6mqpIPdfZ9V-mzMr8")