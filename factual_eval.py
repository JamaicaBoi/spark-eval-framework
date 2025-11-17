from dotenv import load_dotenv
from langsmith import Client
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable
import os, json, datetime

from config import CLAIMS_EXTRACTION_PROMPT, CLAIMS_VERIFICATION_PROMPT

load_dotenv()
client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))

def claims_extraction(method_comp:str,ref:str, model:Runnable) -> list:
    extraction_prompt = client.pull_prompt(CLAIMS_EXTRACTION_PROMPT)
    extraction_chain = extraction_prompt | model
    response = extraction_chain.invoke({"method component": method_comp, "reference":ref})
    return response["claims"]

def reference_grouping(extraction_claims:list) -> dict:
    grouped = {}
    for claim in extraction_claims:
        src = claim["source"]
        if src not in grouped:
            grouped[src] = []
        grouped[src].append(claim)
    return grouped

def claims_verification(ref_content:str, claims:list, model:Runnable) -> list:
    verification_prompt = client.pull_prompt(CLAIMS_VERIFICATION_PROMPT)
    verification_chain = verification_prompt | model
    response = verification_chain.invoke({"ref content": ref_content, "claims":claims})
    return response['verifications']

def reference_context_retreival(src:str) -> str:
    return """
Graphs and Charts
Swimlane Diagram: Ultimate Guide to Designing Better Business Processes

Swimlane Diagram: Ultimate Guide to Designing Better Business Processes
Written By

Letícia Fonseca
Updated: Oct 29, 2024
swimlane diagram
A swimlane diagram is a visual representation of a process and its multiple facets.

For businesses, swimlane diagrams are helpful in process mapping and project management.

This guide will provide you with an in-depth view of swimlane diagrams and how they can communicate and enhance business processes.

You will also learn how to create your own swimlane diagram for various projects with the help of Venngage’s Swimlane Diagram Maker and flowchart diagram templates.

START CREATING FOR FREE
 
Click to jump ahead:

What are swimlane diagrams?
What are swimlane diagram symbols?
3 types of swimlane diagrams
5 steps to make a swimlane diagram
Swimlane diagram best practices
FAQs about swimlane diagrams
What are swimlane diagrams?
Swimlane diagrams or process flow diagrams are types of flowcharts that divide the steps of a process into ‘swimlanes’ or categories, hence its name.

These categories represent the groups or individuals that perform each step in the process.

As you can see in this swimlane diagram example, the steps in an order processing flow are categorized into four aspects or departments:

swimlane diagram
Because it shows how a process extends to multiple business units or departments with different functions, a swimlane diagram is also called a cross-functional diagram.

Unlike a simple flowchart, a swimlane flowchart depicts who is in charge of each process step. Swimlanes can be arranged horizontally or vertically.

What are the benefits of using a swimlane diagram?
Swimlane diagrams have many uses and benefits. These include:

Highlighting the process steps and responsibilities that are assigned to an employee or department
Providing a better structure for business processes in order to clarify and organize workflows
Standardizing and streamlining a process flow to improve performance and prevent inefficiencies
Promoting clear communication between teams and better analysis of the phases of a project or business process
In a business setting, swimlane diagrams can be used for project management, onboarding a new employee, illustrating internal workflows, and documenting business processes.

Swimlanes are also used in unified modeling language (UML), which is the modeling and diagramming language used for software design.

What are swimlane diagram symbols?
Swimlane diagrams make use of various shapes and symbols to convey the different components of a process. These are:

Start or endpoints: These are rectangle shapes with rounded corners used to indicate that a step is the start or end of the process flow
Activity shapes: Which are rectangles that represent an action or task
Lines or arrows: Are used to connect the process steps and portray the correct sequence of the process flow
Decision shapes: Which are diamond shapes that symbolize a question or decision that needs to be answered with a yes or no
Input or output symbols: Which are parallelograms that signal data coming in and out of the process flow
Document symbols: Which are rectangles with wavy lines at the bottom side which signify any document that is needed to complete a process step
Connector symbols: These are small circles that denote that another flowchart is connected to the current diagram
Swimlane Workflow Diagram
EDIT THIS SWIMLANE DIAGRAM
 
3 types of swimlane diagrams
Here are the three types of swimlane diagrams that you can use depending on the project or process requirement.

Swimlane activity diagram
A swimlane activity diagram details the coordination of tasks or activities in a process. This type of swimlane diagram is used to create and systematize workflows.

Swimlane activity diagrams are designed for processes with a straightforward flow that does not create branches or multiple outcomes.

For example, this swimlane activity diagram describes the activities involved in a engineering process flow:

Swimlane Activity Diagram
EDIT THIS SWIMLANE DIAGRAM
 
Swimlane process map
As the name suggests, this type of swimlane diagram is made for process mapping. Swimlane process maps are used for planning, documenting, and modeling processes.

Unlike swimlane activity diagrams, a swimlane process map illustrates potential scenarios in a process that can result in more than one outcome.

Here is an example of a swimlane process map that shows how an order request process works:

Business Planning Swimlane Diagram Template for PowerPoint
EDIT THIS SWIMLANE DIAGRAM
 
Related: 10+ Swimlane Diagram Templates and How to Create Them

Cross-functional flowchart
There are three types of cross-functional flowcharts for business use. They are:

Deployment flowchart
A deployment flowchart is the most common and basic type of cross-functional flowchart that organizes a process from start to finish.

In a deployment flowchart, the process steps are arranged in a logical sequence and distributed to the different departments that they cover. It can have as many lanes as needed. This is a great example:

Flowchart with Swim Lanes Template
EDIT THIS SWIMLANE DIAGRAM
 
Opportunity flowchart
On the other hand, an opportunity flowchart groups the process steps into activities that produce value, and activities that don’t. This means it has only two swimlanes, which are ‘value-added’ and ‘non-value-added.’

Opportunity flowcharts are especially useful in business analysis as they can help determine which parts of a business process will result in profit or loss.

Here is an opportunity flowchart that shows the step-by-step of the product order process:

Ordering Swimlane Process Flow Diagram
EDIT THIS SWIMLANE DIAGRAM
 
Matrix flowchart
Lastly, a matrix flowchart is a complex flowchart designed for complex processes.

It consists of process steps with sub-processes that are aligned into more than one swimlane, which means it doesn’t follow any clear rows or columns.

Matrix flowcharts are much harder to understand and are mostly used in programming, in here we have a customer service example:

Customer Service Swimlane Chart Template
EDIT THIS SWIMLANE DIAGRAM
 
5 steps to make a swimlane diagram
Creating a clear and well-developed swimlane diagram involves following a series of steps and helpful guidelines. Here are the steps you can easily follow:

Step 1: Outline the process
Before you start drawing your diagram, you need to define the process and all its components first. This means writing down the title or name of the process, the objectives behind it or why you are creating a diagram in the first place, the complete process steps, and its performers.

Step 2: Plot the starting point
Once you have everything prepared, proceed with drafting your swimlane diagram. On a separate sheet of paper, start by plotting the first step in the process on the left side of the page. Draw a rounded rectangle around it to mark it as the starting point.

Step 3: Divide the page into swimlanes
Now, draw vertical or horizontal lines across the page to create your swimlanes then list before them the involved departments or individuals according to the order of the process steps. They should be at the top of the page for a vertical swimlane or on the left side for a horizontal one. Your starting point should now be aligned on the correct swimlane or the department in charge of it.

Step 4: Chart the steps
Next, starting from the left side of the page to the right, write the rest of the process steps and align them on their respective swimlanes. Draw the correct shapes or symbols around them to ensure that each part in the process flow is conveyed properly. Then, connect the process steps using lines or arrows to show the correct sequence. Once you have completed all the steps, mark the last step as the end of the process flow.

Step 5: Use a powerful swimlane diagram maker
To finalize your swimlane diagram, choose a diagramming tool that can not only turn your design vision into a reality but can also help you produce an impressive diagram. Venngage’s Swimlane Diagram Maker is an intuitive design tool that allows you to create a swimlane diagram for free, in just a few easy clicks.

swimlane diagram
With Venngage, you don’t need to be an artist or designer to be able to create professional swimlane diagrams. Aside from its easy-to-use editor and drag-and-drop interface, Venngage has customizable templates that you can edit to achieve the design and impact you want for your swimlane diagram.

We also invite you to upgrade to a Venngage business account to access My Brand Kit, which lets you add your company’s logo, color palette, and fonts to all your designs with a single click.


A business account also includes the real-time collaboration feature, so you can invite members of your team to work simultaneously on a project.

Swimlane diagram best practices
Here are some things to keep in mind when creating a swimlane diagram:

Keep the diagram small and focused as much as possible. Include only the specific departments or individuals that are actually part of the process and use not more than twelve swimlanes.
Be direct and concise when writing the steps. Stick to phrases and sentence fragments and if you shall use technical terminology, add notes under the document to define them.
When connecting steps in the same swimlane, the steps should be listed sequentially (top to bottom) and should still be connected using lines or arrows.
Make use of colors for better distinction between the departments or individuals and to make your diagram easier to understand. Add supplementary icons and graphics but keep them to a minimum.
Don’t forget to analyze your swimlane diagram to identify possible gaps, redundancies, and bottlenecks in the process.
Getting Things Done Flowchart
EDIT THIS SWIMLANE DIAGRAM
 
FAQs about swimlane diagrams
How do you make a swimlane diagram in Venngage?
To create a swimlane diagram using Venngage’s Swimlane Diagram Maker, simply follow these steps:

Step 1: Sign up for a new account to start using Venngage’s Swimlane Diagram Maker for free
Step 2: Choose a swimlane diagram template from Venngage’s massive collection of diagrams and flowchart templates
Step 3: Customize the template of your choice by adding or changing the shapes, colors, and labels to reflect the process steps and flow
Step 4: Enhance your design using icons, backgrounds, and graphics from our library
Step 5: Download your finished swimlane diagram or share it online
Why are swimlanes used in activity diagrams?
Activity diagrams are a type of flowchart that shows the flow of activities in a system. In an activity diagram, swimlanes are used to illustrate which activities are carried out by a certain group or individual and describe the logical order of events.

When should you create a swimlane diagram?
Swimlane diagrams are usually created when demonstrating complex processes and delegating the tasks needed to complete them. They are used during business planning for projects or business processes that involve different departments or business units.

Use swimlane diagrams to design, communicate, and improve business processes
Swimlane diagrams can effectively represent and translate a business process into actionable steps.

Use Venngage’s Swimlane Diagram Maker to create a swimlane diagram.

START CREATING FOR FREE
 

About Letícia Fonseca
Letícia Fonseca was a content marketing specialist at Venngage, with expertise in business processes, diagram creation, and content marketing strategies. She provides valuable insights that empower marketers and business professionals to streamline operations and enhance their marketing efforts. Through her deep understanding of both content creation and business strategy, Letícia helps brands communicate more effectively and achieve their goals.

Related Posts
How AI Simplifies Data Visualization for Business Reports
14 Best Pitch Deck Software for Startups & Entrepreneurs
How to Use Process Flowcharts to Improve Business Efficiency
HR Data Visualization: Turning Data into Powerful Stories
How To Use Infographics to Streamline Business Processes
Discover popular designs
"""

def calculate_score(claims:list) -> tuple[float,float]:
    count_with_source = sum(1 for item in claims if item["source"] != '')
    count_support = sum(1 for item in claims if item["support"] == "yes")
    count_claims = len(claims)
    try:
        groundness_score = count_with_source/count_claims
    except:
        groundness_score = 0
    try:
        faithfulness_score = count_support/count_with_source
    except:
        faithfulness_score = 0
        
    return groundness_score, faithfulness_score

def factual_eval_pipeline(method_comp:str,ref:str, model:Runnable) -> tuple[float,float]:
    claims = claims_extraction(method_comp,ref,model)
    source_grouped_claims = reference_grouping(claims)
    for source in source_grouped_claims.keys():
        ref_content = reference_context_retreival(source)
        verified_claims = claims_verification(ref_content,source_grouped_claims[source],model)
        for verified_claim in verified_claims:
            item = next((x for x in claims if x["id"] == verified_claim["id"]), None)
            if item:
                item["support"] = verified_claim["result"]

    print(claims)
    g_score, f_score = calculate_score(claims)

    result = {}
    result["claims"] = claims
    result["score"] = {
        "groundness_score" : g_score,
        "faithfulness_score": f_score
    }
    result["method_component"] = method_comp
    result["eval_model"] = model.get_name()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("Saved to:", filename)
    return g_score, f_score
