# prashnottar

- Change the first line of test_input.txt to match your file path to developset-v2 folder
- Download perl (for Windows) https://www.activestate.com/products/perl/downloads/ (I aslo added a extension for VS Code which was part of the installation process)

To run on terminal (in Windows) - python .\qa.py test_input.txt

- Generates two files, 'my_custom_list.response' and 'my_custom_list.answers' in the same folder
- Copy these two files to the scoring_program folder

To run on termial (from the scoring_program folder) - perl .\score-answers.pl .\my_custom_list.response .\my_custom_list.answers 
