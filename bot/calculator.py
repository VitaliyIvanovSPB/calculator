import math

from .get_data import (get_esxi_disks, get_cpus_filtered, get_servers_filtered, get_rams_filtered, get_cache_disks,
                       get_network_cards, get_hba_adapters, get_capacity_disks, get_raid_config, get_raids_data,
                       get_parameters, get_works_coefficient)

parameters = get_parameters()


def get_works_price(hosts_qty: int, main: str, additional: str):
    coefficients = [8, 16, 24, 32, 64, 96, 128]
    index = next((i for i, limit in enumerate(coefficients) if hosts_qty < limit), -1)

    if index == -1:
        return "Очень много."

    return parameters['works_base'] * (
                get_works_coefficient()[main][index] + get_works_coefficient()[additional][index])


def get_switches_price(value: int, ports_qty: list):
    coefficients = [0.125, 0.25, 0.5, 1, 2, 3, 4]
    index = next((coefficients[i] for i, limit in enumerate(ports_qty) if value <= limit), -1)
    if index == -1:
        return "Больше 4х"

    return index


def get_network_coefficient(value):
    ports_map = {6: 0.125, 12: 0.25, 24: 0.5, 48: 1, 72: 1.5, 96: 2, 120: 2.5, 144: 3, 168: 3.5, 192: 4, 216: 5}
    return next((v for k, v in ports_map.items() if value <= k), "Больше 5х")


def get_network_ipmi_coefficient(value):
    ports_map = {6: 0.125, 12: 0.25, 24: 0.5, 48: 1, 96: 2, 144: 3, 240: 4}
    return next((v for k, v in ports_map.items() if value <= k), "Больше 5х")


def get_network_price(host_qty: int, network_card_qty: int):
    network = get_network_coefficient(host_qty * network_card_qty * 2)
    network_ipmi = get_network_ipmi_coefficient(host_qty * network_card_qty)
    return network * parameters['switches'] + network_ipmi * parameters['switches_ipmi']


def get_ram_in_host(cpu_hosts, ram, vram):
    ram_host = math.ceil(vram / parameters['max_ram_usage'] / cpu_hosts / ram['ram_size'])
    return ram_host + (ram_host % 2)


def get_vsan_disks_price(capacity_disk_type, disk_size, disks_qty, cache_disc, capacity_disks):
    host_cache_disks_price = cache_disc['price'] * int(str(disks_qty)[0])
    host_capacity_disks_price = capacity_disks[capacity_disk_type][disk_size]['price'] * int(
        str(disks_qty)[1]) * int(str(disks_qty)[0])
    return host_cache_disks_price + host_capacity_disks_price


def check_vsan_and_disks_limit(cpu_hosts, disks_capacity, host_disks_qty, server, vsan_raw, vssd):
    min_vsan_condition = vssd <= disks_capacity * cpu_hosts
    max_vsan_condition = disks_capacity * cpu_hosts < vsan_raw * 1.2
    disks_limit_condition = host_disks_qty < server['max_disks_qty']
    return min_vsan_condition and max_vsan_condition and disks_limit_condition


def create_config(all_configs, capacity_disk_type, cpu, cpu_hosts, cpu_overcommit, network_card_qty, ram, ram_1host,
                  server, slack_space, vssd, works_add, works_main, currency):
    esxi_disc = get_esxi_disks()
    cache_disc = get_cache_disks()[0]
    network_card = get_network_cards()[0]
    hba_adapter = get_hba_adapters()
    capacity_disks = get_capacity_disks()
    raid_config = get_raid_config()
    cpu_hosts_n = cpu_hosts + 1
    key = 6 if cpu_hosts_n >= 6 else (5 if cpu_hosts_n == 5 else 1)
    vsan_raw = vssd * raid_config[key]['disk_usage_overhead'] / (1 - slack_space)

    for disk_size, disk_groups in get_raids_data()[key][slack_space].items():
        for disk_group, disks_capacity in disk_groups.items():
            host_disks_qty = int(str(disk_group)[0]) * int(str(disk_group)[1]) + int(str(disk_group)[0])
            host_disks_hba_qty = int(str(disk_group)[0]) * int(str(disk_group)[1])
            vsan_and_disks_limit = check_vsan_and_disks_limit(cpu_hosts, disks_capacity, host_disks_qty, server,
                                                              vsan_raw, vssd)
            if vsan_and_disks_limit:
                hba = hba_adapter[8] if host_disks_hba_qty < 9 else hba_adapter[16]
                vsan_disks_price = get_vsan_disks_price(capacity_disk_type=capacity_disk_type, disk_size=disk_size,
                                                        disks_qty=disk_group, cache_disc=cache_disc,
                                                        capacity_disks=capacity_disks)
                host_price = (cpu['price'] * 2 + server['price'] + ram_1host * ram['price'] +
                              esxi_disc[capacity_disk_type]['price'] + network_card['price'] + vsan_disks_price +
                              hba['price'])
                rms = math.ceil(host_price * currency / parameters['payback_period'] * parameters['coefficient'])
                vmware = rms * cpu_hosts_n
                works = math.ceil(
                    get_works_price(hosts_qty=cpu_hosts_n, main=works_main, additional=works_add))
                network_price = math.ceil(get_network_price(host_qty=cpu_hosts_n,
                                                            network_card_qty=network_card_qty))
                total_price = vmware + works + network_price

                vcpu_available = math.ceil(
                    (cpu["cores_quantity"] * 2 * cpu_hosts * cpu_overcommit * parameters['max_cpu_usage']))
                vram_available = math.ceil(ram_1host * ram["ram_size"] * cpu_hosts * parameters['max_ram_usage'])
                all_configs.append({
                    'Need hosts by CPU(n+1)': cpu_hosts_n,
                    'AllFlash vSAN': raid_config[key]['FTM'],
                    'Failures to Tolerate': raid_config[key]['FTT'],
                    'CPU overcommit': f'{cpu_overcommit}',
                    'CPU': f'{cpu["name"]} {cpu["price"]}$ - 2 шт',
                    'Server': f'{server["name"]} {server["price"]}$ - 1 шт',
                    f'{ram["ram_size"]}Gb {ram["ram_gen"]} {ram["price"]}$': f'{ram_1host} шт',
                    'Esxi disk': f'{esxi_disc[capacity_disk_type]["type"]} '
                                 f'{esxi_disc[capacity_disk_type]["price"]}$ - 1 шт',
                    'Cache disk': f'{cache_disc["size"]} {cache_disc["type"]} {cache_disc["price"]}$ - '
                                  f'{int(str(disk_group)[0])} шт',
                    'Capacity disk': f'{disk_size} {capacity_disk_type} '
                                     f'{capacity_disks[capacity_disk_type][disk_size]["name"]} '
                                     f'{capacity_disks[capacity_disk_type][disk_size]["price"]}$ - '
                                     f'{int(str(disk_group)[1]) * int(str(disk_group)[0])} шт',
                    'Network card': f'{network_card["name"]} {network_card["price"]}$ - {network_card_qty} шт',
                    'HBA adapter': f'{hba["name"]} {hba["price"]}$ - 1 шт',
                    'Admin main works': f'{works_main}',
                    'Additional works': f'{works_add}',
                    'Works price': f'{works} руб.',
                    'Network': f'{network_price} руб.',
                    'vCPU available': f'{vcpu_available}',
                    'vRAM available': f'{vram_available}',
                    'vSSD available': f'{disks_capacity * cpu_hosts}',
                    'vSSD raw': f'{vsan_raw}',
                    '1 host rms, Rub': f'{rms} руб.',
                    'Total price, Rub': f'{total_price} руб.',
                    'USD/RUB': f'{currency} руб.',
                })





def requested_config(vcpu: int, vram: int, vssd: int, cpu_vendor: str, cpu_min_frequency: int, cpu_overcommit: float,
                     works_main: str, works_add: str, network_card_qty: int, slack_space:float, capacity_disk_type: str,
                     currency: int):
    all_configs = []
    for cpu in get_cpus_filtered(cpu_vendor=cpu_vendor, cpu_min_frequency=cpu_min_frequency):
        for server in get_servers_filtered(socket_filter=cpu['socket']):
            for ram in get_rams_filtered(server['ram_gen']):
                cpu_hosts = math.ceil(vcpu / cpu_overcommit / (cpu['cores_quantity'] * 2 * parameters['max_cpu_usage']))
                ram_1host = get_ram_in_host(cpu_hosts, ram, vram)
                if ram_1host > server['max_ram']:
                    continue

                create_config(all_configs, capacity_disk_type, cpu, cpu_hosts, cpu_overcommit, network_card_qty, ram,
                              ram_1host, server, slack_space, vssd, works_add, works_main, currency)

    sorted_configs = sorted(all_configs, key=lambda x: int(x['Total price, Rub'].split(' ')[0]))

    return sorted_configs


if __name__ == '__main__':
    print(requested_config(vcpu=3900, vram=8000, vssd=2200, cpu_min_frequency=3000, cpu_overcommit=5, cpu_vendor='any',
                           network_card_qty=1, works_main='vSphere', works_add='Нет', slack_space=0.2,
                           capacity_disk_type='nvme', currency=100))
