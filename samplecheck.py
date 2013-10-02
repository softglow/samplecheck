#!/usr/bin/env python3

import argparse
import struct
import sys

SPC_START_OFFSET = 0x100
SPC_RAM_SIZE = 0x10000

INST_TBL = 0x6C00
INST_ENTRY_LEN = 0x6
SAMPLE_TBL = 0x6D00
SAMPLE_ENTRY_LEN = 0x4
SAMPLE_MAX_ID = 0x4F # completely arbitrary limit

class InstrEntry (object):
    srcn = None
    adsr = None
    gain = None
    pitch_adj = None

    @classmethod
    def decode (cls, entry):
        u = struct.unpack("<BHBH", entry)
        return cls(srcn=u[0], adsr=u[1], gain=u[2], pitch_adj=u[3])

    def __init__ (self, **kwargs):
        self.__dict__.update(kwargs)

    def encode (self):
        return struct.pack("<BHBH", self.srcn, self.adsr, self.gain, self.pitch_adj)

    def __str__ (self):
        m = "InstrEntry<srcn={0:02X} adsr={1:04X} gain={2:02X} pitch_adj={3:04X}"
        return m.format(self.srcn, self.adsr, self.gain, self.pitch_adj)

def parse_fp (f):
    ram = f.read(SPC_START_OFFSET)
    ram = f.read(SPC_RAM_SIZE)

    signatures = []

    ptr = INST_TBL
    for inst in range(0x2a):
        entry = InstrEntry.decode(ram[ptr:ptr+INST_ENTRY_LEN])
        ptr += INST_ENTRY_LEN

        if (0 <= entry.srcn <= SAMPLE_MAX_ID):
            signatures.append(entry)

    return signatures

def dump_signature (sig_ary, fn=print):
    for i, v in enumerate(sig_ary):
        fn("{0:2X}: {1}".format(i, str(v)))
    return

def main (args, prog='samplecheck'):
    p = argparse.ArgumentParser()
    p.add_argument("SPC", help="The SPC file to fingerprint")
    args = p.parse_args()
    with open(args.SPC, "rb") as f:
        dump_signature(parse_fp(f))

if __name__ == "__main__":
    main(sys.argv[1:], sys.argv[0])
