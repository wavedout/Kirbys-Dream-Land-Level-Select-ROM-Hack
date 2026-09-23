from pathlib import Path
import hashlib

SRC = Path("/mnt/data/Kirby's Dream Land (USA, Europe).gb")
OUT = Path("/mnt/data/Kirbys_Dream_Land_Level_Select_v1.0.gb")
IPS = Path("/mnt/data/Kirbys_Dream_Land_Level_Select_v1.0.ips")
rom = bytearray(SRC.read_bytes())
orig = bytes(rom)
assert len(rom) == 0x40000
assert hashlib.md5(rom).hexdigest() == 'a66e4918edcd042ec171a57fe3ce36c3'

BANK = 6
BANK_FILE = BANK * 0x4000
FREE_CPU = 0x7DF0
FREE_FILE = BANK_FILE + (FREE_CPU - 0x4000)
assert FREE_FILE == 0x1BDF0

class Asm:
    def __init__(self, origin):
        self.origin = origin
        self.buf = bytearray()
        self.labels = {}
        self.fix = []
    @property
    def pc(self): return self.origin + len(self.buf)
    def label(self, name):
        assert name not in self.labels
        self.labels[name] = self.pc
    def emit(self, *bs): self.buf.extend(bs)
    def word(self, v): self.emit(v & 0xff, (v >> 8) & 0xff)
    def jp(self, opcode, target):
        self.emit(opcode)
        if isinstance(target, str):
            self.fix.append(('abs', len(self.buf), target)); self.word(0)
        else: self.word(target)
    def call(self, target): self.jp(0xCD, target)
    def jr(self, opcode, target):
        self.emit(opcode)
        self.fix.append(('rel', len(self.buf), target)); self.emit(0)
    def ld_hl_label(self, target):
        self.emit(0x21)
        self.fix.append(('abs', len(self.buf), target)); self.word(0)
    def ld_de_label(self, target):
        self.emit(0x11)
        self.fix.append(('abs', len(self.buf), target)); self.word(0)
    def resolve(self):
        out = bytearray(self.buf)
        for typ, pos, name in self.fix:
            t = self.labels[name]
            if typ == 'abs':
                out[pos] = t & 0xff; out[pos+1] = (t >> 8) & 0xff
            else:
                src = self.origin + pos + 1
                d = t - src
                if not -128 <= d <= 127:
                    raise ValueError((name, d, hex(src), hex(t)))
                out[pos] = d & 0xff
        return bytes(out)

A = Asm(FREE_CPU)

# Title-menu initialization hook. Called while LCD is disabled.
A.label('InitMenuPre')
A.emit(0xAF)
A.emit(0xEA, 0xFF, 0xCF)

A.ld_hl_label('ColonTile')
A.emit(0x11, 0x90, 0x8F)
A.emit(0x06, 16)
A.label('copy_colon')
A.emit(0x2A)
A.emit(0x12)
A.emit(0x13)
A.emit(0x05)
A.jr(0x20, 'copy_colon')

A.ld_hl_label('MenuLines')
for dest in (0x99E0, 0x9A00, 0x9A20):
    A.emit(0x11, dest & 0xff, dest >> 8)
    A.call('Copy20')

A.emit(0xFA, 0x3B, 0xD0)
A.emit(0xFE, 0x05)
A.jr(0x38, 'init_stage_valid')
A.emit(0xAF)
A.emit(0xEA, 0x3B, 0xD0)
A.label('init_stage_valid')
A.emit(0x5F)
A.emit(0x16, 0x00)
A.ld_hl_label('StageDigits')
A.emit(0x19)
A.emit(0x7E)
A.emit(0xEA, 0xEE, 0x99)

A.emit(0xFA, 0x3A, 0xD0)
A.emit(0xA7)
A.jr(0x28, 'init_menu_done')
A.ld_hl_label('ExtraText11')
A.emit(0x11, 0x06, 0x9A)
A.emit(0x06, 0x0B)
A.label('copy_extra_direct')
A.emit(0x2A, 0x12, 0x13, 0x05)
A.jr(0x20, 'copy_extra_direct')
A.label('init_menu_done')
A.jp(0xC3, 0x1E67)

A.label('Copy20')
A.emit(0x06, 20)
A.label('copy20_loop')
A.emit(0x2A, 0x12, 0x13, 0x05)
A.jr(0x20, 'copy20_loop')
A.emit(0xC9)

# Per-frame input handler.
A.label('HandleMenuInput')
A.emit(0xFA, 0x8B, 0xFF)
A.emit(0xFE, 0x45)
A.jr(0x28, 'input_none')
A.emit(0x47)
A.emit(0x21, 0xFF, 0xCF)

A.emit(0xCB, 0x40)
A.jr(0x20, 'a_still_down')
A.emit(0xCB, 0x86)
A.label('a_still_down')
A.emit(0xCB, 0x48)
A.jr(0x20, 'b_still_down')
A.emit(0xCB, 0x8E)
A.label('b_still_down')

A.emit(0xCB, 0x50)
A.jp(0xC2, 0x6386)

A.emit(0xCB, 0x58)
A.jr(0x20, 'input_start')

A.emit(0xCB, 0x40)
A.jr(0x28, 'check_b')
A.emit(0xCB, 0x46)
A.jr(0x20, 'check_b')
A.emit(0xCB, 0xC6)
A.emit(0xFA, 0x3B, 0xD0)
A.emit(0x3C)
A.emit(0xFE, 0x05)
A.jr(0x38, 'stage_ok')
A.emit(0xAF)
A.label('stage_ok')
A.emit(0xEA, 0x3B, 0xD0)
A.emit(0x3E, 0x1A)
A.call(0x1E96)
A.call('DrawStageUpdate')
A.jr(0x18, 'input_none')

A.label('check_b')
A.emit(0xCB, 0x48)
A.jr(0x28, 'input_none')
A.emit(0xCB, 0x4E)
A.jr(0x20, 'input_none')
A.emit(0xCB, 0xCE)
A.emit(0xFA, 0x3A, 0xD0)
A.emit(0xEE, 0x01)
A.emit(0xEA, 0x3A, 0xD0)
A.emit(0x3E, 0x1A)
A.call(0x1E96)
A.call('DrawModeUpdate')
A.label('input_none')
A.emit(0xAF)
A.emit(0xC9)
A.label('input_start')
A.emit(0x3E, 0x01)
A.emit(0xC9)

# Small title tilemap updates using the game's existing VBlank path.
A.label('DrawStageUpdate')
A.emit(0x3E, 0x99, 0xEA, 0x00, 0xCB)
A.emit(0x3E, 0xEE, 0xEA, 0x01, 0xCB)
A.emit(0xFA, 0x3B, 0xD0)
A.emit(0x5F, 0x16, 0x00)
A.ld_hl_label('StageDigits')
A.emit(0x19, 0x7E)
A.emit(0xEA, 0x02, 0xCB)
A.emit(0xAF, 0xEA, 0x03, 0xCB)
A.call('FlagTilemapUpdate')
A.emit(0xC9)

A.label('DrawModeUpdate')
A.emit(0xFA, 0x3A, 0xD0)
A.emit(0xA7)
A.jr(0x28, 'mode_normal')
A.ld_de_label('ExtraText11')
A.jr(0x18, 'mode_source_ready')
A.label('mode_normal')
A.ld_de_label('NormalText11')
A.label('mode_source_ready')
A.emit(0x01, 0x06, 0x9A)
A.emit(0x21, 0x00, 0xCB)
A.emit(0x3E, 0x0B)
A.label('mode_queue_loop')
A.emit(0xF5)
A.emit(0x78, 0x22)
A.emit(0x79, 0x22)
A.emit(0x1A, 0x22)
A.emit(0x13, 0x03)
A.emit(0xF1, 0x3D)
A.jr(0x20, 'mode_queue_loop')
A.emit(0xAF, 0x77)
A.call('FlagTilemapUpdate')
A.emit(0xC9)

A.label('FlagTilemapUpdate')
A.emit(0xFA, 0x91, 0xFF)
A.emit(0xCB, 0xD7)
A.emit(0xEA, 0x91, 0xFF)
A.emit(0xC9)

cm = {
    ' ':0x00, 'X':0x79,
    'A':0xE0,'B':0xE1,'C':0xE2,'D':0xE3,'E':0xE4,'F':0xE5,'G':0xE6,'H':0xE7,
    'I':0xE8,'J':0xE9,'K':0xEA,'L':0xEB,'M':0xEC,'N':0xED,'O':0xEE,'P':0xEF,
    'R':0xF0,'S':0xF1,'T':0xF2,'U':0xF3,'Y':0xF4,
    '1':0xF5,'9':0xF6,'2':0xFA,'3':0xFB,'4':0xFC,'5':0xFD, ':':0xF9,
}
A.label('MenuLines')
menu_lines = [
    '     A: STAGE 1     ',
    '   B: NORMAL MODE   ',
    '   SELECT: CONFIG   ',
]
for s in menu_lines:
    assert len(s) == 20, (s, len(s))
    A.emit(*(cm[ch] for ch in s))

A.label('StageDigits')
A.emit(cm['1'], cm['2'], cm['3'], cm['4'], cm['5'])
A.label('NormalText11')
A.emit(*(cm[ch] for ch in 'NORMAL MODE'))
A.label('ExtraText11')
A.emit(*(cm[ch] for ch in 'EXTRA MODE '))
A.label('ColonTile')
A.emit(*bytes.fromhex('00000000606060600000000060606060'))

code = A.resolve()
assert len(code) <= 0x210, (len(code), 0x210)
rom[FREE_FILE:FREE_FILE+len(code)] = code

def fileoff(cpu): return BANK_FILE + (cpu - 0x4000)

assert rom[fileoff(0x405E):fileoff(0x4061)] == bytes.fromhex('CD 67 1E')
rom[fileoff(0x405E):fileoff(0x4061)] = bytes([0xCD, A.labels['InitMenuPre'] & 0xff, A.labels['InitMenuPre'] >> 8])

assert rom[fileoff(0x406A):fileoff(0x406D)] == bytes.fromhex('CD A0 40')
rom[fileoff(0x406A):fileoff(0x406D)] = b'\x00\x00\x00'

stub_start, stub_end = 0x4093, 0x40A0
assert rom[fileoff(stub_start):fileoff(stub_end)] == bytes.fromhex('FA 8B FF E6 08 28 E0 3E 1B CD 96 1E C9')
stub = bytearray()
stub += bytes([0xCD, A.labels['HandleMenuInput'] & 0xff, A.labels['HandleMenuInput'] >> 8])
stub += b'\xA7'
jr_from = stub_start + len(stub) + 2
rel = 0x407A - jr_from
assert -128 <= rel <= 127
stub += bytes([0x28, rel & 0xff])
stub += b'\x3E\x1B'
stub += b'\xCD\x96\x1E'
stub += b'\xC9'
stub += b'\x00' * ((stub_end - stub_start) - len(stub))
assert len(stub) == stub_end - stub_start
rom[fileoff(stub_start):fileoff(stub_end)] = stub

assert rom[fileoff(0x40A0):fileoff(0x40A3)] == bytes.fromhex('FA 3A D0')
rom[fileoff(0x40A0):fileoff(0x40A3)] = bytes([0xC3, A.labels['DrawModeUpdate'] & 0xff, A.labels['DrawModeUpdate'] >> 8])

chk = 0
for x in rom[0x134:0x14D]: chk = (chk - x - 1) & 0xff
rom[0x14D] = chk
rom[0x14E] = rom[0x14F] = 0
g = sum(rom) & 0xffff
rom[0x14E] = (g >> 8) & 0xff
rom[0x14F] = g & 0xff

OUT.write_bytes(rom)

def make_ips(src: bytes, dst: bytes) -> bytes:
    assert len(src) == len(dst)
    out = bytearray(b'PATCH')
    i = 0
    n = len(src)
    while i < n:
        if src[i] == dst[i]:
            i += 1; continue
        start = i
        while i < n and src[i] != dst[i] and i - start < 0xffff:
            i += 1
        chunk = dst[start:i]
        out += start.to_bytes(3, 'big')
        out += len(chunk).to_bytes(2, 'big')
        out += chunk
    out += b'EOF'
    return bytes(out)
ips = make_ips(orig, bytes(rom))
IPS.write_bytes(ips)

def apply_ips(src: bytes, patch: bytes) -> bytes:
    assert patch[:5] == b'PATCH' and patch[-3:] == b'EOF'
    out = bytearray(src); p = 5
    while patch[p:p+3] != b'EOF':
        off = int.from_bytes(patch[p:p+3], 'big'); p += 3
        size = int.from_bytes(patch[p:p+2], 'big'); p += 2
        if size:
            out[off:off+size] = patch[p:p+size]; p += size
        else:
            rle = int.from_bytes(patch[p:p+2], 'big'); p += 2
            val = patch[p]; p += 1
            out[off:off+rle] = bytes([val]) * rle
    return bytes(out)
assert apply_ips(orig, ips) == bytes(rom)

calc = (sum(rom[:0x14E]) + sum(rom[0x150:])) & 0xffff
assert calc == int.from_bytes(rom[0x14E:0x150], 'big')

diffs = [i for i,(a,b) in enumerate(zip(orig,rom)) if a != b]
ranges=[]
if diffs:
    s=p=diffs[0]
    for x in diffs[1:]:
        if x == p+1: p=x
        else: ranges.append((s,p)); s=p=x
    ranges.append((s,p))

print('output:', OUT)
print('ips:', IPS)
print('injected code/data bytes:', len(code), 'free remaining:', 0x210-len(code))
print('labels:', {k:hex(v) for k,v in A.labels.items()})
print('md5:', hashlib.md5(rom).hexdigest())
print('sha1:', hashlib.sha1(rom).hexdigest())
print('header checksum:', hex(rom[0x14d]), 'global:', rom[0x14e:0x150].hex())
print('changed byte count:', len(diffs))
print('changed ranges:', [(hex(a),hex(b)) for a,b in ranges])
