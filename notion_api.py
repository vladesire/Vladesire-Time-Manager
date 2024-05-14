import requests
import yaml

KEYS_FILE = '/home/vladesire/bin/py/tm/keys.yaml'

class NotionApi: 
    def __init__(self):
        with open(KEYS_FILE, 'r') as file:
            keys = yaml.safe_load(file)

        token = keys['token']

        self.page = keys['port-page']
        self.database = keys['database']
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28", 
            "Content-Type": "application/json"
        }


    def generate_table_row(self, cells):
        return {
            "type": "table_row",
            "table_row": {
                "cells": [
                    [   
                        {
                            "type": "text",
                            "text": {
                                "content": cell
                            }
                        }
                    ]               
                    for cell in cells
                ]
            }
        }


    def generate_table(self, width, rows, has_column_header = False, has_row_header = False):
        return {
            "table_width": width, 
            "has_column_header": has_column_header,
            "has_row_header": has_row_header,
            "children": rows
        }   

    def send_table(self, table: list[list[str]]):

        json = {
            "children": [
                {
                    "object": "block",
                    "type": "table",
                    "table": self.generate_table(
                        width = len(table[0]),
                        rows = [self.generate_table_row(row) for row in table], 
                        has_column_header = True, 
                        has_row_header = True,
                    )
                }, 

            ]
        }   
            
        r = requests.patch(
            url = f"https://api.notion.com/v1/blocks/{self.page}/children",
            headers = self.headers,
            json = json
        )    

        return r


    def query_schedule_database(self, categories: list[str], start_date: str, end_date: str): 

        json = {
            "filter": {
                "and": [
                    {
                        "property": "Date", 
                        "date": {
                            "on_or_after": start_date
                        }
                    },
                    {
                        "property": "Date", 
                        "date": {
                            "on_or_before": end_date
                        }
                    }
                ]
            },

            "page_size": 100
        }

        time = {category: 0 for category in categories}

        has_more = True

        while has_more: 

            r = requests.post(
                url = f"https://api.notion.com/v1/databases/{self.database}/query",
                headers = self.headers,
                json = json
            )    

            if r.status_code == 200:
                response = r.json()

                pages = response['results']

                for page in pages: 

                    # print(f"{page['properties']['Name']['title'][0]['text']['content']} {page['properties']['Hours']['formula']['number']}", end="")

                    hours = page['properties']['Hours']['formula']['number']
                    category = page['properties']['Category']['select']
                    
                    if category == None:
                        time['Other'] += hours
                    else: 
                        time[category['name']] += hours

                has_more = response['has_more']

                if has_more: 
                    json['start_cursor'] = response['next_cursor']

            else:
                raise Exception(f"Something went wrong with Notion API: {r.json()}")

        time['Sleep'] = 168 - sum(time.values())

        return time