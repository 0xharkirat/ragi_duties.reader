import json
import docx
import requests
import doc_to_docx
import os

def main():

    try:
        doc_to_docx.main()

        doc = docx.Document('list.docx')
        extracted_tables = []
        duty_timings = {
            0:{'duty_start':'03:00', 'duty_end':'03:55'
            },
            1:{'duty_start':'03:55', 'duty_end':'07:00'
            },
            2:{'duty_start':'07:10', 'duty_end':'08:00'
            },
            3:{'duty_start':'08:00:', 'duty_end':'09:00'
            },
            4:{'duty_start':'09:00', 'duty_end':'10:00'
            },
            5:{'duty_start':'10:00', 'duty_end':'11:00'
            },
            6:{'duty_start':'11:00', 'duty_end':'12:00'
            },
            7:{'duty_start':'12:00', 'duty_end':'13:10'
            },
            8:{'duty_start':'13:10', 'duty_end':'14:20'
            },
            9:{'duty_start':'14:20', 'duty_end':'15:20'
            },
            10:{'duty_start':'15:20', 'duty_end':'16:20'
            },
            11:{'duty_start':'16:20', 'duty_end':'18:00'
            },
            12:{'duty_start':'18:20', 'duty_end':'19:30'
            },
            13:{'duty_start':'19:30', 'duty_end':'20:30'
            },
            14:{'duty_start':'20:30', 'duty_end':'22:30'
            }
        }



        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_data = []
                for cell in row.cells:
                    row_data.append(cell.text)
                table_data.append(row_data)
            extracted_tables.append(table_data)

        table_0 = []
        table_1 = []

        if len(extracted_tables) == 3:
            table_0 = extracted_tables[0]
            table_1 = extracted_tables[1]

        ragi_duties = {}

        # Process table 1
        for i, row in enumerate(table_1):
            if i > 1:
                date = row[0]
                unsorted_ragi_duties = {}

                for j, col in enumerate(row):
                    if j != 0:
                        col = clean_strings(col)  # Remove escape characters
                        
                        unsorted_ragi_duties[j + 3] = {
                            "ragi": col,
                            "duty_start": duty_timings[j + 3]["duty_start"],
                            "duty_end": duty_timings[j + 3]["duty_end"],
                        }
                        unsorted_ragi_duties[j + 10] = {
                            "ragi": col,
                            "duty_start": duty_timings[j + 10]["duty_start"],
                            "duty_end": duty_timings[j + 10]["duty_end"],
                        }
                ragi_duties[date] = dict(sorted(unsorted_ragi_duties.items()))

        # Process table 0
        for i, row in enumerate(table_0):
            if i > 1:
                date = row[0]
                unsorted_ragi_duties = {}

                for j, col in enumerate(row):
                    if j != 0:
                        col = clean_strings(col)  # Remove escape characters
                        if j == 1:
                            
                                unsorted_ragi_duties[0] = {
                                    "ragi": col,
                                    "duty_start": duty_timings[0]["duty_start"],
                                    "duty_end": duty_timings[0]["duty_end"],
                                }
                            
                                unsorted_ragi_duties[8] = {
                                    "ragi": col,
                                    "duty_start": duty_timings[8]["duty_start"],
                                    "duty_end": duty_timings[8]["duty_end"],
                                }
                        elif j == 2:
                            
                                unsorted_ragi_duties[1] = {
                                    "ragi": col,
                                    "duty_start": duty_timings[1]["duty_start"],
                                    "duty_end": duty_timings[1]["duty_end"],
                                }
                        else:
                           
                                unsorted_ragi_duties[j - 1] = {
                                    "ragi": col,
                                    "duty_start": duty_timings[j - 1]["duty_start"],
                                    "duty_end": duty_timings[j - 1]["duty_end"],
                                }
                           
                                unsorted_ragi_duties[j + 6] = {
                                    "ragi": col,
                                    "duty_start": duty_timings[j + 6]["duty_start"],
                                    "duty_end": duty_timings[j + 6]["duty_end"],
                                }

                # Merge if the date exists
                if date in ragi_duties:
                    existing_ragi_duties = ragi_duties[date]
                    unsorted_ragi_duties.update(existing_ragi_duties)

                ragi_duties[date] = dict(sorted(unsorted_ragi_duties.items()))


        json_object = json.dumps(ragi_duties, indent=4)
        # with open("ragi_duties.json", "w") as outfile:
        #     outfile.write(json_object)


        # Your GitHub username
        username = "0xharkirat"

        # The Gist ID of the Gist you want to update
        gist_id = "587f68228c0a01ccf53d8339008d479f"

        # The filename you want to update in the Gist
        filename = "ragi_duties.json"

        # Your GitHub Personal Access Token
        access_token = os.environ.get('ACCESS_TOKEN')

        # URL of the GitHub Gist API endpoint
        gist_url = f"https://api.github.com/gists/{gist_id}"

        # New content to update the Gist file with
        new_content = {
            filename: {
                "content": "New content goes here"
            }
        }

        headers = {
            "Authorization": f"token {access_token}"
        }

        # Get the current Gist data
        response = requests.get(gist_url, headers=headers)

        if response.status_code == 200:
            gist_data = response.json()
            gist_data["files"]["ragi_duties.json"]["content"] = json_object

            # Update the Gist with the new content
            update_response = requests.patch(gist_url, headers=headers, data=json.dumps(gist_data))

            if update_response.status_code == 200:
                print(f"Gist updated successfully.")
            else:
                print(f"Failed to update Gist. Status code: {update_response.status_code}")
        else:
            print(f"Failed to fetch Gist data. Status code: {response.status_code}")

        

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def clean_strings(unclean_string):
    return unclean_string.replace('\n', '')

if __name__ == "__main__":
    main()
# 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