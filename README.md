# prashnottar

- Moved from Windows (Visual Studio) to Ubuntu (PyCharm), as working with spaCy and NLTK packages in Windows was getting difficult.

- Change the first line of test_input.txt to match your file path to developset-v2 folder

- Download stopwords set `python3 -m nltk.downloader stopwords`
 - Run `python3 qa.py test_input.txt`
    - Generates two files, 'my_custom_list.response' and 'my_custom_list.answers' in the same folder
    - Copy these two files to the scoring_program folder

 - Run the scoring program (from the scoring_program folder)
    - `perl score-answers.pl my_custom_list.response my_custom_list.answers`

*We got an average f-measure of 0.1379 with our initial sentence-question word matching algorithm.*