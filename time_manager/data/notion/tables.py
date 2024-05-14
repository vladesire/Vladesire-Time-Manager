def generate_table_row(cells):
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


def generate_table(width, rows, has_column_header = False, has_row_header = False):
        return {
                "table_width": width, 
                "has_column_header": has_column_header,
                "has_row_header": has_row_header,
                "children": rows
        }   
