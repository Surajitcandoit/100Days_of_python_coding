
# Colors
# ======================
rest = "\033[0m"
clrs = [
    "\033[91m",  # 0 Red
    "\033[92m",  # 1 Green
    "\033[93m",  # 2 Yellow
    "\033[94m",  # 3 Blue
    "\033[95m",  # 4 Magenta
    "\033[96m"   # 5 Cyan
]


def color(text, code_idx=2, end=rest):
    print(f"{clrs[code_idx]}{text}{end}")
