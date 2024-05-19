import json
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive.file']

def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    return service

def read_sheet(service, spreadsheet_id, range_name):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get('values', [])

def clean_data(values):
    values = [row for row in values if any(row)]
    if values:
        num_cols = max(len(row) for row in values)
        for row in values:
            while len(row) < num_cols:
                row.append('')
    return values

def parse_cases(cases_values, rewards_table):
    case_config = {}
    if len(cases_values) < 5:
        print("Ошибка: Недостаточно данных в cases_values")
        return case_config
    case_name = cases_values[0][0]
    case_tech_name = cases_values[2][1]
    case_config[case_name] = {"case_tech_name": case_tech_name, "groups": {}}
    group_idx = 3
    group_number = 1
    while group_idx < len(cases_values[1]):
        if "Group" in cases_values[1][group_idx]:
            group_name = f"group_{group_number}"
            group_chance_str = cases_values[3][group_idx + 1].strip('%').strip() if cases_values[3][group_idx + 1] else None
            if group_chance_str:
                try:
                    group_chance = float(group_chance_str) / 100.0
                except ValueError:
                    print(f"Неверное значение шанса группы для {group_name}: {group_chance_str}")
                    group_idx += 4
                    group_number += 1
                    continue
            else:
                group_idx += 4
                group_number += 1
                continue
            rewards = []
            print(f"Processing {group_name} with chance {group_chance}")
            for reward_idx in range(5, len(cases_values)):
                if len(cases_values[reward_idx]) <= group_idx:
                    continue
                reward_name = cases_values[reward_idx][group_idx] if cases_values[reward_idx][group_idx] else None
                count_str = cases_values[reward_idx][group_idx + 1].strip() if len(cases_values[reward_idx]) > group_idx + 1 and cases_values[reward_idx][group_idx + 1] else None
                chance_str = cases_values[reward_idx][group_idx + 2].strip('%').strip() if len(cases_values[reward_idx]) > group_idx + 2 and cases_values[reward_idx][group_idx + 2] else None
                if not reward_name or not count_str or not chance_str:
                    continue
                print(f"Reward: {reward_name}, Count: {count_str}, Chance: {chance_str}")
                try:
                    count = int(count_str)
                    chance = float(chance_str) / 100.0
                except ValueError:
                    print(f"Invalid count or chance value for reward {reward_name}")
                    continue
                reward_data = find_reward_data(reward_name, rewards_table)
                if reward_data:
                    rewards.append({"item_tech_name": reward_name, "type": reward_data["type"], "parameters": {"count": count, "item_id": reward_data["item_id"], "chance": chance}})
                else:
                    print(f"Не найдены данные для награды: {reward_name}")
            if rewards:
                case_config[case_name]["groups"][group_name] = {"group_chance": group_chance, "rewards": rewards}
            else:
                print(f"Нет наград для {group_name}")
        group_idx += 4
        group_number += 1
    return case_config

def find_reward_data(reward_name, rewards_table):
    return rewards_table.get(reward_name, None)

def parse_rewards_table(rewards_values):
    rewards_table = {}
    for row in rewards_values[2:]:
        if row[0]:
            rewards_table[row[0]] = {"item_id": row[2].strip(), "type": row[3].strip()}
        if row[5]:
            rewards_table[row[5]] = {"item_id": row[7].strip(), "type": row[8].strip()}
    return rewards_table

def main():
    service = get_service()
    SAMPLE_SPREADSHEET_ID = '152DYxNLgmBMcNXDCTNuTWoOkwLvwteO2Wmv-zW_aoxE'
    cases_values = read_sheet(service, SAMPLE_SPREADSHEET_ID, 'Кейсы!A:N')
    rewards_values = read_sheet(service, SAMPLE_SPREADSHEET_ID, 'Таблица Наград!A:I')
    cases_values = clean_data(cases_values)
    rewards_values = clean_data(rewards_values)
    print("cases_values:", cases_values)
    print("rewards_values:", rewards_values)
    rewards_table = parse_rewards_table(rewards_values)
    case_config = parse_cases(cases_values, rewards_table)
    json_config = json.dumps(case_config, indent=4, ensure_ascii=False)
    print(json_config)
    with open('case_config.json', 'w', encoding='utf-8') as f:
        f.write(json_config)

if __name__ == '__main__':
    main()
