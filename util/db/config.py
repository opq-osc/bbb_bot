# -*- coding:utf-8 -*-

import json


class _config:
    friend_list_updating = set()
    troop_list_updating = set()
    member_list_updating = set()
    table_creating = set()

    def add_friend_list_updating(self, flag):
        self.friend_list_updating.add(flag)

    def add_troop_list_updating(self, flag):
        self.troop_list_updating.add(flag)

    def add_member_list_updating(self, flag):
        self.member_list_updating.add(flag)

    def add_table_creating(self, flag):
        self.table_creating.add(flag)

    def remove_friend_list_updating(self, flag):
        self.friend_list_updating.discard(flag)

    def remove_troop_list_updating(self, flag):
        self.troop_list_updating.discard(flag)

    def remove_member_list_updating(self, flag):
        self.member_list_updating.discard(flag)

    def remove_table_creating(self, flag):
        self.table_creating.discard(flag)

    def friend_list_is_updating(self, flag):
        return flag in self.friend_list_updating

    def troop_list_is_updating(self, flag):
        return flag in self.troop_list_updating

    def member_list_is_updating(self, flag):
        return flag in self.member_list_updating

    def table_is_creating(self, flag):
        return flag in self.table_creating


config_dict = {}
try:
    with open('./mysql.json', encoding='utf-8') as f:
        config_dict = json.load(f)
except FileNotFoundError:
    pass
except json.JSONDecodeError as e:
    print('Mysql 数据库配置文件不规范')

config = _config()
