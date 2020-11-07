# prashnottar

- Moved from Windows (Visual Studio) to Ubuntu (PyCharm), as working with spaCy and NLTK packages in Windows was getting difficult.

- Change the first line of test_input.txt to match your file path to developset-v2 folder

- Download stopwords set `python3 -m nltk.downloader stopwords`
- Download names set `python3 -m nltk.downloader names`
- Download spaCy `pip install -U spacy`
- Download spaCy's english language model `python3 -m spacy download en_core_web_sm`
- Download Average perceptron tagger `python3 -m nltk.downloader averaged_perceptron_tagger`
 - Run `python3 qa.py test_input.txt`
    - Generates two files, 'my_custom_list.response' and 'my_custom_list.answers' in the scoring_program folder

 - Run the scoring program (from the scoring_program folder)
    - `perl score-answers.pl my_custom_list.response my_custom_list.answers`

*We got an average f-measure of 0.1379 with our initial sentence-question word matching algorithm.*
