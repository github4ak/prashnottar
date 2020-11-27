# prashnottar

Moved from Windows (Visual Studio) to Ubuntu (PyCharm), as working with spaCy and NLTK packages in Windows was getting difficult.

Steps to setup the project locally,

- Download stopwords set `python3 -m nltk.downloader stopwords`
- Download names set `python3 -m nltk.downloader names`
- If needed, upgrade pip3 `pip3 install --upgrade pip`
- Download spaCy `pip3 install -U spacy`
- Download spaCy's english language model `python3 -m spacy download en_core_web_sm`
- Download Average perceptron tagger `python3 -m nltk.downloader averaged_perceptron_tagger`
- Download Punkt `python3 -m nltk.downloader punkt`
- Change the first line of test_input.txt to match your file path to developset-v2 folder

Steps to run the project locally,

 - Run `python3 qa.py test_input.txt`
    - Generates two files, 'my_custom_list.response' and 'my_custom_list.answers' in the scoring_program folder

 - Run the scoring program (from the scoring_program folder)
    - `perl score-answers.pl my_custom_list.response my_custom_list.answers`

Our results,

*We got an average f-measure of 0.3141 for our mid-point evaluation (on testset-2) and 0.425 for our final evaluation.*
