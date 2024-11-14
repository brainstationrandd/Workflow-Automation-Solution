from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from utils.helper import model_gpt_4o_mini


# sort_review_prompt="""
# Act as an Expert in HR and Recruitment.
# You will be given a CV text and a job description. Your task is to evaluate the CV based on the relevance to the job description and provide a score out of 10 points. Additionally, you should provide a detailed review explaining why the given score was awarded.

# You should consider the following aspects for scoring:
# 1. Relevance of the candidate's skills to the job description.
# 2. Match of experience level and years of experience to the job requirements.
# 3. Alignment of educational background with the job description.
# 4. Specific relevant keywords present in both the CV and the job description.
# 5. Demonstrated accomplishments that align with the job requirements.
# 6. Relevance of the candidate's location to the job role.
# 7. Certifications and degrees that match the job requirements.
# 8. Clarity and conciseness of the information presented in the CV.
# 9. Overall presentation and organization of the CV.
# 10. Any other relevant factors that make the candidate a good fit for the job.

# CV Text: {cv_text}

# -----------------------------------------

# Job Description: {job_desc}

# After evaluating the CV based on the job description, strictly provide the output in the following JSON format:

# {{
#   "score": "8",
#   "remarks": [
#     "The candidate has relevant skills such as Python and Data Analysis, which align well with the job description.",
#     "The experience level matches the job requirement, with 5 years of relevant experience.",
#     "The educational background is suitable, having a degree in Computer Science, which is preferred for this role.",
#     "The candidate's location is in New York, which is relevant to the job posting.",
#     "However, there is a lack of specific certifications that could enhance the candidate's profile.",
#     "The CV is well-organized and easy to read."
#   ]
# }}

# Strictly give the output in the above JSON format only.
# Do not use the word 'JSON' in the output. Just provide the output in the specified format.

# """

sort_review_prompt = """
Act as an Expert in HR and Recruitment.
You will be given a CV text, a job description, and integer weights for scoring parameters. Your task is to evaluate the CV based on these parameters and provide a match percentage out of 100%, considering the weight of each parameter. Additionally, provide a detailed review explaining why the given match percentage was awarded.

-Strictly be a professional and provide constructive feedback based on the evaluation criteria.
-Be objective in your assessment and avoid personal biases.
-Be specific in your analysis and provide clear reasoning for the match percentage.
-Be strict in your evaluation and consider all aspects of the CV and job description.

Each parameter will be weighted, contributing to the final match percentage as follows:

1. **Skill Relevance** (Weight: {weight_skills}): Assess how well the candidate’s skills match the job description.
2. **Experience Match** (Weight: {weight_experience}): Evaluate if the candidate’s experience level and years of experience align with the job requirements.
3. **Educational Alignment** (Weight: {weight_education}): Check if the candidate’s educational background meets the job requirements.
4. **Keywords Match** (Weight: {weight_keywords}): Look for specific relevant keywords in both the CV and job description.
5. **Accomplishments and Certifications** (Weight: {weight_accomplishments}): Consider any specific accomplishments, certifications, or degrees that match the job requirements.

CV Text: {cv_text}

-----------------------------------------

Job Description: {job_desc}

After evaluating the CV based on the job description and weighted parameters, strictly provide the output in the following JSON format:

{{
  "match_percentage": "X",
  "strengths": [
    "The candidate's skills closely align with the job requirements, especially in Python programming and data analysis.",
    "The candidate has 5 years of relevant experience, which is a good match for the job role.",
    "The educational background in Computer Science is well-suited for this position.",
    "The CV contains specific keywords related to the job description.",
    "The candidate has relevant certifications and accomplishments that enhance their profile."
  ],
  "weaknesses": [
    "The candidate's location is not specified, which could be a potential drawback.",
    "The CV lacks details on recent projects and achievements.",
    "There are no specific certifications mentioned that could further strengthen the candidate's profile."
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