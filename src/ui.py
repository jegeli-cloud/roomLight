# komentorivikäyttöliittymä
# admin- ja guest-valikot yhdessä moduulissa

from light import LIGHT_NAMES, LightConfiguration
from preset import LightingPreset


def _prompt(msg):
    # lue rivi
    return input(msg).strip()


def _pick(options, msg="Choose"):
    # numeroitu valinta
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    c = _prompt(f"{msg} (0 cancel): ")
    if not c.isdigit() or not 1 <= int(c) <= len(options):
        return None
    return options[int(c) - 1]


def _read_int(msg, lo, hi):
    # lue kokonaisluku
    try:
        v = int(_prompt(msg))
    except ValueError:
        return None
    return v if lo <= v <= hi else None


def _read_rgb(msg="RGB as 'r g b' (0-255 each): "):
    # lue RGB-väri
    parts = _prompt(msg).split()
    if len(parts) != 3:
        return None
    try:
        vals = tuple(int(p) for p in parts)
    except ValueError:
        return None
    return vals if all(0 <= v <= 255 for v in vals) else None


def run(hotel):
    # päävalikko
    print("roomLight prototype CLI")
    while True:
        c = _prompt("\n[a]dmin / [g]uest / [q]uit: ").lower()
        if c == "a":
            _admin(hotel)
        elif c == "g":
            _guest(hotel)
        elif c == "q":
            return


def _admin(hotel):
    # adminin valikko
    while True:
        c = _prompt("\n[s]tatus / [a]pply preset / [l]ibrary / [b]ack: ").lower()
        if c == "s":
            print("\n" + hotel.status_report())
        elif c == "a":
            _apply_preset(hotel)
        elif c == "l":
            _library(hotel.preset_library)
        elif c == "b":
            return


def _apply_preset(hotel):
    # valitse esiasetus ja kohde
    preset = _pick_preset(hotel)
    if preset is None:
        return
    target = _pick(["All rooms"] + [str(n) for n in hotel.rooms], "Target")
    if target is None:
        return
    if target == "All rooms":
        # varmista guest override -huoneiden ylikirjoitus
        overridden = [n for n, r in hotel.rooms.items() if r.guest_override]
        rooms_to_apply = list(hotel.rooms)
        if overridden and not _confirm_override(overridden):
            rooms_to_apply = [n for n in rooms_to_apply if n not in overridden]
        if not rooms_to_apply:
            print("No rooms updated.")
            return
        hotel.apply_preset_to_rooms(preset, rooms_to_apply)
        print(f"Applied '{preset.name}' to rooms: {', '.join(str(n) for n in rooms_to_apply)}.")
        return
    room_num = int(target)
    if hotel.rooms[room_num].guest_override and not _confirm_override([room_num]):
        print("Cancelled.")
        return
    scope = _pick(["All lights"] + list(LIGHT_NAMES), "Scope")
    if scope is None:
        return
    lights = None if scope == "All lights" else [scope]
    hotel.apply_preset_to_rooms(preset, [room_num], light_names=lights)
    print(f"Applied '{preset.name}' to room {room_num}" + (f" ({scope})." if lights else "."))


def _confirm_override(room_numbers):
    # vahvista override
    rooms_str = ", ".join(str(n) for n in room_numbers)
    answer = _prompt(f"Guest override active in room(s) {rooms_str}. Override anyway? [y/N]: ").lower()
    return answer == "y"


def _library(lib):
    # esiasetuskirjaston hallinta
    while True:
        print("\nPresets:", ", ".join(lib.list_names()) or "(empty)")
        c = _prompt("[a]dd/edit / [r]emove / [b]ack: ").lower()
        if c == "a":
            _add_preset(lib)
        elif c == "r":
            name = _prompt("Name to remove: ")
            print("Removed." if lib.remove(name) else "Not found.")
        elif c == "b":
            return


def _add_preset(lib):
    # lisää tai muokkaa esiasetusta
    name = _prompt("Preset name: ")
    if not name:
        return
    configs = []
    for light_name in LIGHT_NAMES:
        print(f"-- {light_name} --")
        brightness = _read_int("Brightness 0-100: ", 0, 100)
        color = _read_rgb()
        if brightness is None or color is None:
            print("Cancelled (invalid input).")
            return
        configs.append(LightConfiguration(light_name, brightness, color))
    lib.add(LightingPreset(name, configs))
    print(f"Saved '{name}'.")


def _guest(hotel):
    # guest-valikko
    room_str = _pick([str(n) for n in hotel.rooms], "Your room")
    if room_str is None:
        return
    room = hotel.rooms[int(room_str)]
    while True:
        print("\n" + "\n".join(room.status_lines()))
        c = _prompt("\n[p]reset / [l]ight / [b]ack: ").lower()
        if c == "p":
            preset = _pick_preset(hotel)
            if preset:
                room.apply_preset(preset, by_guest=True)
        elif c == "l":
            _control_light(room)
        elif c == "b":
            return


def _control_light(room):
    # säädä yhtä valoa
    name = _pick(list(room.lights), "Light")
    if name is None:
        return
    brightness = _read_int("Brightness 0-100 (enter to skip): ", 0, 100)
    color = _read_rgb("RGB 'r g b' (enter to skip): ")
    if brightness is None and color is None:
        print("Nothing to change.")
        return
    room.set_light(name, brightness=brightness, color=color, by_guest=True)


def _pick_preset(hotel):
    # esiasetuksen valinta
    name = _pick(hotel.preset_library.list_names(), "Preset")
    return hotel.preset_library.get(name) if name else None
