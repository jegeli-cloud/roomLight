# esiasetusluokkien määrittelyt
# LightingPreset on nimetty esiasetus
# PresetLibrary hallinnoi esiasetuksia

from light import LIGHT_NAMES, LightConfiguration

# oletusesiasetukset: (nimi, [(kirkkaus, väri) per valo LIGHT_NAMES-järjestyksessä])
_DEFAULT_PRESETS = [
    ("Night",     [(  0, (  0,   0,   0)), (  0, (  0,   0,   0)), ( 15, (255,   0,   0))]),
    ("Morning",   [( 60, (255, 230, 150)), ( 60, (255, 230, 150)), ( 60, (255, 230, 150))]),
    ("Forest",    [(100, ( 50, 220,  80)), (100, ( 50, 220,  80)), (100, ( 50, 220,  80))]),
    ("Alert", [(100, (255,   0,   0)), (100, (255,   0,   0)), (100, (255,   0,   0))]),
    ("Evening",   [( 30, (255, 140,   0)), ( 30, (255,   0,   0)), ( 30, ( 30, 100, 255))]),
]


class LightingPreset:
    def __init__(self, name, configs):
        # nimi ja valokohtaiset konfiguraatiot
        self.name = name
        self.configs = {c.name: c for c in configs}

    def config_for(self, light_name):
        # hae valon konfiguraatio
        return self.configs.get(light_name)


class PresetLibrary:
    def __init__(self):
        self.presets = {}
        self._seed_defaults()

    def _seed_defaults(self):
        # lisää oletusesiasetukset
        for name, per_light in _DEFAULT_PRESETS:
            configs = [
                LightConfiguration(light_name, brightness, color)
                for light_name, (brightness, color) in zip(LIGHT_NAMES, per_light)
            ]
            self.add(LightingPreset(name, configs))

    def add(self, preset):
        # lisää tai korvaa
        self.presets[preset.name] = preset

    def remove(self, name):
        # poista nimellä
        return self.presets.pop(name, None) is not None

    def get(self, name):
        # hae nimellä
        return self.presets.get(name)

    def list_names(self):
        # kaikki nimet
        return list(self.presets)
