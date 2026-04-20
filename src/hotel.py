# hotelliluokan määrittely
# Hotel kokoaa huoneet ja jaetun esiasetuskirjaston

from room import Room
from preset import PresetLibrary


class Hotel:
    def __init__(self, room_numbers=(101, 102, 103)):
        self.rooms = {n: Room(n) for n in room_numbers}
        self.preset_library = PresetLibrary()

    def apply_preset_to_rooms(self, preset, room_numbers, light_names=None, by_guest=False):
        # sovella esiasetus useaan huoneeseen
        for n in room_numbers:
            if n in self.rooms:
                self.rooms[n].apply_preset(preset, by_guest=by_guest, light_names=light_names)

    def status_report(self):
        # kaikkien huoneiden tilaraportti
        blocks = ["\n".join(room.status_lines()) for room in self.rooms.values()]
        return "\n\n".join(blocks)
