import pymem
import time

PROCESS_NAME = "Gothic2.exe"
STATIC_PTR   = 0x8CECBC

OFFSETS = {
    "hp_cur":      0x1B8,
    "hp_max":      0x1BC,
    "mana_cur":    0x1C0,
    "mana_max":    0x1C4,
    "level":       0x234,
    "exp":         0x42C,
    "next_lvl":    0x430,
    "lp":          0x434,
}

def read_stats(pm):
    obj_base = pm.read_uint(STATIC_PTR)
    if not obj_base:
        return None
    return {name: pm.read_int(obj_base + off) for name, off in OFFSETS.items()}

def main():
    pm = pymem.Pymem(PROCESS_NAME)
    print(f"[+] Attached (PID {pm.process_id})\n")

    while True:
        s = read_stats(pm)
        if not s:
            print("Could not read stats")
            time.sleep(1)
            continue

        remaining = s["next_lvl"] - s["exp"]
        pct = s["exp"] / s["next_lvl"] * 100 if s["next_lvl"] else 0

        print(
            f"Level {s['level']}  |  LP: {s['lp']}  |  "
            f"HP: {s['hp_cur']}/{s['hp_max']}  |  "
            f"Mana: {s['mana_cur']}/{s['mana_max']}  |  "
            f"EXP: {s['exp']:,}/{s['next_lvl']:,} ({pct:.1f}%)  —  {remaining:,} to next level"
        )
        time.sleep(1)

if __name__ == "__main__":
    main()