import sys
import spacy
from nltk.corpus import stopwords
from nltk.corpus import names
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize


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


def print_formatted_output(stories):
    output_filename = "my_custom_list.response"

    # Clear the file
    open(output_filename, "w").close()

    output_file_content = ""

    for story in stories:
        for q in story.story_questions:
            question_id_response = "QuestionID: " + q.question_id
            print(question_id_response)
            output_file_content += question_id_response + "\n"
            answer = get_answer(story.text, q.question_text)
            answer_response = "Answer: " + answer + "\n"
            print(answer_response)
            output_file_content += answer_response + "\n"

    # Write the output
    with open(output_filename, "a") as f3:
        f3.write(output_file_content.rstrip())


def get_answer(story_text, question_text):
    sentences_dict = get_sentence_tokenized(story_text)
    max_sentence_index = 0
    sentence_score_dict = {}

    # Tokenize question text
    question_words = []
    for word in word_tokenize(question_text):
        question_words.append(word.lower())

    for key, value in sentences_dict.items():
        curr_score = 0
        # Remove stop words and tokenize
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(value)
        sentence_words = [w for w in word_tokens if w not in stop_words]

        # Remove non-alphanumeric words
        clean_sentence_words = []
        for word in sentence_words:
            if word.isalpha():
                clean_sentence_words.append(word.lower())

        # Evaluate word-match score
        curr_score += get_word_match_score_for_sentence(clean_sentence_words, question_words)

        if question_words.__contains__("who"):
            curr_score += update_score_for_who(value, question_text, question_words)
        sentence_score_dict[key] = curr_score

    # Return single line equivalent of multi-line sentence to concur with the scoring system
    return get_most_likely_sentence(sentence_score_dict, sentences_dict)


def get_most_likely_sentence(sentence_score_dict, sentences_dict):
    sorted_sentence_score_dict = {k: v for k, v in
                                  sorted(sentence_score_dict.items(), key=lambda item: item[1], reverse=True)}

    # Need to add tie-breaker logic

    return sentences_dict[list(sorted_sentence_score_dict)[0]].replace("\n", " ")


def update_score_for_who(value, question_text, question_words):
    s_contains_person = False
    q_contains_person = False
    score = 0

    nlp_ner_tagging = spacy.load("en_core_web_sm")
    tagged_sentence = nlp_ner_tagging(value)
    tagged_question = nlp_ner_tagging(question_text)

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

    names_male_list = [name.lower() for name in names.words('male.txt')]
    names_female_list = [name.lower() for name in names.words('male.txt')]
    names_list = names_male_list + names_female_list

    for tagged_words in tagged_sentence.ents:
        if tagged_words.label_ == "PERSON":
            text = tagged_words.text
            name_words = text.split(" ")
            for name in name_words:
                if name.lower() in names_list:
                    score += 20
                    break

    return score


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
    output_filename = "my_custom_list.answers"

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
