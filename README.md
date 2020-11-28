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

Example
-------

Given a story, for e.g.
```
A new Canadian radar satellite sees too much, too clearly, according to
NASA, 
the American space agency. NASA is refusing to send the Radarsat-2
satellite into 
the sky.

The United States government says the Canadian satellite provides images
that 
are too revealing for national security. The Radarsat-2 can see objects
as small as 
three metres through clouds and darkness.

"Anything below five metres causes concern to the U.S. intelligence
community," 
said Hugues Gilbert, director of strategic development for the Canadian
Space 
Agency. "But we think that having the three-metre resolution is really
crucial 
to Canadian industry."

The ability of this "eye in the sky" to see such detail would give
Canada a 
competitive edge over the U.S. in the business of earth resources
imagery. These satellites 
can help farmers forecast crop yields, keep track of ice conditions in
the Arctic ocean 
and help mining companies look for mineral
resources.

The Radarsat-2 satellite is owned and operated by Macdonald Dettwiler of 
Richmond, British Columbia, near Vancouver. It cost 300 million
dollars. The government 
of Canada paid for three-quarters of that cost.

The government may pay another space agency to launch the satellite.
```
the following output shows the gold standard and Prashnottar's answer to the questions based on this story,

```
Question: How can the satellite help farmers?
Gold standard answer: it can help forecast crop yields
Prashnottar's answer: These satellites  can help farmers forecast crop yields, keep track of ice conditions in the Arctic ocean  and help mining companies look for mineral resources.

Question: Why might the Canadian government have to get someone else beside NASA to launch the satellite for them?
Gold standard answer: NASA is refusing to send the Radarsat-2 satellite into the sky | NASA Refuses to Launch the Satellite
Prashnottar's answer: The government may pay another space agency to launch the satellite.

Question: Who is concerned about Radarsat-2's powerful abilities?
Gold standard answer: the United States | the U.S. | the U.S. government | the United States government | the U.S. intelligence community
Prashnottar's answer: Hugues Gilbert the Canadian Space  Agency 

Question: Who is the director of strategic development for the Canadian Space Agency?
Gold standard answer: Hugues Gilbert
Prashnottar's answer: Hugues Gilbert the Canadian Space  Agency 
```


Results
-------
*We got an average f-measure of 0.3141 on our mid-point evaluation (on testset1) and 0.425 on our final evaluation.*
