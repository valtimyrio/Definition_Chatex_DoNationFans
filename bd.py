import datetime
import json
import os.path

file_path = "data/servers.json"


class FileJson:
    @staticmethod
    def _is_json(data):
        # data = str(data)
        try:
            _ = json.dumps(data)
        except ValueError:
            return False
        return True

    def _check_path(self):
        if os.path.exists(self.path):
            return True
        return False

    def _read_json(self):
        if self._check_path():
            with open(self.path, 'r', encoding='utf8') as f:
                return json.load(f)
        else:
            print("File path does not exist")

    def _write_json(self, data):
        # data = str(data)
        if self._check_path() and self._is_json(data):
            with open(self.path, 'w', encoding='utf8') as f:
                json.dump(data, f, ensure_ascii=False)
        else:
            print("Cannot write data to file")


class bd(FileJson):
    def __init__(self):
        self.path = file_path

    def get_server_inner_id_by_id(self, id):
        data = self._read_json()
        # print("Запрошенный айди серва: " + str(id))
        for inner_id in data:
            if id in data[inner_id]["id"]:
                return inner_id
        return False

    def get_server_inner_id_by_name(self, name):
        data = self._read_json()
        # print("Пришло имя: " + str(name))
        # print("Запрошенное имя серва: " + str(name))
        for inner_id in data:
            if name == data[inner_id]["name"]:
                return inner_id
        return False

    def check_member_existence(self, member_id, name):
        data = self._read_json()
        inner_server_id = self.get_server_inner_id_by_name(name)
        for member in data[inner_server_id]["members"]:
            if str(member) == str(member_id):
                return True
        return False

    def get_servers(self):
        data = self._read_json()
        return data

    def get_channels(self, name):
        data = self._read_json()
        if self.get_server_inner_id_by_name(name):
            return data[self.get_server_inner_id_by_name(name)]["channels"]
        else:
            return False

    def get_roles(self, name):
        data = self._read_json()
        if self.get_server_inner_id_by_name(name):
            return data[self.get_server_inner_id_by_name(name)]["roles"]
        else:
            return False

    def get_roles_list(self, name):
        temp_list = list()
        roles = self.get_roles(name)
        for i in roles:
            temp_list.append(roles[i]["name"])
        return temp_list

    def get_role_price(self, name, server_name):
        roles = self.get_roles(server_name)
        for i in roles:
            if roles[i]["name"] == name:
                return roles[i]["price"]

    def get_members(self, name):
        data = self._read_json()
        if self.get_server_inner_id_by_name(name):
            return data[self.get_server_inner_id_by_name(name)]["members"]
        else:
            return False

    def check_member_has_role(self, member_id, name, role):
        if self.check_member_existence(member_id, name):
            data = self._read_json()
            if role in data[self.get_server_inner_id_by_name(name)]["members"][str(member_id)]["roles"]:
                return True
            return False
        print("Пользователя не найдено")

    def add_role(self, user_id, user_name, server_id, name, role):
        user_id = str(user_id)
        if self.check_member_existence(user_id, name):
            data = self._read_json()
            data[self.get_server_inner_id_by_name(name)]["members"][user_id]["roles"][role] = {
                "start_datetime": str(datetime.datetime.now()),
                "end_datetime": str(datetime.datetime.now() + datetime.timedelta(seconds=1))
            }

            self._write_json(data)

    def delete_role(self, user_id, user_name, server_id, name, role):
        user_id = str(user_id)
        if self.check_member_existence(user_id, name):
            data = self._read_json()
            data[self.get_server_inner_id_by_name(name)]["members"][user_id]["roles"].pop(role)

            self._write_json(data)

    def add_user(self, user_id, user_name, name):
        if self.check_member_existence(user_id, name):
            return True
        data = self._read_json()
        if self.get_server_inner_id_by_name(name):
            data[self.get_server_inner_id_by_name(name)]["members"][user_id] = {
                "name": user_name,
                "balance": 0,
                "last_id": "",
                "last_amount": 0,
                "roles": {}
            }
            self._write_json(data)
            return True
        return False

    def get_member_balance(self, user_id, user_name, server_id, name):
        if self.add_user(user_id, user_name, name):
            data = self._read_json()
            return data[self.get_server_inner_id_by_name(name)]["members"][str(user_id)]["balance"]

    def change_member_balance(self, user_id, user_name, server_id, amount, name):
        if self.add_user(user_id, user_name, name):
            data = self._read_json()
            data[self.get_server_inner_id_by_name(name)]["members"][str(user_id)]["balance"] += amount
            self._write_json(data)

    def get_member_last_id(self, user_id, user_name, server_id, name):
        if self.add_user(user_id, user_name, name):
            data = self._read_json()
            return data[self.get_server_inner_id_by_name(name)]["members"][str(user_id)]["last_id"]

    def get_member_last_amount(self, user_id, user_name, server_id, name):
        if self.add_user(user_id, user_name, name):
            data = self._read_json()
            return data[self.get_server_inner_id_by_name(name)]["members"][str(user_id)]["last_amount"]

    def change_member_last_id(self, user_id, user_name, server_id, last_id, name):
        if self.add_user(user_id, user_name, name):
            data = self._read_json()
            data[self.get_server_inner_id_by_name(name)]["members"][str(user_id)]["last_id"] = last_id
            self._write_json(data)

    def change_member_last_amount(self, user_id, user_name, server_id, last_amount, name):
        if self.add_user(user_id, user_name, name):
            data = self._read_json()
            data[self.get_server_inner_id_by_name(name)]["members"][str(user_id)]["last_amount"] = last_amount
            self._write_json(data)

    def check_all_dates(self):
        data = self._read_json()
        temp_list = list()
        curr_date = datetime.datetime.now()
        for i in data:
            for memb in data[i]["members"]:
                for role in data[i]["members"][memb]["roles"]:
                    print(role)
                    date = data[i]["members"][memb]["roles"][role]["end_datetime"]
                    time_obj = datetime.datetime.strptime(date[:19], "%Y-%m-%d %H:%M:%S")
                    if curr_date > time_obj:
                        temp_list.append(
                            [memb, data[i]["members"][memb]["name"], 0, data[i]["name"], role, data[i]["name"]])

        return temp_list
