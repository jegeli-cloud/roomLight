# valoluokkien määrittelyt
# Light on yksi huoneen valo
# LightConfiguration on yhden valon konfiguraatio

from dataclasses import dataclass, field

# huoneen valojen vakionimet
LIGHT_NAMES = ("Main", "Bedside", "Bathroom")


@dataclass
class Light:
    name: str
    brightness: int = 0
    color: tuple = (255, 255, 255)

    def set(self, brightness=None, color=None):
        # kirkkaus ja väri
        if brightness is not None:
            self.brightness = max(0, min(100, brightness))
        if color is not None:
            self.color = color

    def apply_config(self, config):
        # konfigurointiolion mukainen asetus
        self.brightness = config.brightness
        self.color = config.color

    def status(self):
        # palauta valon tila string
        r, g, b = self.color
        state = "off" if self.brightness == 0 else f"{self.brightness}%"
        return f"{self.name}: {state} RGB({r},{g},{b})"


@dataclass
class LightConfiguration:
    # luokka konfigurointiin
    name: str
    brightness: int
    color: tuple
