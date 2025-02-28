import google.generativeai as genai
import os
import time
import re

def natural_sort_key(filename):
    """Extract numeric part of filename for proper sorting (page_1, page_2, ..., page_10)"""
    numbers = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else filename

def process_files_with_gemini(api_key, folder_path, output_file, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    files.sort(key=natural_sort_key)  # Sort properly (page_1, page_2, ..., page_10)

    with open(output_file, "w", encoding="utf-8") as out_file:
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing {file_name}...")

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    file_content = file.read()

                response = model.generate_content([prompt, file_content])

                out_file.write(response.text + "\n\n")
                print(f"✔ {file_name} processed successfully.\n")

                time.sleep(30)  # Sleep for 30 seconds to prevent rate limits

            except Exception as e:
                print(f"❌ Error processing {file_name}: {e}")

    print(f"✅ All pages processed. Output saved to {output_file}")

# Example usage
if __name__ == "__main__":
    api_key = "AIzaSyBTh1RmO86Gr7IY79WN3CeU8VXWegYVK7A"
    folder_path = "Page_wise_data"  # Folder containing text files
    output_file = "output.txt"  # Output file
    prompt = """You are an information extraction system. You will be given text from PDF documents such as concall transcripts and annual reports. Your goal is to build an intelligent and detailed knowledge graph for an investor to analyze the overall story outlined in these texts. The knowledge graph will be represented as a Python list of 5-element tuples, each of the form:

[
  ('h', 'type', 'r', 'o', 'type'), 
  ...
]

where:

'h' is the simplified subject entity (fewer than four words),
'type' is the subject entity's type (for example 'COMP', 'SECTOR', 'FIN_INSTRUMENT', 'RAW_MATERIAL', 'CAPEX', 'MANAGEMENT', etc.),
'r' is the relationship verb (must be taken from a set of common verbs like 'Introduce', 'Operate_In', 'Invest_In', 'Positive_Impact_On', 'Acquired', etc.),
'o' is the simplified object entity (fewer than four words),
'type' is the object entity's type.

Important Instructions

1. Entity Disambiguation and Consistency
If the text uses different names or acronyms for the same entity (e.g., "UK Central Bank", "BOE", "Bank of England"), unify them into one consistent name (e.g., "Bank of England").
Do this for management references, CAPEX references, raw materials, etc., so that the same underlying concept has a single name.
Apply this to date formats, percentages, financial metrics, and timeframes as well (e.g., "Rs. 18 crore" → "INR 18 Cr").

2. Simplify Entities
Each entity (in both 'h' and 'o') must be fewer than four words.
For example, "Board of Directors" or "Management Team" could be unified as "Management" if appropriate.

3. Additional Node Properties
Although your final output must be strictly the 5-element tuples, each entity should be imagined as a node with enriched properties in a Neo4j knowledge graph, including:

name: Standardized entity name (e.g., "GHCL Textiles")
type: Entity type (e.g., 'COMP', 'PRODUCT', 'SECTOR', etc.)
source_chunk: Reference to the relevant "master chunk" of the PDF where the entity appears
metadata: Any additional relevant information (e.g., date, percentage, timeframe, financial metrics, etc.)
These properties should not appear in the output directly, but should inform how entities and relationships are structured in the tuples.

4. Output Format
Only output the Python list of tuples.
No additional text, commentary, or JSON structure is allowed—just a Python list of the form:
python
Copy
Edit
[
  ('Entity1', 'Entity1Type', 'Relationship', 'Entity2', 'Entity2Type'),
  ...
]
Each element in each tuple must be a string.
Maintain a consistent and precise output format.

5. Relationships
Use relationship verbs relevant to the scenario, including:
'Invest_In' (for CAPEX or expansions)
'Operate_In' (for sectors or regions)
'Acquire' (for acquisitions)
'Manage' (for management connections)
'Positive_Impact_On' (for stock or performance outcomes)
'Negative_Impact_On'
'Produce' (for raw materials or products)
'Report' (for metrics and performance)
'Face' (for risks and challenges)
'Target' (for goals and financial projections)
'Generate' (for financial outcomes)
'Role' (for management roles)
'Complete_By' (for project timelines)
'Increase_From' and 'Increase_To' (for metrics with percentage growth)


6. Examples
Example Input:
"Apple Inc. is set to introduce the new iPhone 14 in the technology sector this month. The product's release is likely to positively impact Apple's stock value."

Expected Output:

python
Copy
Edit
[
  ('Apple Inc.', 'COMP', 'Introduce', 'iPhone 14', 'PRODUCT'),
  ('Apple Inc.', 'COMP', 'Operate_In', 'Technology Sector', 'SECTOR'),
  ('iPhone 14', 'PRODUCT', 'Positive_Impact_On', "Apple's Stock Value", 'FIN_INSTRUMENT')
]
Enriched Node Details (Conceptual Only):

For 'Apple Inc.':

name: "Apple Inc."
type: 'COMP'
source_chunk: "Paragraph 3, Page 5"
metadata: {}
For 'iPhone 14':

name: "iPhone 14"
type: 'PRODUCT'
source_chunk: "Paragraph 4, Page 5"
metadata: {"launch_date": "This month"}

7. Your Task
Read the provided PDF text (or textual input).
Identify important entities (including CAPEX, management, raw materials, etc.), unify references, and condense them to fewer than four words if necessary.
Enrich each entity internally with additional metadata, but only present the simplified output.
Link these entities with appropriate relationship verbs.
Produce only a Python list of tuples of the form:
python
Copy
Edit
[
  ('h', 'type', 'r', 'o', 'type'),
  ...
]
No extra commentary or explanation—just that list as your output."""  # Keep your original prompt

    process_files_with_gemini(api_key, folder_path, output_file, prompt)
