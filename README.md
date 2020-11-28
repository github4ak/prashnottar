# prashnottar

CS-6340 Natural Language Processing project

Term: Fall, 2020

Authors
* [Abishek Krishnan](https://github.com/github4ak)
* [Monesha Murdeshwar](https://github.com/moneshamurdeshwar)

Overview
--------
Prashnottar(प्रश्नोत्तर): A hindi word which means "question and answer".

We have built a Question-Answering system for reading compreshension tasks using NLP techniques, which are mostly based on the [Quarc](https://www.cs.utah.edu/~riloff/pdfs/quarc.pdf) paper.

Setup steps
----------
- Download stopwords set <br/>
`$ python3 -m nltk.downloader stopwords`
- Download names set <br/>
`$ python3 -m nltk.downloader names`
- If needed, upgrade pip3 <br/>
`$ pip3 install --upgrade pip`
- Download spaCy <br/>
`$ pip3 install -U spacy`
- Download spaCy's english language model <br/>
`$ python3 -m spacy download en_core_web_sm`
- Download Average perceptron tagger <br/>
`$ python3 -m nltk.downloader averaged_perceptron_tagger`
- Download Punkt <br/>
`$ python3 -m nltk.downloader punkt`
- Change the first line of test_input.txt to match your file path to test (e.g. developset-v2) folder

Run steps
---------
- Run `$ python3 qa.py test_input.txt`
    - Generates two files, 'my_custom_list.response' and 'my_custom_list.answers' in the scoring_program folder

- Run the scoring program (from the scoring_program folder)
    - `$ perl score-answers.pl my_custom_list.response my_custom_list.answers`

Results
-------
*We got an average f-measure of 0.3141 on our mid-point evaluation (on testset1) and 0.425 on our final evaluation.*
