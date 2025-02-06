import math
from .data import cpus, rams, servers, esxi_disc, network_card, works_base, works_coefficient, max_cpu_usage, \
    max_ram_usage, payback_period, coefficient, currency, switches, switches_ipmi


# def get_cpus(vendor: str, min_frequency: int):
#     if vendor == 'any':
#         return [cpu for cpu in cpus if cpu['cores_frequency'] >= min_frequency]
#     else:
#         return [cpu for cpu in cpus if cpu['manufacturer'] == vendor and cpu['cores_frequency'] >= min_frequency]

def get_cpus(vendor: str, min_frequency: int):
    return [cpu for cpu in cpus if
            (vendor == 'any' or cpu['manufacturer'] == vendor) and cpu['cores_frequency'] >= min_frequency]


# def get_works_price(hosts_qty: int, main: str, additional: str):
#     if hosts_qty < 8:
#         return works_base * (works_coefficient[main][0] + works_coefficient[additional][0])
#     elif hosts_qty < 16:
#         return works_base * (works_coefficient[main][1] + works_coefficient[additional][1])
#     elif hosts_qty < 24:
#         return works_base * (works_coefficient[main][2] + works_coefficient[additional][2])
#     elif hosts_qty < 32:
#         return works_base * (works_coefficient[main][3] + works_coefficient[additional][3])
#     elif hosts_qty < 64:
#         return works_base * (works_coefficient[main][4] + works_coefficient[additional][4])
#     elif hosts_qty < 96:
#         return works_base * (works_coefficient[main][5] + works_coefficient[additional][5])
#     elif hosts_qty < 128:
#         return works_base * (works_coefficient[main][6] + works_coefficient[additional][6])
#     else:
#         return 'Очень много.'

def get_works_price(hosts_qty: int, main: str, additional: str):
    coefficients = [8, 16, 24, 32, 64, 96, 128]
    index = next((i for i, limit in enumerate(coefficients) if hosts_qty < limit), -1)

    if index == -1:
        return "Очень много."

    return works_base * (works_coefficient[main][index] + works_coefficient[additional][index])


# def get_switches_price(hosts_qty: int, network_card_qty: int):
#     value = hosts_qty * network_card_qty * 2
#
#     if value <= 12:
#         return 0.125
#     elif value <= 24:
#         return 0.25
#     elif value <= 48:
#         return 0.5
#     elif value <= 96:
#         return 1
#     elif value <= 192:
#         return 2
#     elif value <= 288:
#         return 3
#     elif value <= 384:
#         return 4
#     else:
#         return "Больше 4х"


# def get_ipmi_switches_prices(hosts_qty: int, network_card_qty: int):
#     value = hosts_qty * network_card_qty
#
#     if value <= 6:
#         return 0.125
#     elif value <= 12:
#         return 0.25
#     elif value <= 24:
#         return 0.5
#     elif value <= 48:
#         return 1
#     elif value <= 96:
#         return 2
#     elif value <= 144:
#         return 3
#     elif value <= 240:
#         return 4
#     else:
#         return "Больше 4х"


def get_switches_price(value: int, ports_qty: list):
    coefficients = [0.125, 0.25, 0.5, 1, 2, 3, 4]
    index = next((coefficients[i] for i, limit in enumerate(ports_qty) if value <= limit), -1)
    if index == -1:
        return "Больше 4х"

    return index


def get_network_price(host_qty: int, network_card_qty: int):
    coefficients = [0.125, 0.25, 0.5, 1, 2, 3, 4]
    ports_qty = [12, 24, 48, 96, 192, 288, 384]
    ports_ipmi_qty = [6, 12, 24, 48, 96, 144, 240]

    ports = host_qty * network_card_qty * 2
    network = next((coefficients[i] for i, limit in enumerate(ports_qty) if ports <= limit), -1)
    if network == -1:
        return "Больше 4х"

    ports_ipmi = host_qty * network_card_qty
    network_ipmi = next((coefficients[i] for i, limit in enumerate(ports_ipmi_qty) if ports_ipmi <= limit), -1)
    if network_ipmi == -1:
        return "Больше 4х"

    return network * switches + network_ipmi * switches_ipmi


def requested_config(vcpu: int, vram: int, vssd: int, cpu_vendor: str, cpu_min_frequency: int, cpu_overcommit: int,
                     works_main: str, works_add: str, network_card_qty: int):
    all_configs = {}
    cpu_list = get_cpus(cpu_vendor, cpu_min_frequency)

    for cpu in cpu_list:
        cpu_hosts = math.ceil(vcpu / cpu_overcommit / (cpu['cores_quantity'] * 2 * max_cpu_usage))

        for server in filter(lambda s: s['socket'] == cpu['socket'], servers):
            for ram in filter(lambda r: r['ram_gen'] == server['ram_gen'], rams):
                ram_host = math.ceil(vram / max_ram_usage / cpu_hosts / ram['ram_size'])
                ram_1host = ram_host + (ram_host % 2)
                if ram_1host > server['max_ram']:
                    continue

                # TODO:
                # vsan
                vsan = vssd+1

                cpu_hosts_n = cpu_hosts + 1
                host_price = (cpu['price'] * 2 + server['price'] + ram_1host * ram['price'] + esxi_disc['price'] +
                              network_card['price'])
                rms = math.ceil(host_price * currency / payback_period * coefficient)
                vmware = rms * cpu_hosts_n
                works = math.ceil(get_works_price(hosts_qty=cpu_hosts_n, main=works_main, additional=works_add))
                # network_price = math.ceil(
                #     get_switches_price(value=(cpu_hosts + 1) * network_card_qty * 2,
                #                        ports_qty=[12, 24, 48, 96, 192, 288, 384]) * switches
                #     + get_switches_price(value=(cpu_hosts + 1) * network_card_qty,
                #                          ports_qty=[6, 12, 24, 48, 96, 144, 240]) * switches_ipmi
                # )
                network_price = math.ceil(get_network_price(host_qty=cpu_hosts_n,
                                                            network_card_qty=network_card_qty))
                # network_price = math.ceil((get_switches_price(cpu_hosts + 1, network_card_qty) * switches
                #                            + get_ipmi_switches_prices(cpu_hosts + 1, network_card_qty) * switches_ipmi))
                total_price = vmware + works + network_price

                all_configs[len(all_configs)] = {'Need hosts by CPU(n+1)': cpu_hosts_n,
                                                 'CPU overcommit': f'{cpu_overcommit}',
                                                 'CPU': f'{cpu["name"]} - 2 шт',
                                                 'Server': f'{server["name"]} - 1 шт',
                                                 f'{ram["ram_size"]}Gb {ram["ram_gen"]}': f'{ram_1host} шт',
                                                 'Esxi disk': f'{esxi_disc["type"]} - 1 шт',
                                                 'Network card': f'{network_card["name"]} - {network_card_qty} шт',
                                                 'Admin main works': works_main,
                                                 'Additional works': works_add,
                                                 'Works price': f'{works} руб.',
                                                 'Network': f'{network_price} руб.',
                                                 '1 host rms, Rub': f'{rms} руб.',
                                                 'Total price, Rub': f'{total_price} руб. ',
                                                 }

    sorted_configs = sorted(all_configs.items(), key=lambda x: int(x[1]['Total price, Rub'].split(' ')[0]))[:5]
    top5 = []
    for index, (config_id, config) in enumerate(sorted_configs, 1):
        conf = [f'\nТоп {index}: Вариант {config_id}\n']
        for key, value in config.items():
            conf.append(f'{key}: {value}\n')
        # print(''.join(conf))
        top5.append(conf)
    return [item for sublist in top5 for item in sublist]


if __name__ == '__main__':
    print(requested_config(vcpu=3900, vram=8000, vssd=2200, cpu_min_frequency=3000, cpu_overcommit=5, cpu_vendor='any', network_card_qty=1, works_main='vSphere', works_add='Нет'))

