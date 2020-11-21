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
        story_file_path = directory_path + \
                          str(input_file_contents[i]).rstrip() + ".story"
        question_file_path = directory_path + \
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
        sentence_score_dict[key] = get_word_match_score_for_sentence(word_tokens, clean_sentence_words, question_words)
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
                                sentence_score_dict, word_tokens_dict, nlp_ner_tagging)
            answer_response = "Answer: " + answer + "\n"
            print(answer_response)
            output_file_content += answer_response + "\n"

    # Write the output
    with open(output_filename, "a") as f3:
        f3.write(output_file_content.rstrip())


def get_answer(sentences_dict, question_text, question_words, tagged_sentence_dict, tagged_question,
               sentence_score_dict, word_tokens_dict, nlp_ner_tagging):
    current_question_type = ""

    if question_words.__contains__("who"):
        current_question_type = "who"
        for key, value in sentences_dict.items():
            sentence_score_dict[key] += update_score_for_who(value, question_text, question_words,
                                                             tagged_sentence_dict[key], tagged_question)

    elif question_words.__contains__("what"):
        current_question_type = "what"
        for key, value in sentences_dict.items():
            sentence_score_dict[key] += update_score_for_what(value, question_text, question_words,
                                                              tagged_sentence_dict[key], tagged_question,
                                                              word_tokens_dict[key])

    elif question_words.__contains__("when"):
        current_question_type = "when"
        for key, value in sentences_dict.items():
            sentence_score_dict[key] += update_score_for_when(value, question_text, question_words,
                                                              tagged_sentence_dict[key], tagged_question,
                                                              word_tokens_dict[key])

    elif question_words.__contains__("where"):
        current_question_type = "where"
        for key, value in sentences_dict.items():
            sentence_score_dict[key] += update_score_for_where(value, question_text, question_words,
                                                               tagged_sentence_dict[key], tagged_question,
                                                               word_tokens_dict[key])

    elif question_words.__contains__("why"):
        current_question_type = "why"
        sentence_score_dict = update_score_for_why(sentences_dict, sentence_score_dict, question_text, question_words,
                                                   tagged_sentence_dict, tagged_question,
                                                   word_tokens_dict)

    elif question_words.__contains__("how"):
        current_question_type = "how"
        for key, value in sentences_dict.items():
            sentence_score_dict[key] += update_score_for_how(value, question_text, question_words,
                                                             tagged_sentence_dict[key], tagged_question,
                                                             word_tokens_dict[key])

    # Return single line equivalent of multi-line sentence to concur with the scoring system
    return get_most_likely_sentence(question_words, sentence_score_dict, sentences_dict, current_question_type,
                                    nlp_ner_tagging)


def get_most_likely_sentence(question_words, sentence_score_dict, sentences_dict, current_question_type,
                             nlp_ner_tagging):
    sorted_sentence_score_dict = {k: v for k, v in
                                  sorted(sentence_score_dict.items(), key=lambda item: item[1], reverse=True)}

    # TODO:Need to add tie-breaker logic

    best_sentence = sentences_dict[list(sorted_sentence_score_dict)[0]].replace("\n", " ")

    pos_tagged_best_sentence = pos_tag(word_tokenize(best_sentence))
    ner_tagged_best_sentence = nlp_ner_tagging(best_sentence)

    # TODO: To improve my checking more pos and ner tags, WHAT
    best_extracted_sentence = ""
    if current_question_type == "who":
        for e in ner_tagged_best_sentence.ents:
            if e.label_ == "PERSON":
                best_extracted_sentence += e.text + " "

    elif current_question_type == "what":
        # To do something
        best_extracted_sentence = ""

    elif current_question_type == "why":
        # To do something
        best_extracted_sentence = ""

    elif current_question_type == "when":
        for e in ner_tagged_best_sentence.ents:
            if e.label_ == "DATE" or e.label_ == "TIME":
                best_extracted_sentence += e.text + " "

    elif current_question_type == "where":
        for e in ner_tagged_best_sentence.ents:
            if e.label_ == "LOC" or e.label_ == "GPE" or e.label_ == "FAC" or e.label_ == "EVENT":
                best_extracted_sentence += e.text + " "

    elif current_question_type == "how":
        if question_words.__contains__("much"):
            for e in ner_tagged_best_sentence.ents:
                if e.label_ == "PERCENT" or e.label_ == "MONEY" or e.label_ == "ORDINAL":
                    best_extracted_sentence += e.text + " "

        if question_words.__contains__("many"):
            for e in ner_tagged_best_sentence.ents:
                if e.label_ == "QUANTITY" or e.label_ == "ORDINAL" or e.label_ == "CARDINAL":
                    best_extracted_sentence += e.text + " "

        if question_words.__contains__("old") or question_words.__contains__("often"):
            for e in ner_tagged_best_sentence.ents:
                if e.label_ == "DATE":
                    best_extracted_sentence += e.text + " "

        if question_words.__contains__("tall") or question_words.__contains__("large") or question_words.__contains__(
                "high") or question_words.__contains__("deep"):
            for e in ner_tagged_best_sentence.ents:
                if e.label_ == "QUANTITY":
                    best_extracted_sentence += e.text + " "

        if question_words.__contains__("long"):
            for e in ner_tagged_best_sentence.ents:
                if e.label_ == "QUANTITY" or e.label_ == "DATE" or e.label_ == "TIME":
                    best_extracted_sentence += e.text + " "

        if question_words.__contains__("far"):
            for e in ner_tagged_best_sentence.ents:
                if e.label_ == "QUANTITY" or e.label_ == "TIME":
                    best_extracted_sentence += e.text + " "

    if best_extracted_sentence != "":
        return best_extracted_sentence
    else:
        return best_sentence


def get_best_sentences(sentences_dict, sentence_score_dict):
    sorted_sentence_score_dict = {k: v for k, v in
                                  sorted(sentence_score_dict.items(), key=lambda item: item[1], reverse=True)}

    best_word_match_score = list(sorted_sentence_score_dict)[0]

    best_sentence_dict = {}

    for key, value in sentences_dict.items():
        if value == best_word_match_score:
            best_sentence_dict[key] = value

    return best_sentence_dict


def update_score_for_why(sentences_dict, sentence_score_dict, question_text, question_words, tagged_sentence_dict,
                         tagged_question, word_tokens_dict):
    best_sentences_dict = get_best_sentences(sentences_dict, sentence_score_dict)

    for key, value in best_sentences_dict.items():
        sentence_score_dict[key] += 3
        prev_s = key - 1
        next_s = key + 1
        if prev_s >= 0:
            sentence_score_dict[prev_s] += 3
        if next_s < len(best_sentences_dict):
            sentence_score_dict[next_s] += 3
        if "want" in value:
            sentence_score_dict[key] += 4
        if "so" in value and "because" in value:
            sentence_score_dict[key] += 4

    return sentence_score_dict


def update_score_for_how(value, question_text, question_words, tagged_sentence, tagged_question, word_tokens):
    score = 0

    tagged_word_label_list = []

    for tagged_words in tagged_sentence.ents:
        tagged_word_label_list.append(tagged_words.label_)

    if question_words.__contains__("much"):
        if "PERCENT" or "MONEY" or "ORDINAL" in tagged_word_label_list:
            score += 10

    if question_words.__contains__("many"):
        if "QUANTITY" or "ORDINAL" or "CARDINAL" in tagged_word_label_list:
            score += 10

    if question_words.__contains__("old") or question_words.__contains__("often"):
        if "DATE" in tagged_word_label_list:
            score += 10

    if question_words.__contains__("tall") or question_words.__contains__("large") or question_words.__contains__(
            "high") or question_words.__contains__("deep"):
        if "QUANTITY" in tagged_word_label_list:
            score += 10

    if question_words.__contains__("long"):
        if "QUANTITY" or "DATE" or "TIME" in tagged_word_label_list:
            score += 10

    if question_words.__contains__("far"):
        if "QUANTITY" or "TIME" in tagged_word_label_list:
            score += 10

    return score


def update_score_for_when(value, question_text, question_words, tagged_sentence, tagged_question, word_tokens):
    score = 0

    for tagged_words in tagged_sentence.ents:
        if tagged_words.label_ in "TIME" or "DATE":
            score += 6
            break

    if question_words.__contains__("last") and (
            ("first" in value) or ("last" in value) or ("since" in value) or ("ago" in value)):
        score += 20

    if question_words.__contains__("start") or question_words.__contains__("begin"):
        if ("start" in value) or ("begin" in value) or ("since" in value) or ("year" in value):
            score += 20

    return score


def update_score_for_where(value, question_text, question_words, tagged_sentence, tagged_question, word_tokens):
    score = 0

    pos_tagged_sentence = pos_tag(word_tokenize(value))

    for tagged_word in pos_tagged_sentence:
        if list(tagged_word)[1] == 'P':
            score += 4

    for tagged_words in tagged_sentence.ents:
        if tagged_words.label_ == "GPE" or tagged_words.label_ == "LOC":
            score += 6
            break

    return score


def update_score_for_what(value, question_text, question_words, tagged_sentence, tagged_question, word_tokens):
    score = 0
    s_contains_name = False
    q_contains_name = False
    month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                  'november', 'december']

    if len(set(month_list).intersection(question_words)) != 0 and (
            ("today" in value) or ("yesterday" in value) or ("tomorrow" in value) or ("last night" in value)):
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

    # Rule 5
    pos_tagged_question = pos_tag(word_tokenize(question_text))

    pos_tagged_sentence = pos_tag(word_tokenize(value))

    for tagged_words in tagged_question.ents:
        if tagged_words.label_ == "PERSON":
            text = tagged_words.text
            name_words = text.split(" ")
            for name in name_words:
                if name.lower() in names_list:
                    for tagged_word in pos_tagged_question:
                        if list(tagged_word)[1] == 'PP':
                            for tag_word in pos_tagged_sentence:
                                if list(tag_word)[1] == 'NNP':
                                    score += 20

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


def get_word_match_score_for_sentence(word_tokens, clean_sentence_words, question_words):
    score = 0

    pos_tagged_sentence = pos_tag(word_tokens)

    pos_tagged_dict = {}

    for tagged_word in pos_tagged_sentence:
        pos_tagged_dict[list(tagged_word)[0].lower()] = list(tagged_word)[1]

    clean_question_words = []
    for word in question_words:
        if word.isalpha():
            clean_question_words.append(word.lower())

    stop_words_english = stopwords.words('english')

    sentence_set = {w for w in clean_sentence_words if not w in stop_words_english}
    question_set = {w for w in clean_question_words if not w in stop_words_english}

    sentence_vector = []
    question_vector = []
    result_vector = sentence_set.union(question_set)
    for w in result_vector:
        if w in sentence_set:
            sentence_vector.append(1)
        else:
            sentence_vector.append(0)
        if w in question_set:
            question_vector.append(1)
        else:
            question_vector.append(0)

    c = 0
    for i in range(len(result_vector)):
        c += sentence_vector[i] * question_vector[i]
    if float((sum(sentence_vector) * sum(question_vector)) ** 0.5) > 0:
        cosine_sim = c / float((sum(sentence_vector) * sum(question_vector)) ** 0.5)
    else:
        cosine_sim = 0

    for word in clean_sentence_words:
        if word in clean_question_words:
            if word in pos_tagged_dict.keys() and pos_tagged_dict[word] == 'VBP':
                # Increase weight when an verb phrase match occurs
                score += 5

    # Multiply by cosine_sim by a factor of x to represent word matches on an average
    return score + cosine_sim * 100


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
