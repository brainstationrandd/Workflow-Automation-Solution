prompt_data_extract="""Act as an Expert in Extracting Information from a Resume.
Given a resume text, your task is to extract specific features from it and return the information in a fixed JSON format.
Strictly complete the task with the given information only.

Resume Text: {resume}

The extracted features should include:
- Name
- Career Objectives
- Education
- Skills
- Certifications
- Experience
- Achievements
- Projects (including info, description, GitHub link of the project, and deployed link)
- Recommendations

Strictly follow this output format in the following JSON format and make sure to complete the task with the given information only:



{{
  "Name": "",
  "CareerObjectives": "",
  "Education": [
    {{
      "Degree": "",
      "Institution": "",
      "Year": ""
    }}
  ],
  "Skills": [
    ""
  ],
  "Certifications": [
    {{
      "CertificationName": "",
      "IssuingOrganization": "",
      "IssueDate": ""
    }}
  ],
  "Experience": [
    {{
      "JobTitle": "",
      "Company": "",
      "Duration": "",
      "Responsibilities": [
        ""
      ]
    }}
  ],
  "Achievements": [
    ""
  ],
  "Projects": [
    {{
      "Info": "",
      "Description": "",
      "GitHubLink": "",
      "DeployedLink": ""
    }}
  ],
  "Recommendations": [
    {{
      "Name": "",
      "Position": "",
      "RecommendationText": ""
    }}
  ]
}}

"""