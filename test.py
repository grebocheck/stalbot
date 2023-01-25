from sc_bot_api import StalcraftAPI
import box

sca = StalcraftAPI()

item_id = box.search_item_id_by_name("Viper")
region = "EU"
item_name = box.search_item_name_by_id(item_id)
history = sca.get_price_history(item_id, region)
histe = box.HistoryLot(history, item_name, region)
histe.create_plot_prices()

# friends = sca.get_friends(character="Test-1")
# print(friends)
# friends = ['Test-2', 'Test-3']

# emission = sca.get_emission()
# print(emission)
# emission = {'currentStart': '2023-01-23T12:23:13.900887Z', 'previousStart': '2023-01-23T10:21:13.900887Z', 'previousEnd': '2023-01-23T10:26:13.900887Z'}

# clan_list = sca.get_clans()
# print(clan_list)
# clan_list = {'totalClans': 2, 'data': [
#     {'id': '647d6c53-b3d7-4d30-8d08-de874eb1d845', 'name': 'Clan #1', 'tag': 'TAG', 'level': 2, 'levelPoints': 239323,
#      'registrationTime': '2022-07-03T10:15:30Z', 'alliance': 'covenant', 'description': 'Sample description',
#      'leader': 'Test-1', 'memberCount': 1},
#     {'id': 'a5a7f97f-5725-4b84-85c2-fffb15feea39', 'name': 'Clan #2', 'tag': 'TBA', 'level': 1, 'levelPoints': 3732342,
#      'registrationTime': '2022-12-13T10:15:30Z', 'alliance': 'duty', 'description': 'Sample description',
#      'leader': 'Test-2', 'memberCount': 2}]}

# clan_members = sca.get_clan_member(clan_id="647d6c53-b3d7-4d30-8d08-de874eb1d845")
# print(clan_members)
# clan_members = [{'name': 'Test-1', 'rank': 'LEADER', 'joinTime': '2022-07-03T10:15:30Z'}]

# clan = sca.get_clan_info(clan_id="647d6c53-b3d7-4d30-8d08-de874eb1d845")
# print(clan)
# clan = {'id': '647d6c53-b3d7-4d30-8d08-de874eb1d845', 'name': 'Clan #1', 'tag': 'TAG', 'level': 2,
#         'levelPoints': 239323, 'registrationTime': '2022-07-03T10:15:30Z', 'alliance': 'covenant',
#         'description': 'Sample description', 'leader': 'Test-1', 'memberCount': 1}

# history = sca.get_price_history("y1q9")
# print(history)
# history = {'total': 10, 'prices': [{'amount': 1, 'price': 1000, 'time': '2023-01-23T12:09:15.842149Z'},
#                                    {'amount': 2, 'price': 2000, 'time': '2023-01-23T11:54:15.842151Z'},
#                                    {'amount': 3, 'price': 3000, 'time': '2023-01-23T11:39:15.842151Z'},
#                                    {'amount': 4, 'price': 4000, 'time': '2023-01-23T11:24:15.842152Z'},
#                                    {'amount': 1, 'price': 0, 'time': '2023-01-23T11:09:15.842152Z'},
#                                    {'amount': 2, 'price': 1000, 'time': '2023-01-23T10:54:15.842152Z'},
#                                    {'amount': 3, 'price': 2000, 'time': '2023-01-23T10:39:15.842153Z'},
#                                    {'amount': 4, 'price': 3000, 'time': '2023-01-23T10:24:15.842153Z'},
#                                    {'amount': 1, 'price': 4000, 'time': '2023-01-23T10:09:15.842154Z'},
#                                    {'amount': 2, 'price': 0, 'time': '2023-01-23T09:54:15.842154Z'}]}

# regions = sca.get_regions()
# print(regions)
# regions = [{'id': 'RU', 'name': 'RUSSIA'},
#            {'id': 'EU', 'name': 'EUROPE'},
#            {'id': 'NA', 'name': 'NORTH AMERICA'},
#            {'id': 'SEA', 'name': 'SOUTH EAST ASIA'}]

# lots = sca.get_auction_lots("y1q9")
# print(lots)
# lots = {'total': 10, 'lots': [
#     {'itemId': 'y1q9', 'startPrice': 100, 'buyoutPrice': 10000, 'startTime': '2023-01-23T10:05:06.465068Z',
#      'endTime': '2023-01-23T22:05:06.465069Z', 'additional': {}},
#     {'itemId': 'y1q9', 'startPrice': 100, 'buyoutPrice': 10000, 'startTime': '2023-01-22T10:05:06.465071Z',
#      'endTime': '2023-01-23T22:05:06.465072Z', 'additional': {}},
#     {'itemId': 'y1q9', 'startPrice': 100, 'buyoutPrice': 10000, 'startTime': '2023-01-21T10:05:06.465073Z',
#      'endTime': '2023-01-23T22:05:06.465073Z', 'additional': {}},
#     {'itemId': 'y1q9', 'startPrice': 100, 'buyoutPrice': 10000, 'startTime': '2023-01-20T10:05:06.465075Z',
#      'endTime': '2023-01-23T22:05:06.465075Z', 'additional': {}},
#     {'itemId': 'y1q9', 'startPrice': 100, 'buyoutPrice': 10000, 'startTime': '2023-01-19T10:05:06.465076Z',
#      'endTime': '2023-01-23T22:05:06.465077Z', 'additional': {}},
#     {'itemId': 'y1q9', 'startPrice': 100, 'buyoutPrice': 10000, 'startTime': '2023-01-18T10:05:06.465078Z',
#      'endTime': '2023-01-23T22:05:06.465078Z', 'additional': {}},
#     {'itemId': 'y1q9', 'startPrice': 100, 'buyoutPrice': 10000, 'startTime': '2023-01-17T10:05:06.465080Z',
#      'endTime': '2023-01-23T22:05:06.465080Z', 'additional': {}},
#     {'itemId': 'y1q9', 'startPrice': 100, 'buyoutPrice': 10000, 'startTime': '2023-01-16T10:05:06.465081Z',
#      'endTime': '2023-01-23T22:05:06.465082Z', 'additional': {}},
#     {'itemId': 'y1q9', 'startPrice': 100, 'buyoutPrice': 10000, 'startTime': '2023-01-15T10:05:06.465083Z',
#      'endTime': '2023-01-23T22:05:06.465083Z', 'additional': {}},
#     {'itemId': 'y1q9', 'startPrice': 100, 'buyoutPrice': 10000, 'startTime': '2023-01-14T10:05:06.465085Z',
#      'endTime': '2023-01-23T22:05:06.465085Z', 'additional': {}}]}

# characters = sca.get_characters()
# print(characters)
# characters = [{'information': {'id': '5c7e0994-bc22-4190-9774-5f197b1500e6', 'name': 'Test-1',
#                           'creationTime': '2021-12-03T10:15:30Z'}, 'clan': {
#     'info': {'id': '647d6c53-b3d7-4d30-8d08-de874eb1d845', 'name': 'Clan #1', 'tag': 'TAG', 'level': 2,
#              'levelPoints': 239323, 'registrationTime': '2022-07-03T10:15:30Z', 'alliance': 'covenant',
#              'description': 'Sample description', 'leader': 'Test-1', 'memberCount': 1},
#     'member': {'name': 'Test-1', 'rank': 'LEADER', 'joinTime': '2022-07-03T10:15:30Z'}}}, {
#              'information': {'id': '996e2cf9-5f36-4a38-97e8-1aecec42b5f0', 'name': 'Test-2',
#                              'creationTime': '2022-12-03T10:15:30Z'}, 'clan': {
#         'info': {'id': 'a5a7f97f-5725-4b84-85c2-fffb15feea39', 'name': 'Clan #2', 'tag': 'TBA', 'level': 1,
#                  'levelPoints': 3732342, 'registrationTime': '2022-12-13T10:15:30Z', 'alliance': 'duty',
#                  'description': 'Sample description', 'leader': 'Test-2', 'memberCount': 2},
#         'member': {'name': 'Test-2', 'rank': 'LEADER', 'joinTime': '2022-12-13T10:15:30Z'}}}, {
#              'information': {'id': '9219dfbb-1332-4dc7-b3be-fc4b089710cb', 'name': 'Test-3',
#                              'creationTime': '2023-01-03T10:15:30Z'}, 'clan': {
#         'info': {'id': 'a5a7f97f-5725-4b84-85c2-fffb15feea39', 'name': 'Clan #2', 'tag': 'TBA', 'level': 1,
#                  'levelPoints': 3732342, 'registrationTime': '2022-12-13T10:15:30Z', 'alliance': 'duty',
#                  'description': 'Sample description', 'leader': 'Test-2', 'memberCount': 2},
#         'member': {'name': 'Test-3', 'rank': 'OFFICER', 'joinTime': '2023-01-03T10:15:30Z'}}}]
