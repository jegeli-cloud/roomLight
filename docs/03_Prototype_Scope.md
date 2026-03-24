# Roomlight - Prototype Scope
## Eemeli Group

The prototype consists of these parts:
    - 3 rooms:
        - A room object with 3 lights, each with a brightness and color.
            - Main ceiling light
            - Bedside lights
            - Bathroom light
    - Admin UI:
        - Can create lighting presets
        - Can push the preset into any set of rooms, any single room, any set of lights in any room, or any single light in any room
        - Shows the status of the lighting in all 3 rooms
    - Guest UI:
        - Can override the admin-set preset and apply any named preset availble
        - Can control any one of the lights individually and thus override any preset applied

The prototype aims to demonstrate these requirements:

| 01 | **Centralized Light Configuration:** Hotel admins can create, edit, and save named presets from the hotel dashboard. Configurations can be pushed to individual rooms or hotel-wide from a single overview system, or any individual lights. |
| 02 | **Per-Room In-Room Control:** Guests can adjust lighting directly from within their room. An in-room panel or digital interface allows overriding the active preset without affecting other rooms. |
| 04 | **Full Brightness & Color Range:** Each light supports continuous dimming and color temperature control. |
| 09 | **Room Status Overview:** The admin dashboard shows live lighting status for every room. Each room entry displays its active preset, brightness level, and whether it is in guest or admin control mode. |