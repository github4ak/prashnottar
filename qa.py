import sys
import spacy
from nltk.corpus import stopwords
from nltk.corpus import names
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag


class Story:
    def __init__(self, headline, date, story_id, text, story_questions):
        self.headline = headline
        self.date = date
        self.story_id = story_id
        self.text = text
        self.story_questions = story_questions


class Question:
    def __init__(self, question_id, question_text, question_difficulty):
        self.question_id = question_id
        self.question_text = question_text
        self.question_difficulty = question_difficulty


def main(argv):
    # Read the input file
    with open(argv[0], 'r') as f:
        input_file_contents = f.readlines()
    directory_path = input_file_contents[0].rstrip()

    # Create list of stories together with its questions
    stories = get_story_objects(directory_path, input_file_contents)

    # Print formatted output and make the response file
    print_formatted_output(stories)

    # Make the perfect answer file
    make_perfect_answer(directory_path, input_file_contents)


def get_story_objects(directory_path, input_file_contents):
    temp = []

    for i in range(1, len(input_file_contents)):
        story_file_path = directory_path + "/" + \
                          str(input_file_contents[i]).rstrip() + ".story"
        question_file_path = directory_path + "/" + \
                             str(input_file_contents[i]).rstrip() + ".questions"
        questions = []
        # Create story
        with open(story_file_path, 'r') as s:
            story_contents = s.readlines()
            story_headline = story_contents[0].split(":")[1].strip()
            story_date = story_contents[1].split(":")[1].strip()
            story_id = story_contents[2].split(":")[1].strip()
            story_text = ""
            # Get the text portion of the story, Note: TO CHECK LIST INDEXING
            for i in range(6, len(story_contents)):
                story_text += str(story_contents[i])
        # Append question list to story
        with open(question_file_path, 'r') as q:
            question_contents = q.readlines()
            for i in range(0, len(question_contents), 4):
                question_id = question_contents[i].split(":")[1].strip()
                question_text = question_contents[i + 1].split(":")[1].strip()
                question_difficulty = question_contents[i + 2].split(":")[
                    1].strip()
                questions.append(
                    Question(question_id, question_text, question_difficulty))
        temp.append(Story(story_headline, story_date,
                          story_id, story_text, questions))

    return temp


def get_sentence_ner(nlp_ner_tagging, sentences_dict):
    tagged_sentence_dict = {}
    for key, value in sentences_dict.items():
        tagged_sentence_dict[key] = nlp_ner_tagging(value)
    return tagged_sentence_dict


def get_question_tokenized(question_text):
    question_words = []
    for word in word_tokenize(question_text):
        question_words.append(word.lower())
    return question_words


def get_word_tokenize(sentences_dict):
    word_tokens_dict = {}
    for key, value in sentences_dict.items():
        word_tokens_dict[key] = word_tokenize(value)

    return word_tokens_dict


def get_word_score_for_each_sentence(sentences_dict, question_words):
    sentence_score_dict = {}
    for key, value in sentences_dict.items():
        # Remove stop words and tokenize
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(value)
        sentence_words = [w for w in word_tokens if w not in stop_words]

        # Remove non-alphanumeric words
        clean_sentence_words = []
        for word in sentence_words:
            if word.isalpha():
                clean_sentence_words.append(word.lower())
        sentence_score_dict[key] = get_word_match_score_for_sentence(clean_sentence_words, question_words)
    return sentence_score_dict


def print_formatted_output(stories):
    output_filename = "scoring_program/my_custom_list.response"

    # Clear the file
    open(output_filename, "w").close()

    output_file_content = ""

    nlp_ner_tagging = spacy.load("en_core_web_sm")

    for story in stories:
        # For each story, get tokenized sentence
        sentences_dict = get_sentence_tokenized(story.text)
        # Prepare NER tags for each sentence
        tagged_sentence_dict = get_sentence_ner(nlp_ner_tagging, sentences_dict)
        #  For each sentence in story, get tokenized words
        word_tokens_dict = get_word_tokenize(sentences_dict)
        for q in story.story_questions:
            question_id_response = "QuestionID: " + q.question_id
            print(question_id_response)
            output_file_content += question_id_response + "\n"
            # Prepare NER tags for the current question
            tagged_question = nlp_ner_tagging(q.question_text)
            # Tokenize question sentence
            question_words = get_question_tokenized(q.question_text)
            # Get word-match score for each sentence
            sentence_score_dict = get_word_score_for_each_sentence(sentences_dict, question_words)
            # Get answer based on question-type
            answer = get_answer(sentences_dict, q.question_text, question_words, tagged_sentence_dict, tagged_question,
                                sentence_score_dict, word_tokens_dict)
            answer_response = "Answer: " + answer + "\n"
            print(answer_response)
            output_file_content += answer_response + "\n"

    # Write the output
    with open(output_filename, "a") as f3:
        f3.write(output_file_content.rstrip())


def get_answer(sentences_dict, question_text, question_words, tagged_sentence_dict, tagged_question,
               sentence_score_dict, word_tokens_dict):
    for key, value in sentences_dict.items():
        if question_words.__contains__("who"):
            sentence_score_dict[key] += update_score_for_who(value, question_text, question_words,
                                                             tagged_sentence_dict[key], tagged_question)
        elif question_words.__contains__("what"):
            sentence_score_dict[key] += update_score_for_what(value, question_text, question_words,
                                                              tagged_sentence_dict[key], tagged_question,
                                                              word_tokens_dict[key])

    # Return single line equivalent of multi-line sentence to concur with the scoring system
    return get_most_likely_sentence(sentence_score_dict, sentences_dict)


def get_most_likely_sentence(sentence_score_dict, sentences_dict):
    sorted_sentence_score_dict = {k: v for k, v in
                                  sorted(sentence_score_dict.items(), key=lambda item: item[1], reverse=True)}

    # TODO:Need to add tie-breaker logic

    return sentences_dict[list(sorted_sentence_score_dict)[0]].replace("\n", " ")


def update_score_for_what(value, question_text, question_words, tagged_sentence, tagged_question, word_tokens):
    score = 0
    s_contains_name = False
    q_contains_name = False
    month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                  'november', 'december']

    if len(set(month_list).intersection(question_words)) != 0 and (
            value.contains("today") or value.contains("yesterday") or value.contains("tomorrow") or value.contains(
            "last night")):
        score += 3

    if question_words.__contains__("kind") and (("call" in value) or ("from" in value)):
        score += 4

    names_list = get_name_list()

    for tagged_words in tagged_question.ents:
        if tagged_words.label_ == "PERSON":
            text = tagged_words.text
            name_words = text.split(" ")
            for name in name_words:
                if name.lower() in names_list:
                    q_contains_name = True
                    break

    for tagged_words in tagged_sentence.ents:
        if tagged_words.label_ == "PERSON":
            text = tagged_words.text
            name_words = text.split(" ")
            for name in name_words:
                if name.lower() in names_list:
                    s_contains_name = True
                    break

    if q_contains_name and (s_contains_name or ("call" in value) or ("known" in value)):
        score += 20

    # TODO:To build Rule#5: pos_tagged_sentence = pos_tag(word_tokens)

    return score


def update_score_for_who(value, question_text, question_words, tagged_sentence, tagged_question):
    score = 0
    s_contains_person = False
    q_contains_person = False

    for tagged_words in tagged_sentence.ents:
        if tagged_words.label_ == "PERSON":
            s_contains_person = True
            break

    for tagged_words in tagged_question.ents:
        if tagged_words.label_ == "PERSON":
            q_contains_person = True
            break

    if not q_contains_person and s_contains_person:
        score += 6

    if not q_contains_person and question_words.__contains__("name"):
        score += 4

    names_list = get_name_list()

    for tagged_words in tagged_sentence.ents:
        if tagged_words.label_ == "PERSON":
            text = tagged_words.text
            name_words = text.split(" ")
            for name in name_words:
                if name.lower() in names_list:
                    score += 20
                    break

    return score


def get_name_list():
    names_male_list = [name.lower() for name in names.words('male.txt')]
    names_female_list = [name.lower() for name in names.words('male.txt')]
    return names_male_list + names_female_list


def get_sentence_tokenized(story_text):
    sentences = sent_tokenize(story_text)

    sentences_dict = {}

    for i, s in enumerate(sentences):
        sentences_dict[i] = s

    return sentences_dict


def get_word_match_score_for_sentence(clean_sentence_words, question_words):
    intersection_len = get_intersection_length(clean_sentence_words, question_words)
    sentence_len = len(clean_sentence_words)

    match_number = intersection_len / sentence_len

    # Scoring range 3,4 and 6
    score = 0
    if match_number > 0.8:
        score = 6
    elif match_number > 0.4:
        score = 4
    else:
        score = 3

    return score


def get_intersection_length(clean_sentence_words, question_words):
    intersection_words = [word for word in clean_sentence_words if word in question_words]
    return len(intersection_words)


def make_perfect_answer(directory_path, input_file_contents):
    output_filename = "scoring_program/my_custom_list.answers"

    # Clear the file
    open(output_filename, "w").close()

    output_file_content = ""

    for i in range(1, len(input_file_contents)):
        answer_file_path = directory_path + "/" + \
                           str(input_file_contents[i]).rstrip() + ".answers"
        # Create answers
        with open(answer_file_path, 'r') as a:
            answer_content = a.readlines()
            for answer_line in answer_content:
                output_file_content += answer_line

    # Write the output
    with open(output_filename, "a") as f3:
        f3.write(output_file_content.rstrip())


if __name__ == "__main__":
    main(sys.argv[1:])
