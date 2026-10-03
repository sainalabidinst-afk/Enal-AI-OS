"""
Translator Expert — Core Translation Engine module.

Provides language detection and multilingual translation using
HuggingFace MarianMT/M2M-100 models (lazy import). Falls back to
rule-based translation when ML libraries are not available.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from apps.translator_expert.glossary_manager import GlossaryManager
from apps.translator_expert.schemas import (
    GlossaryConfig,
    TranslationResult,
    TranslationStyle,
)

logger = logging.getLogger(__name__)


class TranslationEngine:
    """
    Core translation engine with lazy-loaded HuggingFace models.

    - Language detection via lazy `langdetect` import
    - Translation via lazy `transformers` pipeline (MarianMT/M2M-100)
    - Rule-based fallback when ML libraries unavailable
    """

    STYLE_PREFIXES: dict[TranslationStyle, str] = {
        TranslationStyle.formal: "[formal]",
        TranslationStyle.casual: "[casual]",
        TranslationStyle.technical: "[technical]",
        TranslationStyle.creative: "[creative]",
    }

    IDIOM_MAP: dict[str, dict[str, str]] = {
        "en→id": {
            "break the ice": "memulai dengan santai",
            "piece of cake": "mudah seperti makan kue",
            "hit the books": "membuka buku",
            "under the weather": "kurang enek",
            "cost an arm and a leg": "mahal seperti lengan dan kaki",
            "bite the bullet": "menanggungnya",
            "kick the bucket": "meninggal",
            "hit the hay": "tidur",
            "raining cats and dogs": "hujan deras",
        },
        "id→en": {
            "jalan terus": "straight ahead",
            "kuda hitam": "white elephant",
            "makan kubur": "underutilized",
        },
        "en→es": {
            "break the ice": "romper el hielo",
            "piece of cake": "un pastel",
            "hit the books": "estudiar",
            "under the weather": "mal de por medio",
            "cost an arm and a leg": "costar un brazo y una pierna",
            "bite the bullet": "muerde la bala",
            "kick the bucket": "estirar la pata",
            "hit the hay": "cerrar la osata",
            "raining cats and dogs": "llovendo a cántaros",
        },
        "en→zh": {
            "break the ice": "打破僵局",
            "piece of cake": "小菜一碟",
            "hit the books": "用功学习",
            "under the weather": "身体不适",
            "cost an arm and a leg": "贵得人尽锤折",
            "kick the bucket": "走了",
            "hit the hay": "睡觉",
            "raining cats and dogs": "倾盆大雨",
        },
        "en→fr": {
            "break the ice": "casser la glace",
            "piece of cake": "un gâteau",
            "hit the books": "réviser",
            "under the weather": "malade",
            "cost an arm and a leg": "coûter les yeux de la tête",
            "kick the bucket": "rendre l'âme",
            "hit the hay": "aller se coucher",
            "raining cats and dogs": "pleuvoir des cordes",
        },
        "en→de": {
            "break the ice": "das Eis brechen",
            "piece of cake": "ein Stück Kuchen",
            "hit the books": "lernen",
            "under the weather": "nicht fit",
            "cost an arm and a leg": "einen Arm und ein Bein kosten",
            "kick the bucket": "den Lohn des Grundmans genießen",
            "hit the hay": "ins Heu kratzen",
            "raining cats and dogs": "Schieße regnet",
        },
        "en→it": {
            "break the ice": "rompere il ghiaccio",
            "piece of cake": "un dolce",
            "hit the books": "studia",
            "under the weather": "sotto la pioggia",
            "cost an arm and a leg": "costare un braccio e una gamba",
            "kick the bucket": "prendere cantoni",
            "hit the hay": "andare a dormire",
            "raining cats and dogs": "piovere a dirotti",
        },
        "en→ja": {
            "break the ice": "氷破り",
            "piece of cake": "簡単くらい",
            "hit the books": "勉強する",
            "under the weather": "ちょっと具合が悪い",
            "cost an arm and a leg": "非常に高い",
            "kick the bucket": "お陀仏になる",
            "hit the hay": "寝る",
            "raining cats and dogs": "土石流のように降る",
        },
        "en→ar": {
            "break the ice": "كسر الجليد",
            "piece of cake": "قطعة من الحلوى",
            "hit the books": "افتح الكتب",
            "under the weather": "غير جيد",
            "cost an arm and a leg": "يكلف ذراع وساق",
            "kick the bucket": "القام بخطوة أخيرة",
            "hit the hay": "النوم",
            "raining cats and dogs": "مطر غزير",
        },
        "en→pt": {
            "break the ice": "quebrar o gelo",
            "piece of cake": "um pedaço de torta",
            "hit the books": "estudar",
            "under the weather": "mal dosados",
            "cost an arm and a leg": "custar um braço e uma perna",
            "kick the bucket": "errar",
            "hit the hay": "deitar",
            "raining cats and dogs": "chovendo a cântaros",
        },
        "en→ru": {
            "break the ice": "разрушить лёд",
            "piece of cake": "кусок торта",
            "hit the books": "учиться",
            "under the weather": "не в форме",
            "cost an arm and a leg": "стоить каких-то денег",
            "kick the bucket": "сойти с дистанции",
            "hit the hay": "ложиться спать",
            "raining cats and dogs": "льется как из ведра",
        },
        "en→ko": {
            "break the ice": "얼음 깨기",
            "piece of cake": "한 조각 케이크",
            "hit the books": "공부하다",
            "under the weather": "몸이가 안 좋아",
            "cost an arm and a leg": "한 팔 한 다리 가격",
            "kick the bucket": "끝장",
            "hit the hay": "잠자리에 들다",
            "raining cats and dogs": "폭우가 내리다",
        },
        "en→vi": {
            "break the ice": "phá băng",
            "piece of cake": "một mảnh bánh",
            "hit the books": "học sách",
            "under the weather": "không ổn",
            "cost an arm and a leg": "giá một cánh tay và một chân",
            "kick the bucket": "rời xa",
            "hit the hay": "đi ngủ",
            "raining cats and dogs": "mưa to",
        },
        "en→th": {
            "break the ice": "ทะลวงน้ำแข็ง",
            "piece of cake": "ชิ้นเค้ก",
            "hit the books": "อ่านหนังสือ",
            "under the weather": "ไม่สบสน",
            "cost an arm and a leg": "ราคาแรกงาน",
            "kick the bucket": "ลาออกไป",
            "hit the hay": "นอนพัก",
            "raining cats and dogs": "ฝนตกหนัก",
        },
        "en→tr": {
            "break the ice": "buzu kırmak",
            "piece of cake": "bir dilim pasta",
            "hit the books": "kitap okumak",
            "under the weather": "kötü hissetmek",
            "cost an arm and a leg": "bir kol ve bir bacak mal olmak",
            "kick the bucket": "çıkma",
            "hit the hay": "yatmak",
            "raining cats and dogs": "kedi köpek yağmur gibi",
        },
        "en→pl": {
            "break the ice": "złamać lód",
            "piece of cake": "kawałek ciasta",
            "hit the books": "uczyć się",
            "under the weather": "nie na najlepszej",
            "cost an arm and a leg": "kosztować rękę i nogę",
            "kick the bucket": "wpasować się",
            "hit the hay": "iść spać",
            "raining cats and dogs": "deszczować jak z wiadra",
        },
        "en→hi": {
            "break the ice": "बरफ़ तोड़ना",
            "piece of cake": "एक पiece केँकड़",
            "hit the books": "पढ़ाई करना",
            "under the weather": "ख़राब महसूस होना",
            "cost an arm and a leg": "एक बाँह और एक पैर की कीमत",
            "kick the bucket": "झूल जाना",
            "hit the hay": "सोना",
            "raining cats and dogs": "बाढ़ की तरह बारिश करना",
        },
        "en→ms": {
            "break the ice": "retakkan ais",
            "piece of cake": "sepotong kuih",
            "hit the books": "baca buku",
            "under the weather": "tidak sihat",
            "cost an arm and a leg": "mahal seperti lengan dan kaki",
            "kick the bucket": "pindah",
            "hit the hay": "tidur",
            "raining cats and dogs": "hujan lebat",
        },
        "en→sw": {
            "break the ice": "vunja barafu",
            "piece of cake": "kipea keki",
            "hit the books": "somaa vitabu",
            "under the weather": "si sawa",
            "cost an arm and a leg": "gharama mkononi na mguu",
            "kick the bucket": "ondokaa",
            "hit the hay": "kulala",
            "raining cats and dogs": "mvua inaanza",
        },
        "en→ur": {
            "break the ice": "برف توڑنا",
            "piece of cake": "ایک پیس کیک",
            "hit the books": "کتابیں پڑھنا",
            "under the weather": "برا محسوس ہو رہا ہے",
            "cost an arm and a leg": "ایک بانہ اور ایک پیروں کی قیمت",
            "kick the bucket": "جان بحق ہو گیا",
            "hit the hay": "سو گیا",
            "raining cats and dogs": "بارش بہت ہو رہی ہے",
        },
        "en→bn": {
            "break the ice": "বরফ ভাঙ্গা",
            "piece of cake": "একটি পিরামিড",
            "hit the books": "বই পড়া",
            "under the weather": "খারাপ লাগছে",
            "cost an arm and a leg": "একটি হাত আর একটি পা খরচ",
            "kick the bucket": "মেঝে গেছে",
            "hit the hay": "ঘুমোয়ানো",
            "raining cats and dogs": "বৃষ্টি হচ্ছে",
        },
    }

    RULE_BASED_MAP: dict[str, dict[str, str]] = {
        "en→id": {
            "hello": "halo",
            "world": "dunia",
            "good morning": "selamat pagi",
            "good afternoon": "selamat siang",
            "good evening": "selamat malam",
            "thank you": "terima kasih",
            "please": "silakan",
            "excuse me": "maaf",
            "how are you": "bagaimana kabar Anda",
            "goodbye": "selamat taslim",
            "congratulations": "selamat",
            "welcome": "selamat datang",
            "yes": "ya",
            "no": "tidak",
            "sorry": "maaf",
            "help": "bantuan",
        },
        "id→en": {
            "halo": "hello",
            "terima kasih": "thank you",
            "selamat pagi": "good morning",
            "selamat siang": "good afternoon",
            "selamat malam": "good evening",
            "selamat taslim": "goodbye",
            "bagaimana kabar Anda": "how are you",
            "tolong": "please",
            "maaf": "sorry",
            "ya": "yes",
            "tidak": "no",
        },
        "en→es": {
            "hello": "hola",
            "world": "mundo",
            "good morning": "buenos días",
            "good afternoon": "buenas tardes",
            "good evening": "buenas noches",
            "thank you": "gracias",
            "please": "por favor",
            "excuse me": "disculpe",
            "how are you": "¿cómo estás?",
            "goodbye": "adiós",
            "congratulations": "felicidades",
            "welcome": "bienvenido",
            "yes": "sí",
            "no": "no",
            "sorry": "lo siento",
            "help": "ayuda",
        },
        "en→zh": {
            "hello": "你好",
            "world": "世界",
            "good morning": "早上好",
            "good afternoon": "下午好",
            "good evening": "晚上好",
            "thank you": "谢谢",
            "please": "请",
            "excuse me": "对不起",
            "how are you": "你好吗",
            "goodbye": "再见",
            "congratulations": "恭喜",
            "welcome": "欢迎",
            "yes": "是",
            "no": "不是",
            "sorry": "对不起",
        },
        "en→fr": {
            "hello": "bonjour",
            "world": "monde",
            "good morning": "bonjour",
            "good afternoon": "bonne après-midi",
            "good evening": "bonne soirée",
            "thank you": "merci",
            "please": "s'il vous plaît",
            "excuse me": "excusez-moi",
            "how are you": "comment allez-vous",
            "goodbye": "au revoir",
            "congratulations": "félicitations",
            "welcome": "bienvenue",
            "yes": "oui",
            "no": "non",
            "sorry": "désolé",
            "help": "aide",
        },
        "en→de": {
            "hello": "hallo",
            "world": "welt",
            "good morning": "guten Morgen",
            "good afternoon": "guten Tag",
            "good evening": "guten Abend",
            "thank you": "danke",
            "please": "bitte",
            "excuse me": "entschuldigung",
            "how are you": "wie geht es dir",
            "goodbye": "auf Wiedersehen",
            "congratulations": "herzlichen Glückwunsch",
            "welcome": "willkommen",
            "yes": "ja",
            "no": "nein",
            "sorry": "es tut mir leid",
            "help": "hilfe",
        },
        "en→it": {
            "hello": "ciao",
            "world": "mondo",
            "good morning": "buongiorno",
            "good afternoon": "buon pomeriggio",
            "good evening": "buona serata",
            "thank you": "grazie",
            "please": "per favore",
            "excuse me": "scusa",
            "how are you": "come stai",
            "goodbye": "arrivederci",
            "congratulations": "congratulazioni",
            "welcome": "benvenuto",
            "yes": "sì",
            "no": "no",
            "sorry": "mi dispiace",
            "help": "aiuto",
        },
        "en→ja": {
            "hello": "こんにちは",
            "world": "世界",
            "good morning": "おはようございます",
            "good afternoon": "こんにちは",
            "good evening": "こんばんは",
            "thank you": "ありがとう",
            "please": "ください",
            "excuse me": "すみません",
            "how are you": "お元気ですか",
            "goodbye": "さようなら",
            "congratulations": "おめでとう",
            "welcome": "ようこそ",
            "yes": "はい",
            "no": "いいえ",
            "sorry": "ごめんなさい",
            "help": "助けて",
        },
        "en→ar": {
            "hello": "مرحبا",
            "world": "العالم",
            "good morning": "صباح الخير",
            "good afternoon": "مساء الخير",
            "good evening": "مساء الخير",
            "thank you": "شكرا",
            "please": "من فضلك",
            "excuse me": "عذرا",
            "how are you": "كيف حالك",
            "goodbye": "مع السلامة",
            "congratulations": "مبروك",
            "welcome": "أهلا",
            "yes": "نعم",
            "no": "لا",
            "sorry": "أنا آسف",
            "help": "مساعدة",
        },
        "en→pt": {
            "hello": "olá",
            "world": "mundo",
            "good morning": "bom dia",
            "good afternoon": "boa tarde",
            "good evening": "boa noite",
            "thank you": "obrigado",
            "please": "por favor",
            "excuse me": "desculpe",
            "how are you": "como você está",
            "goodbye": "adeus",
            "congratulations": "parabéns",
            "welcome": "bem-vindo",
            "yes": "sim",
            "no": "não",
            "sorry": "desculpe",
            "help": "ajuda",
        },
        "en→ru": {
            "hello": "привет",
            "world": "мир",
            "good morning": "доброе утро",
            "good afternoon": "добрый день",
            "good evening": "добрый вечер",
            "thank you": "спасибо",
            "please": "пожалуйста",
            "excuse me": "извините",
            "how are you": "как дела",
            "goodbye": "до свидания",
            "congratulations": "поздравляю",
            "welcome": "добро пожаловать",
            "yes": "да",
            "no": "нет",
            "sorry": "извините",
            "help": "помощь",
        },
        "en→ko": {
            "hello": "안녕하세요",
            "world": "세계",
            "good morning": "좋은 아침",
            "good afternoon": "안녕하세요",
            "good evening": "안녕히 가세요",
            "thank you": "감사합니다",
            "please": "부탁합니다",
            "excuse me": "죄송합니다",
            "how are you": "어떻게 지내세요",
            "goodbye": "안녕히 계세요",
            "congratulations": "축하합니다",
            "welcome": "환영합니다",
            "yes": "네",
            "no": "아니요",
            "sorry": "죄송합니다",
            "help": "도움말",
        },
        "en→vi": {
            "hello": "xin chào",
            "world": "thế giới",
            "good morning": "chào buổi sáng",
            "good afternoon": "chào buổi chiều",
            "good evening": "chào buổi tối",
            "thank you": "cảm ơn",
            "please": "làm ơn",
            "excuse me": "xin lỗi",
            "how are you": "bạn khỏe không",
            "goodbye": "tạm biệt",
            "congratulations": "chúc mừng",
            "welcome": "chào mừng",
            "yes": "vâng",
            "no": "không",
            "sorry": "xin lỗi",
            "help": "giúp đỡ",
        },
        "en→th": {
            "hello": "สวัสดี",
            "world": "โลก",
            "good morning": "สวัสดีตอนเช้า",
            "good afternoon": "สวัสดีตอนบ่าย",
            "good evening": "สวัสดีตอนเย็น",
            "thank you": "ขอบคุณ",
            "please": "กรุณา",
            "excuse me": "ขออภัย",
            "how are you": "คุณเป็นอย่างไร",
            "goodbye": "ลาก่อน",
            "congratulations": "ขอแสดงความยินดี",
            "welcome": "ยินดีต้อนรับ",
            "yes": "ใช่",
            "no": "ไม่",
            "sorry": "ขออภัย",
            "help": "ช่วยเหลือ",
        },
        "en→tr": {
            "hello": "merhaba",
            "world": "dünya",
            "good morning": "günaydın",
            "good afternoon": "öğlen açılışı",
            "good evening": "iyi akşamlar",
            "thank you": "teşekkür ederim",
            "please": "lütfen",
            "excuse me": "affedersiniz",
            "how are you": "nasılsın",
            "goodbye": "güle güle",
            "congratulations": "tebrikler",
            "welcome": "hoş geldiniz",
            "yes": "evet",
            "no": "hayır",
            "sorry": "özür dilerim",
            "help": "yardım",
        },
        "en→nl": {
            "hello": "hallo",
            "world": "wereld",
            "good morning": "goedemorgen",
            "good afternoon": "goedemiddag",
            "good evening": "goedenavond",
            "thank you": "dank u",
            "please": "alsjeblieft",
            "excuse me": "excuseer",
            "how are you": "hoe gaat het",
            "goodbye": "tot ziens",
            "congratulations": "gefeliciteerd",
            "welcome": "welkom",
            "yes": "ja",
            "no": "nee",
            "sorry": "sorry",
            "help": "help",
            "break the ice": "de ijs breken",
            "piece of cake": "een stukje taart",
            "hit the books": "studeren",
            "under the weather": "niet goed",
            "cost an arm and a leg": "een arm en een been kosten",
            "kick the bucket": "bij de hoek winkelen",
            "hit the hay": "op de hay zitten",
            "raining cats and dogs": "honden en katten regenen",
        },
        "en→pl": {
            "hello": "cześć",
            "world": "świecie",
            "good morning": "dzień dobry",
            "good afternoon": "dzień dobry",
            "good evening": "dobry wieczór",
            "thank you": "dziękuję",
            "please": "proszę",
            "excuse me": "przepraszam",
            "how are you": "jak się masz",
            "goodbye": "do widzenia",
            "congratulations": "gratulacje",
            "welcome": "witam",
            "yes": "tak",
            "no": "nie",
            "sorry": "przepraszam",
            "help": "pomoc",
        },
        "en→hi": {
            "hello": "नमस्ते",
            "world": "दुनिया",
            "good morning": "सुप्रभात",
            "good afternoon": "नमस्ते",
            "good evening": "शुभ रात्रि",
            "thank you": "धन्यवाद",
            "please": "कृपया",
            "excuse me": "माफ़ कीजिए",
            "how are you": "आप कैसे हैं",
            "goodbye": "अलविदा",
            "congratulations": "बधावाद",
            "welcome": "स्वागत है",
            "yes": "हाँ",
            "no": "नहीं",
            "sorry": "माफ़ कीजिए",
            "help": "मदद",
        },
        "en→ms": {
            "hello": "halo",
            "world": "dunia",
            "good morning": "selamat pagi",
            "good afternoon": "selamat tengah hari",
            "good evening": "selamat malam",
            "thank you": "terima kasih",
            "please": "sila",
            "excuse me": "maaf",
            "how are you": "bagaimana keadaan",
            "goodbye": "selamat taslim",
            "congratulations": "tahniah",
            "welcome": "selamat datang",
            "yes": "ya",
            "no": "tidak",
            "sorry": "maaf",
            "help": "bantuan",
        },
        "en→sw": {
            "hello": "habari",
            "world": "dunia",
            "good morning": "habari za leo",
            "good afternoon": "mchana mwema",
            "good evening": "jioni njema",
            "thank you": "asante",
            "please": "tafadhari",
            "excuse me": "samahani",
            "how are you": "habari yako",
            "goodbye": "kwaheri",
            "congratulations": "kongamitolea",
            "welcome": "karibu",
            "yes": "ndio",
            "no": "hapana",
            "sorry": "pole",
            "help": "sasaidia",
        },
        "en→ur": {
            "hello": "ہیلو",
            "world": "دنیا",
            "good morning": "صبح بخیر",
            "good afternoon": "دوپہر مبارک",
            "good evening": "شام مبارک",
            "thank you": "شکریہ",
            "please": "براہ کرم",
            "excuse me": "معذرت",
            "how are you": "آپ کیسے ہیں",
            "goodbye": "خدا حافظ",
            "congratulations": "مبروب",
            "welcome": "خیر مقدم",
            "yes": "جی ہاں",
            "no": "نہیں",
            "sorry": "معذرت",
            "help": "مدد",
        },
        "en→bn": {
            "hello": "হ্যালো",
            "world": "বিশ্ব",
            "good morning": "সুপ্রভাত",
            "good afternoon": "শুভ দুপুর",
            "good evening": "শুভ সন্ধ্যা",
            "thank you": "ধন্যবাদ",
            "please": "অনুগ্রহ করে",
            "excuse me": "দয়া করে",
            "how are you": "আপনি কেমন আছেন",
            "goodbye": "বিদায়",
            "congratulations": "অভিনন্দন",
            "welcome": " স্বাগত জানাই",
            "yes": "হ্যাঁ",
            "no": "না",
            "sorry": "দয়া করে",
            "help": "সাহায্য্য",
        },
        "fr→en": {
            "bonjour": "hello",
            "merci": "thank you",
            "s'il vous plaît": "please",
            "au revoir": "goodbye",
            "oui": "yes",
            "non": "no",
            "désolé": "sorry",
            "aide": "help",
        },
        "de→en": {
            "hallo": "hello",
            "danke": "thank you",
            "bitte": "please",
            "auf Wiedersehen": "goodbye",
            "ja": "yes",
            "nein": "no",
            "entschuldigung": "sorry",
            "hilfe": "help",
        },
        "it→en": {
            "ciao": "hello",
            "grazie": "thank you",
            "per favore": "please",
            "arrivederci": "goodbye",
            "sì": "yes",
            "no": "no",
            "mi dispiace": "sorry",
            "aiuto": "help",
        },
        "nl→en": {
            "hallo": "hello",
            "dank": "thank you",
            "alsjeblieft": "please",
            "tot ziens": "goodbye",
            "ja": "yes",
            "nee": "no",
            "sorry": "sorry",
            "help": "help",
        },
        "ja→en": {
            "こんにちは": "hello",
            "ありがとう": "thank you",
            "ください": "please",
            "さようなら": "goodbye",
            "はい": "yes",
            "いいえ": "no",
            "ごめんなさい": "sorry",
            "助けて": "help",
        },
        "ar→en": {
            "مرحبا": "hello",
            "شكرا": "thank you",
            "من فضلك": "please",
            "مع السلامة": "goodbye",
            "نعم": "yes",
            "لا": "no",
            "أنا آسف": "sorry",
            "مساعدة": "help",
        },
        "pt→en": {
            "olá": "hello",
            "obrigado": "thank you",
            "por favor": "please",
            "adeus": "goodbye",
            "sim": "yes",
            "não": "no",
            "desculpe": "sorry",
            "ajuda": "help",
        },
        "ru→en": {
            "привет": "hello",
            "спасибо": "thank you",
            "пожалуйста": "please",
            "до свидания": "goodbye",
            "да": "yes",
            "нет": "no",
            "извините": "sorry",
            "помощь": "help",
        },
        "ko→en": {
            "안녕하세요": "hello",
            "감사합니다": "thank you",
            "부탁합니다": "please",
            "안녕히 계세요": "goodbye",
            "네": "yes",
            "아니요": "no",
            "죄송합니다": "sorry",
            "도움말": "help",
        },
        "vi→en": {
            "xin chào": "hello",
            "cảm ơn": "thank you",
            "làm ơn": "please",
            "tạm biệt": "goodbye",
            "vâng": "yes",
            "không": "no",
            "xin lỗi": "sorry",
            "giúp đỡ": "help",
        },
        "th→en": {
            "สวัสดี": "hello",
            "ขอบคุณ": "thank you",
            "กรุณา": "please",
            "ลาก่อน": "goodbye",
            "ใช่": "yes",
            "ไม่": "no",
            "ขออภัย": "sorry",
            "ช่วยเหลือ": "help",
        },
        "tr→en": {
            "merhaba": "hello",
            "teşekkür ederim": "thank you",
            "lütfen": "please",
            "güle güle": "goodbye",
            "evet": "yes",
            "hayır": "no",
            "özür dilerim": "sorry",
            "yardım": "help",
        },
        "pl→en": {
            "cześć": "hello",
            "dziękuję": "thank you",
            "proszę": "please",
            "do widzenia": "goodbye",
            "tak": "yes",
            "nie": "no",
            "przepraszam": "sorry",
            "pomoc": "help",
        },
        "hi→en": {
            "नमस्ते": "hello",
            "धन्यवाद": "thank you",
            "कृपया": "please",
            "अलविदा": "goodbye",
            "हाँ": "yes",
            "नहीं": "no",
            "माफ़ कीजिए": "sorry",
            "मदद": "help",
        },
        "ms→en": {
            "halo": "hello",
            "terima kasih": "thank you",
            "sila": "please",
            "selamat taslim": "goodbye",
            "ya": "yes",
            "tidak": "no",
            "maaf": "sorry",
            "bantuan": "help",
        },
        "sw→en": {
            "habari": "hello",
            "asante": "thank you",
            "tafadhari": "please",
            "kwaheri": "goodbye",
            "ndio": "yes",
            "hapana": "no",
            "pole": "sorry",
            "sasaidia": "help",
        },
        "ur→en": {
            "ہیلو": "hello",
            "شکریہ": "thank you",
            "براہ کرم": "please",
            "خدا حافظ": "goodbye",
            "جی ہاں": "yes",
            "نہیں": "no",
            "معذرت": "sorry",
            "مدد": "help",
        },
        "bn→en": {
            "হ্যালো": "hello",
            "ধন্যবাদ": "thank you",
            "অনুগ্রহ করে": "please",
            "বিদায়": "goodbye",
            "হ্যাঁ": "yes",
            "না": "no",
            "দয়া করে": "sorry",
            "সাহায্য্য": "help",
        },
    }

    REVERSE_LANG_PAIRS: dict[str, dict[str, str]] = {
        "fr→en": {},
        "de→en": {},
        "it→en": {},
        "nl→en": {},
        "ja→en": {},
        "ar→en": {},
        "pt→en": {},
        "ru→en": {},
        "ko→en": {},
        "vi→en": {},
        "th→en": {},
        "tr→en": {},
        "pl→en": {},
        "hi→en": {},
        "ms→en": {},
        "sw→en": {},
        "ur→en": {},
        "bn→en": {},
    }

    def __init__(self) -> None:
        self.glossary_manager = GlossaryManager()
        self._model_cache: dict[str, Any] = {}

    def detect_language(self, text: str) -> tuple[str, float]:
        """Detect the language of the input text."""
        try:
            from langdetect import detect, detect_langs  # type: ignore[import-untyped]

            lang = detect(text)
            langs = detect_langs(text)
            confidence = float(langs[0].prob) if langs else 0.8
            return self._normalize_lang(lang), confidence
        except ImportError:
            return self._heuristic_detect(text)
        except Exception:
            logger.warning("Language detection failed, using heuristic")
            return self._heuristic_detect(text)

    def _normalize_lang(self, lang: str) -> str:
        """Normalize language codes to supported short forms."""
        lang_map = {
            "eng": "en",
            "ind": "id",
            "spa": "es",
            "zho": "zh",
            "fra": "fr",
            "deu": "de",
            "jpn": "ja",
            "ara": "ar",
            "por": "pt",
            "rus": "ru",
            "ita": "it",
            "nld": "nl",
            "kor": "ko",
            "vie": "vi",
            "tha": "th",
            "tur": "tr",
            "pol": "pl",
            "hin": "hi",
            "msa": "ms",
            "swa": "sw",
            "urd": "ur",
            "ben": "bn",
        }
        return lang_map.get(lang[:3], lang[:2])

    def _heuristic_detect(self, text: str) -> tuple[str, float]:
        """Fallback language detection using word-pattern heuristics."""
        text_lower = text.lower()
        scores: dict[str, float] = {
            "en": 0, "id": 0, "es": 0, "zh": 0, "fr": 0,
            "de": 0, "ja": 0, "ar": 0, "pt": 0, "ru": 0,
            "it": 0, "nl": 0, "ko": 0, "vi": 0, "th": 0,
            "tr": 0, "pl": 0, "hi": 0, "ms": 0, "sw": 0,
            "ur": 0, "bn": 0,
        }

        if re.search(r"[\u4e00-\u9fff]", text):
            scores["zh"] = 0.9
            scores["ja"] = 0.3
        if re.search(r"[\u3040-\u309f\u30a0-\u30ff]", text):
            scores["ja"] = 0.9
        if re.search(r"[\u0600-\u06ff]", text):
            scores["ar"] = 0.9
        if re.search(r"[\uac00-\ud7af]", text):
            scores["ko"] = 0.9
        if re.search(r"[\u0e00-\u0e7f]", text):
            scores["th"] = 0.9
        if re.search(r"[\u0900-\u097f]", text):
            scores["hi"] = 0.5

        words = set(re.findall(r"[a-z]+", text_lower))
        if any(w in words for w in ["dan", "yang", "di", "ke", "dari"]):
            scores["id"] += 0.2
            scores["ms"] += 0.1
        if any(w in words for w in ["el", "la", "de", "que", "con"]):
            scores["es"] += 0.15
        if any(w in words for w in ["le", "la", "de", "et", "en"]):
            scores["fr"] += 0.1
        if any(w in words for w in ["der", "die", "das", "und", "ist"]):
            scores["de"] += 0.1
        if any(w in words for w in ["il", "la", "di", "e", "è"]):
            scores["it"] += 0.1
        if any(w in words for w in ["de", "het", "en", "van", "een"]):
            scores["nl"] += 0.1
        if any(w in words for w in ["y", "que", "de", "el", "con"]):
            scores["pt"] += 0.08
        if any(w in words for w in ["и", "в", "не", "что", "на"]):
            scores["ru"] += 0.1
        if any(w in words for w in ["the", "and", "is", "of", "to"]):
            scores["en"] += 0.3
        if any(w in words for w in ["dan", "untuk", "dengan", "tidak", "yang"]):
            scores["id"] += 0.15

        best_lang = max(scores, key=lambda k: scores[k])
        confidence = max(scores.values()) if scores else 0.0
        if confidence == 0:
            return "en", 0.5
        return best_lang, min(confidence + 0.3, 0.95)

    def translate_with_model(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        style: TranslationStyle,
        glossary_config: GlossaryConfig,
    ) -> TranslationResult:
        """Translate using HuggingFace MarianMT/M2M-100 (lazy import)."""
        model_name = self._get_model_name(source_lang, target_lang)

        try:
            from transformers import pipeline  # type: ignore[import-untyped]

            if model_name not in self._model_cache:
                self._model_cache[model_name] = pipeline(
                    "translation",
                    model=model_name,
                )

            model = self._model_cache[model_name]

            preprocessed, prep_terms = self.glossary_manager.apply_preprocessing(
                text, glossary_config, source_lang, target_lang
            )

            style_prefix = self.STYLE_PREFIXES.get(style, "")
            model_input = f"{style_prefix} {preprocessed}" if style_prefix else preprocessed

            result = model(model_input, max_length=max(len(model_input) * 3, 512))
            raw_translation = result[0]["translation_text"]

            postprocessed, post_terms = self.glossary_manager.apply_postprocessing(
                raw_translation, glossary_config, source_lang, target_lang
            )

            all_terms = list(set(prep_terms + post_terms))
            confidence = 0.92 if all_terms else 0.88

            return TranslationResult(
                translated_text=postprocessed,
                confidence=round(confidence, 2),
                glossary_terms_used=all_terms,
                style_applied=style,
                model_used=model_name,
            )
        except ImportError:
            logger.info("transformers not available; using rule-based fallback")
            return self._rule_based_translate(
                text, source_lang, target_lang, style, glossary_config
            )
        except Exception as e:
            logger.warning(f"Model translation failed ({e}); using rule-based fallback")
            return self._rule_based_translate(
                text, source_lang, target_lang, style, glossary_config
            )

    def _rule_based_translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        style: TranslationStyle,
        glossary_config: GlossaryConfig,
    ) -> TranslationResult:
        """Fallback rule-based translation when no ML model is available."""
        lang_pair = f"{source_lang}→{target_lang}"

        preprocessed, prep_terms = self.glossary_manager.apply_preprocessing(
            text, glossary_config, source_lang, target_lang
        )

        rule_map = self.RULE_BASED_MAP.get(lang_pair, {})
        idiom_map = self.IDIOM_MAP.get(lang_pair, {})

        processed = preprocessed
        for idiom, replacement in sorted(idiom_map.items(), key=lambda x: len(x[0]), reverse=True):
            if idiom in processed:
                processed = processed.replace(idiom, f"__IDIOM_{replacement}__")

        words = processed.split()
        translated_words: list[str] = []
        for w in words:
            if w.startswith("[") and w.endswith("]"):
                translated_words.append(w)
                continue
            cleaned = w.strip(".,!?;:\"'()[]")
            matched = False
            if cleaned.lower() in rule_map:
                replacement = rule_map[cleaned.lower()]
                if cleaned[0].isupper():
                    replacement = replacement.capitalize()
                translated_words.append(replacement)
                matched = True
            if not matched:
                if "__IDIOM_" in w:
                    translated_words.append(w.replace("__IDIOM_", "").replace("__", ""))
                else:
                    translated_words.append(w)

        raw_translation = " ".join(translated_words)

        postprocessed, post_terms = self.glossary_manager.apply_postprocessing(
            raw_translation, glossary_config, source_lang, target_lang
        )

        all_terms = list(set(prep_terms + post_terms))
        confidence = 0.85

        if style == TranslationStyle.technical:
            confidence += 0.10
        elif style == TranslationStyle.formal:
            confidence += 0.05

        return TranslationResult(
            translated_text=postprocessed,
            confidence=round(min(confidence, 0.90), 2),
            glossary_terms_used=all_terms,
            style_applied=style,
            model_used="rule-based-fallback",
        )

    def _get_model_name(self, source_lang: str, target_lang: str) -> str:
        """Get the HuggingFace model name for a language pair."""
        return f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"

    def translate_text(
        self,
        text: str,
        source_lang: str | None,
        target_lang: str,
        style: TranslationStyle,
        glossary_config: GlossaryConfig,
    ) -> TranslationResult:
        """Translate a single text string, auto-detecting source language if needed."""
        if source_lang:
            detected_lang = source_lang
            detected_confidence = 0.95
        else:
            detected_lang, detected_confidence = self.detect_language(text)

        if detected_lang == target_lang:
            return TranslationResult(
                translated_text=text,
                detected_source_language=detected_lang,
                confidence=round(detected_confidence, 2),
                glossary_terms_used=[],
                style_applied=style,
                model_used="passthrough",
            )

        return self.translate_with_model(
            text, detected_lang, target_lang, style, glossary_config
        ) if detected_lang != target_lang else TranslationResult(
            translated_text=text,
            detected_source_language=detected_lang,
            confidence=round(detected_confidence, 2),
            glossary_terms_used=[],
            style_applied=style,
            model_used="passthrough",
        )


__all__ = ["TranslationEngine"]
