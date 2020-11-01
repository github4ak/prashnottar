class Story:
    def __init__(self, headline, date, story_id, text):
        self.headline = headline
        self.date = date
        self.story_id = story_id
        self.text = text

class Question:
    def __init__(self, question_id, question_text, question_difficulty):
        self.question_id = question_id
        self.question_text = question_text
        self.question_difficulty = question_difficulty

import sys

def main(argv):

    # Read the input file
    with open(argv[0], 'r') as f:
        input_file_contents = f.readlines()

    directory_path = input_file_contents[0].rstrip()

    # Create lists for stories and questions
    stories = []
    questions = []

    for i in range(1,len(input_file_contents)):
        story_file_path = directory_path + "\\" + str(input_file_contents[i]).rstrip() + ".story"
        question_file_path = directory_path + "\\" + str(input_file_contents[i]).rstrip() + ".questions"
        # Create story
        with open(story_file_path, 'r') as s:
            story_contents = s.readlines()
            story_headline = story_contents[0].split(":")[1].strip()
            story_date = story_contents[1].split(":")[1].strip()
            story_id = story_contents[2].split(":")[1].strip()
            story_text = ""
            # Get the text portion of the story, Note: TO CHECK LIST INDEXING
            for i in range(6,len(story_contents)):
                story_text += str(story_contents[i])
            stories.append(Story(story_headline,story_date,story_id,story_text))
        # Create question
        with open(question_file_path,'r') as q:
            question_contents = q.readlines()
            for i in range(0, len(question_contents), 4):
                question_id = question_contents[i].split(":")[1].strip()
                question_text = question_contents[i+1].split(":")[1].strip()
                question_difficulty = question_contents[i+2].split(":")[1].strip()
                print(question_text)
                questions.append(Question(question_id, question_text, question_difficulty))

if __name__ == "__main__":
    main(sys.argv[1:])