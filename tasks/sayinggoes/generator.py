from kyzylborda_lib.generator import get_attachments_dir
from kyzylborda_lib.secrets import get_flag


WORDS = "jᵿɡra ðoʊ θɹu tʌf θʌɹoʊ θɔt "  # ugra_though_through_tough_thorough_thought_
DIGITS = dict(zip("0123456789abcdef", "zɪɹoʊ wan tu θɹi fɔɹ faɪv sɪks sɛvən eɪt naɪn eɪ bi si di i ɛf".split()))
NAMES = {"a": "vocale anteriore aperta non arrotondata",
         "b": "occlusiva bilabiale sonora",
         "d": "occlusiva alveolare sonora",
         "e": "vocale anteriore semichiusa non arrotondata",
         "f": "fricativa labiodentale sorda",
         "i": "vocale anteriore chiusa non arrotondata",
         "j": "approssimante palatale sonora",
         "k": "occlusiva velare sorda",
         "n": "nasale alveolare",
         "o": "vocale posteriore semichiusa arrotondata",
         "r": "vibrante postalveolare sonora",
         "s": "fricativa alveolare sorda",
         "t": "occlusiva alveolare sorda",
         "u": "vocale posteriore chiusa arrotondata",
         "v": "fricativa labiodentale sonora",
         "w": "approssimante labiovelare sonora",
         "z": "fricativa alveolare sonora",
         "ð": "fricativa dentale sonora",
         "ɔ": "vocale posteriore semiaperta arrotondata",
         "ə": "vocale centrale media",
         "ɛ": "vocale anteriore semiaperta non arrotondata",
         "ɡ": "occlusiva velare sonora",
         "ɪ": "vocale quasi anteriore quasi chiusa non arrotondata",
         "ɹ": "approssimante alveolare",
         "ʊ": "vocale quasi posteriore quasi chiusa arrotondata",
         "ʌ": "vocale posteriore semiaperta non arrotondata",
         "θ": "fricativa dentale sorda",
         "ᵿ": "vocale centrale quasi chiusa arrotondata"}
NAMES = {k: v[0].upper() + v[1:] for k, v in NAMES.items()}
NUMERALS = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
    8: "VIII",
    9: "IX",
    10: "X",
    11: "XI",
    12: "XII",
    13: "XIII",
    14: "XIV",
    15: "XV",
    16: "XVI",
    17: "XVII",
    18: "XVIII",
    19: "XIX",
    20: "XX",
    21: "XXI",
    22: "XXII",
    23: "XXIII",
    24: "XXIV",
    25: "XXV",
    26: "XXVI",
    27: "XXVII",
    28: "XXVIII",
    29: "XXIX",
    30: "XXX",
    31: "XXXI",
    32: "XXXII",
    33: "XXXIII",
    34: "XXXIV",
    35: "XXXV",
    36: "XXXVI",
    37: "XXXVII",
    38: "XXXVIII",
    39: "XXXIX",
    40: "XL",
    41: "XLI",
    42: "XLII",
    43: "XLIII",
    44: "XLIV",
    45: "XLV",
    46: "XLVI",
    47: "XLVII",
    48: "XLVIII",
    49: "XLIX",
    50: "L"
}

def generate():
    flag = get_flag()

    full_text = ""
    number = 0

    for c in WORDS:
        number += 1
        if c != " ":
            name = NAMES[c]
            full_text += f"{NUMERALS[number]}. {name}.\n"

    for cc in flag.split("_")[-1]:
        number += 1
        subnumber = 0
        for c in DIGITS[cc]:
            subnumber += 1
            name = NAMES[c]
            full_text += f"{NUMERALS[number]}.{NUMERALS[subnumber]}. {name}.\n"

    with open(get_attachments_dir() + "/sayinggoes.txt", "w") as f:
        f.write(full_text)
