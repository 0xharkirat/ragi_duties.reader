import cloudconvert
import requests
import os

api_key = os.environ.get("CLOUD_CONVERT_API_KEY")



def main():
    try:
        cloudconvert.configure(api_key=api_key)

        job = cloudconvert.Job.create(payload={
            "tasks": {
                'import-my-file': {
                    'operation': 'import/url',
                    'url': 'https://old.sgpc.net/Ragi%20List_Eng.doc'
                },
                'convert-my-file': {
                    'operation': 'convert',
                    'input': 'import-my-file',
                    "input_format": "doc",
                    "output_format": "docx",
                    "engine": "office",
                },
                'export-my-file': {
                    'operation': 'export/url',
                    'input': 'convert-my-file'
                }
            }
        })

        job = cloudconvert.Job.wait(id=job['id'])

        for task in job["tasks"]:
            if task.get("name") == "export-my-file" and task.get("status") == "finished":
                export_task = task

        file = export_task.get("result").get("files")[0]
        doc_url = file['url']
        # print(doc_url)

        local_doc_file = 'list.docx'

        # Download the file
        response = requests.get(doc_url)
        with open(local_doc_file, 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print(f"{str(e)}")
