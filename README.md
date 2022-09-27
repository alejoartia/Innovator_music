# Innovator_music
This is a repo for an app created in django, in order to upload , process and download files, this is created for a test MusicBMAT 
was used sync_to_async in order to handle multiples request at the same time 
and its possible to upload multiples files at the same time 

## How to run 

  $ git clone https://github.com/alejoartia/Innovator_music.git
  
  $ python manage.py makemigrations  
  
  $ python manage.py migrate     
  
  $ python3 manage.py runserver  
  
  
### go to localhost:  http://127.0.0.1:8000/
  
 ## ![alt text](https://github.com/alejoartia/Innovator_music/blob/master/imgreadme.png)
 
 Clic in the button BROWSE to select the CSV file you want to upload and then click UPLOAD 
 Its possible to upload many files at the same time
 
 after that you will be able to see and hiperlink (Download) if you click there you will be able to download the processed file
 
 the CSV file should have an structure similar to this structure:
 
| Song         | Date            | Number of Plays |
| :------------|:---------------:| -----:|
| Umbrella     | 2020-01-02      | 200   |
| Umbrella     | 2020-01-01      | 200   |
| In The End   | 2020-01-01      | 100   |



## CSV processing module explanation

This module is in https://github.com/alejoartia/Innovator_music/blob/master/CsvProcessing/csvprocessing.py 
Here its recived a dict (payload) from the original file and then processed to return last_payload_files

<pre>
		```
		
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

		```
</pre>



