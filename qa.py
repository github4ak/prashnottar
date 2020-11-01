import sys


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

    # Print formatted ouput
    print_formatted_output(stories)


def get_story_objects(directory_path, input_file_contents):

    temp = []

    for i in range(1, len(input_file_contents)):
        story_file_path = directory_path + "\\" + \
            str(input_file_contents[i]).rstrip() + ".story"
        question_file_path = directory_path + "\\" + \
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
                question_text = question_contents[i+1].split(":")[1].strip()
                question_difficulty = question_contents[i+2].split(":")[
                    1].strip()
                questions.append(
                    Question(question_id, question_text, question_difficulty))
        temp.append(Story(story_headline, story_date,
                          story_id, story_text, questions))

    return temp


def print_formatted_output(stories):
    for story in stories:
        for q in story.story_questions:
            print("Question ID: " + q.question_id)
            answer = get_answer(story.text, q.question_text)
            print("Answer: " + answer + "\n")


def get_answer(story_text, question_text):

    # TO ADD LOGIC HERE
    return "insert-answer-string"


if __name__ == "__main__":
    main(sys.argv[1:])
