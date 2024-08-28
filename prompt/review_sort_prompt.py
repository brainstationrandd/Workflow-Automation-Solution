from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from utils.helper import model_gpt_4o_mini


sort_review_prompt="""
Act as an Expert in HR and Recruitment.
You will be given a CV text and a job description. Your task is to evaluate the CV based on the relevance to the job description and provide a score out of 10 points. Additionally, you should provide a detailed review explaining why the given score was awarded.

You should consider the following aspects for scoring:
1. Relevance of the candidate's skills to the job description.
2. Match of experience level and years of experience to the job requirements.
3. Alignment of educational background with the job description.
4. Specific relevant keywords present in both the CV and the job description.
5. Demonstrated accomplishments that align with the job requirements.
6. Relevance of the candidate's location to the job role.
7. Certifications and degrees that match the job requirements.
8. Clarity and conciseness of the information presented in the CV.
9. Overall presentation and organization of the CV.
10. Any other relevant factors that make the candidate a good fit for the job.

CV Text: {cv_text}

-----------------------------------------

Job Description: {job_desc}

After evaluating the CV based on the job description, strictly provide the output in the following JSON format:

{{
  "score": "8",
  "remarks": [
    "The candidate has relevant skills such as Python and Data Analysis, which align well with the job description.",
    "The experience level matches the job requirement, with 5 years of relevant experience.",
    "The educational background is suitable, having a degree in Computer Science, which is preferred for this role.",
    "The candidate's location is in New York, which is relevant to the job posting.",
    "However, there is a lack of specific certifications that could enhance the candidate's profile.",
    "The CV is well-organized and easy to read."
  ]
}}

Strictly give the output in the above JSON format only.
Do not use the word 'JSON' in the output. Just provide the output in the specified format.

"""


sort_review_prompt_temp = ChatPromptTemplate.from_template(
    sort_review_prompt
          
)

output_parser = StrOutputParser()

sort_review_chain = sort_review_prompt_temp | model_gpt_4o_mini | output_parser