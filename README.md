# Kirby's Dream Land - Level Select

A small quality-of-life ROM hack for the original **Kirby's Dream Land** on Game Boy. It adds a clean title-screen level selector while keeping the game itself essentially unchanged.

![Normal Mode title screen](screenshots/01-title-normal.png)

## Features

- **A:** cycle through **Stage 1–5**
- **B:** toggle **Normal Mode / Extra Mode**
- **Select:** open the original **Configuration Mode**
- **Start:** launch the selected stage and mode
- Original Extra Game and Configuration Mode secret codes are preserved
- Configuration settings remain in effect when you return to the title screen
- No stage layouts, music, physics, or normal gameplay mechanics are changed

## Download

Download the current release from the [Releases page](https://github.com/wavedout/Kirbys-Dream-Land-Level-Select-ROM-Hack/releases).

The release ZIP contains **BPS** and **IPS** patches plus a detailed README. **No game ROM is included.**

## Patching

**BPS is recommended** because it validates the source ROM. IPS is included for compatibility with older patchers.

The easiest option is [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/):

1. Select a clean **Kirby's Dream Land (USA, Europe)** ROM.
2. Select `Kirby's Dream Land - Level Select.bps`.
3. Click **Apply patch**.

Do not apply both the BPS and IPS patches.

### Required source ROM

| | |
|---|---|
| Name | `Kirby's Dream Land (USA, Europe)` |
| Size | `262144 bytes` |
| CRC32 | `40F25740` |
| MD5 | `A66E4918EDCD042EC171A57FE3CE36C3` |
| SHA-1 | `90979BAA1D0E24B41B5C304C5DDAF77450692D5A` |
| SHA-256 | `0F6DBA94FAE248D419083001C42C02A78BE6BD3DFF679C895517559E72C98D58` |

## Configuration Mode note

Configuration Mode behaves like the original game: pressing Start there does **not** launch a stage. Choose **EXIT** to return to the title screen; the level/mode selection and configuration settings are retained.

![Configuration Mode](screenshots/03-config-mode.png) ![Stage 3 intro](screenshots/04-stage-3-intro.png) ![Stage 3 gameplay](screenshots/05-stage-3-gameplay.png)

## Technical notes

The hack hooks the original title-screen code in bank 6 and stores its menu routine/data in verified unused padding in that bank. The original per-frame title-screen animation/wait loop remains in place, and dynamic menu changes use the game's VBlank tilemap update path.

Development testing was performed with **SameBoy 1.0.3**, including all five stages, Normal/Extra Mode, Configuration Mode return behavior, held-button input, original secret codes, and long title-screen idle testing.

### Patched ROM hashes

| | |
|---|---|
| CRC32 | `CC927740` |
| MD5 | `B633AF7B36A7CC0BB9E1FC1E59570A1E` |
| SHA-1 | `F3CFAB0BABC62ABBED49D78608B7FBAF29DEF5EB` |
| SHA-256 | `D0499CCAFDB9D2B5FAF96B556E11624CFF7FB28FEE44E54A46D728EAC007424C` |

## Credits

- Hack / release: **wavedout**
- Development reference: **huderlem's Kirby's Dream Land disassembly**
- **Kirby's Dream Land** was developed by HAL Laboratory and published by Nintendo.

This repository contains patches and original project material only. **No original game ROM is included.**
