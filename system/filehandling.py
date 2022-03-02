import os


class FileHandling:

    def __init__(self, SPAR10_directory):
        self.dir = SPAR10_directory

    def create_folder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_all_paths(self):
        UPLOAD_FOLDER = self.create_folder(self.dir + '/static/uploads')
        DOWNLOAD_FOLDER = self.create_folder(self.dir + '/static/downloads')

        REDACTION_FOLDER = self.create_folder(UPLOAD_FOLDER + '/redaction')
        REVSUM_FOLDER = self.create_folder(
            UPLOAD_FOLDER + '/review_summarization')
        PARASUM_FOLDER = self.create_folder(
            UPLOAD_FOLDER + '/para_summarization')
        EXTRACTION_FOLDER = self.create_folder(
            UPLOAD_FOLDER + '/text_extraction')
        DOCCLASS_FOLDER = self.create_folder(
            UPLOAD_FOLDER + '/document_classification')

        return UPLOAD_FOLDER, DOWNLOAD_FOLDER, REDACTION_FOLDER, REVSUM_FOLDER, PARASUM_FOLDER, EXTRACTION_FOLDER, DOCCLASS_FOLDER
