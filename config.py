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

EVAL_LEARNER_BG_PROMPT = "agent-spark-eval-learner_background"
EVAL_KNOWLEDGE_DOMAIN_PROMPT = "agent-spark-eval-knowledge_domain"

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

EVAL_OVERVIEW_ASSE_PROMPT = "agent-spark-eval-overview_assessment"
EVAL_ARTIFACT_ASSE_PROMPT = "agent-spark-eval-artifact_assessment"
EVAL_REFLECTION_ASSE_PROMPT = "agent-spark-eval-reflection_assessment"

EVAL_METHOD_COMP_PROMPT = "agent-spark-eval-mrthod_component"
EVAL_KEY_METHOD_PROMPT = "agent-spark-eval-key_method"
EVAL_DESCRIPTION_PROMPT = "agent-spark-eval-description"