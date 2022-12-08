import os
import string
import random
import json
import errno
import shutil
from .log import Log
from pathlib import Path

class File:

    @staticmethod
    def get_random_string(string_length: int = 10) -> str:
        """Generate a random string of fixed length."""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(string_length))

    @staticmethod
    def get_file_path(folder: str, filename: str, extension: str = None) -> str:
        """Combine folder, filename and extension to file path."""
        file_extension: str = ''
        if extension:
            file_extension = '{0}{1}'.format(".", extension)
        return '{0}/{1}{2}'.format(folder, filename, file_extension)

    # writing

    @staticmethod
    def dump_to_file(data: bytearray, filename: str, write_new: bool = False) -> bool:
        """Write data to file."""
        if not data:
            Log.error('No data to write.')
        
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        mode: str = File.write_mode_string(write_new)
        with open(filename, mode) as file:
            file.write(data)
            return True
        return False

    @staticmethod
    def write_to_folder(data: bytearray, folder: str, extension: str = None,
                        write_new: bool = False) -> None:
        """Write file with random name to specified folder."""
        Path(folder).mkdir(parents=True, exist_ok=True)

        file_prefix = File.get_random_string()
        filepath = File.get_file_path(
            folder, file_prefix, extension=extension)

        if File.dump_to_file(data, filename=filepath, write_new=write_new):
            Log.info("Data written to file", filepath)

    @staticmethod
    def write_mode_string(write_new: bool) -> str:
        """Write new file or append data."""
        if write_new:
            return 'wb'
        return 'ab'
    
    @staticmethod
    def dump_json_to_file(filepath: str, data: dict, print_logs: bool = False,
                          indent: int = 4) -> bool:
        File.create_path_if_not_exists(filepath)
        with open(filepath, "w") as file:
            json.dump(data, file, indent=indent)
            if print_logs:
                Log.info('Json written', filepath)
            return True
                
    @staticmethod
    def create_path_if_not_exists(filepath: str) -> None:
        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    @staticmethod
    def create_folder(folder: str) -> None:
        os.mkdir(folder)

    # reading

    @staticmethod
    def get_data(filepath: str) -> bytearray:
        if not os.path.exists(filepath):
            Log.error('Error: File path does not exist', filepath)
            return []
        data: bytearray = []
        with open(filepath, 'rb') as file:
            data = file.read()    
        return data

    # delete

    @staticmethod
    def delete_file(filepath: str) -> None:
        os.remove(filepath)

    @staticmethod
    def delete_folder(folder: str, if_empty_only: bool) -> bool:
        if not os.path.exists(folder):
            print('Error: Folder does not exist.', folder)
            return False
        
        if if_empty_only:
            if len(os.listdir(folder)) > 0:
                print('Error: Folder not empty.', folder)
                return False
            os.rmdir(folder)
            return True
        
        shutil.rmtree(folder)
        return True
