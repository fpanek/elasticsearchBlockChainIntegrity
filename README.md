Detailed Readme will follow.


Short Description how to use:
For simple operation only three python files are required. "prepareSystemService.py" needs to executed first. This part is responsible for testing connectivity to the database, to the blockchain but it also verify if the smart contract is already deployed and if not deploys it or a newer version of it. In the next step data can be inserted into the monitored indexes. If the application is not running all the time it is now time to create a checksum for the inserted documents executing "secureIntegrityService.py". Which will create a checksum of each inserted document and stores it in the blockchain. Now the data could be altered. After the modification the data is verified using the "verifyIntegrityService.py" script. If the inserted data was tampered a new file called integrityResult.json is created. This file contains the modified documents and their actual content.
