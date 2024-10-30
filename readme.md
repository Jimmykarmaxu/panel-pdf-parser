This is a POC repo to demonstrate the parsing of different panel pdfs 

Due to the unique structure of different lab pdfs, we have to create multiple script to parse them. There are mutliple sub folders to store those scripts and example pdf 

make sure you have python installed in your environment 

`brew install python`

Make sure python is available 

`python3 --versionn`

Install the pdf utility tool 

`pipx install pdfplumber`

Run the code with python for example in alere folder 

`python3 alere.py`

To run the ai example 

create .env file and put in token like this

`OPENAI_API_KEY=hello world`