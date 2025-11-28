
import base64
import os

from typing import Dict


class FileHandler:

    def __init__(self, store_dir: str):
        self.store_dir = store_dir

    def store_file_from_json(self, json_object: Dict):
        """
        Prompt:
        given a json object with keys 'data' and 'file-name' convert the string in the data value from base64 to binary.
        Then store the binary object in a directory named store_dir with the name given in the 'file-name' value

        comment from ai assistant
        This code reads a JSON object with the keys data (containing the base64 encoded data) and file-name
        (containing the name of the file where the data should be stored). It decodes the base64 data back
        into binary, then stores the binary data in a file within the store_dir directory with the name given
        by file-name. It outputs a message indicating the file path of the written file.

        The provided base64 data 'SGVsbG8gd29ybGQ=' in the JSON object is 'Hello world' encoded in base64. If you run
        this script, it will create a file named 'test.txt' within 'store_dir' containing 'Hello world'. Replace
        the JSON object with your actual JSON.

        Please remember to handle any errors that might occur during file handling, for example by using try/except blocks.
        :return:
        """

        # Extract the data and file_name from json_object
        file_name = json_object['file-name']
        data = json_object['data']

        # Convert the data from base64 to binary
        binary_data = base64.b64decode(data)

        # Ensure the store_dir directory exists
        os.makedirs(self.store_dir, exist_ok=True)

        # Create the full file path
        file_path = os.path.join(self.store_dir, file_name)

        # Write the binary data to a file
        with open(file_path, 'wb') as f:
            f.write(binary_data)

        print(f'Successfully wrote file to {file_path}')
