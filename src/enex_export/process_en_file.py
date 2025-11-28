import sqlalchemy.orm
from sqlalchemy.orm import sessionmaker, Session
from typing import Dict, Union
from datetime import datetime

from .file_reader import EnexFileReader

from .schema_classes import DbMeta, DocMeta, Attributes, ContentFiles, Tags


class ProcessEnexFile:
    """
    Given a path to an enex file & a notebook name
      - Open the file
      - extract each note
      - save the file(s) to disk
      - save the metadata for the note to the database, including the filename(s) & the notebook name
        - Use the filenames from the note, which are (I'm pretty sure) unique
      - return a list of objects containing an object with:
        - notebook name
        - note title
        - number of files
        - note record id
    """

    def __init__(self, file_path: str, path_to_db: str):
        """
        Keep track of the into to do the store & save
        :param file_path: where to store the files
        :param path_to_db: where to find the db
        """
        self.file_path = file_path
        self.path_to_db = path_to_db

    def process_file(self, path_to_file: str):
        """
        Pick up a file from disk & store the contents
        :param path_to_file: The file to process
        :return:
        """
        file_reader = EnexFileReader()
        file_contents = file_reader.parse(path_to_file)

        for note in file_contents:
            doc_meta = DocMeta(
                title=note["title"],
                create_date=datetime.fromisoformat(note["created"]),
                update_date=datetime.fromisoformat(note["updated"]),
            )

            attribute = Attributes(
                source_url=note["source-url"], doc_meta_id=doc_meta.id
            )
            resource_list = note["resource_list"] if "resource_list" in note else None
            file_meta_list = []
            if resource_list:
                for note_contents in resource_list:
                    file_meta = ContentFiles()
                    file_meta.mime_type = self.get_item(note_contents, "mime")
                    file_meta.data = self.get_item(note_contents, "data")
                    file_meta.filename = self.get_item(note_contents, "filename")
                    note_contents["width"] = self.get_item(
                        note_contents, "width", "int"
                    )
                    note_contents["height"] = self.get_item(
                        note_contents, "height", "int"
                    )
                    file_meta_list.append(file_meta)

    @staticmethod
    def get_item(
        source: Dict, name: str, item_type: str = "str"
    ) -> Union[str, int, None]:
        """
        Get the given item from the dictionary if it is there & return it
        :param item_type: int or str, the type of item to return
        :param source: the dictionary to read from
        :param name: the name of the item
        :return: The contents
        """
        val = source[name] if name in source else None
        if val and item_type == "int":
            return int(val)
        return val

    @staticmethod
    def main(argv=None) -> int:
        """Run ProcessEnexFile from the command line.

        Usage example:
          python -m enex_export.process_en_file --store-path /path/to/store --db-path /path/to/db.sqlite /path/to/input.enex
        """
        import argparse

        parser = argparse.ArgumentParser(
            prog="enex_export.process_en_file",
            description="Process an Evernote .enex file and store contents/metadata.",
        )
        parser.add_argument(
            "enex_file",
            help="Path to the .enex file to process",
        )
        parser.add_argument(
            "--store-path",
            required=True,
            help="Directory path where extracted files should be stored",
        )
        parser.add_argument(
            "--db-path",
            required=True,
            help="Path to the SQLite database (or DB URL) where metadata is stored",
        )

        args = parser.parse_args(argv)

        processor = ProcessEnexFile(file_path=args.store_path, path_to_db=args.db_path)
        processor.process_file(args.enex_file)

        return 0

if __name__ == "__main__":
    import sys

    sys.exit(ProcessEnexFile.main(sys.argv[1:]))
