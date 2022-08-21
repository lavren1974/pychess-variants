# TODO: make videos page paginated

VIDEO_TAGS = (
    "Howto",
    "Introduction",
    "Opening",
    "Middlegame",
    "Endgame",
    "Fundamentals",
    "Tactics",
    "Puzzle",
    "Janggi",
    "Xiangqi",
    "Makruk",
    "Shogi",
    "S-Chess",
    "Match",
    "Tournament",
)

VIDEOS = [
    {
        "_id": "Vyc4Llxgke8",
        "title": "Introduction to the PyChess Website",
        "author": "PyChess",
        "tags": ["Introduction"],
        "target": "beginner",
        "duration": "20:48",
    },
    {
        "_id": "WmMw97hp8C0",
        "title": "Makpong, Ouk Chatrang (Cambodian Chess), and ASEAN Chess - How to play",
        "author": "PyChess",
        "tags": ["Howto", "Makruk"],
        "target": "beginner",
        "duration": "5:26",
    },
    {
        "_id": "LWl8nMYrONM",
        "title": "How to checkmate with 2 knights (in Hoppel-Poppel)",
        "author": "PyChess",
        "tags": ["Endgame", "Puzzle"],
        "target": "intermediate",
        "duration": "13:36",
    },
    {
        "_id": "uyNsTgo8ylI",
        "title": "Makruk (Thai Chess) - How to play",
        "author": "PyChess",
        "tags": ["Howto", "Makruk"],
        "target": "beginner",
        "duration": "6:19",
    },
    {
        "_id": "p1WEdE3TdM8",
        "title": "如果你一直想找個集分析、對奕、競技於一身的網站，那這隻影片將帶給你Pychess這個好地方。",
        "author": "PyChess",
        "tags": ["Introduction"],
        "target": "beginner",
        "duration": "30:05",
    },
    {
        "_id": "0HqKri2R5ls",
        "title": "Empire Chess - How to play",
        "author": "PyChess",
        "tags": ["Howto"],
        "target": "beginner",
        "duration": "6:32",
    },
    {
        "_id": "Ap4mGkR8HDA",
        "title": "Orda Chess (and Mirror) - How to play",
        "author": "PyChess",
        "tags": ["Howto"],
        "target": "beginner",
        "duration": "11:15",
    },
    {
        "_id": "5f9QKK7cm20",
        "title": "Tori Shogi - How to play",
        "author": "PyChess",
        "tags": ["Howto"],
        "target": "beginner",
        "duration": "12:14",
    },
    {
        "_id": "YH63AlxpXkg",
        "title": "Shogi - How to play (using internationalized piece set)",
        "author": "PyChess",
        "tags": ["Howto", "Shogi"],
        "target": "beginner",
        "duration": "17:40",
    },
    {
        "_id": "KDkF2dEt41g",
        "title": "Janggi (Korean Chess) - How to play (using internationalized piece set)",
        "author": "PyChess",
        "tags": ["Howto", "Janggi"],
        "target": "beginner",
        "duration": "17:13",
    },
    {
        "_id": "e4jYQ0UMmGk",
        "title": "Hybrid Piece Basics",
        "author": "PyChess",
        "tags": ["Fundamentals", "Tactics"],
        "target": "beginner",
        "duration": "9:02",
    },
    {
        "_id": "WRk3ZbX2bpA",
        "title": "Shogun Chess - How to play",
        "author": "PyChess",
        "tags": ["Howto"],
        "target": "beginner",
        "duration": "4:37",
    },
    {
        "_id": "E6AzOO4-340",
        "title": "S-Chess (Seiwaran Chess, SHARPER Chess) - How to play",
        "author": "PyChess",
        "tags": ["Howto", "S-Chess"],
        "target": "beginner",
        "duration": "3:02",
    },
    {
        "_id": "CRrncO-w524",
        "title": "Grand Chess - How to play",
        "author": "PyChess",
        "tags": ["Howto"],
        "target": "beginner",
        "duration": "2:06",
    },
    {
        "_id": "HNYWioiltH0",
        "title": "Capablanca Chess - How to Play",
        "author": "PyChess",
        "tags": ["Howto"],
        "target": "beginner",
        "duration": "6:18",
    },
    {
        "_id": "boT1qyDA5RA",
        "title": "Xiangqi Basics",
        "author": "PyChess",
        "tags": ["Xiangqi", "Opening", "Endgame"],
        "target": "beginner",
        "duration": "16:53",
    },
    {
        "_id": "5EDG5RP8OZ8",
        "title": "Xiangqi (Chinese Chess) - How to play (Using Internationalized Piece Set)",
        "author": "PyChess",
        "tags": ["Xiangqi", "Howto"],
        "target": "beginner",
        "duration": "8:13",
    },
    {
        "_id": "ujWzsxm18aQ",
        "title": "Seirawan-Sharper Chess introduction with GM Yasser and JannLee",
        "author": "JannLee Crazyhouse",
        "tags": ["Howto", "S-Chess"],
        "target": "beginner",
        "duration": "2:27:11",
    },
    {
        "_id": "-b91uceklhM",
        "title": "หมากรุกไทย: เว็บใหม่มาเเรง Pychess.org (มีเอไอให้เล่นฟรี)",
        "author": "หมากรุกไทย ฆราวาสผู้ใฝ่รู้",
        "tags": ["Introduction"],
        "target": "beginner",
        "duration": "15:10",
    },
    {
        "_id": "xw6NpYeuozQ",
        "title": "Crazyhouse 960 - opperwezen vs JannLee (Series 3)",
        "author": "JannLee Crazyhouse",
        "tags": ["Match"],
        "target": "advanced",
        "duration": "1:50:52",
    },
    {
        "_id": "WCJZj6szAJk",
        "title": "Xiangqi opening principles - and why they differ from chess",
        "author": "Xiangqi Chinese Chess",
        "tags": ["Xiangqi", "Fundamentals", "Opening"],
        "target": "beginner",
        "duration": "32:35",
    },
    {
        "_id": "-DHY3xhB0aE",
        "title": "European Grandmaster Joep Nabuurs' #1 Tip for Chess Players Trying to Improve at Xiangqi",
        "author": "Xiangqi Chinese Chess",
        "tags": ["Xiangqi"],
        "target": "intermediate",
        "duration": "12:47",
    },
    {
        "_id": "pX_ZDjeqlJs",
        "title": "Janggi - basic opening principles",
        "author": "Shogi TV",
        "tags": ["Janggi", "Opening"],
        "target": "beginner",
        "duration": "21:18",
    },
    {
        "_id": "-4ETYXWLEXs",
        "title": "Round1",
        "author": "Janggi France - 제르제레미",
        "tags": ["Janggi", "Tournament"],
        "target": "beginner",
        "duration": "39:50",
    },
    {
        "_id": "WALKTGnkrYM",
        "title": "Round2",
        "author": "Janggi France - 제르제레미",
        "tags": ["Janggi", "Tournament"],
        "target": "beginner",
        "duration": "32:13",
    },
    {
        "_id": "wWEvpvct8QQ",
        "title": "Round3",
        "author": "Janggi France - 제르제레미",
        "tags": ["Janggi", "Tournament"],
        "target": "beginner",
        "duration": "35:50",
    },
    {
        "_id": "INYX4zIoDOY",
        "title": "Round4",
        "author": "Janggi France - 제르제레미",
        "tags": ["Janggi", "Tournament"],
        "target": "beginner",
        "duration": "36:50",
    },
    {
        "_id": "iqHXpdsyVYM",
        "title": "Round5",
        "author": "Janggi France - 제르제레미",
        "tags": ["Janggi", "Tournament"],
        "target": "beginner",
        "duration": "1:12:16",
    },
    {
        "_id": "MEmptahUlgI",
        "title": "Round6",
        "author": "Janggi France - 제르제레미",
        "tags": ["Janggi", "Tournament"],
        "target": "beginner",
        "duration": "47:28",
    },
    {
        "_id": "lXRKxfXxsHk",
        "title": "Round7",
        "author": "Janggi France - 제르제레미",
        "tags": ["Janggi", "Tournament"],
        "target": "beginner",
        "duration": "41:02",
    },
    {
        "_id": "W9ccSduSw6Q",
        "title": "Final blitz decider and results",
        "author": "Janggi France - 제르제레미",
        "tags": ["Janggi", "Tournament"],
        "target": "beginner",
        "duration": "20:38",
    },
    {
        "_id": "6BgHBQ8AN6o",
        "title": "How to play Shogi(将棋) -Lesson#37- Shogi Variants",
        "author": "HIDETCHI",
        "tags": ["Shogi"],
        "target": "beginner",
        "duration": "10:17",
    },
    {
        "_id": "QnkQW7ICj3Y",
        "title": "Shogi Exercise #1 - Pawn Tactics",
        "author": "HIDETCHI",
        "tags": ["Shogi", "Tactics"],
        "target": "beginner",
        "duration": "10:17",
    },
    {
        "_id": "PKRdiUIwVwg",
        "title": "Shogi Exercise #2 - Pawn Tactics",
        "author": "HIDETCHI",
        "tags": ["Shogi", "Tactics"],
        "target": "beginner",
        "duration": "10:17",
    },
]
