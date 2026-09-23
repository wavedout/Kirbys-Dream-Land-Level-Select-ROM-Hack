KIRBY'S DREAM LAND - LEVEL SELECT
Version 1.0
Release date: September 23, 2026
Platform: Nintendo Game Boy
Author: wavedout

OVERVIEW
========
This quality-of-life hack adds a simple level select directly to the title
screen of Kirby's Dream Land.

The goal is quick access to any stage while otherwise preserving the original
game. Normal Mode and Extra Mode can both be launched from any of the five
stages, and the game's original Configuration Mode remains available.

HOW TO USE
==========
At the title screen:

  A       Cycle through STAGE 1 to STAGE 5.
  B       Toggle NORMAL MODE / EXTRA MODE.
  SELECT  Open the original CONFIGURATION MODE screen.
  START   Begin the currently selected stage and mode.

Configuration Mode behaves like the original game: START does not launch the
game from that screen. Choose EXIT to return to the title screen. Your selected
stage/mode and Configuration Mode settings are retained when you return.

The original secret-button combinations for Extra Game and Configuration Mode
are also preserved.

PATCHING
========
Two patch formats are included:

  Kirby's Dream Land - Level Select.bps
  Kirby's Dream Land - Level Select.ips

BPS is recommended because the format validates the source ROM.
IPS is included for compatibility with older patching utilities.

Apply ONE patch to a clean, unmodified copy of:

  Kirby's Dream Land (USA, Europe)

The easiest browser-based option is Rom Patcher JS:
  https://www.marcrobledo.com/RomPatcher.js/

1. Select your clean Kirby's Dream Land ROM as the ROM file.
2. Select the included .bps patch as the patch file.
3. Click Apply patch.

Do not apply both patches. Other revisions, translations, colorization hacks,
or already-modified ROMs are not supported unless they match the source hashes
below exactly.

SOURCE ROM INFORMATION
======================
Name:    Kirby's Dream Land (USA, Europe)
Size:    262144 bytes
CRC32:   40F25740
MD5:     A66E4918EDCD042EC171A57FE3CE36C3
SHA-1:   90979BAA1D0E24B41B5C304C5DDAF77450692D5A
SHA-256: 0F6DBA94FAE248D419083001C42C02A78BE6BD3DFF679C895517559E72C98D58

PATCHED ROM INFORMATION
=======================
Size:    262144 bytes
CRC32:   CC927740
MD5:     B633AF7B36A7CC0BB9E1FC1E59570A1E
SHA-1:   F3CFAB0BABC62ABBED49D78608B7FBAF29DEF5EB
SHA-256: D0499CCAFDB9D2B5FAF96B556E11624CFF7FB28FEE44E54A46D728EAC007424C

FEATURES / PRESERVED BEHAVIOR
=============================
- Title-screen stage selector for all five stages.
- Normal Mode / Extra Mode toggle on the title screen.
- Direct shortcut to the original Configuration Mode.
- Configuration settings persist after returning to the title screen.
- Original Extra Game and Configuration Mode secret codes remain functional.
- Original title-screen animation/timing loop is retained.
- No stage layouts, music, physics, or normal gameplay mechanics are changed.

TECHNICAL NOTES
===============
The hack hooks the original title-screen code in bank 6 and stores its custom
menu routine/data in verified unused padding in the same bank. The title screen's
original once-per-frame wait/animation loop is left intact; menu code runs only
for initialization or input-related updates.

The original three copyright-text rows are repurposed for:

  A: STAGE 1
  B: NORMAL MODE
  SELECT: CONFIG

A repurposed title-font punctuation tile supplies the colon glyph. Stage and
mode changes are written using the game's existing VBlank tilemap update path.
The Game Boy header/global checksums are recalculated.

TESTING
=======
Tested in SameBoy 1.0.3 during development.

Verified:
- Stages 1 through 5 launch successfully.
- Every tested stage launches in both Normal and Extra Mode.
- A/B input latching prevents rapid unintended cycling while buttons are held.
- Configuration Mode opens and returns correctly while retaining selections.
- Original secret codes remain functional.
- Long title-screen idle testing did not reproduce the slowdown seen in an
  early prototype.
- The final IPS and BPS patches reconstruct the v1.0 ROM byte-for-byte.

PATCH FILE CHECKSUMS
====================
BPS:
  Size:    440 bytes
  CRC32:   2144DF1C
  MD5:     4D685946253F0B652ED0D750453FB8CD
  SHA-1:   DD9ADA575AE96B59FF39C747D5A052549D4C6232
  SHA-256: 39645EECC2C41DDA4705CD425BD4D90894791FE05268FA7FBC990BDA6888DA57

IPS:
  Size:    474 bytes
  CRC32:   BC8BCD3E
  MD5:     4066272ED10A1078C5529D90358D1F3A
  SHA-1:   B32058E1B83995081AD0D1550961A8A4FC409B83
  SHA-256: 74821B6CC2BD5837AA05D41A32AC3292D62A18A70FB20630D77F0E463F0ACDF2

CREDITS
=======
Hack / release: wavedout
Development reference: huderlem's Kirby's Dream Land disassembly

Kirby's Dream Land was developed by HAL Laboratory and published by Nintendo.
This patch contains no original game ROM.

CHANGELOG
=========
v1.0 - September 23, 2026
- Initial public release.
- Added title-screen selection for all five stages.
- Added Normal Mode / Extra Mode toggle.
- Added direct access to the original Configuration Mode.
- Preserved the original secret codes and Configuration Mode behavior.
