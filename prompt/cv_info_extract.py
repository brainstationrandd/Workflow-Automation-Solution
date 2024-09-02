from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from utils.helper import model_gpt_4o_mini

CV_Extract_Info_Prompt="""
Act as an Expert in Text Analysis.
Given a CV text, your task is to extract the following information from the text and return it in a strict JSON format. You should extract:

- Full name of the candidate
- Email address
- Phone number
- A list of relevant keywords (5-10) from the CV
- Number of years of experience
- List of degrees or certifications
- List of skills mentioned
- Candidate's location (city, state, or country)

Strictly complete the task with the given information only.


CV Text: {cv_text}

The extracted information should be relevant and accurate according to the CV provided.

Strictly follow this output format in the following JSON format:

{{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "phone": "+123456789",
  "keywords": [
    "keyword1",
    "keyword2",
    "keyword3",...
  ],
  "experience": 5,
  "education": [
    "B.Sc. Computer Science",
    "M.Sc. Data Science",...
  ],
  "skills": [
    "Python",
    "Machine Learning",
    "Data Analysis",...
  ],
  "location": "New York, USA"
}}



Strictly give the json output in the above format only.
Dont use the json word in the output. Just provide the json output in the above format.

"""

cv_prompt = ChatPromptTemplate.from_template(
    
    CV_Extract_Info_Prompt 
)

output_parser = StrOutputParser()
chain = cv_prompt | model_gpt_4o_mini | output_parser