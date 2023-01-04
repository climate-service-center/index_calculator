_freq = {
    "fx": None,
    "day": "D",
    "week": "7D",
    "mon": "MS",
    "sem": "QS-DEC",
    "year": "YS",
}

_tfreq = {
    "fx": None,
    "day": "D",
    "week": "7D",
    "mon": ["MS", "M"],
    "sem": ["QS-DEC", "Q-FEB"],
    "year": ["AS", "A"],
}

_bfreq = {
    "fx": None,
    "day": ["D", "D", 12],
    "week": ["7D", "7D", 42],
    "mon": ["MS", "M", 12],
    "sem": ["QS-DEC", "Q-FEB", 12],
    "year": ["AS", "A", 12],
}
_bounds = {
    "fx": {
        "start": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "end": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    },
    "day": {
        "start": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "end": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    },
    "week": {
        "start": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "end": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    },
    "mon": {
        "start": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "end": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    },
    "sem": {"start": [3, 6, 9, 12], "end": [2, 5, 8, 11]},
    "year": {"start": [1], "end": [12]},
}

_fmt = {
    "fx": "%Y%m%d",
    "day": "%Y%m%d",
    "week": "%Y%m%d",
    "mon": "%Y%m",
    "sem": "%Y%m",
    "year": "%Y",
}

_split = {
    "fx": False,
    "day": "5A",
    "week": "10A",
    "mon": "10A",
    "sem": "10A",
    "year": "20A",
}
