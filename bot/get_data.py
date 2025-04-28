import csv
import os
import sqlite3
from collections import defaultdict

DB_PATH = 'bot/data.db'


# DB_PATH = 'data.db'


def get_parameters():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT param_name, param_value FROM parameters")
        return {row[0]: float(row[1]) for row in cursor.fetchall()}


def get_works_coefficient():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT service, hosts_8, hosts_16, hosts_24, hosts_32, hosts_64, hosts_96, hosts_128 FROM works_coefficient")
        return {row[0]: list(row[1:]) for row in cursor.fetchall()}


def get_raid_config():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT raid_level, FTM, FTT, disk_usage_overhead FROM raid_config")
        return {row[0]: {'FTM': row[1], 'FTT': row[2], 'disk_usage_overhead': row[3]} for row in cursor.fetchall()}


def get_raids_data():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT raid_type, level, item_id, value_id, value FROM raids')
        raids_data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        for raid_type, level, item_id, value_id, value in cursor.fetchall():
            raids_data[raid_type][level][item_id][value_id] = value
        return {raid_type: {level: {item_id: dict(values) for item_id, values in items.items()} for level, items in
                            levels.items()} for raid_type, levels in raids_data.items()}


def get_cpus_filtered(cpu_vendor='any', cpu_min_frequency=0):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM cpus WHERE cores_frequency >= ?"
        params = [cpu_min_frequency]

        if cpu_vendor != 'any':
            query += " AND manufacturer = ?"
            params.append(cpu_vendor)

        cursor.execute(query, params)

        return [
            {
                'manufacturer': row[1],
                'name': row[2],
                'cores_quantity': row[3],
                'cores_frequency': row[4],
                'price': row[5],
                'socket': row[6],
                'ram_gen': row[7]
            }
            for row in cursor.fetchall()
        ]


def get_servers_filtered(socket_filter=3647):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM servers WHERE socket = ?", (socket_filter,))

        return [
            {
                'name': row[1],
                'cpu_vendor': row[2],
                'socket': row[3],
                'max_ram': row[4],
                'ram_gen': row[5],
                'max_disks_qty': row[6],
                'price': row[7]
            }
            for row in cursor.fetchall()
        ]


def get_esxi_disks():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM esxi_disks')
        return {row[1]: {'disk_type': row[2], 'price': row[3]} for row in cursor.fetchall()}


def get_cache_disks():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cache_disks')
        return [{'disk_type': row[1], 'capacity': row[2], 'price': row[3]} for row in cursor.fetchall()]


def get_network_cards():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM network_cards')
        return [{'name': row[1], 'price': row[2]} for row in cursor.fetchall()]


def get_hba_adapters():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM hba_adapters')
        return {row[1]: {'name': row[2], 'price': row[3]} for row in cursor.fetchall()}


def get_capacity_disks():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM capacity_disks')
        capacity_disks = {'ssd': {}, 'nvme': {}}
        for row in cursor.fetchall():
            disk_type = row[1]
            capacity = row[2]
            price = row[3]
            capacity_disks[disk_type][capacity] = {'price': price}
        return capacity_disks


def get_rams_filtered(ram_gen_filter):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rams WHERE ram_gen = ?", (ram_gen_filter,))

        return [
            {
                'ram_gen': row[1],
                'ram_size': row[2],
                'price': row[3]
            }
            for row in cursor.fetchall()
        ]


def get_tables():
    files = []
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            # Получаем названия колонок
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            # Получаем данные таблицы
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Создаем временный CSV файл
            filename = f"{table_name}.csv"
            files.append(filename)
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)
    return files


def update_prices(table_name, file_path):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            return f"Таблица {table_name} не существует."

        # Читаем CSV
        with open(file_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            csv_columns = next(csv_reader)  # Пропускаем заголовки

            # Получаем структуру таблицы
            cursor.execute(f"PRAGMA table_info({table_name})")
            table_columns = [col[1] for col in cursor.fetchall()]

            if csv_columns != table_columns:
                return "Структура CSV не совпадает с таблицей."
                # Очищаем таблицу перед вставкой новых данных
            cursor.execute(f"DELETE FROM {table_name}")
            conn.commit()
            # Получаем данные
            data = list(csv_reader)

        # Определяем первичный ключ
        cursor.execute(f"PRAGMA table_info({table_name})")
        primary_key = next((col[1] for col in cursor.fetchall() if col[5] == 1), None)

        # Формируем SQL-запрос
        columns_str = ', '.join(table_columns)
        placeholders = ', '.join(['?'] * len(table_columns))
        conflict_clause = f"ON CONFLICT({primary_key}) DO UPDATE SET " if primary_key else ""
        set_clause = ', '.join(
            [f"{col}=excluded.{col}" for col in table_columns if col != primary_key]) if primary_key else ""

        query = f"""
            INSERT INTO {table_name} ({columns_str})
            VALUES ({placeholders})
            {conflict_clause}{set_clause}
        """ if primary_key else f"""
            INSERT INTO {table_name} ({columns_str})
            VALUES ({placeholders})
        """

        # Выполняем запрос
        cursor.executemany(query, data)
        conn.commit()
        return f"Данные в таблице {table_name} успешно обновлены!"


def main():
    print("Основные параметры:", get_parameters())
    print("Коэффициенты работ:", get_works_coefficient())
    print("Конфигурация RAID:", get_raid_config())
    print("Конфигурация RAID ГБ:", get_raids_data())
    print("ЦП", get_cpus_filtered())
    print("Servers", get_servers_filtered())
    print(f'ESXI: {get_esxi_disks()}')
    print("Cache Disc:", get_cache_disks())
    print("Network Card:", get_network_cards())
    print("HBA Adapters:", get_hba_adapters())
    print("Capacity Disks:", get_capacity_disks())
    # print("RAM Modules:", get_rams_filtered())


if __name__ == "__main__":
    main()
