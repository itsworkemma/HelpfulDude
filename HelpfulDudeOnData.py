import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from openai import OpenAI

from flask import Flask
app = Flask(__name__)

### get the OPENAI KEY from env file
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return """<form action="" method="get">
                <label for="orgname">What is your organisation called?</label><br>
                <input type="text" id="orgname" name="orgname">
                <label for="orgpurpose">What is your organisations purpose?</label><br>
                <input type="text" id="orgpurpose" name="orgpurpose">
                <label for="focusarea">Tell me about the area you want to focus on:</label><br>
                <input type="text" id="focusarea" name="focusarea">
                <label for="problem">Tell me about the problem(s) you are trying to solve?</label><br>
                <input type="text" id="problem" name="problem">
                <label for="questions">Imagine the data was a person blahblah etc what questions would you ask?</label><br>
                <input type="text" id="questions" name="questions">
                <label for="knowledge">What knowledge would you like to gain after your meeting?</label><br>
                <input type="text" id="knowledge" name="knowledge">
                <label for="actions">What sort of actions would you expect to take after the meeting, based on your discussion?</label><br>
                <input type="text" id="actions" name="actions">
                <input type="submit" value="please and thanks">
              </form>"""

"""
### collect user input basic mode
orgname = input("What is your organisation called?")
orgpurpose = input("What is your organisations purpose?")
focusarea = input("Tell me about the area you want to focus on:")
problem = input("Tell me about the problem(s) you are trying to solve?")
questions = input("Imagine the data was a person blahblah etc what questions would you ask?")
knowledge = input("What knowledge would you like to gain after your meeting?")
actions = input("What sort of actions would you expect to take after the meeting, based on your discussion?")

### collect user input static answers
orgname = "bert"
orgpurpose = "a thriving area with happy residents"
focusarea = "the planning department and planning applications"
problem = "applications taking ages to be assessed and decided on, residents unhappy with developments proposed"
questions = "what could we change in our application process? why are they taking so long? how can we work better with residents and deal with unhappiness quickly before it becomes a big issue?"
knowledge = "why local residents are so anti development"
actions = "improve our planning application process, find new or better ways to engage with residents on proposed applications"
"""

###@app.route("/")
### assemble the prompt
def request_action_plan(orgname, orgpurpose, focusarea, problem, questions, knowledge, actions):
    messages = [{"role": "system",
                 "content": "You are a consultant specialising in data analysis for local councils. Your clients contact you with details of their priorities and problems. Your clients want to start leveraging their data to improve the efficiency of their operations, enable them to better respond to change and to provide improved services to their residents. They are often overwhelmed with the scale of the task and get caught up on creating dashboards and reports from data that is easily available, rather than focusing on the outcomes they want to achieve. You help them by advising on action plans that help them identify improvements and deliver meaningful change. You use a structured thinking technique that involves four key activities: recognizing the current problem or situation, organizing available information, identifying gaps and opportunities, and identifying your options."}]
    prompt = """You have been contcated by {orgname} who's purpose is {orgpurpose}. They would like to focus on {focusarea} to resolve the following problem(s): {problem}.
    Their goals are:
    They would like to leverage their data to answer the following questions: {questions}.
    They would like to gain the following knowledge: {knowledge}.
    After your meeting they should be in a position to take the following actions: {actions}.
    Please work through their brief using structured thinking, and explain your thought process. At the end please produce a bullet point action plan for the client to work towards their goals.""".format(orgname=orgname, orgpurpose=orgpurpose, focusarea=focusarea, problem=problem, questions=questions, knowledge=knowledge, actions=actions)
    
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
   
    return prompt, response.choices[0].message.content


###print(request_action_plan(orgname, orgpurpose, focusarea, problem, questions, knowledge, actions))

#run on dev server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

