"""This will handle all interactions with Google Drive API
Google API documentation found here:
    Drive API  : https://developers.google.com/drive/api/v3/quickstart/python
    Sheets API : https://developers.google.com/sheets/api/quickstart/python
"""

from __future__ import print_function

from pprint import pprint

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import logging
import json

LOGGER = logging.getLogger(f"{__name__}")


class googleApiHelper(object):
    """
    Google Drive API object, through this object youw ill have access to the available API calls
    """
    def __init__(self, service, version):
        """
        Initializer for Google API Helper.
        :param str service: Google API Service.
        :param str version: Google API Service version.
        """
        print("service = %s", service)
        print("version = %s", version)

        creds = None
        scopes = {"sheets": "https://www.googleapis.com/auth/spreadsheets",
                  "drive": "https://www.googleapis.com/auth/drive.metadata.readonly"}
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(f'api/google/configs/token_{service}_{version}.pickle'):
            with open(f'api/google/configs/token_{service}_{version}.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f'api/google/configs/credentials_{service}_{version}.json', scopes[service])
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(f'api/google/configs/token_{service}_{version}.pickle', 'wb') as token:
                pickle.dump(creds, token)

        LOGGER.info(f"Service created for: {service}.{version}")

        self.service = build(service, version, credentials=creds)

    def get_drive_files(self) -> list:
        """
        This will return the file names and ids on google drive.
        :return list: List of dictionaries of file names and ids.
        """
        results = self.service.files().list(pageSize=1000, fields="files(id, name)").execute()

        return results['files']

    def get_file_id(self, filename) -> str:
        """
        This will return the file id based on file name.
        :param str filename: Name of file.
        :return str file_id: File id found.
        """
        print("filename = %s", filename)

        file_id = None
        file_list = self.get_drive_files()
        for file in file_list:
            if file['name'] == filename:
                file_id = file['id']

        return file_id

    def get_sheets_data(self, spreadsheet_id, range='A1:AA1000', major_dimension='ROWS') -> list:
        """
        This will return a list of lists with all spreadsheet data.
        :param str spreadsheet_id: Spreadsheet ID.
        :param str range: Range of data to grab.
        :return list result_values: List of results.
        Example response: api/google/example_responses/get_sheets_data.json
        """
        print("spreadsheet_id = %s", spreadsheet_id)
        print("range = %s", range)
        print("major_dimensions = %s", major_dimension)

        results = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range,
            majorDimension=major_dimension).execute()
        result_values = results['values']
        print(json.dumps(result_values, indent=1))
        return result_values

    def get_spreadsheet_properties(self, spreadsheet_id) -> dict:
        """
        Function will return all properties about a spreadsheet (worksheets, charts, etc.)
        :param str spreadsheet_id: Spreadsheet ID.
        :return dict response: Response dictionary with properties.
        Example response: api/google/example_responses/get_worksheets_in_spreadsheet.json
        """
        request = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id)
        response = request.execute()
        return response

    def get_worksheets_in_spreadsheet(self, spreadsheet_id) -> list:
        """
        Function will return worksheets in a spreadsheet.
        :param str spreadsheet_id: Spreadsheet ID.
        :return list response: Response dictionary with properties.
        Example response: api/google/example_responses/get_worksheets_in_spreadsheet.json
        """
        response = self.get_spreadsheet_properties(spreadsheet_id)
        return response['sheets']

    def get_worksheet_id_by_name(self, spreadsheet_id, worksheet_name):
        """
        Function will return worksheet ID.
        :param spreadsheet_id: Spreadsheet ID.
        :param worksheet_name: Worksheet name.
        :return:
        """
        list_of_worksheets = self.get_worksheets_in_spreadsheet(spreadsheet_id)

        for worksheet in list_of_worksheets:
            print(worksheet)
