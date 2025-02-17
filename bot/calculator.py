import math

from .data import (cpus, rams, servers, esxi_disc, network_card, works_base, works_coefficient, max_cpu_usage,
                   max_ram_usage, payback_period, coefficient, currency, switches, switches_ipmi, raid_config, RAIDS,
                   cache_disc, capacity_disks, hba_adapter)


def get_works_price(hosts_qty: int, main: str, additional: str):
    coefficients = [8, 16, 24, 32, 64, 96, 128]
    index = next((i for i, limit in enumerate(coefficients) if hosts_qty < limit), -1)

    if index == -1:
        return "Очень много."

    return works_base * (works_coefficient[main][index] + works_coefficient[additional][index])


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
    network_price = network * switches + network_ipmi * switches_ipmi
    return network_price


def get_ram_in_host(cpu_hosts, ram, vram):
    ram_host = math.ceil(vram / max_ram_usage / cpu_hosts / ram['ram_size'])
    return ram_host + (ram_host % 2)


def get_vsan_disks_price(capacity_disk_type, disk_size, disks_qty):
    host_cache_disks_price = cache_disc['price'] * int(str(disks_qty)[0])
    host_capacity_disks_price = capacity_disks[capacity_disk_type][disk_size]['price'] * int(
        str(disks_qty)[1]) * int(str(disks_qty)[0])
    return host_cache_disks_price + host_capacity_disks_price


def create_config(all_configs, capacity_disk_type, cpu, cpu_hosts, cpu_overcommit, network_card_qty, ram, ram_1host,
                  server, slack_space, vssd, works_add, works_main):
    cpu_hosts_n = cpu_hosts + 1
    key = 6 if cpu_hosts_n >= 6 else (5 if cpu_hosts_n == 5 else 1)
    config = raid_config[key]
    vsan_raw = vssd * config['disk_usage_overhead'] / (1 - slack_space)
    for disk_size, disk_groups in RAIDS[key][slack_space].items():
        for disk_group, disks_capacity in disk_groups.items():
            host_disks_qty = int(str(disk_group)[0]) * int(str(disk_group)[1])

            min_vsan_condition = vssd <= disks_capacity * cpu_hosts
            max_vsan_condition = disks_capacity * cpu_hosts < vsan_raw * 1.2
            disks_limit_condition = host_disks_qty < server['max_disks_qty']
            if min_vsan_condition and max_vsan_condition and disks_limit_condition:
                hba = hba_adapter[8] if host_disks_qty < 9 else hba_adapter[16]
                vsan_disks_price = get_vsan_disks_price(capacity_disk_type, disk_size, disk_group)
                host_price = (cpu['price'] * 2 + server['price'] + ram_1host * ram['price'] +
                              esxi_disc['price'] + network_card['price'] + vsan_disks_price +
                              hba['price'])
                rms = math.ceil(host_price * currency / payback_period * coefficient)
                vmware = rms * cpu_hosts_n
                works = math.ceil(
                    get_works_price(hosts_qty=cpu_hosts_n, main=works_main, additional=works_add))
                network_price = math.ceil(get_network_price(host_qty=cpu_hosts_n,
                                                            network_card_qty=network_card_qty))
                total_price = vmware + works + network_price

                all_configs.append({
                    'Need hosts by CPU(n+1)': cpu_hosts_n,
                    'AllFlash vSAN': config['FTM'],
                    'Failures to Tolerate': config['FTT'],
                    'CPU overcommit': f'{cpu_overcommit}',
                    'CPU': f'{cpu["name"]} - 2 шт',
                    'Server': f'{server["name"]} - 1 шт',
                    f'{ram["ram_size"]}Gb {ram["ram_gen"]}': f'{ram_1host} шт',
                    'Esxi disk': f'{esxi_disc["type"]} - 1 шт',
                    'Cache disk': f'{cache_disc['size']} {cache_disc['type']} {cache_disc['vendor']} - {int(str(disk_group)[0])} шт',
                    'Capacity disk': f'{disk_size} {capacity_disk_type} {capacity_disks[capacity_disk_type][disk_size]['name']} - {int(str(disk_group)[1])} шт',
                    'Network card': f'{network_card["name"]} - {network_card_qty} шт',
                    'HBA adapter': f'{hba["name"]} - 1 шт',
                    'Admin main works': works_main,
                    'Additional works': works_add,
                    'Works price': f'{works} руб.',
                    'Network': f'{network_price} руб.',
                    'vCPU available': f'{math.ceil((cpu["cores_quantity"] * 2 * cpu_hosts * cpu_overcommit * max_cpu_usage))}',
                    'vRAM available': f'{math.ceil(ram_1host * ram["ram_size"] * cpu_hosts * max_ram_usage)}',
                    'vSSD available': f'{disks_capacity * cpu_hosts}',
                    '1 host rms, Rub': f'{rms} руб.',
                    'Total price, Rub': f'{total_price} руб.', })


def format_top_configs(sorted_configs):
    top5 = []
    for index, config in enumerate(sorted_configs, 1):
        conf = [f'\nТоп {index}:\n']
        for key, value in config.items():
            conf.append(f'{key}: {value}\n')
        top5.append(conf)
    return ''.join([item for sublist in top5 for item in sublist])


def requested_config(vcpu: int, vram: int, vssd: int, cpu_vendor: str, cpu_min_frequency: int, cpu_overcommit: int,
                     works_main: str, works_add: str, network_card_qty: int, slack_space, capacity_disk_type: str):
    all_configs = []
    filtered_cpu_list = [cpu for cpu in cpus if (cpu_vendor == 'any' or cpu['manufacturer'] == cpu_vendor) and cpu[
        'cores_frequency'] >= cpu_min_frequency]
    for cpu in filtered_cpu_list:
        cpu_hosts = math.ceil(vcpu / cpu_overcommit / (cpu['cores_quantity'] * 2 * max_cpu_usage))
        filtered_servers = [s for s in servers if s['socket'] == cpu['socket']]
        for server in filtered_servers:
            filtered_rams = [r for r in rams if r['ram_gen'] == server['ram_gen']]
            for ram in filtered_rams:
                ram_1host = get_ram_in_host(cpu_hosts, ram, vram)
                if ram_1host > server['max_ram']:
                    continue

                create_config(all_configs, capacity_disk_type, cpu, cpu_hosts, cpu_overcommit, network_card_qty, ram,
                              ram_1host, server, slack_space, vssd, works_add, works_main)

    sorted_configs = sorted(all_configs, key=lambda x: int(x['Total price, Rub'].split(' ')[0]))[:5]

    return format_top_configs(sorted_configs)


if __name__ == '__main__':
    print(requested_config(vcpu=3900, vram=8000, vssd=2200, cpu_min_frequency=3000, cpu_overcommit=5, cpu_vendor='any',
                           network_card_qty=1, works_main='vSphere', works_add='Нет'))
