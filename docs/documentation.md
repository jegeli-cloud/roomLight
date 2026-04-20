# Roomlight Prototype — Implementation Documentation

## Eemeli Group

A Python CLI of the Roomlight prototype.

## Running

/src
python main.py 

## Top-level flow

The prototype opens with a simple menu that lets you pick a role:

- Admin, the hotel-side dashboard used by staff.
- Guest, the in-room panel, scoped to a single room the guest selects.

Both roles operate on the same hotel in memory, so anything an admin pushes and anything a guest changes are visible to each other in the same session. No persistence.

## What each module does

The source is split into small, single-purpose modules.

### Light module

Describes a single light in a room class: its name, how bright it is, and what color it is. A light can be updated partially, for example changing only its brightness, or fully from a preset. The module also defines the fixed set of light names:
    - main ceiling light
    - Bedside light
    - Bathroom light
Also describes a light configuration class.

### Preset module

Describes a named mood, which is a group of target settings, one per light. The module also owns the in-memory library of presets. The library can add, edit, remove, and list presets. Editing is done by re-adding a preset under the same name. At startup the library is default with five moods: Night, Morning, Forest, Alert, and Evening.

### Room module

Describes one hotel room. A room owns three lights, one for each fixed name. It remembers which preset was last applied to it and whether the guest has taken control. A room can apply a preset to all of its lights or just some of them, and one light can be set at a time. Each change records if it came from an admin or a guest, so the room always knows who is currently in control.

### Hotel module

Describes the whole hotel. The hotel owns a fixed set of rooms (101, 102, 103) and the shared preset library. It offers one way to push a preset to any group of rooms and any group of lights in them.

### User interface module

The command-line interface. It runs the role picker, the admin menu, and the guest menu.
    - Admin menu: room status overview, apply preset, manage library.
    - Guest menu: pick a room, apply a preset, tweak one light.
Also contains the small input helpers for reading numbers, choices, and colors.

### Main module

The entry point. Creates the hotel and hands it to the user interface.

## How the pieces connect to the domain model

The code mirrors the domain model document.

- A light is a device that can change.
- A light configuration is a frozen copy of target settings used inside presets.
- A preset bundles configurations under a name.
- The preset library holds presets.
- A room owns lights and tracks who last changed them.
- The hotel owns rooms and the library.

Scheduling is left out, since it is out of scope for the prototype.

## Preset targeting

Admin pushes can be aimed at four levels:

- Hotel-wide: every room.
- One room, all lights.
- One room, one light.
- Many rooms, one or more specific lights.

If a preset has no entry for a given light, that light is left as-is. This is what makes partial presets safe.

The admin interface walks through three steps: pick the preset, pick all rooms or one room, and for one room pick all lights or one light.

## Who is in control of each room

Every room tracks whether the guest has taken control and which preset was last applied. The admin status screen prints one line per room showing the room number, the last preset, the control mode (ADMIN or GUEST), and each light's brightness and color.

The rules:

- Admin applies a preset to a room, the room goes back to admin control.
- Guest applies a preset to their room, the room goes to guest control.
- Guest tweaks one light, the room also goes to guest control, but the preset label still shows the last preset applied. The label is not updated by per-light tweaks.

## Confirming an override

Guest privacy mode (fully blocking admin pushes) is out of prototype scope, so admin pushes are never silently rejected. To make guest control meaningful in the demo, the admin is asked to confirm before overwriting a room that is currently in guest control.

- Pushing to one room in guest control: the admin is asked whether to proceed. Declining cancels the push.
- Pushing to all rooms when one or more are in guest control: the admin is asked whether to include those rooms. Declining applies the preset only to rooms that are not in guest control. Accepting applies it everywhere.

## Built-in moods

The library ships with five moods:

- Night: all lights off except a dim red bathroom light.
- Morning: soft yellow light everywhere at medium brightness.
- Forest: bright green light everywhere.
- Alert: full brightness red everywhere.
- Evening: dim orange from the main light, red from the bedside, blue in the bathroom.

Admins can add, edit, and remove moods at runtime from the admin menu.
