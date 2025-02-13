max_cpu_usage = 0.8
max_ram_usage = 0.8
payback_period = 24
coefficient = 3.3
currency = 100
switches = 100000
switches_ipmi = 25000

# Данные для расчета услуг
works_base = 150000
# Тип услуги \ Кол-во хостов	8	16	24	32	64	96	128
works_coefficient = {
    'Нет': [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    'vSphere': [1.00, 1.30, 1.60, 2.00, 2.50, 4.00, 5.00],
    'DR': [1.30, 1.69, 2.08, 2.60, 3.25, 5.20, 6.50],
    'Veeam': [0.33, 0.43, 0.53, 1.00, 1.25, 2.00, 2.50],
    'ALB': [2.60, 3.20, 3.80, 4.60, 5.60, 8.60, 10.60],
    'Tanzu': [0, 0, 0, 0, 0, 0, 0],
    'VDI': [1.5, 1.9, 2.3, 2.7, 3.2, 4.5, 6.0],
    'VDI public': [1.7, 2.1, 2.5, 2.9, 3.4, 4.7, 6.2],
    'VDI GPU': [2.0, 2.4, 2.8, 3.2, 3.7, 5.0, 6.5],
    'NSX': [1.00, 1.30, 1.60, 2.00, 2.50, 4.00, 5.00]

}

raid_config = {
    6: {'FTM': 'RAID-6', 'FTT': 2, 'disk_usage_overhead': 1.5},
    5: {'FTM': 'RAID-5', 'FTT': 1, 'disk_usage_overhead': 1.33},
    1: {'FTM': 'RAID-1', 'FTT': 1, 'disk_usage_overhead': 2},
}

"""расчет места для рейда и дисков в дисковых группах"""
# slack_spaces = [0.2, 0.15]
# disks_size = [960, 1920, 3840, 7680, 15360]
# RAID = {}
# for raid in raid_config:
#     RAID[raid] = {}
#     for slack in slack_spaces:
#         RAID[raid][slack] = {}
#         for disk in disks_size:
#             RAID[raid][slack][disk] = {}
#             for i in range(2, 6):
#                 for j in range(2, 8):
#                     size = int(disk * i * j * (1 - slack) / raid_config[raid]['disk_usage_overhead'])
#                     key = int(f"{i}{j}")
#                     RAID[raid][slack][disk][key] = size
#
# print(RAID)

RAIDS = {
    6: {
        0.2: {
            960: {22: 2048, 23: 3072, 24: 4096, 25: 5120, 26: 6144, 27: 7168, 32: 3072, 33: 4608, 34: 6144, 35: 7680,
                  36: 9216, 37: 10752, 42: 4096, 43: 6144, 44: 8192, 45: 10240, 46: 12288, 47: 14336, 52: 5120,
                  53: 7680, 54: 10240, 55: 12800, 56: 15360, 57: 17920},
            1920: {22: 4096, 23: 6144, 24: 8192, 25: 10240, 26: 12288, 27: 14336, 32: 6144, 33: 9216, 34: 12288,
                   35: 15360, 36: 18432, 37: 21504, 42: 8192, 43: 12288, 44: 16384, 45: 20480, 46: 24576, 47: 28672,
                   52: 10240, 53: 15360, 54: 20480, 55: 25600, 56: 30720, 57: 35840},
            3840: {22: 8192, 23: 12288, 24: 16384, 25: 20480, 26: 24576, 27: 28672, 32: 12288, 33: 18432, 34: 24576,
                   35: 30720, 36: 36864, 37: 43008, 42: 16384, 43: 24576, 44: 32768, 45: 40960, 46: 49152, 47: 57344,
                   52: 20480, 53: 30720, 54: 40960, 55: 51200, 56: 61440, 57: 71680},
            7680: {22: 16384, 23: 24576, 24: 32768, 25: 40960, 26: 49152, 27: 57344, 32: 24576, 33: 36864, 34: 49152,
                   35: 61440, 36: 73728, 37: 86016, 42: 32768, 43: 49152, 44: 65536, 45: 81920, 46: 98304, 47: 114688,
                   52: 40960, 53: 61440, 54: 81920, 55: 102400, 56: 122880, 57: 143360},
            15360: {22: 32768, 23: 49152, 24: 65536, 25: 81920, 26: 98304, 27: 114688, 32: 49152, 33: 73728, 34: 98304,
                    35: 122880, 36: 147456, 37: 172032, 42: 65536, 43: 98304, 44: 131072, 45: 163840, 46: 196608,
                    47: 229376, 52: 81920, 53: 122880, 54: 163840, 55: 204800, 56: 245760, 57: 286720}},
        0.15: {
            960: {22: 2176, 23: 3264, 24: 4352, 25: 5440, 26: 6528, 27: 7616, 32: 3264, 33: 4896, 34: 6528, 35: 8160,
                  36: 9792, 37: 11424, 42: 4352, 43: 6528, 44: 8704, 45: 10880, 46: 13056, 47: 15232, 52: 5440,
                  53: 8160, 54: 10880, 55: 13600, 56: 16320, 57: 19040},
            1920: {22: 4352, 23: 6528, 24: 8704, 25: 10880, 26: 13056, 27: 15232, 32: 6528, 33: 9792, 34: 13056,
                   35: 16320, 36: 19584, 37: 22848, 42: 8704, 43: 13056, 44: 17408, 45: 21760, 46: 26112, 47: 30464,
                   52: 10880, 53: 16320, 54: 21760, 55: 27200, 56: 32640, 57: 38080},
            3840: {22: 8704, 23: 13056, 24: 17408, 25: 21760, 26: 26112, 27: 30464, 32: 13056, 33: 19584, 34: 26112,
                   35: 32640, 36: 39168, 37: 45696, 42: 17408, 43: 26112, 44: 34816, 45: 43520, 46: 52224, 47: 60928,
                   52: 21760, 53: 32640, 54: 43520, 55: 54400, 56: 65280, 57: 76160},
            7680: {22: 17408, 23: 26112, 24: 34816, 25: 43520, 26: 52224, 27: 60928, 32: 26112, 33: 39168, 34: 52224,
                   35: 65280, 36: 78336, 37: 91392, 42: 34816, 43: 52224, 44: 69632, 45: 87040, 46: 104448, 47: 121856,
                   52: 43520, 53: 65280, 54: 87040, 55: 108800, 56: 130560, 57: 152320},
            15360: {22: 34816, 23: 52224, 24: 69632, 25: 87040, 26: 104448, 27: 121856, 32: 52224, 33: 78336,
                    34: 104448, 35: 130560, 36: 156672, 37: 182784, 42: 69632, 43: 104448, 44: 139264, 45: 174080,
                    46: 208896, 47: 243712, 52: 87040, 53: 130560, 54: 174080, 55: 217600, 56: 261120, 57: 304640}}},
    5: {
        0.2: {
            960: {22: 2309, 23: 3464, 24: 4619, 25: 5774, 26: 6929, 27: 8084, 32: 3464, 33: 5196, 34: 6929, 35: 8661,
                  36: 10393,
                  37: 12126, 42: 4619, 43: 6929, 44: 9239, 45: 11548, 46: 13858, 47: 16168, 52: 5774, 53: 8661,
                  54: 11548,
                  55: 14436, 56: 17323, 57: 20210},
            1920: {22: 4619, 23: 6929, 24: 9239, 25: 11548, 26: 13858, 27: 16168, 32: 6929, 33: 10393, 34: 13858,
                   35: 17323,
                   36: 20787, 37: 24252, 42: 9239, 43: 13858, 44: 18478, 45: 23097, 46: 27717, 47: 32336, 52: 11548,
                   53: 17323,
                   54: 23097, 55: 28872, 56: 34646, 57: 40421},
            3840: {22: 9239, 23: 13858, 24: 18478, 25: 23097, 26: 27717, 27: 32336, 32: 13858, 33: 20787, 34: 27717,
                   35: 34646,
                   36: 41575, 37: 48505, 42: 18478, 43: 27717, 44: 36956, 45: 46195, 46: 55434, 47: 64673, 52: 23097,
                   53: 34646,
                   54: 46195, 55: 57744, 56: 69293, 57: 80842},
            7680: {22: 18478, 23: 27717, 24: 36956, 25: 46195, 26: 55434, 27: 64673, 32: 27717, 33: 41575, 34: 55434,
                   35: 69293,
                   36: 83151, 37: 97010, 42: 36956, 43: 55434, 44: 73912, 45: 92390, 46: 110869, 47: 129347, 52: 46195,
                   53: 69293, 54: 92390, 55: 115488, 56: 138586, 57: 161684},
            15360: {22: 36956, 23: 55434, 24: 73912, 25: 92390, 26: 110869, 27: 129347, 32: 55434, 33: 83151,
                    34: 110869,
                    35: 138586, 36: 166303, 37: 194021, 42: 73912, 43: 110869, 44: 147825, 45: 184781, 46: 221738,
                    47: 258694,
                    52: 92390, 53: 138586, 54: 184781, 55: 230977, 56: 277172, 57: 323368}},
        0.15: {
            960: {22: 2454, 23: 3681, 24: 4908, 25: 6135, 26: 7362, 27: 8589, 32: 3681, 33: 5521, 34: 7362, 35: 9203,
                  36: 11043,
                  37: 12884, 42: 4908, 43: 7362, 44: 9816, 45: 12270, 46: 14724, 47: 17178, 52: 6135, 53: 9203,
                  54: 12270,
                  55: 15338, 56: 18406, 57: 21473},
            1920: {22: 4908, 23: 7362, 24: 9816, 25: 12270, 26: 14724, 27: 17178, 32: 7362, 33: 11043, 34: 14724,
                   35: 18406,
                   36: 22087, 37: 25768, 42: 9816, 43: 14724, 44: 19633, 45: 24541, 46: 29449, 47: 34357, 52: 12270,
                   53: 18406,
                   54: 24541, 55: 30676, 56: 36812, 57: 42947},
            3840: {22: 9816, 23: 14724, 24: 19633, 25: 24541, 26: 29449, 27: 34357, 32: 14724, 33: 22087, 34: 29449,
                   35: 36812,
                   36: 44174, 37: 51536, 42: 19633, 43: 29449, 44: 39266, 45: 49082, 46: 58899, 47: 68715, 52: 24541,
                   53: 36812,
                   54: 49082, 55: 61353, 56: 73624, 57: 85894},
            7680: {22: 19633, 23: 29449, 24: 39266, 25: 49082, 26: 58899, 27: 68715, 32: 29449, 33: 44174, 34: 58899,
                   35: 73624,
                   36: 88348, 37: 103073, 42: 39266, 43: 58899, 44: 78532, 45: 98165, 46: 117798, 47: 137431, 52: 49082,
                   53: 73624, 54: 98165, 55: 122706, 56: 147248, 57: 171789},
            15360: {22: 39266, 23: 58899, 24: 78532, 25: 98165, 26: 117798, 27: 137431, 32: 58899, 33: 88348,
                    34: 117798,
                    35: 147248, 36: 176697, 37: 206147, 42: 78532, 43: 117798, 44: 157064, 45: 196330, 46: 235596,
                    47: 274863,
                    52: 98165, 53: 147248, 54: 196330, 55: 245413, 56: 294496, 57: 343578}}},
    1: {
        0.2: {
            960: {22: 1536, 23: 2304, 24: 3072, 25: 3840, 26: 4608, 27: 5376, 32: 2304, 33: 3456, 34: 4608, 35: 5760,
                  36: 6912, 37: 8064, 42: 3072, 43: 4608, 44: 6144, 45: 7680, 46: 9216, 47: 10752, 52: 3840, 53: 5760,
                  54: 7680, 55: 9600, 56: 11520, 57: 13440},
            1920: {22: 3072, 23: 4608, 24: 6144, 25: 7680, 26: 9216, 27: 10752, 32: 4608, 33: 6912, 34: 9216, 35: 11520,
                   36: 13824, 37: 16128, 42: 6144, 43: 9216, 44: 12288, 45: 15360, 46: 18432, 47: 21504, 52: 7680,
                   53: 11520, 54: 15360, 55: 19200, 56: 23040, 57: 26880},
            3840: {22: 6144, 23: 9216, 24: 12288, 25: 15360, 26: 18432, 27: 21504, 32: 9216, 33: 13824, 34: 18432,
                   35: 23040, 36: 27648, 37: 32256, 42: 12288, 43: 18432, 44: 24576, 45: 30720, 46: 36864, 47: 43008,
                   52: 15360, 53: 23040, 54: 30720, 55: 38400, 56: 46080, 57: 53760},
            7680: {22: 12288, 23: 18432, 24: 24576, 25: 30720, 26: 36864, 27: 43008, 32: 18432, 33: 27648, 34: 36864,
                   35: 46080, 36: 55296, 37: 64512, 42: 24576, 43: 36864, 44: 49152, 45: 61440, 46: 73728, 47: 86016,
                   52: 30720, 53: 46080, 54: 61440, 55: 76800, 56: 92160, 57: 107520},
            15360: {22: 24576, 23: 36864, 24: 49152, 25: 61440, 26: 73728, 27: 86016, 32: 36864, 33: 55296, 34: 73728,
                    35: 92160, 36: 110592, 37: 129024, 42: 49152, 43: 73728, 44: 98304, 45: 122880, 46: 147456,
                    47: 172032, 52: 61440, 53: 92160, 54: 122880, 55: 153600, 56: 184320, 57: 215040}},
        0.15: {
            960: {22: 1632, 23: 2448, 24: 3264, 25: 4080, 26: 4896, 27: 5712, 32: 2448, 33: 3672, 34: 4896, 35: 6120,
                  36: 7344, 37: 8568, 42: 3264, 43: 4896, 44: 6528, 45: 8160, 46: 9792, 47: 11424, 52: 4080, 53: 6120,
                  54: 8160, 55: 10200, 56: 12240, 57: 14280},
            1920: {22: 3264, 23: 4896, 24: 6528, 25: 8160, 26: 9792, 27: 11424, 32: 4896, 33: 7344, 34: 9792, 35: 12240,
                   36: 14688, 37: 17136, 42: 6528, 43: 9792, 44: 13056, 45: 16320, 46: 19584, 47: 22848, 52: 8160,
                   53: 12240, 54: 16320, 55: 20400, 56: 24480, 57: 28560},
            3840: {22: 6528, 23: 9792, 24: 13056, 25: 16320, 26: 19584, 27: 22848, 32: 9792, 33: 14688, 34: 19584,
                   35: 24480, 36: 29376, 37: 34272, 42: 13056, 43: 19584, 44: 26112, 45: 32640, 46: 39168, 47: 45696,
                   52: 16320, 53: 24480, 54: 32640, 55: 40800, 56: 48960, 57: 57120},
            7680: {22: 13056, 23: 19584, 24: 26112, 25: 32640, 26: 39168, 27: 45696, 32: 19584, 33: 29376, 34: 39168,
                   35: 48960, 36: 58752, 37: 68544, 42: 26112, 43: 39168, 44: 52224, 45: 65280, 46: 78336, 47: 91392,
                   52: 32640, 53: 48960, 54: 65280, 55: 81600, 56: 97920, 57: 114240},
            15360: {22: 26112, 23: 39168, 24: 52224, 25: 65280, 26: 78336, 27: 91392, 32: 39168, 33: 58752, 34: 78336,
                    35: 97920, 36: 117504, 37: 137088, 42: 52224, 43: 78336, 44: 104448, 45: 130560, 46: 156672,
                    47: 182784, 52: 65280, 53: 97920, 54: 130560, 55: 163200, 56: 195840, 57: 228480}}}
}

cpus = [
    {
        'manufacturer': 'amd',
        'name': 'EPYC 7343 (16x3.2 GHz)',
        'cores_quantity': 16,
        'cores_frequency': 3200,
        'price': 1420,
        'socket': 4094,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'amd',
        'name': 'EPYC 7513 (32x2.6 GHz)',
        'cores_quantity': 32,
        'cores_frequency': 2600,
        'price': 1200,
        'socket': 4094,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'amd',
        'name': 'EPYC 7763 (64x2.45 GHz)',
        'cores_quantity': 64,
        'cores_frequency': 2450,
        'price': 2515,
        'socket': 4094,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'amd',
        'name': 'EPYC 9354 (32x3.25 GHz)',
        'cores_quantity': 32,
        'cores_frequency': 3250,
        'price': 2400,
        'socket': 6096,
        'ram_gen': 'DDR5',
    },
    {
        'manufacturer': 'amd',
        'name': 'EPYC 9754 SP5 (128x2.25GHz)',
        'cores_quantity': 128,
        'cores_frequency': 2250,
        'price': 4200,
        'socket': 6096,
        'ram_gen': 'DDR5',
    },
    {
        'manufacturer': 'amd',
        'name': 'EPYC 9474F (48x3.6 GHz)',
        'cores_quantity': 48,
        'cores_frequency': 3600,
        'price': 4495,
        'socket': 6096,
        'ram_gen': 'DDR5',
    },
    {
        'manufacturer': 'amd',
        'name': 'EPYC 9654 (96x2.4 GHz)',
        'cores_quantity': 96,
        'cores_frequency': 2400,
        'price': 3100,
        'socket': 6096,
        'ram_gen': 'DDR5',
    },
    {
        'manufacturer': 'amd',
        'name': 'EPYC 9274F (24x4.05 GHz)',
        'cores_quantity': 24,
        'cores_frequency': 4050,
        'price': 3200,
        'socket': 6096,
        'ram_gen': 'DDR5',
    },
    {
        'manufacturer': 'intel',
        'name': 'Gold 6240 (18x2.6 GHz HT)',
        'cores_quantity': 18,
        'cores_frequency': 2600,
        'price': 1500,
        'socket': 3647,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'intel',
        'name': 'Gold 6240R (24x2.4 GHz HT)',
        'cores_quantity': 24,
        'cores_frequency': 2400,
        'price': 2000,
        'socket': 3647,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'intel',
        'name': 'Gold 6242R (20x3.1 GHz HT)',
        'cores_quantity': 20,
        'cores_frequency': 3100,
        'price': 1840,
        'socket': 3647,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'intel',
        'name': 'Gold 6248R (24x3.0 GHz HT)',
        'cores_quantity': 24,
        'cores_frequency': 3000,
        'price': 2823,
        'socket': 3647,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'intel',
        'name': 'Gold 6254 (18x3.1 GHz HT)',
        'cores_quantity': 18,
        'cores_frequency': 3100,
        'price': 3000,
        'socket': 3647,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'intel',
        'name': 'Gold 6256 (12x3.6 GHz HT)',
        'cores_quantity': 12,
        'cores_frequency': 3600,
        'price': 4200,
        'socket': 3647,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'intel',
        'name': 'Gold 6336Y (24x2.4 GHz HT)',
        'cores_quantity': 24,
        'cores_frequency': 2400,
        'price': 2174,
        'socket': 4189,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'intel',
        'name': 'Gold 6354 (18x3.0 GHz HT)',
        'cores_quantity': 18,
        'cores_frequency': 3000,
        'price': 2500,
        'socket': 4189,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'intel',
        'name': 'Gold 6444Y (16x3.6 GHz)',
        'cores_quantity': 16,
        'cores_frequency': 3600,
        'price': 3376,
        'socket': 4677,
        'ram_gen': 'DDR5',
    },
    {
        'manufacturer': 'intel',
        'name': 'Gold 6544Y (16x3.6 GHz)',
        'cores_quantity': 16,
        'cores_frequency': 3600,
        'price': 5439,
        'socket': 4677,
        'ram_gen': 'DDR5',
    },
    {
        'manufacturer': 'intel',
        'name': 'Xeon Gold 6526Y (16x2.8 GHz)',
        'cores_quantity': 16,
        'cores_frequency': 2800,
        'price': 1800,
        'socket': 4677,
        'ram_gen': 'DDR5',
    },
    {
        'manufacturer': 'intel',
        'name': 'Xeon Gold 6530 (32x2.1 GHz)',
        'cores_quantity': 32,
        'cores_frequency': 2100,
        'price': 1850,
        'socket': 4677,
        'ram_gen': 'DDR5',
    },
    # {
    #     'manufacturer': 'intel',
    #     'name': 'PLATINUM 8276 (28x2.2 GHz)',
    #     'cores_quantity': 28,
    #     'cores_frequency': 2200,
    #     'price': 7427,
    #     'socket': 3647,
    #     'ram_gen': 'DDR4',
    # },
    # {
    #     'manufacturer': 'intel',
    #     'name': 'PLATINUM 8360H (24x3.0 GHz)',
    #     'cores_quantity': 24,
    #     'cores_frequency': 3000,
    #     'price': 3214,
    #     'socket': 4189,
    #     'ram_gen': 'DDR5',
    # },
    {
        'manufacturer': 'intel',
        'name': 'Silver 4314 (16x2.4 GHz HT)',
        'cores_quantity': 16,
        'cores_frequency': 2400,
        'price': 784,
        'socket': 4189,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'intel',
        'name': 'Silver 4510 (12x2.4 GHz HT)',
        'cores_quantity': 12,
        'cores_frequency': 2400,
        'price': 863,
        'socket': 4677,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'intel',
        'name': 'Silver 4516Y+ (24x2.2 GHz HT)',
        'cores_quantity': 24,
        'cores_frequency': 2200,
        'price': 1777,
        'socket': 4677,
        'ram_gen': 'DDR4',
    },
]

servers = [
    {
        'name': 'ASUS ESC8000-G4',
        'cpu_vendor': 'intel',
        'socket': 3647,
        'max_ram': 24,
        'ram_gen': 'DDR4',
        'price': 7409,
    },
    {
        'name': 'ASUS ESC8000A-E11',
        'cpu_vendor': 'amd',
        'socket': 4094,
        'max_ram': 32,
        'ram_gen': 'DDR4',
        'price': 7100,
    },
    {
        'name': 'ASUS RS700-E10-RS12U',
        'cpu_vendor': 'intel',
        'socket': 4189,
        'max_ram': 32,
        'ram_gen': 'DDR4',
        'price': 4000,
    },
    {
        'name': 'ASUS RS700-E11-RS12U',
        'cpu_vendor': 'intel',
        'socket': 4677,
        'max_ram': 32,
        'ram_gen': 'DDR5',
        'price': 4410,
    },
    # {
    #     'name': 'ASUS RS700A-E11-RS4U 1U',
    #     'cpu_vendor': 'amd',
    #     'socket': 4094,
    #     'max_ram': 32,
    #     'ram_gen': 'DDR4',
    #     'price': 2370,
    # },
    {
        'name': 'ASUS RS700A-E12-RS12U',
        'cpu_vendor': 'amd',
        'socket': 6096,
        'max_ram': 24,
        'ram_gen': 'DDR5',
        'price': 5500,
    },
    {
        'name': 'ASUS RS720-E11-RS24',
        'cpu_vendor': 'intel',
        'socket': 4677,
        'max_ram': 32,
        'ram_gen': 'DDR5',
        'price': 6525,
    },
    {
        'name': 'ASUS RS720-E10-RS24U 2U',
        'cpu_vendor': 'intel',
        'socket': 4189,
        'max_ram': 32,
        'ram_gen': 'DDR4',
        'price': 6846,
    },
    {
        'name': 'ASUS RS720-E11-RS12U',
        'cpu_vendor': 'intel',
        'socket': 4677,
        'max_ram': 32,
        'ram_gen': 'DDR5',
        'price': 6425,
    },
    {
        'name': 'ASUS RS720A-E11-RS12 2U',
        'cpu_vendor': 'amd',
        'socket': 4094,
        'max_ram': 32,
        'ram_gen': 'DDR4',
        'price': 6000,
    },
    {
        'name': 'ASUS RS720A-E11-RS24U',
        'cpu_vendor': 'amd',
        'socket': 4094,
        'max_ram': 32,
        'ram_gen': 'DDR4',
        'price': 7000,
    },
    {
        'name': 'ASUS RS720A-E12-RS12',
        'cpu_vendor': 'amd',
        'socket': 6096,
        'max_ram': 24,
        'ram_gen': 'DDR5',
        'price': 6259,
    },
    {
        'name': 'ASUS RS720A-E12-RS24U',
        'cpu_vendor': 'amd',
        'socket': 6096,
        'max_ram': 24,
        'ram_gen': 'DDR5',
        'price': 8285,
    },
    {
        'name': 'Gigabyte R282-3C0 2U',
        'cpu_vendor': 'intel',
        'socket': 4189,
        'max_ram': 32,
        'ram_gen': 'DDR4',
        'price': 2490,
    },
    {
        'name': 'Gigabyte R292-4S0',
        'cpu_vendor': 'intel',
        'socket': 4189,
        'max_ram': 48,
        'ram_gen': 'DDR4',
        'price': 6850,
    },
    # {
    #     'name': 'Inspur NF5280A6',
    #     'cpu_vendor': 'amd',
    #     'socket': 4094,
    #     'max_ram': 32,
    #     'ram_gen': 'DDR4',
    #     'price': 5347,
    # },
    # {
    #     'name': 'Inspur NF5280M5',
    #     'cpu_vendor': 'intel',
    #     'socket': 3647,
    #     'max_ram': 24,
    #     'ram_gen': 'DDR4',
    #     'price': 5200,
    # },
    # {
    #     'name': 'Inspur NF5280M6',
    #     'cpu_vendor': 'intel',
    #     'socket': 4189,
    #     'max_ram': 32,
    #     'ram_gen': 'DDR4',
    #     'price': 6000,
    # },
    # {
    #     'name': 'INTEL M50CYP1UR212',
    #     'cpu_vendor': 'intel',
    #     'socket': 4189,
    #     'max_ram': 32,
    #     'ram_gen': 'DDR4',
    #     'price': 2320,
    # },
    # {
    #     'name': 'INTEL M50CYP2UR312',
    #     'cpu_vendor': 'intel',
    #     'socket': 4189,
    #     'max_ram': 32,
    #     'ram_gen': 'DDR4',
    #     'price': 2890,
    # },
    # {
    #     'name': 'INTEL R1208WFTZSR',
    #     'cpu_vendor': 'intel',
    #     'socket': 3647,
    #     'max_ram': 24,
    #     'ram_gen': 'DDR4',
    #     'price': 3805,
    # },
    # {
    #     'name': 'INTEL R2312WFTZSR',
    #     'cpu_vendor': 'intel',
    #     'socket': 3647,
    #     'max_ram': 24,
    #     'ram_gen': 'DDR4',
    #     'price': 1605,
    # },
    {
        'name': 'SUPERMICRO SYS-121H-TNR',
        'cpu_vendor': 'intel',
        'socket': 4677,
        'max_ram': 32,
        'ram_gen': 'DDR5',
        'price': 8500,
    },
    {
        'name': 'SUPERMICRO AS-1125HS-TNR',
        'cpu_vendor': 'amd',
        'socket': 6096,
        'max_ram': 24,
        'ram_gen': 'DDR5',
        'price': 7000,
    },
    {
        'name': 'SUPERMICRO SYS-4029GP-TRT',
        'cpu_vendor': 'intel',
        'socket': 3647,
        'max_ram': 24,
        'ram_gen': 'DDR4',
        'price': 7500,
    },
    {
        'name': 'SUPERMICRO SYS-221H-TN24R',
        'cpu_vendor': 'intel',
        'socket': 4677,
        'max_ram': 32,
        'ram_gen': 'DDR5',
        'price': 12000,
    },
    {
        'name': 'X12DPI',
        'cpu_vendor': 'intel',
        'socket': 4189,
        'max_ram': 16,
        'ram_gen': 'DDR4',
        'price': 2700,
    },
    {
        'name': 'X11DPI',
        'cpu_vendor': 'intel',
        'socket': 3647,
        'max_ram': 16,
        'ram_gen': 'DDR4',
        'price': 2700,
    },
    {
        'name': 'H12DSI',
        'cpu_vendor': 'amd',
        'socket': 4094,
        'max_ram': 16,
        'ram_gen': 'DDR4',
        'price': 2700,
    },
]

rams = [
    {
        'ram_gen': 'DDR4',
        'ram_size': 32,
        'price': 120
    },
    {
        'ram_gen': 'DDR4',
        'ram_size': 64,
        'price': 245
    },
    {
        'ram_gen': 'DDR4',
        'ram_size': 128,
        'price': 684
    },
    {
        'ram_gen': 'DDR5',
        'ram_size': 32,
        'price': 137
    },
    {
        'ram_gen': 'DDR5',
        'ram_size': 64,
        'price': 280
    },
    {
        'ram_gen': 'DDR5',
        'ram_size': 128,
        'price': 1250
    },

]

esxi_disc = {
    'type': '512Gb sata/m2',
    'price': 60
}

cache_disc = {
    'type': 'nvme',
    'size': '1.6-3.2Gb',
    'vendor': 'micron 7450',
    'price': 300
}

network_card = {
    'name': '25GB DUAL MCX512A',
    'price': 270,
}

hba_adapter = {
    8: {
        'name': 'LSI9300-8i',
        'spec': 8,
        'price': 330,
    },
    16: {
        'name': 'LSI9560-16i',
        'spec': 16,
        'price': 1100,
    }
}

capacity_disks = {
    'ssd': {
        960: {
            'name': 'Micron 5300 Pro',
            'price': 160
        },
        1920: {
            'name': 'Micron 5300 Pro',
            'price': 300
        },
        3840: {
            'name': 'Micron 5300 Pro',
            'price': 670
        },
        7680: {
            'name': 'Micron 5300 Pro',
            'price': 1300
        },
        15360: {
            'name': 'Micron 7400 PRO',
            'price': 2000
        },
    },
    'nvme': {
        960: {
            'name': 'Micron 7400 PRO',
            'price': 320
        },
        1920: {
            'name': 'Micron 7400 PRO',
            'price': 475
        },
        3840: {
            'name': 'Micron 7400 PRO',
            'price': 700
        },
        7680: {
            'name': 'Micron 7400 PRO',
            'price': 1500
        },
        15360: {
            'name': 'Micron 7400 PRO',
            'price': 2600
        },
    }
}

# GPUСтоимостьСтоимость1ед.Тех.показателиCUDAядра
# Нет    $0
# NvidiaT4    $1 500    $94 16 2560
# NvidiaA2    $650    $41 16 1280
# Nvidia A10    $3 700    $154 24 9216
