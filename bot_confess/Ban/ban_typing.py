BAN_WORD = [
    "kontol", "kontl", "kntl", "ktl", "memek", "momok", "mmk",
    "memk", "pepek", "ppek", "goblok", "gblk", "bangsat", "bgst",
    "tai", "mmok", "taik", "ajg", "anjing", "babi", "monyet", "setan", "iblis",
    "sial", "bodoh", "bngng", "cilaka", "laknat", "bool",
    "baka", "kusotare", "kutabare", "shine", "shabi", "cao ni ma", "gou ri de",
    "gaesaekki", "byeongshin", "jot", "ssibal", "blyat", "pidaras",
    "cabron", "pendejo", "hijo de puta", "connard", "merde", "pute", "arschloch",
    "scheisse", "fuck", "shit", "bitch", "asshole", "bastard", "cunt", "dick",
    "fck", "fuk", "sh1t", "b1tch", "bstrd", "cnt", "d1ck", "idiot", "ewe",
    "anjg", "bngst", "tolol", "kampret", "keparat", "brengsek", "asw", "kimak",
    "anjing", "ajng", "anj1ng", "@jing", "4nj1ng",
    "bangsat", "b4ngs4t", "b@ngsat", "bngst",
    "babi", "b4b1", "b@bi", "bbi",
    "kontol", "k0nt0l", "kntl", "k@ntol",
    "memek", "mem3k", "m3mek", "mmk",
    "tolol", "t0l0l", "tll", "t@lol",
    "goblok", "gblk", "g0bl0k", "gob1ok",
    "ngentot", "ngntt", "ng3nt0t", "ngetot",
    "sinting", "s1nting", "snting",
    "jembut", "j3mbut", "jmbt",
    "pepek", "pep3k", "p3pek",
    "kimak", "k1mak", "kmk",
    "setan", "s3tan", "stn",
    "tai", "tae", "t@i", "t4i",
    "dick", "d1ck", "d!ck", "dch",
    "shit", "sh1t", "sh!t", "s*it",
    "bitch", "btch", "b1tch", "b!tch",
    "asshole", "a$$hole", "@sshole",
    "faggot", "fag", "f@g",
    "whore", "wh0re", "wh*re",
]


def contains_bad_word(text: str) -> bool:
    normalized = text.lower().replace("1", "i").replace("3", "e").replace("4", "a").replace("0", "o").replace("@", "a")
    text_lower = text.lower()
    return any(bad in normalized for bad in BAN_WORD)