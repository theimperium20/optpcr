# optpcr
A python script to fetch FNO stocks from NSE and find the Put to Call ratio of the options. The script also writes the data to a google sheet.


Requirements:
Requests<br>
`pipenv install requests`

Pandas<br>
`python3 -m pip install --upgrade pandas`

Beautiful Soup<br>
`pip install beautifulsoup4`

lxml<br>
`pip install lxml`

Pygsheets -- thanks to @nithinmurali for this amazing tool<br>
`pip install pygsheets`<br>
*the documentation of the tool is kinda messed up. Read the documentation here : https://pygsheets.readthedocs.io/index.html<br>

<b><h4>How to use :</h4></b>
1) Enable Sheets API and Drive API and download Service account credentials in a JSON file.
2) Replace the YOUR_CREDENTIAL_FILE_HERE.json' with the path to the json file you downloaded.
3) The files created by service account are not visible in your account. Replace `YOUR_EMAIL_HERE` with your Gmail id to be able to access the   files.<br>
            `sh.share('YOUR_EMAIL_HERE', role='writer', expirationTime=None, is_group=False)`<br>
4) By default the sheet is publicly accesible, you can change it by commenting out this line<br>
             `sh.share('anyone', role='reader', expirationTime=None, is_group=False)`
   *note : By doing this, only email-ids that you share the file with will be able to access the file.
