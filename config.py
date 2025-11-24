CLAIMS_EXTRACTION_PROMPT = """
## Task Description
Extract all factual claims from the provided <method component>, an outline of content that will be taught in micro-credential. Each claim should be a factual statement that can be verified. Claims may or may not have supporting citations.
---

## Input
The <method component> containing factual claims, some of which may have
citation markers and corresponding URLs (either inline or in a <reference> section).
---

## Output Requirements
- Extract each distinct factual claim throughout the entire <method component>
- For each claim, output a JSON object with:
    - id run from 1 to number of claims extracted
    - The exact claim text as a string
    - The corresponding citation URL as source (if a citation marker directly follows the claim)
- If a claim has a citation marker directly following it, return the supporting URL as source
- If a claim does not have a citation marker directly following it, return an empty string for source
- Ensure all string values are properly escaped for valid JSON format (e.g. Replace internal quotation
marks (”) with escaped quotation marks (\”)) in the claim and context
- Return a JSON array containing all claim objects
---

## Format Specification
[
    {
        "id": 1
        "claim": "The exact statement representing a factual claim",
        "source": "https://example.com/source1"
    },
    {
        "id": 2
        "claim": "The exact statement representing a factual claim",
        "source": "https://example.com/source1"
    },
]
---

## Guidelines for Claim Identification
1. A claim may consist of a single sentence or a group of sentences when they collectively express one coherent, inseparable factual idea.
2. A claim (single or multi-sentence) must represent a complete, standalone factual assertion that can be verified independently.
3. Maintain the original wording where possible, removing only context that does not contribute to the factual meaning.
4. Extract all factual claims regardless of whether they have citation support.
5. Only map citation markers (numbers, author names, etc.) to their corresponding URLs in the <reference> section when the marker directly follows the claim (whether a single sentence or multi-sentence group). If the URL does not exist in the <reference>, then provide the entire reference in the source field.
6. Exclude opinions, speculations, recommendations, interpretations, or methodological descriptions.
7. Determine whether multiple sentences belong to the same claim by checking:
   - They refer to the same subject or concept without shifting focus.
   - They describe components or aspects of the same factual idea.
   - Removing a sentence would make the claim incomplete or misleading.
   - No new independent factual idea is introduced.
   - If a citation marker applies, it follows the entire multi-sentence claim.
   If any of these conditions fail, extract sentences as separate claims.
8. If multiple independent claims share the same citation marker, extract them as separate entries but assign the same source URL.

---

## Citation URL Mapping
• If URLs appear directly after claims, use those URLs directly
• Citation markers (e.g. follows a number or [number]) must directly follow the claim to be considered as supporting that claim
• If claims use citation markers that <reference>e a bibliography or <reference> section, locate the corresponding URLs in that section
• If a claim has no directly following citation marker, use an empty string for source
---

## Example
# Input
<method component>
"This micro-credential focuses on foundational data science skills suitable for entry-level roles. [1]
Participants will engage with real-world datasets throughout the program.
The course introduces core statistical concepts such as mean, variance, and probability distributions. [2]
Learners will explore data cleaning techniques, including handling missing values and detecting outliers.
The program covers essential Python libraries used in data science, such as NumPy, pandas, and Matplotlib. [3]
A dedicated module explains how to build and evaluate regression models. [4]
The course also introduces classification algorithms, including decision trees and logistic regression.
Participants will learn to implement cross-validation for model assessment. [4]
The micro-credential includes an introduction to data visualization principles.
The program teaches how to design dashboards using widely adopted BI tools. [5]
Students will explore ethical considerations in data science, including fairness and privacy issues.
The course provides an overview of cloud-based machine learning platforms. [6]
Learners will complete a capstone project analyzing an open-source dataset.
Instruction is delivered asynchronously over an 8-week period.
All course materials are provided online.
The micro-credential requires approximately 40 hours of total effort. [7]"
</method component>

<reference>
"[1] https://abc.com/data-science-foundations  
[2] https://def.com/statistics-basics  
[3] https://ghi.com/python-libraries  
[4] https://jkl.com/regression-models  
[5] Shi Baoguang, Bai Xiang, Yao Cong. Power BI instruction guide for business analysis
[6] Huaqiao University. A comparative of cloud ML service in 2025
[7] https://abcdefg.com/40-hours "
</reference>

# Output
<output>
[
    {
        "id": 1,
        "claim": "This micro-credential focuses on foundational data science skills suitable for entry-level roles.",
        "source": "https://abc.com/data-science-foundations"
    },
    {
        "id": 2,
        "claim": "Participants will engage with real-world datasets throughout the program.",
        "source": ""
    },
    {
        "id": 3,
        "claim": "The course introduces core statistical concepts such as mean, variance, and probability distributions.",
        "source": "https://def.com/statistics-basics"
    },
    {
        "id": 4,
        "claim": "Learners will explore data cleaning techniques, including handling missing values and detecting outliers.",
        "source": ""
    },
    {
        "id": 5,
        "claim": "The program covers essential Python libraries used in data science, such as NumPy, pandas, and Matplotlib.",
        "source": "https://ghi.com/python-libraries"
    },
    {
        "id": 6,
        "claim": "A dedicated module explains how to build and evaluate regression models.",
        "source": " https://jkl.com/regression-models"
    },
    {
        "id": 7,
        "claim": "The course also introduces classification algorithms, including decision trees and logistic regression.",
        "source": ""
    },
    {
        "id": 8,
        "claim": "Participants will learn to implement cross-validation for model assessment.",
        "source": " https://jkl.com/regression-models"
    },
    {
        "id": 9,
        "claim": "The micro-credential includes an introduction to data visualization principles.",
        "source": ""
    },
    {
        "id": 10,
        "claim": "The program teaches how to design dashboards using widely adopted BI tools.",
        "source": "Shi Baoguang, Bai Xiang, Yao Cong. Power BI instruction guide for business analysis"
    },
    {
        "id": 11,
        "claim": "Students will explore ethical considerations in data science, including fairness and privacy issues.",
        "source": ""
    },
    {
        "id": 12,
        "claim": "The course provides an overview of cloud-based machine learning platforms.",
        "source": "Huaqiao University. A comparative of cloud ML service in 2025"
    },
    {
        "id": 13,
        "claim": "Learners will complete a capstone project analyzing an open-source dataset.",
        "source": ""
    },
    {
        "id": 14,
        "claim": "Instruction is delivered asynchronously over an 8-week period.",
        "source": ""
    },
    {
        "id": 15,
        "claim": "All course materials are provided online.",
        "source": ""
    },
    {
        "id": 16,
        "claim": "The micro-credential requires approximately 40 hours of total effort.",
        "source": "https://abcdefg.com/40-hours"
    }
]

</output>
---

*Please extract all claims from the following paper and provide them in the specified JSON format:*
<method component>
{{method_component}}
</method component>

<reference>
{{reference}}
</reference>
"""
CLAIMS_EXTRACTION_OUTPUT = {
  "title": "extract_factual_claims",
  "description": "Extract all distinct verifiable factual claims from a provided method component and map any directly following citation markers to their corresponding URLs. Returns an array of claim objects with the exact claim text and the supporting URL (or empty string if none).",
  "type": "object",
  "properties": {
    "claims": {
      "type": "array",
      "description": "List of extracted factual claims from the method component. Each array item is an object with the claim text and its source URL (empty string if no directly following citation).",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "number",
            "description": "number run from 1 to total number of claims extracted"
          },
          "claim": {
            "type": "string",
            "description": "The exact statement representing a factual claim, preserved from the method component and properly JSON-escaped."
          },
          "source": {
            "type": "string",
            "description": "The URL directly following the claim in the method component that supports the claim, or an empty string if no direct citation follows the claim."
          }
        },
        "required": [
          "id",
          "claim",
          "source"
        ],
        "additionalProperties": False
      }
    }
  },
  "required": [
    "claims"
  ],
  "additionalProperties": False,
  "strict": False
}
CLAIMS_VERIFICATION_PROMPT = """
## Task Description
Your task is to verify whether multiple claims are supported by the provided reference content.
---

## Input
- <ref content>, A reference content that contains supporting information
- <claims>, A list of claim that need to be verified against the reference
---

## Output
For each claim, respond with ‘yes’, ‘no’, or ‘unknown’ to indicate whether the claim, in <claims>, is supported by the
reference content ('<ref content>'). Output in the specified JSON format.
---

## Output Format Specification
[
    {
        "id": 1,
        "result": "yes"
    },
    {
        "id": 2,
        "result": "no"
    },
    {
        "id": 3,
        "result": "unknown"
    },
]
---

## Verification Guidelines
### Claim Support Determination
If the reference is valid, for each given claim:
    - ‘yes’: If the facts or data in the claim can be found entirely or partially within the <ref content>
    - ‘no’: If all facts and data in the statement cannot be found in the <ref content>
    - ‘unknown’: If verification encounters difficulties (such as semantic incompleteness, ambiguity, or
other issues that make verification impossible), or reference contains are not available (‘page not
found’ message, connection errors, or other non-content responses)

**Notice that claims must be verifiable from the content provided, not based on general knowledge.
---

Please provide your verification results in the specified JSON format.
<ref content>
{{ref_content}}
</ref content>

<claims>
{{claims}}
</claims>
"""
CLAIMS_VERIFICATION_OUTPUT = {
  "title": "claim_verification",
  "description": "Verify whether multiple claims are supported by the provided reference content. For each claim, return an object with the claim's id and a result: 'yes', 'no', or 'unknown'.",
  "type": "object",
  "properties": {
    "verifications": {
      "type": "array",
      "description": "An array of verification results, one per claim.",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer",
            "description": "The identifier of the claim (must match the input claim id)."
          },
          "result": {
            "type": "string",
            "description": "Verification outcome for the claim: 'yes' if supported, 'no' if not supported, 'unknown' if verification is impossible or reference unavailable.",
            "enum": [
              "yes",
              "no",
              "unknown"
            ]
          }
        },
        "required": [
          "id",
          "result"
        ],
        "additionalProperties": False
      }
    }
  },
  "required": [
    "verifications"
  ],
  "additionalProperties": False,
  "strict": False
}

LEARNER_BG_SYSTEM_PROMPT ="""
You are an experienced education professor specializing in evaluating the quality of learner background profiles.
Your role is to analyze the provided learner background content, identify strengths and weaknesses, and give clear, actionable feedback on areas that need improvement.
At the beginning of every task, you must always use the search tool to gather all necessary context before performing your assessment.
"""
EVAL_LEARNER_BG_PROMPT = """
<instruction>
**Your Goal**: Evaluate the <learner background> describing the learner profile and their needs/pain points. You must assess quality and provide targeted refinement suggestions using the following dimensions.

---
## DIMENSIONS
1. **Profile Concisability**
evaluate the clarity and brevity of the learner profile, ensuring it succinctly describes who the learners are and the occupations they hold.
   - Output **true** if concise, specific, and easy to understand the learner profile.  
   - Output **false** if vague, overly long, missing key details, or repetitive.
2. **Need Concisability**  
evaluate the information that describe concisely about what do they want, the situation that they want to solve or their responsibility
   - Output **true** if the problem or needs of the learner is specific and concise.  
   - Output **false** if vague, unfocused, too long, or missing clear problem context.
---

## YOUR TASKS
### **1. Analyze the User Input**
For each dimension:
- Evaluate whether it meets the dimension's requirements.  
- Return only **true/false** ('<dimension's result>').  
- Provide a short explanation of your reasoning ('<dimension's explanation>').
---

### **2. Summarize feedback**
- Create a summarized feedback that cover all <dimension's explanation>.
- Return a short summary paragraph ('<feedback>')
---

### **3. Refinement Logic**
For each dimension:
**If the score is `false`, you MUST return 2-3 <refinement_topic> object ** consisting of:
  - <type>: ["profile", "needs"] depend on the area that need to refine.
  - <topic_name>: A short label describing topic about the suggestion version
  - <topic_suggestion>: A suggestion that will be used to revise the current learner background follow the <topic_name> and <feedback>
**If the score is `true`,`<type>` ,`<topic_name>` and `<topic_suggestion>` must be empty strings.**
---

## OUTPUT FORMAT
Respond strictly in this JSON structure:
{
    "profile_concisability_result": <dimension's result>,
    "profile_concisability_explanation": <dimension's explanation>,
    "need_concisability_result": <dimension's result>,
    "need_concisability_explanation": <dimension's explanation>,
    "feedback": <feedback>,
    "refinement_topic": [
        {
            "type": <type>,
            "topic_name": <topic_name>,
            "topic_suggestion": <topic_suggestion>,
        },
        {
            "type": <type>,
            "topic_name": <topic_name>,
            "topic_suggestion": <topic_suggestion>,
        }
    ]
}
---

## EXAMPLE
<learner background>
"officer"
</learner background>

<output>
{
"profile_concisability_result": false,
"profile_concisability_explanation": "The profile contains only the single word 'officer' which is too brief and ambiguous — it lacks sector (police, military, security, compliance, etc.), rank, responsibilities, experience level, and context.",
"need_concisability_result": false,
"need_concisability_explanation": "No needs or pain points are provided — the submission doesn't state what the learner wants to achieve, what problems they face, or which responsibilities they need help with.",
"feedback": "The learner profile is overly vague and lacks essential details about the type of officer and their specific responsibilities. Additionally, there are no stated needs or pain points, making it difficult to understand what the learner requires assistance with.",
  "refinement_topic": [
    {
      "type": "profile",
      "topic_name": "Security officer",
      "topic_suggestion": "Expand the profile by specifying the security environment (such as campus, corporate office, hospital, or event venue) and add relevant responsibilities like patrol duties, monitoring, access control, or incident reporting."
    },
    {
      "type": "profile",
      "topic_name": "Compliance officer",
      "topic_suggestion": "Refine the profile by identifying the compliance domain (e.g., AML, regulatory monitoring, internal audit) and describing responsibilities such as reviewing reports, monitoring risks, or ensuring regulatory adherence."
    },
    {
      "type": "needs",
      "topic_name": "Procedures documentation",
      "topic_suggestion": "Enhance the needs description by adding the types of procedures involved, the regulatory context, and the specific challenges the officer faces in creating or maintaining documentation."
    },
    {
      "type": "needs",
      "topic_name": "Operational training goal",
      "topic_suggestion": "Improve the needs statement by specifying the operational skills to be developed, such as de-escalation, communication, safety protocol execution, or incident report writing."
    }
  ]
</output>

### Additional Requirements
- All suggestions must directly solve the issue described in your analysis.  
- Suggested versions must be **concise**, **specific**, and **aligned with the user’s intent**.  
</instruction>

**Please analyze the provided <learner background> content below following the <instruction> described above**

<learner background>
{{learner_background}}
</learner background>
"""
EVAL_LEARNER_BG_OUTPUT = {
  "title": "evaluate_learner_background",
  "description": "Schema for the evaluation of a learner background describing profile and needs. Contains dimension results (true/false), short explanations, a combined feedback paragraph, and a list of 2-3 refinement topic suggestions.",
  "type": "object",
  "properties": {
    "profile_concisability_result": {
      "type": "boolean",
      "description": "Result for Profile Concisability dimension: true if the learner profile is concise, specific, and easy to understand; false otherwise."
    },
    "profile_concisability_explanation": {
      "type": "string",
      "description": "Short explanation supporting the profile_concisability_result. Should state why the profile is concise or what is missing/unclear."
    },
    "need_concisability_result": {
      "type": "boolean",
      "description": "Result for Need Concisability dimension: true if the learner's needs/problems are specific and concise; false otherwise."
    },
    "need_concisability_explanation": {
      "type": "string",
      "description": "Short explanation supporting the need_concisability_result. Should state why the needs are clear or what is vague/missing."
    },
    "feedback": {
      "type": "string",
      "description": "A concise summary paragraph that synthesizes the explanations for both dimensions and gives overall feedback."
    },
    "refinement_topic": {
      "type": "array",
      "description": "A list of 2-3 suggested refinement topics. If a dimension result is true, corresponding suggestion fields must be empty strings. If false, provide 2-3 concise, specific suggestion objects addressing the deficiency.",
      "items": {
        "type": "object",
        "properties": {
          "type": {
            "type": [
              "string",
              "null"
            ],
            "description": "Area to refine: one of 'profile' or 'needs' (or empty string when not applicable).",
            "enum": [
              "profile",
              " needs",
              "null"
            ]
          },
          "topic_name": {
            "type": "string",
            "description": "Short label describing the refinement topic (or empty string when not applicable)."
          },
          "topic_suggestion": {
            "type": "string",
            "description": "Concise, actionable suggestion to revise the learner background according to the topic_name and feedback (or empty string when not applicable)."
          }
        },
        "required": [
          "type",
          "topic_name",
          "topic_suggestion"
        ],
        "additionalProperties": False
      },
      "minItems": 2,
      "maxItems": 4
    }
  },
  "required": [
    "profile_concisability_result",
    "profile_concisability_explanation",
    "need_concisability_result",
    "need_concisability_explanation",
    "feedback",
    "refinement_topic"
  ],
  "additionalProperties": False,
  "strict": False
}

KNOWLEDGE_DOMAIN_SYSTEM_PROMPT = """
You are an experienced education professor specializing in evaluating the quality of interest knowledge domain or knowledge background of student.
Your role is to analyze the provided knwoledge domain content, identify strengths and weaknesses, and give clear, actionable feedback on areas that need improvement.
At the beginning of every task, you must always use the search tool to gather all necessary context before performing your assessment.
"""
EVAL_KNOWLEDGE_DOMAIN_PROMPT = """
<instruction>
**Your Goal**: Evaluate the <teaching domain> describing the knowledge domain that the user want to teach. You must assess quality and provide targeted refinement suggestions using the following dimensions.

---
## DIMENSIONS
1. **Comprehensive**
evaluate whether the provided information thoroughly describes the domain of instruction, encompassing the intended knowledge area, its application scenarios, and the specific tools or frameworks to be taught.
   - Output **true** if the information is detailed, clearly defines the knowledge area, includes relevant application scenarios, and specifies the tools or frameworks to be taught.
   - Output **false** if the information is unclear, lacks detail, omits key elements, or is unnecessarily lengthy or repetitive.
---

## YOUR TASKS
### **1. Analyze the User Input**
For each dimension:
- Evaluate whether it meets the dimension's requirements.  
- Return only **true/false** ('<dimension's result>').  
- Provide a short explanation of your reasoning ('<dimension's explanation>').
---

### **2. Summarize feedback**
- Create a summarized feedback that cover all <dimension's explanation>.
- Return a short summary paragraph ('<feedback>')
---

### **3. Refinement Logic**
For each dimension:
**If the score is `false`, you MUST return 2-3 <refinement_topic> object ** consisting of:
  - <topic_name>: A short label describing topic about the suggestion version
  - <topic_suggestion>: A suggestion that will be used to revise the current learner background follow the <topic_name> and <feedback>
**If the score is `true`, both `<topic_name>` and `<topic_suggestion>` must be empty strings.**
---

## OUTPUT FORMAT
Respond strictly in this JSON structure:
{
    "comprehensive_result": <dimension's result>,
    "comprehensive_explanation": <dimension's explanation>,
    "feedback": <feedback>
    "refinement_topic":[
        {
            "topic_name": <topic_name>,
            "topic_suggestion": <topic_suggestion>
        },
        {
            "topic_name": <topic_name>,
            "topic_suggestion": <topic_suggestion>
        },
        ...
    ],
}
---

## EXAMPLE
<teaching domain>
"Power Automate"
</teaching domain>

<output>
{
  "comprehensive_result": false,
  "comprehensive_explanation": "The input only names the product ('Power Automate') and does not define the teaching scope, learning objectives, target audience, application scenarios, nor the specific tools and frameworks (cloud flows vs Desktop, connectors, related Power Platform components) that will be taught.",
  "feedback": "The input only states the product name and lacks details on scope, objectives, audience, scenarios, and specific Power Automate components to be taught.",
  "refinement_topic": [
    {
      "topic_name": "Automation pipeline",
      "topic_suggestion": "Expand the content by describing the automation focus, such as specifying whether it covers cloud flows, desktop automation, RPA tasks, common business process scenarios, and key Power Automate components relevant to building an automation pipeline."
    },
    {
      "topic_name": "Data analysis",
      "topic_suggestion": "Enhance the content by detailing how Power Automate is used for data processing, integration with other Power Platform tools, typical data workflows, and scenarios where automation supports analysis, reporting, or real-time data interactions."
    }
  ]
}
</output>
---

### Additional Requirements
- All suggestions must directly solve the issue described in your analysis.  
- Suggested versions must be **concise**, **specific**, and **aligned with the user’s intent**.  
</instruction>

**Please analyze the provided <teaching domain> content below following the <instruction> described above**

<teaching domain>
{{teaching_domain}}
</teaching domain>
"""
EVAL_KNOWLEDGE_DOMAIN_OUTPUT = {
  "title": "teaching_domain_evaluation",
  "description": "Evaluate a teaching domain description for completeness (Comprehensive dimension). Return a boolean result, a brief explanation, a consolidated feedback paragraph, and 2-3 refinement topic suggestions when the dimension is not met.",
  "type": "object",
  "properties": {
    "comprehensive_result": {
      "type": "boolean",
      "description": "Result of the 'Comprehensive' dimension evaluation: true if the teaching domain description thoroughly defines the knowledge area, application scenarios, and specific tools/frameworks to be taught; false otherwise."
    },
    "comprehensive_explanation": {
      "type": "string",
      "description": "A short explanation (one or two sentences) justifying the comprehensive_result, describing which elements are present or missing."
    },
    "feedback": {
      "type": "string",
      "description": "A concise summary paragraph that synthesizes the comprehensive_explanation(s) into unified feedback for improving the teaching domain description."
    },
    "refinement_topic": {
      "type": "array",
      "description": "If comprehensive_result is false, return 2-3 suggestion objects. If true, return one or more objects with empty strings for both fields.",
      "items": {
        "type": "object",
        "properties": {
          "topic_name": {
            "type": "string",
            "description": "Short label describing the suggestion topic (empty string if no suggestion required)."
          },
          "topic_suggestion": {
            "type": "string",
            "description": "Concise, specific suggestion to revise the teaching domain to address the identified deficiency (empty string if not required)."
          }
        },
        "required": [
          "topic_name",
          "topic_suggestion"
        ],
        "additionalProperties": False
      },
      "minItems": 2
    }
  },
  "required": [
    "comprehensive_result",
    "comprehensive_explanation",
    "feedback",
    "refinement_topic"
  ],
  "additionalProperties": False,
  "strict": False
}

EVAL_WHOISTHISFOR_PROMPT = """
<instruction>
**Your Goal**: Evaluate the <who is this for> which describing the learner profile and their needs/pain points. You must assess quality of <who is this for> and provide targeted refinement suggestions using the following dimensions.

---
## DIMENSIONS
1. **Profile Concisability**
evaluate the clarity and brevity of the learner profile, ensuring it succinctly describes who the learners are and the occupations they hold.
   - Output **true** if concise, specific, and easy to understand the learner profile.  
   - Output **false** if vague, overly long, missing key details, or repetitive.
2. **Need Concisability**  
evaluate the information that describe concisely about what do they want, the situation that they want to solve or their responsibility
   - Output **true** if the problem or needs of the learner is specific and concise.  
   - Output **false** if vague, unfocused, too long, or missing clear problem context.
3. **Format Criteria**  
Evaluate the information that is structured as a short sentence, paragraph, or list of sentences. The part of speech used in the information should be similar to or align with <job/role> + <need/responsibility>.
   - Output **true** if the format of the information is similar to the defined format.  
   - Output **false** if the format is vague, unfocused, too long, or lacks a clear structure.
---

## YOUR TASKS
### **Analyze the User Input**
For each dimension:
- Evaluate whether it meets the dimension's requirements.  
- Return only **true/false** ('<dimension's result>').  
- Provide a short explanation of your reasoning ('<dimension's explanation>').
---

## OUTPUT FORMAT
Respond strictly in this JSON structure:
{
    "profile_concisability_result": <dimension's result>,
    "profile_concisability_explanation": <dimension's explanation>,
    "need_concisability_result": <dimension's result>,
    "need_concisability_explanation": <dimension's explanation>,
    "format_criteria_result": <dimension's result>,
    "format_criteria_explanation": <dimension's explanation>,
}
---

## EXAMPLE
### *example 1*
<learner background>
"officer"
</learner background>

<output>
{
    "profile_concisability_result": false,
    "profile_concisability_explanation": "The profile contains only the single word 'officer' which is too brief and ambiguous — it lacks sector (police, military, security, compliance, etc.), rank, responsibilities, experience level, and context.",
    "need_concisability_result": false,
    "need_concisability_explanation": "No needs or pain points are provided — the submission doesn't state what the learner wants to achieve, what problems they face, or which responsibilities they need help with.",
    "format_criteria_result": false,
    "format_criteria_explanation": "The information is only 'officer'. So, it is structured in wrong format both overall part of speech and write as a word not a sentence or paragraph",
}
</output>

### *example 2*
<learner background>
"Business Analyst, นักพัฒนาระบบ, Citizen Developer ผู้มีหน้าที่ในการแปลงความต้องการทางธุรกิจเป็นระบบดิจิทัลที่ใช้งานได้จริง"
</learner background>

<output>
{
    "profile_concisability_result": true,
    "profile_concisability_explanation": "The profile contains a clear specific role, it clear enough to understand the scnario or background of the learner",
    "need_concisability_result": true,
    "need_concisability_explanation": "Provided a scenario or example that want to tranform business need to digital solution that can applied in real-word",
    "format_criteria_result": true,
    "format_criteria_explanation": "Provided a correct format and structured as job/role then followed by their responsibility",
}
</output>

### Additional Requirements
- All suggestions must directly solve the issue described in your analysis.  
- Suggested versions must be **concise**, **specific**, and **aligned with the user’s intent**.  
</instruction>

**Please assess the provided <who is this for> content below following the <instruction> described above**

<who is this for>
{{whoisthisfor}}
</who is this for>
"""
EVAL_WHOISTHISFOR_OUTPUT = {
  "title": "evaluate_learner_profile",
  "description": "Assess the learner profile and needs/pain points for concisability",
  "type": "object",
  "properties": {
    "profile_concisability_result": {
      "type": "boolean",
      "description": "true if the learner profile is concise, specific, and easy to understand; false otherwise."
    },
    "profile_concisability_explanation": {
      "type": "string",
      "description": "A short explanation justifying the profile_concisability_result."
    },
    "need_concisability_result": {
      "type": "boolean",
      "description": "true if the learner's needs/pain points are specific and concise; false otherwise."
    },
    "need_concisability_explanation": {
      "type": "string",
      "description": "A short explanation justifying the need_concisability_result."
    },
    "format_criteria_result": {
      "type": "boolean",
      "description": "true if the input structured in the defined format"
    },
    "format_criteria_explanation": {
      "type": "string",
      "description": "A short explanation justifying the format_criteria_result."
    }
  },
  "required": [
    "profile_concisability_result",
    "profile_concisability_explanation",
    "need_concisability_result",
    "need_concisability_explanation",
    "format_criteria_result",
    "format_criteria_explanation"
  ],
  "additionalProperties": False,
  "strict": False
}
EVAL_WHOISTHISFOR_WEIGHT = {
    "profile_concisability_result": 2,
    "need_concisability_result": 2,
    "format_criteria_result": 1
}

EVAL_COMPETENCY_PROMPT = """
<instruction>
**Your Goal**: Evaluate the <competency> which describing the skill or evidence-backed task that the learner will achieve after complete the micro-credential based on the learner profile provided as <who is this for> below. You must assess quality of <competency> and provide targeted refinement suggestions using the following dimensions.

<who is this for>
{{whoisthisfor}}
</who is this for>

---
## DIMENSIONS
1. **Concisability**
evaluate that the competency is describe concisely in a sentence about what skill that learner will acheive at the end of the course.
   - Output **true** if concise, specific, and easy to understand what the learner will achieve at the end of the course  
   - Output **false** if vague, overly long, missing key details, or repetitive.
2. **Alignment**  
evaluate that the competency is align to the learner profile ('<who is this for>') and solve the leaner need. Proof of skill mentioned in the competency should be directly relevant to those needs.
   - Output **true** if the competency directly addresses the learner's profile and needs, and the proof of skill is relevant to those needs.
   - Output **false** if the competency does not align with the learner's profile or needs, or if the proof of skill is irrelevant.
3. **Action verb **
evaluate whether the verb used in competency is an action verb defined in 'bloom's taxonomy', included with 'create','evaluate','analyze', and 'apply'
   - Output **true** if the verb is an action verb or has the similar meaning to the verb from Bloom's taxonomy.
   - Output **false** if the verb is not an action verb from Bloom's taxonomy.
4. **Format Criteria**  
Evaluate the information that is structured as a short sentence only. The content should constructed from <learner> + <action verb> + <proof of skill> + <additional context>   
   - Output **true** if the format of the information is similar to the defined format.  
   - Output **false** if the format is vague, unfocused, too long, or lacks a clear structure.
---

## YOUR TASKS
### **Analyze the User Input**
For each dimension:
- Evaluate whether it meets the dimension's requirements.  
- Return only **true/false** ('<dimension's result>').  
- Provide a short explanation of your reasoning ('<dimension's explanation>').
---

## OUTPUT FORMAT
Respond strictly in this JSON structure:
{
    "concisability_result": <dimension's result>,
    "concisability_explanation": <dimension's explanation>,
    "alignment_result": <dimension's result>,
    "alignment_explanation": <dimension's explanation>,
    "action_verb_criteria_result": <dimension's result>,
    "action_verb_criteria_explanation": <dimension's explanation>,
    "format_criteria_result": <dimension's result>,
    "format_criteria_explanation": <dimension's explanation>,
}
---

## EXAMPLE
### *example 1*
<competency>
"สามารถวางแผนโครงการโซลูชันดิจิทัลที่สร้างคุณค่าทางธุรกิจได้"
</competency>

<output>
{
    "concisability_result": true,
    "concisability_explanation": "The sentence is short, concise, and clearly conveys the skill being learned, which is planning a digital solution project that creates value. However, it should specify a measurable outcome or a single deliverable, such as a project plan or business case, to make it clearer (Example adjustment: 'Able to plan and create a digital solution project plan that demonstrates business returns').",
    "alignment_result": false,
    "alignment_explanation": "The content aligns with the learner (Product Owner/PM) but lacks evidence of work that meets actual needs, such as identifying opportunities, analyzing feasibility, or preparing proposals for management. Recommendation: Specify work outcomes, such as 'create a business case/feasibility and project plan' (Example adjustment: 'Able to create a business case and digital solution project plan that proves business value').",
    "action_verb_criteria_result": true,
    "action_verb_criteria_explanation": "The verb 'plan' is not in the provided Bloom's verb examples (create, evaluate, analyze, apply) but is closely related to 'create'.",
    "format_criteria_result": false,
    "format_criteria_explanation": "The format does not follow the structure <learner> + <action verb> + <proof of skill> + <additional context> because there is no clear proof of skill (e.g., deliverable outcome). Recommendation: Specify work as evidence, such as 'create a project plan and business case'. Example sentence following the format: 'The learner can design and create a business case and project plan for a digital solution that demonstrates business returns'.",
}
</output>

### Additional Requirements
- All suggestions must directly solve the issue described in your analysis.  
- Suggested versions must be **concise**, **specific**, and **aligned with the user’s intent**.  
</instruction>

**Please assess the provided <competency> content below following the <instruction> described above**

<competency>
{{competency}}
</competency>
"""
EVAL_COMPETENCY_OUTPUT = {
  "title": "evaluate_competency",
  "description": "Evaluate a proposed competency statement against concisability, alignment, action-verb usage (Bloom's taxonomy), and format criteria; return boolean results and short explanations for each dimension.",
  "type": "object",
  "properties": {
    "concisability_result": {
      "type": "boolean",
      "description": "true if the competency is concise, specific, and easy to understand what the learner will achieve; false otherwise."
    },
    "concisability_explanation": {
      "type": "string",
      "description": "A short explanation justifying the concisability_result, highlighting what is concise or what makes it vague/overly long and recommending a focused improvement."
    },
    "alignment_result": {
      "type": "boolean",
      "description": "true if the competency aligns with the provided learner profile and addresses their needs with relevant proof of skill; false otherwise."
    },
    "alignment_explanation": {
      "type": "string",
      "description": "A short explanation justifying the alignment_result, describing how the competency does or does not meet the learner's needs and suggesting targeted fixes."
    },
    "action_verb_criteria_result": {
      "type": "boolean",
      "description": "true if the competency uses an action verb consistent with Bloom's taxonomy (e.g., create, evaluate, analyze, apply) or a close equivalent; false otherwise."
    },
    "action_verb_criteria_explanation": {
      "type": "string",
      "description": "A short explanation justifying the action_verb_criteria_result, identifying the verb used and why it does or does not match Bloom's taxonomy verbs, with correction suggestions."
    },
    "format_criteria_result": {
      "type": "boolean",
      "description": "true if the competency follows the required short-sentence format: <learner> + <action verb> + <proof of skill> + <additional context>; false otherwise."
    },
    "format_criteria_explanation": {
      "type": "string",
      "description": "A short explanation justifying the format_criteria_result, pointing out missing or extra elements and recommending a concise reformulation that fits the format."
    }
  },
  "required": [
    "concisability_result",
    "concisability_explanation",
    "alignment_result",
    "alignment_explanation",
    "action_verb_criteria_result",
    "action_verb_criteria_explanation",
    "format_criteria_result",
    "format_criteria_explanation"
  ],
  "additionalProperties": False,
  "strict": False
}
EVAL_COMPETENCY_WEIGHT = {
    "concisability_result": 1,
    "alignment_result": 1,
    "action_verb_criteria_result": 1,
    "format_criteria_result": 1
}

EVAL_OVERVIEW_ASSE_PROMPT = """
<instruction>
**Your Goal**: Evaluate the <assessment> which designed to assess learner about their environment or scenario context that relevant to process to achieve the competency provided as <competency> below. You must assess quality of <assessment> and provide targeted refinement suggestions using the following dimensions.

<competency>
{{competency}}
</competency>

---
## DIMENSIONS
1. **Alignment**
evaluate whether the questions are align to the <competency> and ask for the context that relevant or useful to complete the evidence of <competency>.
- Output **true** if the questions are related to the <competency> and provide necessary context for evidence.
- Output **false** if the questions do not relate to the <competency> or lack necessary context for evidence.
2. **Rubric Quality**
evaluate whether the pass criteria generally align with the questions in the <assessment> only and can reasonably guide the classification of learner responses as pass or not pass. The rubrics can be both qualitative descriptions, quantitative indicators, or a mix of both. Focus on the <assessment> questions only
- Output **true** if the pass criteria show reasonable alignment with the assessment question and can be used to make a basic pass/fail judgment.
- Output **false** if the pass criteria are unclear or do not align with the questions.
3. **Readability**
evaluate that the questions and rubrics are clearly structured, logically organized, and written in a fluent, coherent manner that facilitates understanding and effective communication of ideas.
- Output **true** if the questions and rubrics are clear, logical, and easy to understand.
- Output **false** if the questions and rubrics are unclear, disorganized, or difficult to understand.
4. **Format Criteria**
evaluate the information that is structured as a open-ended question or list of open-ended question which assess learner response to pass or not pass. The assessment should included with response word-limit criteria
- Output **true** if the format of the information is similar to the defined format.
- Output **false** if the format is vague, unfocused, too long, or lacks a clear structure.
---

## YOUR TASKS
### **Analyze the User Input**
For each dimension:
- Evaluate whether it meets the dimension's requirements.
- Return only **true/false** ('<dimension's result>').
- Provide a short explanation of your reasoning ('<dimension's explanation>').
---

## OUTPUT FORMAT
Respond strictly in this JSON structure:
{
"alignment_result": <dimension's result>,
"alignment_explanation": <dimension's explanation>,
"rubric_quality_result": <dimension's result>,
"rubric_quality_explanation": <dimension's explanation>,
"readability_result": <dimension's result>,
"readability_explanation": <dimension's explanation>,
"format_criteria_result": <dimension's result>,
"format_criteria_explanation": <dimension's explanation>,
}
---
## EXAMPLE
### *example 1*
<assessment>
"โปรดตอบคำถามต่อไปนี้
จำกัด 500-word limit
อธิบาย
- บริบทในการทำงานของคุณ:
- ทีมและบทบาทในองค์กร
- อธิบายโครงการดิจิทัลที่ต้องการริเริ่ม
ผ่าน: คำตอบของผู้เรียนประกอบด้วยคำอธิบายที่ชัดเจนเกี่ยวกับทีมและบทบาทในองค์กร พร้อมทั้งระบุโครงการดิจิทัลที่เฉพาะเจาะจงที่ต้องการริเริ่ม โดยแสดงให้เห็นถึงความเข้าใจในความต้องการทางธุรกิจและโอกาสในการสร้างมูลค่าผ่านเทคโนโลยีดิจิทัล
ไม่ผ่าน: การตอบขาดความชัดเจนในการอธิบายบทบาทหรือโครงการที่ต้องการริเริ่ม หรือไม่แสดงให้เห็นถึงความเข้าใจในการเชื่อมโยงระหว่างความต้องการทางธุรกิจกับโซลูชันดิจิทัล"
</assessment>

<competency>
"ผู้เรียนสามารถวางแผนโครงการโซลูชันดิจิทัลที่สร้างคุณค่าทางธุรกิจ โดยเชื่อมโยงวิสัยทัศน์ กลยุทธ์องค์กร และการวิเคราะห์ความเป็นไปได้ทางเศรษฐกิจและความเสี่ยง"
</competency>

<output>
{
"alignment_result": false,
"alignment_explanation": "Partially aligned — The question covers basic capability information like work context and project description but lacks connection to the organization's vision, strategy, economic feasibility, and risks. Consider adding questions on the project's alignment with organizational goals, estimated economic benefits (e.g., KPI, ROI), and key risks with mitigation plans.",
"rubric_quality_result": true,
"rubric_quality_explanation": "The pass/fail criteria provide general direction and define list of components that should include in the learner response to be assess as 'pass'. The rubric also focus on how the learner demonstrate their understanding their context",
"readability_result": true,
"readability_explanation": "The questions and pass/fail criteria are clearly written and have a simple structure, making them easy to understand. The word limit helps respondents know the scope of the task, but it can be adjusted to specify the components that need to be addressed more precisely.",
"format_criteria_result": true,
"format_criteria_explanation": "The format consists of open-ended questions (context, team/role, and project description) with a 500-word limit, aligning with the desired format criteria."
}
</output>

### Additional Requirements
- All suggestions must directly solve the issue described in your analysis.
- Suggested versions must be **concise** and **aligned with the user’s intent**.
</instruction>

**Please assess the provided <assessment> content below following the <instruction> described above**

<assessment>
{{assessment}}
</assessment>
"""
EVAL_OVERVIEW_ASSE_OUTPUT = {
  "title": "assessment_evaluation",
  "description": "Evaluate an assessment against four dimensions (Alignment, Rubric Quality, Readability, Format Criteria). For each dimension return a boolean result and a short explanation describing the reasoning.",
  "type": "object",
  "properties": {
    "alignment_result": {
      "type": "boolean",
      "description": "True if the assessment questions are related to the competency and provide necessary context for evidence; otherwise false."
    },
    "alignment_explanation": {
      "type": "string",
      "description": "A concise explanation of why the alignment_result was chosen, noting specific alignment strengths or gaps."
    },
    "rubric_quality_result": {
      "type": "boolean",
      "description": "True if the pass criteria align with the assessment questions and can reasonably guide pass/fail classification; otherwise false."
    },
    "rubric_quality_explanation": {
      "type": "string",
      "description": "A concise explanation of why the rubric_quality_result was chosen, highlighting clarity, relevance, or misalignment of the rubric relative to the questions."
    },
    "readability_result": {
      "type": "boolean",
      "description": "True if the questions and rubrics are clear, logical, and easy to understand; otherwise false."
    },
    "readability_explanation": {
      "type": "string",
      "description": "A concise explanation of why the readability_result was chosen, noting issues such as unclear phrasing, poor organization, or good clarity."
    },
    "format_criteria_result": {
      "type": "boolean",
      "description": "True if the assessment is structured as open-ended question(s) with a response word-limit and clear structure; otherwise false."
    },
    "format_criteria_explanation": {
      "type": "string",
      "description": "A concise explanation of why the format_criteria_result was chosen, specifying whether the format matches the required open-ended + word-limit structure and any deviations."
    }
  },
  "required": [
    "alignment_result",
    "alignment_explanation",
    "rubric_quality_result",
    "rubric_quality_explanation",
    "readability_result",
    "readability_explanation",
    "format_criteria_result",
    "format_criteria_explanation"
  ],
  "additionalProperties": False,
  "strict": False
}
EVAL_OVERVIEW_ASSE_WEIGHT = {
    "alignment_result":1,
    "rubric_quality_result":1,
    "readability_result":1,
    "format_criteria_result":1
}

EVAL_MAIN_ASSE_PROMPT = """
<instruction>
**Your Goal**: Evaluate the <assessment> which designed to assess learner about the understanding to the micro-credential and use to assess learner that they can achieve the <competency> or not. You must assess quality of <assessment> and provide targeted refinement suggestions using the following dimensions and based on the relevant context included with <competency> and <overview assessment>.

<competency>
{{competency}}
</competency>

<overview assessment>
{{overview_assessment}}
</overview assessment>

---
## DIMENSIONS
1. **Alignment**
evaluate whether the deliverables align with the overview assessment. Each deliverable should clearly relate to the expected responses outlined in the overview, and the report deliverable should demonstrate consistency with the main deliverable.
- Output **true** if the deliverables are consistent with the overview assessment and clearly relate to the expected responses.
- Output **false** if the deliverables do not align with the overview assessment or fail to relate to the expected responses.
2. **Comprehensive**
evaluate whether the deliverable fully meets the <competency> requirements by demonstrating a broad and accurate understanding of the topic. All key elements, such as submission information, scope, deliverable detail are present and well developed.
- Output **true** if the deliverable meets all <competency> requirements and includes all key elements.
- Output **false** if the deliverable does not meet the <competency> requirements or lacks key elements.
3. **Concisability**
evaluate whether the deliverables are clearly and concisely described, avoiding redundancy and ensuring that all essential information is included in a well-summarized form.
- Output **true** if the deliverables are concise, clear, and free from redundancy.
- Output **false** if the deliverables are not concise, unclear, or contain redundant information.
4. **Learner Relevance**
evaluates whether method to complete each deliverable match the expected knowledge level of the learner profile — neither too basic nor too advanced for the micro-credential scope.
- Output **true** if the deliverable methods match the learner's knowledge level and are appropriate for the micro-credential scope.
- Output **false** if the deliverable methods do not match the learner's knowledge level or are inappropriate for the micro-credential scope.
5. **Readability**
evaluate that the description and rubrics of each deliverable are clearly structured, logically organized, and written in a fluent, coherent manner that facilitates understanding and effective communication of ideas.
- Output **true** if the descriptions and rubrics are clear, logical, and coherent.
- Output **false** if the descriptions and rubrics are unclear, illogical, or incoherent.
6. **Rubric Quality**
evaluates whether rubric for each deliverable should present clear, observable, and measurable criteria that reflect progressive levels of mastery. Each level must distinctly communicate what constitutes full achievement (“Yes”), partial fulfillment (“Almost”), and insufficient performance (“Not Yet”), ensuring evaluators and learners share a consistent understanding of expectations.
- Output **true** if the rubric presents clear, observable, and measurable criteria with distinct levels of mastery.
- Output **false** if the rubric does not present clear, observable, and measurable criteria or lacks distinct levels of mastery.
7. **Format Criteria**
evaluate the information that is included with 2 deliverable, main deliverable artifact which can be code, exercise, experiment, etc. and report which describe more deeply about te main artifact deliverable. the assessment should provided submission instruction that tell learner how to submit, submit channel.
- Output **true** if the format of the information is similar to the defined format.
- Output **false** if the format is vague, unfocused, too long, or lacks a clear structure.
---

## YOUR TASKS
### **Analyze the User Input**
For each dimension:
- Evaluate whether it meets the dimension's requirements.
- Return only **true/false** ('<dimension's result>').
- Provide a short explanation of your reasoning ('<dimension's explanation>').
---

## OUTPUT FORMAT
Respond strictly in this JSON structure:
{
"alignment_result": <dimension's result>,
"alignment_explanation": <dimension's explanation>,
"comprehensive_result": <dimension's result>,
"comprehensive_explanation": <dimension's explanation>,
"concisability_result": <dimension's result>,
"concisability_explanation": <dimension's explanation>,
"learner_relevance_result": <dimension's result>,
"learner_relevance_explanation": <dimension's explanation>,
"readability_result": <dimension's result>,
"readability_explanation": <dimension's explanation>,
"rubric_quality_result": <dimension's result>,
"rubric_quality_explanation": <dimension's explanation>,
"format_criteria_result": <dimension's result>,
"format_criteria_explanation": <dimension's explanation>,
}
---

## EXAMPLE
### *example 1*
<assessment>
"ผู้เรียนแสดง Solution Blueprint และ/หรือ Digital Solution Prototype โดยต้องจัดทำเอกสารในรูปแบบไฟล์ .docx หรือ .pdf ผ่านแพล็ตฟอร์มขององค์กร (เพื่อรักษาความลับทางการค้า) 
ผู้เรียนส่ง To-be Swimlane Diagram (Solution Blueprint) 1 ไดอะแกรม ที่แบ่ง Lanes เป็น 3 ประเภท: Human Tasks (งานที่คนต้องทำ), Digital Solution (ระบบดิจิทัลที่จะสร้างใหม่), Legacy System (ระบบเดิมที่ยังใช้งานอยู่) แสดง:
User Workflow: ขั้นตอนการทำงานของผู้ใช้แต่ละประเภท
Business Rules: กฎการทำงานของระบบตาม Decision Points
System Components: ส่วนประกอบของระบบและการเชื่อมต่อ Building Blocks
Data Flow: การไหลของข้อมูลผ่านระบบและจุดเก็บข้อมูล
Integration Points: จุดเชื่อมต่อกับระบบเดิม
Technology Stack: เครื่องมือ Microsoft Power Platform ที่ใช้ในแต่ละส่วน
กรณีที่ผู้เรียนได้นำ Blueprint ไปสร้างเป็น Digital Solution Prototype แล้วสามารถนำเสนอโซลูชันในรูปแบบ Presentation แทนได้โดยต้องจัดทำวิดีโอภายในองค์กร (เพื่อรักษาความลับทางการค้า) เป็นเวลา 3-7 นาที ในรูปแบบไฟล์ .mp4 และสไลด์ประกอบการนำเสนอ ที่อธิบาย:
Problem Statement: อธิบายเหตุผลในการพัฒนาโซลูชันและปัญหาที่ดิจิทัลโซลูชันนี้ต้องการแก้ไข
To-be Process: ภาพรวมของกระบวนการทำงานใหม่ แสดงการทำงานของโซลูชันดิจิทัลหรือระบบอัตโนมัติ
User Workflow: ขั้นตอนการทำงานของผู้ใช้แต่ละประเภท
System Description: คำอธิบายระบบที่รวมไปถึง System Components, Data Flow, Integration Points, Technology Stack, User Interface ที่ทำให้เห็นภาพชัดเจนว่าระบบทำงานอย่างไร

## Scoring Rubric — To-be Swimlane Diagram
| Artifact | “Yes” | “Almost” | “Not Yet” |
|---------|--------|-----------|------------|
| **To-be Swimlane Diagram** | - Swimlane Diagram แสดง User Workflow ที่สมบูรณ์ ครอบคลุมผู้ใช้แต่ละประเภท  <br>- มี Business Rules และ Decision Points ที่สะท้อนกระบวนการตัดสินใจจริง <br>- ระบุ System Components และ Building Blocks จาก Microsoft Power Platform ได้เหมาะสม <br>- แสดง Data Flow และ Integration Points กับระบบเดิมได้ชัดเจน Technology Stack สอดคล้องกับความต้องการธุรกิจ | - แสดง Swimlane Diagram แต่บางส่วนขาดรายละเอียด เช่น User Workflow ไม่ครอบคลุมผู้ใช้งานทุกกลุ่ม <br>- Business Rules หรือ Decision Points ยังไม่ชัดเจน <br>- System Components ระบุได้ แต่ยังไม่เชื่อมโยงกับ Building Blocks อย่างเฉพาะเจาะจง <br>- Data Flow หรือ Integration Points มีการระบุแต่ยังไม่สมบูรณ์ | - Swimlane Diagram ขาดรายละเอียดหรือไม่สะท้อนกระบวนการจริง <br>- ไม่มี Business Rules หรือ Decision Points ที่ชัดเจน <br>- System Components ไม่ระบุหรือไม่เหมาะสมกับความต้องการ <br>- ไม่สามารถทำความเข้าใจหรือเห็นภาพ Data Flow / Integration Points ได้ |
| **Digital Solution Prototype Presentation** | - นำเสนอ Prototype ที่ทำงานได้จริงและสาธิตการทำงานของโซลูชันดิจิทัลหรือระบบอัตโนมัติได้ชัดเจน <br>- อธิบายปัญหาที่สะท้อนความต้องการและจำเป็นในการพัฒนาดิจิทัลโซลูชัน <br>- อธิบายกระบวนการทำงานใหม่ (To-Be Process) และ User Workflow ได้อย่างเป็นระบบ รวมถึงอธิบายส่วนประกอบและขั้นตอนการทำงานของดิจิทัลโซลูชันที่เห็นภาพได้ชัด <br>- Prototype สะท้อนการแก้ไขปัญหาทางธุรกิจได้ตรงตามความต้องการ | - สาธิตการทำงานได้แต่ยังขาดรายละเอียด เช่น การเชื่อมต่อกับ Legacy System หรือผู้ใช้งานยังไม่ครอบคลุม <br>- โซลูชันได้รับการอธิบายเป็นส่วนๆ แต่ไม่รวมเข้าเป็น To-Be Process ที่ต่อเนื่องและเป็นระบบ | - การสาธิตไม่ชัดเจนหรือไม่สะท้อนโซลูชันที่ต้องการ <br>- ไม่สามารถอธิบายการเชื่อมต่อระหว่างส่วนประกอบต่างๆ ได้ <br>- ไม่แสดงให้เห็นการแก้ไขปัญหาทางธุรกิจ |"
</assessment>

<competency>
"ผู้เรียนสามารถแปลงกระบวนการทำงานปัจจุบันเป็นโซลูชันดิจิทัล โดยนำเสนอเป็น Solution Blueprint และ/หรือ Digital Prototype ด้วยเครื่องมือ Microsoft Power Platform"
</competency>

<overview assessment>
"โปรดตอบคำถามต่อไปนี้
จำกัด 500-word limit
อธิบายบริบทในการทำงานของคุณ:
ทีมและบทบาทในองค์กร
อธิบายกระบวนการทำงานหรือระบบที่ต้องการออกแบบโซลูชันดิจิทัล
ผ่าน: คำตอบของผู้เรียนประกอบด้วยคำอธิบายที่ชัดเจนเกี่ยวกับทีมและบทบาทในองค์กร พร้อมทั้งระบุกระบวนการทำงานหรือระบบเฉพาะที่ต้องการออกแบบโซลูชันดิจิทัล โดยแสดงให้เห็นถึงความเข้าใจในปัญหาการทำงานปัจจุบันและความต้องการในการปรับปรุงด้วยเทคโนโลยี
ไม่ผ่าน: การตอบขาดความชัดเจน ขาดรายละเอียด กระบวนการที่ต้องการปรับปรุง หรือไม่แสดงให้เห็นถึงความเข้าใจบริบทการทำงาน"
</overview assessment>

<output>
{
    "alignment_result": true,
    "alignment_explanation": "Deliverables directly assess the competency and require a contextual description of team, role, and process. Suggestion: include a 500-word context narrative with the artifact for alignment verification.",
    "comprehensive_result": true,
    "comprehensive_explanation": "Assessment covers key competency elements. Suggestion: add a checklist specifying diagram elements and granularity to remove ambiguity.",
    "concisability_result": false,
    "concisability_explanation": "Instructions are detailed but redundant. Suggestion: condense to a one-page checklist with single-line requirements and remove HTML tags.",
    "learner_relevance_result": true,
    "learner_relevance_explanation": "Tasks match the competency and expected skills. Suggestion: provide optional scaffolding for effort calibration.",
    "readability_result": false,
    "readability_explanation": "Descriptions are lengthy and include HTML entities, impairing comprehension. Suggestion: use bullet points, remove HTML, and separate instructions from scoring.",
    "rubric_quality_result": true,
    "rubric_quality_explanation": "Rubric uses observable categories and identifies artifact elements. Suggestion: add measurable criteria and example evidence for each level.",
    "format_criteria_result": false,
    "format_criteria_explanation": "Submission mechanics are incomplete. Suggestion: add explicit instructions for upload path, filename format, metadata, max file size, and deadline."
}
</output>

### Additional Requirements
- All suggestions must directly solve the issue described in your analysis.
- Suggested versions must be **concise** and **aligned with the user’s intent**.
</instruction>

**Please assess the provided <assessment> content below following the <instruction> described above**

<assessment>
{{assessment}}
</assessment>
"""
EVAL_MAIN_ASSE_OUTPUT = {
  "title": "evaluate_assessment",
  "description": "Schema for the evaluator output that assesses an assessment artifact against seven dimensions (Alignment, Comprehensive, Concisability, Learner Relevance, Readability, Rubric Quality, Format Criteria). Each dimension must include a boolean result and a short explanatory string.",
  "type": "object",
  "properties": {
    "alignment_result": {
      "type": "boolean",
      "description": "Whether the deliverables align with the overview assessment and expected responses (true/false)."
    },
    "alignment_explanation": {
      "type": "string",
      "description": "Short explanation of why the deliverables do or do not align with the overview assessment."
    },
    "comprehensive_result": {
      "type": "boolean",
      "description": "Whether the deliverable fully meets the competency requirements and includes key elements (true/false)."
    },
    "comprehensive_explanation": {
      "type": "string",
      "description": "Short explanation of why the deliverable is or is not comprehensive relative to the competency."
    },
    "concisability_result": {
      "type": "boolean",
      "description": "Whether the deliverables are clear and concise, avoiding redundancy (true/false)."
    },
    "concisability_explanation": {
      "type": "string",
      "description": "Short explanation of why the deliverables are or are not concise and free from redundancy."
    },
    "learner_relevance_result": {
      "type": "boolean",
      "description": "Whether the deliverable methods match the expected knowledge level of the learner profile (true/false)."
    },
    "learner_relevance_explanation": {
      "type": "string",
      "description": "Short explanation of why the methods are or are not appropriate for the learner's level and micro-credential scope."
    },
    "readability_result": {
      "type": "boolean",
      "description": "Whether descriptions and rubrics are clearly structured, logical, and coherent (true/false)."
    },
    "readability_explanation": {
      "type": "string",
      "description": "Short explanation of why the descriptions and rubrics are or are not readable and well organized."
    },
    "rubric_quality_result": {
      "type": "boolean",
      "description": "Whether the rubric presents clear, observable, and measurable criteria with distinct mastery levels (true/false)."
    },
    "rubric_quality_explanation": {
      "type": "string",
      "description": "Short explanation of why the rubric does or does not meet quality criteria for observable and measurable levels."
    },
    "format_criteria_result": {
      "type": "boolean",
      "description": "Whether the assessment provides clear format and submission instructions for main and report deliverables (true/false)."
    },
    "format_criteria_explanation": {
      "type": "string",
      "description": "Short explanation of why the format and submission instructions are or are not adequate and clear."
    }
  },
  "required": [
    "alignment_result",
    "alignment_explanation",
    "comprehensive_result",
    "comprehensive_explanation",
    "concisability_result",
    "concisability_explanation",
    "learner_relevance_result",
    "learner_relevance_explanation",
    "readability_result",
    "readability_explanation",
    "rubric_quality_result",
    "rubric_quality_explanation",
    "format_criteria_result",
    "format_criteria_explanation"
  ],
  "additionalProperties": False,
  "strict": False
}
EVAL_MAIN_ASSE_WEIGHT = {
    "alignment_result":1,
    "comprehensive_result":1,
    "concisability_result":1,
    "learner_relevance_result":1,
    "readability_result":1,
    "rubric_quality_result":1,
    "format_criteria_result":1
}

EVAL_REFLECTION_ASSE_PROMPT = """
<instruction>
**Your Goal**: Evaluate the <assessment>, which is a sub-assessment designed to assess learner reflection. This reflection may include thoughts about the challenges faced while implementing the assessment after completing their <artifact assessment>, or insights gained after finishing the course. You must assess the quality of the <assessment> and provide targeted refinement suggestions using the following dimensions with provided <competency> and <artifact assessment> as context.
 
<artifact assessment>
{{artifact_assessment}}
</artifact assessment>

<competency>
{{competency}}
</competency>

---
## DIMENSIONS
1. **Question Quality**
evaluate that the questions in <assessment> are aligned and designed to reflect the learner's understanding after completing the assessment. The questions should inquire about how the assessment impacts their scenario or real-world environment or what challenges were faced during the learning process.
- Output **true** if the assessment questions clearly relate to the learner's real-world scenario or address challenges faced during learning.
- Output **false** if the assessment questions do not clearly relate to the learner's real-world scenario or fail to address challenges faced during learning.
2. **Rubric Quality**
evaluate that the pass criteria should describe clear, observable, and measurable criteria that reflect the learner experience or insight after complete the deliverable. The rubrics can be both qualitative descriptions, quantitative indicators, or a mix of both. Focus on the <assessment> questions only
- Output **true** if the rubrics provide clear, observable, and measurable criteria that accurately reflect the learner's experience or insights after completing the deliverable.
- Output **false** if the rubrics do not provide clear, observable, and measurable criteria that accurately reflect the learner's experience or insights after completing the deliverable.
3. **Readability**
evaluate that the questions and rubrics are clearly structured, logically organized, and written in a fluent, coherent manner that facilitates understanding and effective communication of ideas.
- Output **true** if the questions and rubrics are clear, logical, and easy to understand.
- Output **false** if the questions and rubrics are unclear, disorganized, or difficult to understand.
4. **Format Criteria**
evaluate the information that is structured as a open-ended question or list of open-ended question which assess learner response to pass or not pass. The assessment should included with response word-limit criteria
- Output **true** if the format of the information is similar to the defined format.
- Output **false** if the format is vague, unfocused, too long, or lacks a clear structure.
---

## YOUR TASKS
### **Analyze the User Input**
For each dimension:
- Evaluate whether it meets the dimension's requirements.
- Return only **true/false** ('<dimension's result>').
- Provide a short explanation of your reasoning ('<dimension's explanation>').
---

## OUTPUT FORMAT
Respond strictly in this JSON structure:
{
"question_quality_result": <dimension's result>,
"question_quality_explanation": <dimension's explanation>,
"rubric_quality_result": <dimension's result>,
"rubric_quality_explanation": <dimension's explanation>,
"readability_result": <dimension's result>,
"readability_explanation": <dimension's explanation>,
"format_criteria_result": <dimension's result>,
"format_criteria_explanation": <dimension's explanation>,
}
---

## EXAMPLE
### *example 1*
<assessment>
"โปรดตอบคำถามต่อไปนี้ 
จำกัด 300-word limit
คุณเจอความยากหรือความท้าทายอะไรบ้าง ในระหว่างที่แปลงกระบวนการทำงานเป็นดิจิทัลโซลูชัน และจัดการกับความยากหรือท้าทายนั้นอย่างไร?
คุณได้เรียนรู้อะไรจาก Digital Solution Designer ที่คิดว่าจะนำไปใช้ต่อยอดในงานหรือโปรเจ็คต่อไป?
ผ่าน: คำตอบของผู้เรียนอธิบายอย่างน้อย 1 ตัวอย่างของความท้าทายหรือความยากในการแปลงกระบวนการทำงานเป็นดิจิทัลโซลูชัน และยังแสดงการสะท้อนคิดเชื่อมโยงการเรียนรู้กับการปฏิบัติงานจริง มีแผนการนำไปใช้ที่ชัดเจน
ไม่ผ่าน: การสะท้อนคิดผิวเผิน หรือไม่เกี่ยวข้องกับการทำงานจริง"
</assessment>

<artifact assessment>

</artifact assessment>
"ผู้เรียนแสดง Solution Blueprint และ/หรือ Digital Solution Prototype โดยต้องจัดทำเอกสารในรูปแบบไฟล์ .docx หรือ .pdf ผ่านแพล็ตฟอร์มขององค์กร (เพื่อรักษาความลับทางการค้า) 
ผู้เรียนส่ง To-be Swimlane Diagram (Solution Blueprint) 1 ไดอะแกรม ที่แบ่ง Lanes เป็น 3 ประเภท: Human Tasks (งานที่คนต้องทำ), Digital Solution (ระบบดิจิทัลที่จะสร้างใหม่), Legacy System (ระบบเดิมที่ยังใช้งานอยู่) แสดง:
User Workflow: ขั้นตอนการทำงานของผู้ใช้แต่ละประเภท
Business Rules: กฎการทำงานของระบบตาม Decision Points
System Components: ส่วนประกอบของระบบและการเชื่อมต่อ Building Blocks
Data Flow: การไหลของข้อมูลผ่านระบบและจุดเก็บข้อมูล
Integration Points: จุดเชื่อมต่อกับระบบเดิม
Technology Stack: เครื่องมือ Microsoft Power Platform ที่ใช้ในแต่ละส่วน
กรณีที่ผู้เรียนได้นำ Blueprint ไปสร้างเป็น Digital Solution Prototype แล้วสามารถนำเสนอโซลูชันในรูปแบบ Presentation แทนได้โดยต้องจัดทำวิดีโอภายในองค์กร (เพื่อรักษาความลับทางการค้า) เป็นเวลา 3-7 นาที ในรูปแบบไฟล์ .mp4 และสไลด์ประกอบการนำเสนอ ที่อธิบาย:
Problem Statement: อธิบายเหตุผลในการพัฒนาโซลูชันและปัญหาที่ดิจิทัลโซลูชันนี้ต้องการแก้ไข
To-be Process: ภาพรวมของกระบวนการทำงานใหม่ แสดงการทำงานของโซลูชันดิจิทัลหรือระบบอัตโนมัติ
User Workflow: ขั้นตอนการทำงานของผู้ใช้แต่ละประเภท
System Description: คำอธิบายระบบที่รวมไปถึง System Components, Data Flow, Integration Points, Technology Stack, User Interface ที่ทำให้เห็นภาพชัดเจนว่าระบบทำงานอย่างไร

## Scoring Rubric — To-be Swimlane Diagram
| Artifact | “Yes” | “Almost” | “Not Yet” |
|---------|--------|-----------|------------|
| **To-be Swimlane Diagram** | - Swimlane Diagram แสดง User Workflow ที่สมบูรณ์ ครอบคลุมผู้ใช้แต่ละประเภท  <br>- มี Business Rules และ Decision Points ที่สะท้อนกระบวนการตัดสินใจจริง <br>- ระบุ System Components และ Building Blocks จาก Microsoft Power Platform ได้เหมาะสม <br>- แสดง Data Flow และ Integration Points กับระบบเดิมได้ชัดเจน Technology Stack สอดคล้องกับความต้องการธุรกิจ | - แสดง Swimlane Diagram แต่บางส่วนขาดรายละเอียด เช่น User Workflow ไม่ครอบคลุมผู้ใช้งานทุกกลุ่ม <br>- Business Rules หรือ Decision Points ยังไม่ชัดเจน <br>- System Components ระบุได้ แต่ยังไม่เชื่อมโยงกับ Building Blocks อย่างเฉพาะเจาะจง <br>- Data Flow หรือ Integration Points มีการระบุแต่ยังไม่สมบูรณ์ | - Swimlane Diagram ขาดรายละเอียดหรือไม่สะท้อนกระบวนการจริง <br>- ไม่มี Business Rules หรือ Decision Points ที่ชัดเจน <br>- System Components ไม่ระบุหรือไม่เหมาะสมกับความต้องการ <br>- ไม่สามารถทำความเข้าใจหรือเห็นภาพ Data Flow / Integration Points ได้ |
| **Digital Solution Prototype Presentation** | - นำเสนอ Prototype ที่ทำงานได้จริงและสาธิตการทำงานของโซลูชันดิจิทัลหรือระบบอัตโนมัติได้ชัดเจน <br>- อธิบายปัญหาที่สะท้อนความต้องการและจำเป็นในการพัฒนาดิจิทัลโซลูชัน <br>- อธิบายกระบวนการทำงานใหม่ (To-Be Process) และ User Workflow ได้อย่างเป็นระบบ รวมถึงอธิบายส่วนประกอบและขั้นตอนการทำงานของดิจิทัลโซลูชันที่เห็นภาพได้ชัด <br>- Prototype สะท้อนการแก้ไขปัญหาทางธุรกิจได้ตรงตามความต้องการ | - สาธิตการทำงานได้แต่ยังขาดรายละเอียด เช่น การเชื่อมต่อกับ Legacy System หรือผู้ใช้งานยังไม่ครอบคลุม <br>- โซลูชันได้รับการอธิบายเป็นส่วนๆ แต่ไม่รวมเข้าเป็น To-Be Process ที่ต่อเนื่องและเป็นระบบ | - การสาธิตไม่ชัดเจนหรือไม่สะท้อนโซลูชันที่ต้องการ <br>- ไม่สามารถอธิบายการเชื่อมต่อระหว่างส่วนประกอบต่างๆ ได้ <br>- ไม่แสดงให้เห็นการแก้ไขปัญหาทางธุรกิจ |"

<competency>
"ผู้เรียนสามารถแปลงกระบวนการทำงานปัจจุบันเป็นโซลูชันดิจิทัล โดยนำเสนอเป็น Solution Blueprint และ/หรือ Digital Prototype ด้วยเครื่องมือ Microsoft Power Platform"
</competency>

<output>
{
"question_quality_result": true,
"question_quality_explanation": "คำถามเป็นแบบสะท้อนความคิดที่ตรงไปยังประสบการณ์จริงของผู้เรียน (ความยาก/การจัดการ) และขอให้ระบุบทเรียนที่จะนำไปใช้ต่อ จึงเชื่อมโยงกับสถานการณ์การทำงานจริงได้ชัดเจน",
"rubric_quality_result": true,
"rubric_quality_explanation": "เกณฑ์ผ่านกำหนดเงื่อนไขที่สังเกตได้ชัดเจน (อย่างน้อย 1 ตัวอย่างความท้าทาย + การเชื่อมโยงการเรียนรู้กับการปฏิบัติงานจริง + แผนการนำไปใช้) ทำให้การประเมินเป็นไปได้แม้จะเป็นเชิงคุณภาพ",
"readability_result": true,
"readability_explanation": "คำถามและเกณฑ์ผ่าน/ไม่ผ่านเขียนอย่างกระชับและชัดเจน โครงสร้างตรรกะเรียงลำดับดี อ่านเข้าใจง่าย",
"format_criteria_result": true,
"format_criteria_explanation": "เป็นชุดคำถามปลายเปิดตามที่ระบุ และมีการกำหนดขอบเขตคำตอบ (300-word limit) จึงสอดคล้องกับรูปแบบข้อกำหนด"
}
</output>

### Additional Requirements
- All suggestions must directly solve the issue described in your analysis.
- Suggested versions must be **concise** and **aligned with the user’s intent**.
</instruction>

**Please assess the provided <assessment> content below following the <instruction> described above**

<assessment>
{{assessment}}
</assessment>
"""
EVAL_REFLECTION_ASSE_OUTPUT = {
  "title": "evaluate_reflection_assessment",
  "description": "Assess the quality of a learner reflection assessment using four dimensions (Question Quality, Rubric Quality, Readability, Format Criteria). For each dimension return a boolean result and a short explanation of the reasoning.",
  "type": "object",
  "properties": {
    "question_quality_result": {
      "type": "boolean",
      "description": "True if the assessment questions clearly relate to the learner's real-world scenario or address challenges faced during learning; otherwise false."
    },
    "question_quality_explanation": {
      "type": "string",
      "description": "A concise explanation (short sentence) justifying the question_quality_result."
    },
    "rubric_quality_result": {
      "type": "boolean",
      "description": "True if the rubric provides clear, observable, and measurable criteria reflecting the learner's experience/insights; otherwise false."
    },
    "rubric_quality_explanation": {
      "type": "string",
      "description": "A concise explanation (short sentence) justifying the rubric_quality_result."
    },
    "readability_result": {
      "type": "boolean",
      "description": "True if questions and rubrics are clearly structured, logical, and easy to understand; otherwise false."
    },
    "readability_explanation": {
      "type": "string",
      "description": "A concise explanation (short sentence) justifying the readability_result."
    },
    "format_criteria_result": {
      "type": "boolean",
      "description": "True if the assessment is formatted as open-ended question(s) with response word-limit criteria as specified; otherwise false."
    },
    "format_criteria_explanation": {
      "type": "string",
      "description": "A concise explanation (short sentence) justifying the format_criteria_result."
    }
  },
  "required": [
    "question_quality_result",
    "question_quality_explanation",
    "rubric_quality_result",
    "rubric_quality_explanation",
    "readability_result",
    "readability_explanation",
    "format_criteria_result",
    "format_criteria_explanation"
  ],
  "additionalProperties": False,
  "strict": False
}
EVAL_REFLECTION_ASSE_WEIGHT = {
    "question_quality_result":1,
    "rubric_quality_result":1,
    "readability_result":1,
    "format_criteria_result":1
}

EVAL_METHOD_COMP_PROMPT = """
<instruction>
**Your Goal**: Evaluate the <method component> that describe the overview content to be taught in the micro-credential. The content is an overview aimed at teaching the learner, as described in <who is this for>, to achieve the <competency>, as indicated by the designed <artifact assessment>. You must assess the quality of <method components> and provide targeted refinement suggestions using the following dimensions and the provided context, which includes <who is this for>, <competency>, and <artifact assessment>

<who is this for>
{{whoisthisfor}}
</who is this for>

<competency>
{{competency}}
</competency>

<artifact assessment>
{{artifact_assessment}}
</artifact assessment>

---
## DIMENSIONS
1. **Alignment**
evaluates whether the content or topic directly support the targeted <competency> or skill outcomes. The learning experiences should explicitly enable learners to demonstrate the intended performance or behavior. 
- Output **true** if the content directly supports the targeted competency and enables learners to demonstrate the intended performance.
- Output **false** if the content does not support the targeted competency or fails to enable the intended performance.
2. **Coverage**
evaluate whether the method components cover all necessary topic to achieve the <artifact assessment>. No missing key elements
- Output **true** if all necessary topics are covered and no key elements are missing.
- Output **false** if any necessary topics are missing or key elements are not covered.
3. **Learner Relevance**
evaluates whether method content match the expected prior knowledge level of the learner. Methods should neither oversimplify nor exceed the intended level of the micro-credential.
- Output **true** if the content matches the expected prior knowledge level and is appropriately challenging.
- Output **false** if the content is either too simplistic or too advanced for the expected learner level.
4. **Consistency**
evaluates whether the method components are logically connected and structured progressively to support learners in understanding each step toward achieving the <artifact assessment> and <competency>. No redundancy and overlap content in each component
- Output **true** if the components are logically connected, structured progressively, and free of redundancy.
- Output **false** if the components are disjointed, lack progression, or contain redundant content.
5. **Readability**
evaluate that the description and rubrics of each deliverable are clearly structured, logically organized, and written in a fluent, coherent manner that facilitates understanding and effective communication of ideas.
- Output **true** if the descriptions and rubrics are clear, logical, and coherent.
- Output **false** if the descriptions and rubrics are unclear, illogical, or incoherent.
6. **Format Criteria**
evaluate the information are included with the introduction paragraph ,which relate to the <competency> and <who is this for> and structured in topic, sub-topic / bullet-point come with a short description or summary about the topic
- Output **true** if the format of the information is similar to the defined format.
- Output **false** if the format is vague, unfocused, too long, or lacks a clear structure.
---

## YOUR TASKS
### **Analyze the User Input**
For each dimension:
- Evaluate whether it meets the dimension's requirements.
- Return only **true/false** ('<dimension's result>').
- Provide a short explanation of your reasoning ('<dimension's explanation>').
---

## OUTPUT FORMAT
Respond strictly in this JSON structure:
{
"alignment_result": <dimension's result>,
"alignment_explanation": <dimension's explanation>,
"coverage_result": <dimension's result>,
"coverage_explanation": <dimension's explanation>,
"learner_relevance_result": <dimension's result>,
"learner_relevance_explanation": <dimension's explanation>,
"consistency_result": <dimension's result>,
"consistency_explanation": <dimension's explanation>,
"readability_result": <dimension's result>,
"readability_explanation": <dimension's explanation>,
"format_criteria_result": <dimension's result>,
"format_criteria_explanation": <dimension's explanation>
}
---

## EXAMPLE
### *example 1*
<method component>
"การออกแบบโซลูชันดิจิทัลที่ถูกต้องและรวดเร็วต้องอาศัยกระบวนการที่เป็นระบบและเครื่องมือที่ช่วยจัดระเบียบความคิด รวมถึงต้องมีความรู้ความเข้าใจเกี่ยวกับองค์ประกอบของดิจิทัลโซลูชันและความสามารถของเครื่องมือที่จะใช้พัฒนาโซลูชัน 
ผู้เรียนจะฝึกใช้ Business Process Modeling, Gap Analysis และ Digital Building Blocks เพื่อแปลงความต้องการทางธุรกิจเป็นโซลูชันดิจิทัลที่ใช้งานได้จริง โดยเนื้อหาทักษะจะครอบคลุม 4 องค์ประกอบสำคัญดังนี้:
1. Business Process Modeling และ Gap Analysis คือ การวิเคราะห์กระบวนการทำงานอย่างเป็นระบบเพื่อระบุโอกาสในการปรับปรุงด้วยเทคโนโลยีดิจิทัล โดยใช้เครื่องมือ Swimlane Diagram เพื่อให้เห็นภาพชัดเจนของ Workflow และจุดที่ต้องปรับปรุง
1.1. As-is Process Mapping: วิเคราะห์กระบวนการปัจจุบันโดยใช้ Swimlane Diagram เพื่อทำความเข้าใจการทำงานที่เกิดขึ้นจริง (รูปที่ 1)
กำหนด Scope และผู้เกี่ยวข้อง (Players/Lanes): ระบุขอบเขตของกระบวนการ จุดเริ่มต้น-สิ้นสุด และแผนก/บุคคลที่เกี่ยวข้อง
ระบุกิจกรรมหลัก (Key Activities) และลำดับการทำงาน: ลิสต์งานทั้งหมดในกระบวนการและเรียงลำดับตามลำดับเวลา
เชื่อมโยงการไหลของงาน (Flow) และจุดส่งต่อ (Handoffs): วาดเส้นเชื่อมและให้ความสำคัญกับจุดที่งานข้ามระหว่างแผนก
ตรวจสอบความถูกต้อง: นำ Diagram ไปให้เจ้าของกระบวนการตรวจสอบและ Role-Play เพื่อหาข้อผิดพลาด
1.2 Process Improvement Discovery: การค้นหาและวิเคราะห์โอกาสในการปรับปรุงกระบวนการทำงาน เป็นขั้นตอนสำคัญหลังจากที่ผู้เรียนได้ทำการวิเคราะห์กระบวนการปัจจุบัน (As-is) แล้ว เพื่อหาจุดที่เป็นปัญหา (Pain Points) และโอกาสพัฒนา (Opportunities) อย่างเป็นระบบ โดยพิจารณาใน 3 มิติหลัก (รูปที่ 2) ดังนี้
People (บุคลากร)	
Skills (ทักษะ): ตรวจสอบว่าบุคลากรมีทักษะเพียงพอต่อการปฏิบัติงานหรือไม่ เช่น ขาดความรู้ด้านการใช้เครื่องมือดิจิทัล, ต้องใช้เวลามากในการฝึกอบรม
Bottleneck (จุดคอขวด): หาช่วงที่งานติดขัดเพราะต้องรอการอนุมัติ, รอคนเพียงบางตำแหน่ง หรือใช้เวลามากเกินความจำเป็น
Handoffs (การส่งต่องาน): วิเคราะห์ว่าการส่งต่อข้อมูลหรือเอกสารระหว่างบุคคลหรือหน่วยงานทำให้เกิดความล่าช้าหรือข้อมูลสูญหายหรือไม่
Process (กระบวนการ)
Redundancy (ความซ้ำซ้อน): มีขั้นตอนที่ทำซ้ำโดยไม่จำเป็นหรือไม่ เช่น การบันทึกข้อมูลซ้ำในหลายระบบ
Delays (ความล่าช้า): ขั้นตอนใดใช้เวลานานกว่ามาตรฐาน หรือเกิดการรอคอยที่ไม่สร้างคุณค่า
Complexity (ความซับซ้อน): มีขั้นตอนที่ซับซ้อนเกินความจำเป็น ทำให้บุคลากรสับสนหรือเกิดข้อผิดพลาดง่าย
3. Technology (เทคโนโลยี)
Manual Work (งานที่ทำด้วยมือ): งานที่สามารถทำให้อัตโนมัติได้ แต่ยังคงทำด้วยคน เช่น การกรอกข้อมูลซ้ำ หรือการรวมไฟล์ด้วยตนเอง
Tools (เครื่องมือ): เครื่องมือปัจจุบันไม่เพียงพอหรือไม่มีการบูรณาการระหว่างระบบ ทำให้เกิดช่องว่างในการทำงาน
Data (ข้อมูล): ข้อมูลไม่ครบถ้วน, ไม่มีมาตรฐาน หรือไม่สามารถเข้าถึงได้ง่าย ทำให้การตัดสินใจล่าช้าหรือผิดพลาด

รูปที่ 1 ตัวอย่าง As-is Swimlane Diagram จากกระบวนการ Business Process Modeling

รูปที่ 2 Process Improvement Discovery Framework
2. Digital Solution Architecture และ Building Blocks คือ การออกแบบโครงสร้างของโซลูชันดิจิทัลโดยมองภาพรวมว่ามีองค์ประกอบ (Building Blocks) อะไรบ้างและแต่ละส่วนทำงานร่วมกันอย่างไร เพื่อให้ได้โซลูชันที่ตอบโจทย์ปัญหาและความต้องการของธุรกิจ ซึ่งในบริบทของ Microsoft Power Platform Building Blocks จะหมายถึงเครื่องมือและ Components ที่ใช้สร้าง Automation Solution, Data Solution และ AI Solution
2.1. Automation Solution: เชื่อมต่อระบบต่างๆ และทำงานซ้ำแทนคน ประกอบด้วยเครื่องมือดังนี้
Power Automate: แพลตฟอร์มสร้าง Workflow ที่ทำงานได้ 4 ประเภท
Instant (Manual): เริ่มทำงานเมื่อผู้ใช้กดปุ่ม เช่น ปุ่มใน Teams หรือ Power Apps
Scheduled (ตามเวลา): ทำงานตามกำหนดเวลา เช่น ส่งรายงานทุกวันเวลา 9:00 น.
Automated (ตาม Trigger): เริ่มทำงานอัตโนมัติเมื่อเกิดเหตุการณ์ เช่น มีอีเมลใหม่เข้ามา, มีไฟล์ถูกอัปโหลด
AI-Powered (ใช้ AI Builder): ใช้ AI วิเคราะห์ข้อมูลและตัดสินใจ เช่น อ่านเอกสาร PDF และดึงข้อมูลที่ต้องการไปใส่ในระบบ
Connectors: เชื่อมต่อกับระบบภายในและภายนอก (Standard/Premium/Custom Connectors)
Standard Connectors: เช่น Outlook, SharePoint, OneDrive
Premium Connectors: เช่น Salesforce, ServiceNow
Custom Connectors: ผู้พัฒนาสร้างขึ้นเองเพื่อเชื่อมต่อกับระบบเฉพาะขององค์กร
Use Cases ตัวอย่าง: 
ส่งอีเมลแจ้งเตือนลูกค้าอัตโนมัติ
รีเฟรช Power BI Dataset ทุกวันโดยไม่ต้องทำเอง
จัดการเอกสาร เช่น เก็บไฟล์ PDF จากอีเมลลง SharePoint อัตโนมัติ
2.2. Data Solution: จัดการข้อมูลตั้งแต่รวบรวม แปลง จนถึงการแสดงผล ประกอบด้วยเครื่องมือดังนี้
Power Query: ใช้สำหรับ ETL (Extract, Transform, Load)
Extract: ดึงข้อมูลจากแหล่งต่างๆ เช่น Excel, SQL Database
Transform: ทำความสะอาด ปรับรูปแบบ และรวมข้อมูล
Load: นำข้อมูลไปใช้ใน Power BI หรือระบบอื่น
Power BI: ใช้สร้าง Interactive Dashboard และ Data Visualization 
รองรับ Automatic Data Refresh เพื่อให้ข้อมูลทันสมัยอยู่เสมอ
สามารถเจาะลึกข้อมูล (Drill Down) และใช้ Filter เพื่อค้นหาข้อมูลเฉพาะจุด
Data Sources: แหล่งข้อมูลที่เชื่อมต่อได้
Excel, SharePoint Lists, Dataverse, Dynamics 365
Use Cases ตัวอย่าง
รวมข้อมูลยอดขายจากหลายสาขามาแสดงใน Dashboard เดียว
ทำความสะอาดข้อมูลลูกค้าก่อนนำไปใช้ใน AI Model
สร้างรายงาน KPI ที่อัปเดตอัตโนมัติทุกเช้า
2.3. AI Solution: ใช้ปัญญาประดิษฐ์ช่วยในการตัดสินใจและประมวลผลข้อมูล เพื่อเพิ่มความแม่นยำและความรวดเร็ว
Microsoft 365 Copilot Chat: AI Assistant ที่ช่วยสรุปข้อมูล ตอบคำถาม และสร้างเนื้อหา
AI Builder: ใช้ประมวลผลเอกสาร PDF, รูปภาพ, ข้อความ 
Copilot Studio: สร้าง Custom AI Agent ที่ทำงานตามความต้องการเฉพาะขององค์กร
Integration: 
ผสาน AI เข้ากับ Power Automate เพื่อให้ Workflow ตัดสินใจได้เองจากข้อมูล
เชื่อมกับ Microsoft Teams เพื่อให้พนักงานสื่อสารกับ AI ได้ง่าย
รวมกับระบบอื่นๆ เพื่อให้ AI ช่วยวิเคราะห์และส่งคำตอบอัตโนมัติ
Use Cases ตัวอย่าง
AI อ่านและบันทึกข้อมูลจากเอกสาร PDF เข้าระบบ ERP
สร้าง Chatbot ตอบคำถามลูกค้าโดยอัตโนมัติ
วิเคราะห์ข้อมูลลูกค้าและแนะนำโปรโมชั่นที่เหมาะสม
3. To-Be Process Design และ Solution Blueprint Development การพัฒนาโซลูชันดิจิทัลที่มีประสิทธิภาพไม่ได้หยุดแค่การวิเคราะห์สภาพปัจจุบัน (As-Is) แต่ต้อง ออกแบบสภาพที่ต้องการในอนาคต (To-Be) และสร้าง Solution Blueprint ที่เป็นภาพรวมของระบบและการทำงาน เพื่อเป็นคู่มือให้ทีมพัฒนานำไปสร้าง Proof-of-Concept หรือระบบจริงได้ถูกต้องและครบถ้วน
3.1. To-be Process Design: ออกแบบกระบวนการใหม่โดยเปลี่ยนมุมมองจากการแบ่งตามแผนกเป็นการแบ่งตามประเภทงาน เพื่อมองกระบวนการแบบ End-to-End และลดการทำงานซ้ำซ้อนระหว่างฝ่าย โดยองค์ประกอบหลักที่ต้องระบุใน To-Be Process Design ประกอบด้วย
Human Tasks (งานที่ทำโดยคน): รวมงานที่ต้องใช้การตัดสินใจ ความคิดสร้างสรรค์ หรือการติดต่อสื่อสารของคนจากทุกฝ่าย
Automation/Digital Solution (งานที่ระบบทำแทน): ระบุงานที่ระบบดิจิทัลจะทำแทน เช่น การส่งข้อมูล การคำนวณ การแจ้งเตือน
Legacy System (ระบบเดิม): ระบบเดิมที่ยังใช้งานอยู่และจุดที่ต้องเชื่อมต่อหรือดึงข้อมูล
Address Decision Points (จุดตัดสินใจ): ระบุเงื่อนไขที่ส่งผลต่อการไหลของงาน
3.2. Solution Blueprint: เพิ่มรายละเอียดบนแผนผัง To-Be Process Design จากการทดลองทำ สัมภาษณ์ผู้ปฏิบัติงานเพิ่มเติม และพิจารณา Data Schema หรือระบบ Legacy System ที่เกี่ยวข้อง เพื่อปรับปรุง Swimlane Diagram ให้มีรายละเอียดดังนี้
User Workflow: ขั้นตอนการทำงานของผู้ใช้แต่ละประเภท
อธิบายว่าผู้ใช้แต่ละประเภท (เช่น พนักงานปฏิบัติการ, ผู้จัดการ, ลูกค้า) ทำอะไรบ้างในแต่ละขั้นตอน
ใช้ Swimlane Diagram เพื่อแยกบทบาทของผู้ใช้ชัดเจน
Business Rules: กฎการทำงานของระบบตามเงื่อนไขและ Decision Points
ระบุเงื่อนไขที่ระบบต้องทำตาม เช่น การตรวจสอบสิทธิ์ผู้ใช้, การอนุมัติคำสั่งซื้อเมื่อครบจำนวนขั้นต่ำ
อ้างอิงจาก Decision Points ใน To-Be Process
System Components: ส่วนประกอบของระบบและการเชื่อมต่อระหว่าง Building Blocks
แสดงว่าแต่ละส่วนของระบบทำหน้าที่อะไร เช่น ฟอร์มรับข้อมูล, API Gateway, Data Storage
ระบุการเชื่อมต่อระหว่างส่วนต่างๆ และเครื่องมือ (Building Blocks) ที่ใช้ เช่น Power Automate, Power BI, AI Builder
Data Flow: การไหลของข้อมูลผ่านระบบและจุดเก็บข้อมูล
แสดงเส้นทางการไหลของข้อมูลจากต้นทางถึงปลายทาง เช่น จากฟอร์ม → ฐานข้อมูล → Dashboard
ระบุจุดเก็บข้อมูลชัดเจน (Data Storage Locations)
Integration Points: จุดเชื่อมต่อกับระบบเดิมและ API Requirements
ระบุ API Requirements 
อธิบายว่าระบบจะเชื่อมกับ Legacy System อย่างไร เพื่อให้การทำงานเป็นแบบไร้รอยต่อ
Technology Stack: เครื่องมือและเทคโนโลยีที่ใช้ในแต่ละส่วน
ระบุเครื่องมือที่ใช้ในแต่ละส่วน เช่น Power Apps สำหรับ UI, Power Automate สำหรับ Workflow, Dataverse สำหรับ Data Storage
อธิบายเหตุผลที่เลือกเทคโนโลยีนั้น เช่น รองรับการขยายระบบ, ลดค่าใช้จ่าย, ใช้ง่ายต่อผู้ใช้ปลายทาง
4. Data Model, User Interface, Prototype Development (Optional) คือความรู้ความเข้าใจเรื่องการออกแบบรายละเอียดของดิจิทัลโซลูชัน เตรียมพร้อมสำหรับการพัฒนา Prototype ที่ใช้งานได้จริง 
4.1. Data Model Design: ออกแบบโครงสร้างข้อมูลตาม Star Schema 
องค์ประกอบสำคัญของ Star Schema
Dimension Tables: เก็บข้อมูลหลัก (Entities) เช่น Customer, Product, Employee พร้อม Unique ID
Fact Tables: เก็บข้อมูลเหตุการณ์ (Events) ที่เชื่อม Dimension Keys เข้าด้วยกัน
Structured vs Unstructured Data: แยกประเภทข้อมูลและวิธีการจัดเก็บที่เหมาะสม
4.2. User Interface Design: ออกแบบประสบการณ์ผู้ใช้ที่ใช้งานง่าย
Data Collection Interface: 
ใช้ Microsoft Forms (Simple) หมาะสำหรับการเก็บข้อมูลง่ายๆ เช่น แบบสอบถาม, แบบฟอร์มแจ้งปัญหา
Power Apps (Complex Integration) เหมาะสำหรับการทำงานที่ซับซ้อน มีการเชื่อมต่อระบบหลายแหล่ง เช่น การสร้างแอปจัดการคำสั่งซื้อที่เชื่อมกับฐานข้อมูล
Design Principles: 
Single-column layout: จัดข้อมูลในคอลัมน์เดียวเพื่อให้ผู้ใช้เลื่อนดูง่าย
Logical flow: ลำดับขั้นตอนการกรอกข้อมูลมีความต่อเนื่องและเข้าใจง่าย
Clear labels: ใช้คำอธิบายชัดเจนและสั้น
Appropriate validation: ใส่เงื่อนไขตรวจสอบข้อมูล เช่น ห้ามเว้นว่าง, ต้องกรอกอีเมลให้ถูกต้อง
Dashboard Design: 
ใช้ Power BI หรือ Excel เพื่อสร้าง Interactive Visualization
ใส่ Filter, Drill Down และ Highlight เพื่อให้ผู้ใช้สำรวจข้อมูลได้ด้วยตนเอง
ใช้สีและการจัดวางที่ช่วยให้เข้าใจข้อมูลได้เร็ว
4.3. Prototype Development: สร้างต้นแบบที่ทำงานได้จริง
ใช้ No-Code Tools เพื่อพัฒนาอย่างรวดเร็ว
เช่น Power Apps, Power Automate, Power BI เพื่อพัฒนาได้เร็วและแก้ไขได้ง่าย
ทดสอบ User Journey และ Business Logic
ตรวจสอบว่ากระบวนการทำงานเป็นไปตามที่ออกแบบไว้หรือไม่
ทดสอบว่าเงื่อนไข (Business Rules) ทำงานถูกต้อง เช่น การอนุมัติ, การส่งข้อมูล
ยังไม่ต้องกังวลเรื่อง Security, Performance, Edge Cases ในขั้น Proof-of-Concept"
</method component>

<who is this for>
"Business Analyst, นักพัฒนาระบบ, Citizen Developer ผู้มีหน้าที่ในการแปลงความต้องการทางธุรกิจเป็นระบบดิจิทัลที่ใช้งานได้จริง"
</who is this for>

<competency>
"ผู้เรียนสามารถแปลงกระบวนการทำงานปัจจุบันเป็นโซลูชันดิจิทัล โดยนำเสนอเป็น Solution Blueprint และ/หรือ Digital Prototype ด้วยเครื่องมือ Microsoft Power Platform"
</competency>

<artifact assessment>
""ผู้เรียนแสดง Solution Blueprint และ/หรือ Digital Solution Prototype โดยต้องจัดทำเอกสารในรูปแบบไฟล์ .docx หรือ .pdf ผ่านแพล็ตฟอร์มขององค์กร (เพื่อรักษาความลับทางการค้า) 
ผู้เรียนส่ง To-be Swimlane Diagram (Solution Blueprint) 1 ไดอะแกรม ที่แบ่ง Lanes เป็น 3 ประเภท: Human Tasks (งานที่คนต้องทำ), Digital Solution (ระบบดิจิทัลที่จะสร้างใหม่), Legacy System (ระบบเดิมที่ยังใช้งานอยู่) แสดง:
User Workflow: ขั้นตอนการทำงานของผู้ใช้แต่ละประเภท
Business Rules: กฎการทำงานของระบบตาม Decision Points
System Components: ส่วนประกอบของระบบและการเชื่อมต่อ Building Blocks
Data Flow: การไหลของข้อมูลผ่านระบบและจุดเก็บข้อมูล
Integration Points: จุดเชื่อมต่อกับระบบเดิม
Technology Stack: เครื่องมือ Microsoft Power Platform ที่ใช้ในแต่ละส่วน
กรณีที่ผู้เรียนได้นำ Blueprint ไปสร้างเป็น Digital Solution Prototype แล้วสามารถนำเสนอโซลูชันในรูปแบบ Presentation แทนได้โดยต้องจัดทำวิดีโอภายในองค์กร (เพื่อรักษาความลับทางการค้า) เป็นเวลา 3-7 นาที ในรูปแบบไฟล์ .mp4 และสไลด์ประกอบการนำเสนอ ที่อธิบาย:
Problem Statement: อธิบายเหตุผลในการพัฒนาโซลูชันและปัญหาที่ดิจิทัลโซลูชันนี้ต้องการแก้ไข
To-be Process: ภาพรวมของกระบวนการทำงานใหม่ แสดงการทำงานของโซลูชันดิจิทัลหรือระบบอัตโนมัติ
User Workflow: ขั้นตอนการทำงานของผู้ใช้แต่ละประเภท
System Description: คำอธิบายระบบที่รวมไปถึง System Components, Data Flow, Integration Points, Technology Stack, User Interface ที่ทำให้เห็นภาพชัดเจนว่าระบบทำงานอย่างไร

## Scoring Rubric — To-be Swimlane Diagram
| Artifact | “Yes” | “Almost” | “Not Yet” |
|---------|--------|-----------|------------|
| **To-be Swimlane Diagram** | - Swimlane Diagram แสดง User Workflow ที่สมบูรณ์ ครอบคลุมผู้ใช้แต่ละประเภท  <br>- มี Business Rules และ Decision Points ที่สะท้อนกระบวนการตัดสินใจจริง <br>- ระบุ System Components และ Building Blocks จาก Microsoft Power Platform ได้เหมาะสม <br>- แสดง Data Flow และ Integration Points กับระบบเดิมได้ชัดเจน Technology Stack สอดคล้องกับความต้องการธุรกิจ | - แสดง Swimlane Diagram แต่บางส่วนขาดรายละเอียด เช่น User Workflow ไม่ครอบคลุมผู้ใช้งานทุกกลุ่ม <br>- Business Rules หรือ Decision Points ยังไม่ชัดเจน <br>- System Components ระบุได้ แต่ยังไม่เชื่อมโยงกับ Building Blocks อย่างเฉพาะเจาะจง <br>- Data Flow หรือ Integration Points มีการระบุแต่ยังไม่สมบูรณ์ | - Swimlane Diagram ขาดรายละเอียดหรือไม่สะท้อนกระบวนการจริง <br>- ไม่มี Business Rules หรือ Decision Points ที่ชัดเจน <br>- System Components ไม่ระบุหรือไม่เหมาะสมกับความต้องการ <br>- ไม่สามารถทำความเข้าใจหรือเห็นภาพ Data Flow / Integration Points ได้ |
| **Digital Solution Prototype Presentation** | - นำเสนอ Prototype ที่ทำงานได้จริงและสาธิตการทำงานของโซลูชันดิจิทัลหรือระบบอัตโนมัติได้ชัดเจน <br>- อธิบายปัญหาที่สะท้อนความต้องการและจำเป็นในการพัฒนาดิจิทัลโซลูชัน <br>- อธิบายกระบวนการทำงานใหม่ (To-Be Process) และ User Workflow ได้อย่างเป็นระบบ รวมถึงอธิบายส่วนประกอบและขั้นตอนการทำงานของดิจิทัลโซลูชันที่เห็นภาพได้ชัด <br>- Prototype สะท้อนการแก้ไขปัญหาทางธุรกิจได้ตรงตามความต้องการ | - สาธิตการทำงานได้แต่ยังขาดรายละเอียด เช่น การเชื่อมต่อกับ Legacy System หรือผู้ใช้งานยังไม่ครอบคลุม <br>- โซลูชันได้รับการอธิบายเป็นส่วนๆ แต่ไม่รวมเข้าเป็น To-Be Process ที่ต่อเนื่องและเป็นระบบ | - การสาธิตไม่ชัดเจนหรือไม่สะท้อนโซลูชันที่ต้องการ <br>- ไม่สามารถอธิบายการเชื่อมต่อระหว่างส่วนประกอบต่างๆ ได้ <br>- ไม่แสดงให้เห็นการแก้ไขปัญหาทางธุรกิจ |""
</artifact assessment>

<output>
{
  "alignment_result": true,
  "alignment_explanation": "The overall content focuses on teaching the transformation of processes into Solution Blueprints/Prototypes using Microsoft Power Platform, aligning with the specified competencies and enabling learners to create To-be Swimlane Diagrams or Prototypes according to assessment criteria.",
  "coverage_result": true,
  "coverage_explanation": "The method components cover all essential topics required for the assessment: As-Is mapping, Process improvement, To-Be design, Swimlane Diagram with Human/Digital/Legacy lanes, Business Rules, System Components, Data Flow, Integration Points, Technology Stack, and steps for creating Prototypes/Presentations.",
  "learner_relevance_result": true,
  "learner_relevance_explanation": "The content level (process modeling, Power Platform Building Blocks, data model, UI, prototyping) is appropriate for the target audience (Business Analysts, System Developers, Citizen Developers), being neither too simplistic nor unnecessarily complex.",
  "consistency_result": true,
  "consistency_explanation": "The structure is systematically ordered from As-Is analysis → identifying opportunities → To-Be design → specifying Blueprint/Technology → developing Prototype, with connections between sections. There are minor repetitions in details but no contradictions.",
  "readability_result": true,
  "readability_explanation": "The text is organized into subheadings and clearly summarizes actionable points (As-Is, Process Improvement, Building Blocks, To-Be, Data/UI/Prototype), making it easy to read and apply immediately. Although lengthy, it is well-ordered and clear.",
  "format_criteria_result": true,
  "format_criteria_explanation": "There is an introductory paragraph linking to competencies/learners, and it is organized into main-subheadings/bullets with brief explanations as per the specified format."
}
</output>

### Additional Requirements
- All suggestions must directly solve the issue described in your analysis.
- Suggested versions must be **concise** and **aligned with the user’s intent**.
</instruction>

**Please assess the provided <method_component> content below following the <instruction> described above**

<method component>
{{method_component}}
</method component>
"""
EVAL_METHOD_COMP_OUTPUT = {
  "title": "evaluate_method_components",
  "description": "Assess the quality of method components for a micro-credential overview using seven dimensions (Alignment, Coverage, Learner Relevance, Consistency, Readability, Faithfulness, Format Criteria). For each dimension return a boolean result and a short explanation.",
  "type": "object",
  "properties": {
    "alignment_result": {
      "type": "boolean",
      "description": "true if the content directly supports the targeted competency and enables learners to demonstrate the intended performance; false otherwise."
    },
    "alignment_explanation": {
      "type": "string",
      "description": "A short explanation justifying the alignment_result."
    },
    "coverage_result": {
      "type": "boolean",
      "description": "true if all necessary topics are covered to achieve the artifact assessment with no key elements missing; false otherwise."
    },
    "coverage_explanation": {
      "type": "string",
      "description": "A short explanation justifying the coverage_result."
    },
    "learner_relevance_result": {
      "type": "boolean",
      "description": "true if the content matches the expected prior knowledge level and is appropriately challenging; false otherwise."
    },
    "learner_relevance_explanation": {
      "type": "string",
      "description": "A short explanation justifying the learner_relevance_result."
    },
    "consistency_result": {
      "type": "boolean",
      "description": "true if components are logically connected, progressive, and free of redundancy; false otherwise."
    },
    "consistency_explanation": {
      "type": "string",
      "description": "A short explanation justifying the consistency_result."
    },
    "readability_result": {
      "type": "boolean",
      "description": "true if descriptions and rubrics are clear, logical, and coherent; false otherwise."
    },
    "readability_explanation": {
      "type": "string",
      "description": "A short explanation justifying the readability_result."
    },
    "format_criteria_result": {
      "type": "boolean",
      "description": "true if the information includes an introduction linking competency and audience and is structured into topics/sub-topics or bullet points with brief descriptions; false otherwise."
    },
    "format_criteria_explanation": {
      "type": "string",
      "description": "A short explanation justifying the format_criteria_result."
    }
  },
  "required": [
    "alignment_result",
    "alignment_explanation",
    "coverage_result",
    "coverage_explanation",
    "learner_relevance_result",
    "learner_relevance_explanation",
    "consistency_result",
    "consistency_explanation",
    "readability_result",
    "readability_explanation",
    "format_criteria_result",
    "format_criteria_explanation"
  ],
  "additionalProperties": False,
  "strict": False
}
EVAL_METHOD_COMP_WEIGHT = {
    "alignment_result": 1,
    "coverage_result": 1,
    "learner_relevance_result": 1,
    "consistency_result": 1,
    "readability_result": 1,
    "format_criteria_result":1
}

EVAL_KEY_METHOD_PROMPT = """
<instruction>
**Your Goal**: Evaluate the <key method> which summarized the <method component> to tell the learner about the overview of the micro-credential teaching content in several paragraph. The key method aim to make the learner understand their learning path and content included in the course. You must assess quality of <key method> and provide targeted refinement suggestions using the following dimensions.

<method component>
{{method_component}}
</method component>

---
## DIMENSIONS
1. **Concisability**
evaluate whether the key method is clearly and concisely described, avoiding redundancy and ensuring that all essential information is included in a well-summarized form.
- Output **true** if the content is clear, concise, and includes all essential information without redundancy.
- Output **false** if the content is unclear, redundant, or missing essential information.
2. **Coverage**
evaluate whether the key method cover all method component and not compress any necessary information. learner should still understand overall of the method or procedures to achieve the competency
- Output **true** if all components of the method are covered and no necessary information is compressed, allowing the learner to understand the overall method or procedures.
- Output **false** if any components are missing or necessary information is compressed, hindering the learner's understanding of the method or procedures.
3. **Format Criteria**
Evaluate the information that is structured as a summarized paragraph. The content should constructed from <target learner> + <action verb that demonstrates method / procedures>
- Output **true** if the format of the information is similar to the defined format.
- Output **false** if the format is vague, unfocused, too long, or lacks a clear structure.
---

## YOUR TASKS
### **Analyze the User Input**
For each dimension:
- Evaluate whether it meets the dimension's requirements.
- Return only **true/false** ('<dimension's result>').
- Provide a short explanation of your reasoning ('<dimension's explanation>').
---

## OUTPUT FORMAT
Respond strictly in this JSON structure:
{
"concisability_result": <dimension's result>,
"concisability_explanation": <dimension's explanation>,
"coverage_result": <dimension's result>,
"coverage_explanation": <dimension's explanation>,
"format_criteria_result": <dimension's result>,
"format_criteria_explanation": <dimension's explanation>,
}
---

## EXAMPLE
### *example 1*
<key method>
"ผู้เรียนแปลงกระบวนการทำงานปัจจุบันเป็นโซลูชันดิจิทัล โดยพัฒนา Solution Blueprint ที่ใช้ Business Process Modeling เพื่อวิเคราะห์กระบวนการปัจจุบัน (As-is) และออกแบบกระบวนการใหม่ (To-be) ด้วย Swimlane Diagram จากนั้นเลือกใช้ Digital Building Blocks จาก Microsoft Power Platform เพื่อประกอบเป็น Solution Blueprint ครอบคลุม Automation Solution, Data Solution และ AI Solution เพื่อตอบสนองความต้องการทางธุรกิจ"
</key method>

<method component>
"การออกแบบโซลูชันดิจิทัลที่ถูกต้องและรวดเร็วต้องอาศัยกระบวนการที่เป็นระบบและเครื่องมือที่ช่วยจัดระเบียบความคิด รวมถึงต้องมีความรู้ความเข้าใจเกี่ยวกับองค์ประกอบของดิจิทัลโซลูชันและความสามารถของเครื่องมือที่จะใช้พัฒนาโซลูชัน
ผู้เรียนจะฝึกใช้ Business Process Modeling, Gap Analysis และ Digital Building Blocks เพื่อแปลงความต้องการทางธุรกิจเป็นโซลูชันดิจิทัลที่ใช้งานได้จริง โดยเนื้อหาทักษะจะครอบคลุม 4 องค์ประกอบสำคัญดังนี้:
1. Business Process Modeling และ Gap Analysis คือ การวิเคราะห์กระบวนการทำงานอย่างเป็นระบบเพื่อระบุโอกาสในการปรับปรุงด้วยเทคโนโลยีดิจิทัล โดยใช้เครื่องมือ Swimlane Diagram เพื่อให้เห็นภาพชัดเจนของ Workflow และจุดที่ต้องปรับปรุง
1.1. As-is Process Mapping: วิเคราะห์กระบวนการปัจจุบันโดยใช้ Swimlane Diagram เพื่อทำความเข้าใจการทำงานที่เกิดขึ้นจริง (รูปที่ 1)
กำหนด Scope และผู้เกี่ยวข้อง (Players/Lanes): ระบุขอบเขตของกระบวนการ จุดเริ่มต้น-สิ้นสุด และแผนก/บุคคลที่เกี่ยวข้อง
ระบุกิจกรรมหลัก (Key Activities) และลำดับการทำงาน: ลิสต์งานทั้งหมดในกระบวนการและเรียงลำดับตามลำดับเวลา
เชื่อมโยงการไหลของงาน (Flow) และจุดส่งต่อ (Handoffs): วาดเส้นเชื่อมและให้ความสำคัญกับจุดที่งานข้ามระหว่างแผนก
ตรวจสอบความถูกต้อง: นำ Diagram ไปให้เจ้าของกระบวนการตรวจสอบและ Role-Play เพื่อหาข้อผิดพลาด
1.2 Process Improvement Discovery: การค้นหาและวิเคราะห์โอกาสในการปรับปรุงกระบวนการทำงาน เป็นขั้นตอนสำคัญหลังจากที่ผู้เรียนได้ทำการวิเคราะห์กระบวนการปัจจุบัน (As-is) แล้ว เพื่อหาจุดที่เป็นปัญหา (Pain Points) และโอกาสพัฒนา (Opportunities) อย่างเป็นระบบ โดยพิจารณาใน 3 มิติหลัก (รูปที่ 2) ดังนี้
People (บุคลากร)
Skills (ทักษะ): ตรวจสอบว่าบุคลากรมีทักษะเพียงพอต่อการปฏิบัติงานหรือไม่ เช่น ขาดความรู้ด้านการใช้เครื่องมือดิจิทัล, ต้องใช้เวลามากในการฝึกอบรม
Bottleneck (จุดคอขวด): หาช่วงที่งานติดขัดเพราะต้องรอการอนุมัติ, รอคนเพียงบางตำแหน่ง หรือใช้เวลามากเกินความจำเป็น
Handoffs (การส่งต่องาน): วิเคราะห์ว่าการส่งต่อข้อมูลหรือเอกสารระหว่างบุคคลหรือหน่วยงานทำให้เกิดความล่าช้าหรือข้อมูลสูญหายหรือไม่
Process (กระบวนการ)
Redundancy (ความซ้ำซ้อน): มีขั้นตอนที่ทำซ้ำโดยไม่จำเป็นหรือไม่ เช่น การบันทึกข้อมูลซ้ำในหลายระบบ
Delays (ความล่าช้า): ขั้นตอนใดใช้เวลานานกว่ามาตรฐาน หรือเกิดการรอคอยที่ไม่สร้างคุณค่า
Complexity (ความซับซ้อน): มีขั้นตอนที่ซับซ้อนเกินความจำเป็น ทำให้บุคลากรสับสนหรือเกิดข้อผิดพลาดง่าย
3. Technology (เทคโนโลยี)
Manual Work (งานที่ทำด้วยมือ): งานที่สามารถทำให้อัตโนมัติได้ แต่ยังคงทำด้วยคน เช่น การกรอกข้อมูลซ้ำ หรือการรวมไฟล์ด้วยตนเอง
Tools (เครื่องมือ): เครื่องมือปัจจุบันไม่เพียงพอหรือไม่มีการบูรณาการระหว่างระบบ ทำให้เกิดช่องว่างในการทำงาน
Data (ข้อมูล): ข้อมูลไม่ครบถ้วน, ไม่มีมาตรฐาน หรือไม่สามารถเข้าถึงได้ง่าย ทำให้การตัดสินใจล่าช้าหรือผิดพลาด

รูปที่ 1 ตัวอย่าง As-is Swimlane Diagram จากกระบวนการ Business Process Modeling

รูปที่ 2 Process Improvement Discovery Framework
2. Digital Solution Architecture และ Building Blocks คือ การออกแบบโครงสร้างของโซลูชันดิจิทัลโดยมองภาพรวมว่ามีองค์ประกอบ (Building Blocks) อะไรบ้างและแต่ละส่วนทำงานร่วมกันอย่างไร เพื่อให้ได้โซลูชันที่ตอบโจทย์ปัญหาและความต้องการของธุรกิจ ซึ่งในบริบทของ Microsoft Power Platform Building Blocks จะหมายถึงเครื่องมือและ Components ที่ใช้สร้าง Automation Solution, Data Solution และ AI Solution
2.1. Automation Solution: เชื่อมต่อระบบต่างๆ และทำงานซ้ำแทนคน ประกอบด้วยเครื่องมือดังนี้
Power Automate: แพลตฟอร์มสร้าง Workflow ที่ทำงานได้ 4 ประเภท
Instant (Manual): เริ่มทำงานเมื่อผู้ใช้กดปุ่ม เช่น ปุ่มใน Teams หรือ Power Apps
Scheduled (ตามเวลา): ทำงานตามกำหนดเวลา เช่น ส่งรายงานทุกวันเวลา 9:00 น.
Automated (ตาม Trigger): เริ่มทำงานอัตโนมัติเมื่อเกิดเหตุการณ์ เช่น มีอีเมลใหม่เข้ามา, มีไฟล์ถูกอัปโหลด
AI-Powered (ใช้ AI Builder): ใช้ AI วิเคราะห์ข้อมูลและตัดสินใจ เช่น อ่านเอกสาร PDF และดึงข้อมูลที่ต้องการไปใส่ในระบบ
Connectors: เชื่อมต่อกับระบบภายในและภายนอก (Standard/Premium/Custom Connectors)
Standard Connectors: เช่น Outlook, SharePoint, OneDrive
Premium Connectors: เช่น Salesforce, ServiceNow
Custom Connectors: ผู้พัฒนาสร้างขึ้นเองเพื่อเชื่อมต่อกับระบบเฉพาะขององค์กร
Use Cases ตัวอย่าง:
ส่งอีเมลแจ้งเตือนลูกค้าอัตโนมัติ
รีเฟรช Power BI Dataset ทุกวันโดยไม่ต้องทำเอง
จัดการเอกสาร เช่น เก็บไฟล์ PDF จากอีเมลลง SharePoint อัตโนมัติ
2.2. Data Solution: จัดการข้อมูลตั้งแต่รวบรวม แปลง จนถึงการแสดงผล ประกอบด้วยเครื่องมือดังนี้
Power Query: ใช้สำหรับ ETL (Extract, Transform, Load)
Extract: ดึงข้อมูลจากแหล่งต่างๆ เช่น Excel, SQL Database
Transform: ทำความสะอาด ปรับรูปแบบ และรวมข้อมูล
Load: นำข้อมูลไปใช้ใน Power BI หรือระบบอื่น
Power BI: ใช้สร้าง Interactive Dashboard และ Data Visualization
รองรับ Automatic Data Refresh เพื่อให้ข้อมูลทันสมัยอยู่เสมอ
สามารถเจาะลึกข้อมูล (Drill Down) และใช้ Filter เพื่อค้นหาข้อมูลเฉพาะจุด
Data Sources: แหล่งข้อมูลที่เชื่อมต่อได้
Excel, SharePoint Lists, Dataverse, Dynamics 365
Use Cases ตัวอย่าง
รวมข้อมูลยอดขายจากหลายสาขามาแสดงใน Dashboard เดียว
ทำความสะอาดข้อมูลลูกค้าก่อนนำไปใช้ใน AI Model
สร้างรายงาน KPI ที่อัปเดตอัตโนมัติทุกเช้า
2.3. AI Solution: ใช้ปัญญาประดิษฐ์ช่วยในการตัดสินใจและประมวลผลข้อมูล เพื่อเพิ่มความแม่นยำและความรวดเร็ว
Microsoft 365 Copilot Chat: AI Assistant ที่ช่วยสรุปข้อมูล ตอบคำถาม และสร้างเนื้อหา
AI Builder: ใช้ประมวลผลเอกสาร PDF, รูปภาพ, ข้อความ
Copilot Studio: สร้าง Custom AI Agent ที่ทำงานตามความต้องการเฉพาะขององค์กร
Integration:
ผสาน AI เข้ากับ Power Automate เพื่อให้ Workflow ตัดสินใจได้เองจากข้อมูล
เชื่อมกับ Microsoft Teams เพื่อให้พนักงานสื่อสารกับ AI ได้ง่าย
รวมกับระบบอื่นๆ เพื่อให้ AI ช่วยวิเคราะห์และส่งคำตอบอัตโนมัติ
Use Cases ตัวอย่าง
AI อ่านและบันทึกข้อมูลจากเอกสาร PDF เข้าระบบ ERP
สร้าง Chatbot ตอบคำถามลูกค้าโดยอัตโนมัติ
วิเคราะห์ข้อมูลลูกค้าและแนะนำโปรโมชั่นที่เหมาะสม
3. To-Be Process Design และ Solution Blueprint Development การพัฒนาโซลูชันดิจิทัลที่มีประสิทธิภาพไม่ได้หยุดแค่การวิเคราะห์สภาพปัจจุบัน (As-Is) แต่ต้อง ออกแบบสภาพที่ต้องการในอนาคต (To-Be) และสร้าง Solution Blueprint ที่เป็นภาพรวมของระบบและการทำงาน เพื่อเป็นคู่มือให้ทีมพัฒนานำไปสร้าง Proof-of-Concept หรือระบบจริงได้ถูกต้องและครบถ้วน
3.1. To-be Process Design: ออกแบบกระบวนการใหม่โดยเปลี่ยนมุมมองจากการแบ่งตามแผนกเป็นการแบ่งตามประเภทงาน เพื่อมองกระบวนการแบบ End-to-End และลดการทำงานซ้ำซ้อนระหว่างฝ่าย โดยองค์ประกอบหลักที่ต้องระบุใน To-Be Process Design ประกอบด้วย
Human Tasks (งานที่ทำโดยคน): รวมงานที่ต้องใช้การตัดสินใจ ความคิดสร้างสรรค์ หรือการติดต่อสื่อสารของคนจากทุกฝ่าย
Automation/Digital Solution (งานที่ระบบทำแทน): ระบุงานที่ระบบดิจิทัลจะทำแทน เช่น การส่งข้อมูล การคำนวณ การแจ้งเตือน
Legacy System (ระบบเดิม): ระบบเดิมที่ยังใช้งานอยู่และจุดที่ต้องเชื่อมต่อหรือดึงข้อมูล
Address Decision Points (จุดตัดสินใจ): ระบุเงื่อนไขที่ส่งผลต่อการไหลของงาน
3.2. Solution Blueprint: เพิ่มรายละเอียดบนแผนผัง To-Be Process Design จากการทดลองทำ สัมภาษณ์ผู้ปฏิบัติงานเพิ่มเติม และพิจารณา Data Schema หรือระบบ Legacy System ที่เกี่ยวข้อง เพื่อปรับปรุง Swimlane Diagram ให้มีรายละเอียดดังนี้
User Workflow: ขั้นตอนการทำงานของผู้ใช้แต่ละประเภท
อธิบายว่าผู้ใช้แต่ละประเภท (เช่น พนักงานปฏิบัติการ, ผู้จัดการ, ลูกค้า) ทำอะไรบ้างในแต่ละขั้นตอน
ใช้ Swimlane Diagram เพื่อแยกบทบาทของผู้ใช้ชัดเจน
Business Rules: กฎการทำงานของระบบตามเงื่อนไขและ Decision Points
ระบุเงื่อนไขที่ระบบต้องทำตาม เช่น การตรวจสอบสิทธิ์ผู้ใช้, การอนุมัติคำสั่งซื้อเมื่อครบจำนวนขั้นต่ำ
อ้างอิงจาก Decision Points ใน To-Be Process
System Components: ส่วนประกอบของระบบและการเชื่อมต่อระหว่าง Building Blocks
แสดงว่าแต่ละส่วนของระบบทำหน้าที่อะไร เช่น ฟอร์มรับข้อมูล, API Gateway, Data Storage
ระบุการเชื่อมต่อระหว่างส่วนต่างๆ และเครื่องมือ (Building Blocks) ที่ใช้ เช่น Power Automate, Power BI, AI Builder
Data Flow: การไหลของข้อมูลผ่านระบบและจุดเก็บข้อมูล
แสดงเส้นทางการไหลของข้อมูลจากต้นทางถึงปลายทาง เช่น จากฟอร์ม → ฐานข้อมูล → Dashboard
ระบุจุดเก็บข้อมูลชัดเจน (Data Storage Locations)
Integration Points: จุดเชื่อมต่อกับระบบเดิมและ API Requirements
ระบุ API Requirements
อธิบายว่าระบบจะเชื่อมกับ Legacy System อย่างไร เพื่อให้การทำงานเป็นแบบไร้รอยต่อ
Technology Stack: เครื่องมือและเทคโนโลยีที่ใช้ในแต่ละส่วน
ระบุเครื่องมือที่ใช้ในแต่ละส่วน เช่น Power Apps สำหรับ UI, Power Automate สำหรับ Workflow, Dataverse สำหรับ Data Storage
อธิบายเหตุผลที่เลือกเทคโนโลยีนั้น เช่น รองรับการขยายระบบ, ลดค่าใช้จ่าย, ใช้ง่ายต่อผู้ใช้ปลายทาง
4. Data Model, User Interface, Prototype Development (Optional) คือความรู้ความเข้าใจเรื่องการออกแบบรายละเอียดของดิจิทัลโซลูชัน เตรียมพร้อมสำหรับการพัฒนา Prototype ที่ใช้งานได้จริง
4.1. Data Model Design: ออกแบบโครงสร้างข้อมูลตาม Star Schema
องค์ประกอบสำคัญของ Star Schema
Dimension Tables: เก็บข้อมูลหลัก (Entities) เช่น Customer, Product, Employee พร้อม Unique ID
Fact Tables: เก็บข้อมูลเหตุการณ์ (Events) ที่เชื่อม Dimension Keys เข้าด้วยกัน
Structured vs Unstructured Data: แยกประเภทข้อมูลและวิธีการจัดเก็บที่เหมาะสม
4.2. User Interface Design: ออกแบบประสบการณ์ผู้ใช้ที่ใช้งานง่าย
Data Collection Interface:
ใช้ Microsoft Forms (Simple) หมาะสำหรับการเก็บข้อมูลง่ายๆ เช่น แบบสอบถาม, แบบฟอร์มแจ้งปัญหา
Power Apps (Complex Integration) เหมาะสำหรับการทำงานที่ซับซ้อน มีการเชื่อมต่อระบบหลายแหล่ง เช่น การสร้างแอปจัดการคำสั่งซื้อที่เชื่อมกับฐานข้อมูล
Design Principles:
Single-column layout: จัดข้อมูลในคอลัมน์เดียวเพื่อให้ผู้ใช้เลื่อนดูง่าย
Logical flow: ลำดับขั้นตอนการกรอกข้อมูลมีความต่อเนื่องและเข้าใจง่าย
Clear labels: ใช้คำอธิบายชัดเจนและสั้น
Appropriate validation: ใส่เงื่อนไขตรวจสอบข้อมูล เช่น ห้ามเว้นว่าง, ต้องกรอกอีเมลให้ถูกต้อง
Dashboard Design:
ใช้ Power BI หรือ Excel เพื่อสร้าง Interactive Visualization
ใส่ Filter, Drill Down และ Highlight เพื่อให้ผู้ใช้สำรวจข้อมูลได้ด้วยตนเอง
ใช้สีและการจัดวางที่ช่วยให้เข้าใจข้อมูลได้เร็ว
4.3. Prototype Development: สร้างต้นแบบที่ทำงานได้จริง
ใช้ No-Code Tools เพื่อพัฒนาอย่างรวดเร็ว
เช่น Power Apps, Power Automate, Power BI เพื่อพัฒนาได้เร็วและแก้ไขได้ง่าย
ทดสอบ User Journey และ Business Logic
ตรวจสอบว่ากระบวนการทำงานเป็นไปตามที่ออกแบบไว้หรือไม่
ทดสอบว่าเงื่อนไข (Business Rules) ทำงานถูกต้อง เช่น การอนุมัติ, การส่งข้อมูล
ยังไม่ต้องกังวลเรื่อง Security, Performance, Edge Cases ในขั้น Proof-of-Concept"
</method component>

<output>
{
"concisability_result": "true",
"concisability_explanation": "The text is short, concise, and not redundant. It clearly summarizes the main workflow (As‑is → To‑be → Blueprint → Select Building Blocks) — Suggestion: Add short phrases to specify learner activities, such as 'practice analyzing As‑is, identify Pain points, and create Prototype' to highlight practical learning outcomes.",
"coverage_result": "false",
"coverage_explanation": "The content is condensed to the point of missing key components from the method component, such as Process Improvement Discovery (People/Process/Technology), details of the Solution Blueprint (Data Flow, Integration Points, Technology Stack), and parts of the Data Model/UI/Prototype — Suggestion: Add short sentences listing these missing parts to provide learners with a complete picture of the practical steps.",
"format_criteria_result": "true",
"format_criteria_explanation": "The format meets the criteria, starting with 'Learner' (target learner) followed by action verbs (transform, develop, analyze, design, select) making it a well-structured summary paragraph."
}
</output>

### Additional Requirements
- All suggestions must directly solve the issue described in your analysis.
- Suggested versions must be **concise**, **specific**, and **aligned with the user’s intent**.
</instruction>

**Please assess the provided <key method> content below following the <instruction> described above**

<key method>
{{key_method}}
</key method>
"""
EVAL_KEY_METHOD_OUTPUT = {
  "title": "evaluate_key_method",
  "description": "Assess a summarized key method against dimensions (Concisability, Coverage, Format Criteria) and provide boolean results with brief explanations.",
  "type": "object",
  "properties": {
    "concisability_result": {
      "type": "boolean",
      "description": "Result for Concisability dimension: 'true' if the key method is clearly and concisely described without redundancy and includes essential information; otherwise 'false'."
    },
    "concisability_explanation": {
      "type": "string",
      "description": "A short explanation (one or two sentences) justifying the concisability_result."
    },
    "coverage_result": {
      "type": "boolean",
      "description": "Result for Coverage dimension: 'true' if the key method covers all method component elements and preserves necessary procedural detail for learner understanding; otherwise 'false'."
    },
    "coverage_explanation": {
      "type": "string",
      "description": "A short explanation (one or two sentences) justifying the coverage_result."
    },
    "format_criteria_result": {
      "type": "boolean",
      "description": "Result for Format Criteria: 'true' if the summary is structured as a paragraph that begins with the target learner and uses action verbs to describe method/procedures; otherwise 'false'."
    },
    "format_criteria_explanation": {
      "type": "string",
      "description": "A short explanation (one or two sentences) justifying the format_criteria_result."
    }
  },
  "required": [
    "concisability_result",
    "concisability_explanation",
    "coverage_result",
    "coverage_explanation",
    "format_criteria_result",
    "format_criteria_explanation"
  ],
  "additionalProperties": False,
  "strict": False
}
EVAL_KEY_METHOD_WEIGHT = {
    "concisability_result": 1,
    "coverage_result": 1,
    "format_criteria_result": 1,
}

EVAL_DESCRIPTION_PROMPT = """
<instruction>
**Your Goal**: Evaluate the <description> which describing the overall of the micro-credential, included with the content, objective, what will you earn at the end of the course in paragraph. You must assess quality of <description> and provide targeted refinement suggestions using the following dimensions with micro-credential's <competency> and <key method> context provided below

<competency>
{{competency}}
<competency>

<key_method>
{{key_method}}
<key method>

---
## DIMENSIONS
1. **Concisability**
evaluate whether the <description> is clearly and concisely described, avoiding redundancy and ensuring that all essential information is included in a well-summarized form.
   - Output **true** if the description is succinct, free of unnecessary repetition, and includes all critical information in a clear and concise manner.
   - Output **false** if the description is verbose, contains redundant information, or omits essential details.
2. **Coverage**  
evaluate whether the <description> cover all necessary content included with <competency> and <key method>. learner should understand what to achieve and overview of how to achieve the competency
   - Output **true** if the description comprehensively covers all aspects of the competency and key method, providing a clear understanding of objectives and methods.
   - Output **false** if the description lacks important content, leaving gaps in understanding the competency or key method.
3. **Attractive**
evaluate that the description employs an engaging and motivating tone that captures the reader’s attention, encourages further exploration, and inspires interest in learning the micro-credential.
   - Output **true** if the description is written in an engaging, motivating tone that captivates the reader and stimulates interest.
   - Output **false** if the description is dull, unengaging, or fails to inspire interest in the micro-credential.
4. **Format Criteria**  
Evaluate the information that is structured as a summarized paragraph. The content should implicitly summarized from <introduction> + <competency> + <key method>
   - Output **true** if the format of the information is similar to the defined format.  
   - Output **false** if the format is vague, unfocused, too long, or lacks a clear structure.
---

## YOUR TASKS
### **Analyze the User Input**
For each dimension:
- Evaluate whether it meets the dimension's requirements.  
- Return only **true/false** ('<dimension's result>').  
- Provide a short explanation of your reasoning ('<dimension's explanation>').
---

## OUTPUT FORMAT
Respond strictly in this JSON structure:
{
    "concisability_result": <dimension's result>,
    "concisability_explanation": <dimension's explanation>,
    "coverage_result": <dimension's result>,
    "coverage_explanation": <dimension's explanation>,
    "attractive_result": <dimension's result>,
    "attractive_explanation": <dimension's explanation>,
    "format_criteria_result": <dimension's result>,
    "format_criteria_explanation": <dimension's explanation>,
}
---

## EXAMPLE
### *example 1*
<description>
"ในยุคของ Digital Transformation ที่องค์กรต้องการนำระบบดิจิทัลมาใช้แทนกระบวนการทำงานแบบดั้งเดิม ผู้เรียนจะได้พัฒนาทักษะการออกแบบโซลูชันดิจิทัลที่ตอบโจทย์ธุรกิจอย่างเป็นระบบ ตั้งแต่การวิเคราะห์กระบวนการทำงานปัจจุบัน (As-is Process Mapping) การระบุช่องว่างและโอกาสในการปรับปรุง (Gap Analysis) ไปจนถึงการออกแบบ Solution Blueprint ที่สามารถสื่อสาร To-be Process Mapping ทั้งในส่วนของ workflow, data model และ solution components หลักสูตรนี้ใช้ Solution Components จาก Microsoft Power Platform เป็นเครื่องมือเพื่อสร้าง  Automation Solution, Data Solution และ AI Solution แบบ Low-Code/No-Code ผู้เรียนสามารถนำ Solution Blueprint ไปพัฒนาเป็น Prototype ได้จริง เพื่อทดสอบและนำไปใช้จริงในองค์กรต่อไป"
</description>

<competency>
"ผู้เรียนสามารถแปลงกระบวนการทำงานปัจจุบันเป็นโซลูชันดิจิทัล โดยนำเสนอเป็น Solution Blueprint และ/หรือ Digital Prototype ด้วยเครื่องมือ Microsoft Power Platform"
<competency>

<key method>
"ผู้เรียนแปลงกระบวนการทำงานปัจจุบันเป็นโซลูชันดิจิทัล โดยพัฒนา Solution Blueprint ที่ใช้ Business Process Modeling เพื่อวิเคราะห์กระบวนการปัจจุบัน (As-is) และออกแบบกระบวนการใหม่ (To-be) ด้วย Swimlane Diagram จากนั้นเลือกใช้ Digital Building Blocks จาก Microsoft Power Platform เพื่อประกอบเป็น Solution Blueprint ครอบคลุม Automation Solution, Data Solution และ AI Solution เพื่อตอบสนองความต้องการทางธุรกิจ "
<key method>

<output>
{
    "concisability_result": "true",
    "concisability_explanation": "The explanation is concise and not overly redundant. The main points (As-is analysis, Gap Analysis, To-be design, use of Power Platform, development of Prototype) are covered. However, the first sentence is long and could be shortened for brevity. A concise starting example: 'This course teaches digital solution design using Microsoft Power Platform, from As-is analysis to creating a ready-to-use Prototype.'",
    "coverage_result": "false",
    "coverage_explanation": "Lacks technical references found in key methods, such as the use of Business Process Modeling and Swimlane Diagram, and the need to select Digital Building Blocks from Microsoft Power Platform to form a Solution Blueprint. Suggestion: Add a short sentence like 'The course uses Business Process Modeling (including Swimlane Diagram) to analyze As-is and design To-be, and selects Digital Building Blocks from Microsoft Power Platform to cover Automation, Data, and AI.'",
    "attractive_result": "false",
    "attractive_explanation": "The tone is technically informative but somewhat formal and not engaging. It should highlight tangible benefits and target audience, such as 'Learners will be able to create a Solution Blueprint that transforms into a practical Prototype, reducing manual work and increasing organizational efficiency,' to make the text more appealing.",
    "format_criteria_result": "true",
    "format_criteria_explanation": "Organized as a single paragraph summarizing the introduction, purpose, and method (introduction + competency + key method) clearly. The format meets the criteria but should include short sentences as suggested in coverage and attractive sections while maintaining a single-paragraph format."
}
</output>

### Additional Requirements
- All suggestions must directly solve the issue described in your analysis.  
- Suggested versions must be **concise**, **specific**, and **aligned with the user’s intent**.  
</instruction>

**Please assess the provided <description> content below following the <instruction> described above**

<description>
{{description}}
</description>
"""
EVAL_DESCRIPTION_OUTPUT = {
  "title": "evaluate_description",
  "description": "Assess a micro-credential description against dimensions (Concisability, Coverage, Attractive, Format Criteria) given the competency and key method context; return true/false for each dimension plus a short explanation.",
  "type": "object",
  "properties": {
    "concisability_result": {
      "type": "boolean",
      "description": "Result for Concisability dimension: 'true' if the description is succinct, non-redundant, and includes essential information; 'false' otherwise."
    },
    "concisability_explanation": {
      "type": "string",
      "description": "Short explanation supporting the concisability_result, noting what is concise or what is verbose/redundant and suggestions to improve brevity."
    },
    "coverage_result": {
      "type": "boolean",
      "description": "Result for Coverage dimension: 'true' if the description covers competency and key method comprehensively; 'false' if it omits important content or leaves gaps."
    },
    "coverage_explanation": {
      "type": "string",
      "description": "Short explanation supporting the coverage_result, identifying missing elements or confirming coverage and giving targeted suggestions to fill gaps."
    },
    "attractive_result": {
      "type": "boolean",
      "description": "Result for Attractive dimension: 'true' if the description uses an engaging, motivating tone that inspires interest; 'false' if it is dull or unengaging."
    },
    "attractive_explanation": {
      "type": "string",
      "description": "Short explanation supporting the attractive_result, describing tone issues or strengths and providing concise recommendations to make the description more compelling."
    },
    "format_criteria_result": {
      "type": "boolean",
      "description": "Result for Format Criteria dimension: 'true' if the content is structured as a summarized paragraph implicitly combining introduction, competency, and key method; 'false' otherwise."
    },
    "format_criteria_explanation": {
      "type": "string",
      "description": "Short explanation supporting the format_criteria_result, indicating whether the paragraph format is met and what to change to align with the required format."
    }
  },
  "required": [
    "concisability_result",
    "concisability_explanation",
    "coverage_result",
    "coverage_explanation",
    "attractive_result",
    "attractive_explanation",
    "format_criteria_result",
    "format_criteria_explanation"
  ],
  "additionalProperties": False,
  "strict": False
}
EVAL_DESCRIPTION_WEIGHT = {
    "concisability_result":1,
    "coverage_result":1,
    "attractive_result":1,
    "format_criteria_result":1
}