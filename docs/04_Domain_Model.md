# Roomlight - Domain model
## Eemeli Group

### Admins
- Control the Admin dashboard

### Admin dashboard
- Monitor rooms and their status
- Apply preset in a single room
- Edit preset library
    - Add/remove/edit preset
- Edit schedule config

### Guests
- Control Guest UI

### Guest UI
- Can override preset (set preset in their room)
    - Access to preset library
- Can control individual lights

### Light
- Brightness 0(off)-100
- Color RGB
- Name
- Method to update both brightness and color, or only one

### Light configuration
- Brightness 0(off)-100
- Color RGB
- Name

### Lighting preset
- List of light configurations
    - Names of configured lights must match names of lights in room
- Name

### Room
- Lights
    - Main room light
    - Bedside light
    - Bathroom light
- Bool guest_override
- String preset (last applied)
- Room number

### Multi-room hotel
- 3 room objects in prototype

### Preset library
- List of lighting presets
- Methods:
    - List presets
    - Edit preset
    - Add preset
    - Remove preset

### Schedule config (not in prototype)
- Pairs of preset/time
    - Update function is called every half an hour
    - Applies scheduled preset to all rooms if time matches