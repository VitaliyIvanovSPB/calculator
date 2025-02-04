import math
from data import cpus, rams, servers, esxi_disc, network_card


def get_cpus(vendor: str, min_frequency: int):
    """Возвращает список процессоров нужного вендора, отфильтрованных по минимальной частоте"""
    if vendor == 'any':
        return [cpu for cpu in cpus if cpu['cores_frequency'] >= min_frequency]
    else:
        return [cpu for cpu in cpus if cpu['manufacturer'] == vendor and cpu['cores_frequency'] >= min_frequency]


def requested_config(cpu_vendor: str = 'any', vcpu: int = 400, vram: int = 800, vssd: int = 20000,
                     cpu_overcommit: int = 3, cpu_min_frequency: int = 0, max_cpu_usage: float = 0.8,
                     max_ram_usage: float = 0.8, currency: int = 100, payback_period: int = 24,
                     coefficient: float = 3.3):
    """Подбирает конфигурации серверов по заданным параметрам"""

    all_configs = {}
    cpu_list = get_cpus(cpu_vendor, cpu_min_frequency)

    for cpu in cpu_list:
        cpu_hosts = math.ceil(vcpu / cpu_overcommit / (cpu['cores_quantity'] * 2 * max_cpu_usage))

        for server in filter(lambda s: s['socket'] == cpu['socket'], servers):
            for ram in filter(lambda r: r['ram_gen'] == server['ram_gen'], rams):
                ram_host = math.ceil(vram / max_ram_usage / cpu_hosts / ram['ram_size'])
                ram_1host = ram_host + 1 if ram_host % 2 == 1 else ram_host

                if ram_1host > server['max_ram']:
                    continue

                # total_price = (cpu['price'] + server['price'] + ram_1host * ram['price'] + esxi_disc['price'] +
                #                network_card['price']) * (cpu_hosts + 1)

                total_1host_price = cpu['price'] * 2 + server['price'] + ram_1host * ram['price'] + esxi_disc['price'] + network_card['price']
                rms = total_1host_price * currency / payback_period * coefficient
                vmware = rms * (cpu_hosts + 1)

                all_configs[len(all_configs)] = {'Need hosts by CPU(n+1)': cpu_hosts + 1,
                                                 'CPU': cpu['name'] + ' ' + str(cpu['cores_frequency']) + 'GHz',
                                                 'Server': server['name'],
                                                 ram['ram_size']: ram_1host,
                                                 'Esxi disk': esxi_disc['type'],
                                                 'Network card': network_card['name'],
                                                 'rms, Rub': rms,
                                                 'Total price, Rub': vmware}

    sorted_configs = sorted(all_configs.items(), key=lambda x: x[1]['Total price, Rub'])[:5]
    cheapest_config = min(all_configs.items(), key=lambda x: x[1]['Total price, Rub'])
    for index, (config_id, config) in enumerate(sorted_configs, 1):
        conf = [f"\nТоп {index}: Вариант {config_id}\n"]
        for key, value in config.items():
            conf.append(f"{key}: {value}\n")
        print(''.join(conf))
    return cheapest_config


if __name__ == '__main__':
    print(requested_config(vcpu=297, vram=804, vssd=31550, cpu_overcommit=2))

# TODO:
# вся логика пока только на интеле

# итоговая цена за варю рмс на кол-во хостов
# итоговая стоимость = сетевые услуги+варя+админка
