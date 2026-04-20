# huoneluokan määrittely
# Room on yksi hotellihuone, jossa kolme valoa

from light import LIGHT_NAMES, Light


class Room:
    def __init__(self, number):
        self.number = number
        self.lights = {name: Light(name) for name in LIGHT_NAMES}
        self.guest_override = False
        self.last_preset = "(none)"

    def apply_preset(self, preset, by_guest=False, light_names=None):
        # sovella esiasetus valoille
        targets = light_names if light_names else self.lights
        for name in targets:
            config = preset.config_for(name)
            if config and name in self.lights:
                self.lights[name].apply_config(config)
        self.last_preset = preset.name
        self.guest_override = by_guest

    def set_light(self, light_name, brightness=None, color=None, by_guest=False):
        # yksittäisen valon säätö
        if light_name not in self.lights:
            return
        self.lights[light_name].set(brightness=brightness, color=color)
        if by_guest:
            self.guest_override = True

    def status_lines(self):
        # huoneen tila riveiksi
        mode = "GUEST" if self.guest_override else "ADMIN"
        header = f"Room {self.number} | preset: {self.last_preset} | control: {mode}"
        return [header] + [f"  {light.status()}" for light in self.lights.values()]
