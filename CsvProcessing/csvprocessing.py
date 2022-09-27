import csv


class CsvProcessing:

    def __init__(self):
        self.payload_files = []
        self.last_payload_files = []
        self.dict_files = {}
        self.after_processing_dict = {}
        self.last_payload = {}

    def read_csv(self, payload_files_test):
        """
    ≈    this is in charge to read the csv from input folder
        :return: payload_files
        """

        for row in payload_files_test:
            self.dict_files = {'Song': row['Song'], 'Date': row['Date'],
                               'Song-Date': row['Song'] + ',' + row['Date'],
                               'Number of Plays': int(row['Number of Plays'].strip('\r'))}
            self.payload_files.append(self.dict_files)

    def process_csv(self):
        """
        process_csv do the group by using searching into the payload
        :return: after_processing_dict
        """
        for i in self.payload_files:
            if self.after_processing_dict.get(i['Song-Date']) is not None:
                # If the value exist, sum to the key the value
                self.after_processing_dict[i['Song-Date']] += i['Number of Plays']
            else:
                # if the value does not exist, assign new key with a value
                self.after_processing_dict[i['Song-Date']] = i['Number of Plays']

        # Send the payload or dict processed
        last_payload_files = []
        # data_dict = {"Song": "Song", "Date": "Date", "Total Number of Plays for Date": "Total Number of Plays "
        #                                                                                "for Date"}
        # last_payload_files.append(data_dict)
        for i in self.after_processing_dict.items():
            new = i[0].split(sep=',')
            last_payload = {'Song': new[0],
                            'Date': new[1],
                            'Total Number of Plays for Date': str(i[1])}
            last_payload_files.append(last_payload)
        return last_payload_files



