MOV_OPCODES = {
    8: {
        "al": "B0",
        "cl": "B1",
        "dl": "B2",
        "bl": "B3",
        "ah": "B4",
        "ch": "B5",
        "dh": "B6",
        "bh": "B7"
    },
    32: {
        "eax": "B8",
        "ecx": "B9",
        "edx": "BA",
        "ebx": "BB",
        "esp": "BC",
        "ebp": "BD",
        "esi": "BE",
        "edi": "BF"
    }
}

REGISTROS_32_BIT = {
    'eax': 0b000,
    'ecx': 0b001,
    'edx': 0b010,
    'ebx': 0b011,
    'esp': 0b100,
    'ebp': 0b101,
    'esi': 0b110,
    'edi': 0b111
}