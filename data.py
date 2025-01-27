
cpus_intel = [
    {
        'manufacturer': 'intel',
        'name': 'Gold 6336Y',
        'cores_quantity': 24,
        'cores_frequency': 2400,
        'price': 2174,
        'socket': 4189,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'intel',
        'name': 'Silver 4314',
        'cores_quantity': 16,
        'cores_frequency': 2400,
        'price': 784,
        'socket': 4189,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'intel',
        'name': 'Gold 6444Y',
        'cores_quantity': 16,
        'cores_frequency': 3600,
        'price': 3376,
        'socket': 4677,
        'ram_gen': 'DDR5',
    },
    {
        'manufacturer': 'intel',
        'name': 'Silver 4516Y+',
        'cores_quantity': 24,
        'cores_frequency': 2200,
        'price': 1777,
        'socket': 4677,
        'ram_gen': 'DDR5',
    },
    {
        'manufacturer': 'intel',
        'name': 'Gold 6544',
        'cores_quantity': 16,
        'cores_frequency': 3650,
        'price': 5439,
        'socket': 4677,
        'ram_gen': 'ddr5',
    },
]
cpus_amd = [
    {
        'manufacturer': 'amd',
        'name': 'EPYC 7343',
        'cores_quantity': 16,
        'cores_frequency': 3200,
        'price': 1420,
        'soket': 4094,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'amd',
        'name': 'EPYC 7513',
        'cores_quantity': 32,
        'cores_frequency': 2600,
        'price': 1200,
        'soket': 4094,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'amd',
        'name': 'EPYC 7763',
        'cores_quantity': 64,
        'cores_frequency': 2450,
        'price': 2515,
        'soket': 4094,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'amd',
        'name': 'EPYC 9354',
        'cores_quantity': 32,
        'cores_frequency': 3250,
        'price': 2400,
        'soket': 6096,
        'ram_gen': 'DDR4',
    },
    {
        'manufacturer': 'amd',
        'name': 'EPYC 9274',
        'cores_quantity': 24,
        'cores_frequency': 4050,
        'price': 3200,
        'soket': 6096,
        'ram_gen': 'DDR5',
    },
]

servers = [
    {
        'name': 'ASUS RS720 - E11 - RS12U',
        'cpu_vendor': 'intel',
        'socket': 4677,
        'max_ram': 32,
        'ram_gen': 'ddr5',
        'price': 5000,
    },
    {
        'name': 'ASUS RS700 - E11 - RS12U',
        'cpu_vendor': 'intel',
        'socket': 4677,
        'max_ram': 32,
        'ram_gen': 'ddr5',
        'price': 4400,
    },
    {
        'name': 'ASUS RS720A - E11 - RS12',
        'cpu_vendor': 'amd',
        'socket': 4094,
        'max_ram': 32,
        'ram_gen': 'ddr4',
        'price': 6000,
    },
    {
        'name': 'ASUS RS720A - E11 - RS24U',
        'cpu_vendor': 'amd',
        'socket': 4094,
        'max_ram': 32,
        'ram_gen': 'ddr4',
        'price': 7000,
    },
    {
        'name': 'ASUS RS720A - E12 - RS12',
        'cpu_vendor': 'amd',
        'socket': 6096,
        'max_ram': 24,
        'ram_gen': 'ddr5',
        'price': 6259,
    },
    {
        'name': 'ASUS RS720A - E12 - RS24',
        'cpu_vendor': 'amd',
        'socket': 6096,
        'max_ram': 24,
        'ram_gen': 'ddr5',
        'price': 7200,
    },
    {
        'name': 'ASUS RS700 - E10 - RS12U',
        'cpu_vendor': 'intel',
        'socket': 4189,
        'max_ram': 32,
        'ram_gen': 'ddr4',
        'price': 4000,
    },
    {
        'name': 'Gigabyte R282',
        'cpu_vendor': 'intel',
        'socket': 4189,
        'max_ram': 32,
        'ram_gen': 'ddr4',
        'price': 2490,
    },

]

ram = [
    {
        'ram_gen': 'ddr4',
        'ram_size': 32,
        'price': 120
    },
    {
        'ram_gen': 'ddr4',
        'ram_size': 64,
        'price': 245
    },
    {
        'ram_gen': 'ddr4',
        'ram_size': 128,
        'price': 684
    },
    {
        'ram_gen': 'ddr5',
        'ram_size': 32,
        'price': 137
    },
    {
        'ram_gen': 'ddr5',
        'ram_size': 64,
        'price': 280
    },
    {
        'ram_gen': 'ddr5',
        'ram_size': 128,
        'price': 1250
    },

]

esxi_disc = [
    {
        'type': 'sata',
        'size': '480',
        'vendor': 'micron 5300',
        'price': '100'
    },
    {
        'type': 'm2',
        'size': '512',
        'vendor': 'intel 670p',
        'price': '100'
    },
]

cache_disc = [
    {
        'type': 'nvme',
        'size': '1.6-3.2',
        'vendor': 'micron 7450',
        'price': '300'
    },
]

#
# Диски
# Capacite: СтоимостьСтоимость1ед.Тех.показатели
# Нет    $0
# satahdd: 2ТБHDDSATA    $133    $0, 065 2048
# satassd: 960GBMicron5300Pro    $160    $0, 167 960
# satassd: 1.92TbMicron5300Pro    $300    $0, 156 1920
# satassd: 3.84TbMicron5300PRO    $670    $0, 174 3840
# satassd: 7.68TbMicron5300PRO    $1 300    $0, 169 7680
# ssdnvme: 960GBMicron7400PRO    $320    $0, 333 960
# ssdnvme: 1.92TbMicron7300PRO    $475    $0, 247 1920
# ssdnvme: 3.84TbMicron7400Pro    $700    $0, 182 3840
# ssdnvme: 7.68TbMicron7400Pro    $1 500    $0, 195 7680
# ssdnvme: 15.36TbNVMeEnterpriseSamsung    $2 600    $0, 169 15360
#
# СетеваякартаPCI: СтоимостьСтоимость1ед.Тех.показатели
# Нет    $0
# 2x10GBDUALMCX4121A - XCAT    $110    $110 10G, SFP28
# 2 × 25GEDUALMCX4121A - ACAT    $170    $170 10 / 25G, SFP28
# 2 × 25GBDUALMCX512A - ACAT    $270    $270 10 / 25G, SFP28
# 2 × 25GBDUALMCX512F - ACAT    $270    $270 25G, SFP28
#
# HBA
# PCI: СтоимостьСтоимость1ед.Тех.показатели
# Нет
# hbacontroller: LSI9300 -8i    $330    $330 SAS / SATA HBAадаптер
# hbacontroller: LSI9560 - 16i    $1100    $1100 NVMe / SAS / SATARAIDконтроллер
#
# GPUСтоимостьСтоимость1ед.Тех.показателиCUDAядра
# Нет    $0
# NvidiaT4    $1 500    $94 16 2560
# NvidiaA2    $650    $41 16 1280
# Nvidia A10    $3 700    $154 24 9216
# Nvidia A16    $3 550    $55 64 7168
