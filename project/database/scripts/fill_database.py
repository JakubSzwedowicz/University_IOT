from random import choice

from configparser import ConfigParser
from psycopg2.extras import execute_values
import psycopg2

from utils import is_database_empty, Quries, Generator, DatabaseData, insert_many


def generate_data1(entity_generator: callable, range_generator: callable) -> list:
    data = list()
    for i in range_generator():
        data.append(entity_generator(i))
    return list(map(eval, data))


def generate_data2(quantity: int, generator: callable, args: tuple) -> list:
    data = list()
    for _ in range(quantity):
        data.append(generator(*args))
    return list(map(eval, data))


def populate_static_tables():
    mapping = [(Generator.gen_access_level, DatabaseData.get_access_level_entity_definition,
                Quries.get_access_level_insert_query),
               (Generator.gen_card_status, DatabaseData.get_card_status_entity_definition,
                Quries.get_card_status_insert_query),
               (Generator.gen_authorization_message_status,
                DatabaseData.get_authorization_message_status_entity_definition,
                Quries.get_authorization_message_status_insert_status),
               (Generator.gen_device, lambda: [device_door_data["mac_address"] for device_door_data in
                                               DatabaseData.get_device_entity_definitions().values()],
                Quries.get_device_insert_query)]

    for callable_entity_generator, callable_all_values, callable_query in mapping:
        formatted_data = generate_data1(callable_entity_generator, callable_all_values)
        insert_many(callable_query(), formatted_data)


def populate_dynamic_tables():
    access_levels_ids_range = len(
        DatabaseData.get_access_level_entity_definition())
    card_status_ids_range = len(
        DatabaseData.get_card_status_entity_definition())
    authorization_message_status_ids_range = len(
        DatabaseData.get_authorization_message_status_entity_definition())
    employee_ids_range = 20
    cards_ids_range = 45
    authorization_messages_ids_range = 100
    devices_ids_range = len(DatabaseData.get_device_entity_definitions())

    mapping = {"employee": {"quantity": employee_ids_range, "generator": Generator.gen_employee,
                            "args": (access_levels_ids_range,), "query": Quries.get_employee_insert_query},
               "card": {"quantity": cards_ids_range, "generator": Generator.gen_card,
                        "args": (card_status_ids_range, employee_ids_range), "query": Quries.get_card_insert_query},
               "authorization_message": {"quantity": authorization_messages_ids_range,
                                         "generator": Generator.gen_authorization_message, "args": (
                       cards_ids_range, devices_ids_range, authorization_message_status_ids_range),
                                         "query": Quries.get_authorization_message_insert_query}
               }

    for table, data in mapping.items():
        quantity, generator, args, query = data.values()
        # print(f"Generating {quantity} {table} entities with args {args} using query {query()}...")
        formatted_data = generate_data2(quantity, generator, args)
        insert_many(query(), formatted_data)

    data = list()
    for device_id, device_door_data in DatabaseData.get_device_entity_definitions().items():
        data.append(Generator.gen_door(device_door_data["door_description"], device_id,
                                       device_door_data["door_access_level"][1]))
    formatted_data = list(map(eval, data))
    insert_many(Quries.get_door_insert_query(), formatted_data)


def main():
    if is_database_empty():
        populate_static_tables()
        populate_dynamic_tables()
        print('Finished populating tables')
    else:
        print('Database is not empty. Clear it first!')


if __name__ == "__main__":
    main()
