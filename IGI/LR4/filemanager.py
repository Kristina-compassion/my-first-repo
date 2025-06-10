import zipfile

class FileManager():
    @staticmethod
    def read_from_file(path_to_file):
        with open(path_to_file, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def write_to_file(text, path_to_file):
        with open(path_to_file, 'w', encoding='utf-8') as file:
            file.write(text)

    @staticmethod
    def archive_file(file_to_zip, path_to_zip):
        with zipfile.ZipFile(path_to_zip, 'w',compression=zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(file_to_zip)

    @staticmethod
    def get_archive_info(path_to_zip):
        with zipfile.ZipFile(path_to_zip, 'r') as zip_file:
            print("Information about the files in the archive:")
            for info in zip_file.infolist():
                print(f"Name: {info.filename}")
                print(f"Size before compression: {info.file_size} bytes")
                print(f"Size after compression: {info.compress_size} bytes")