import google.generativeai as genai
import fitz  # PyMuPDF
import time

# Function to extract text from PDF and process it page by page with LLM
def process_pdf_with_gemini(api_key, pdf_path, output_file, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    doc = fitz.open(pdf_path)
    with open(output_file, "w", encoding="utf-8") as out_file:
        for page_num in range(len(doc)):
            page_text = doc[page_num].get_text("text")
            print(f"Processing page {page_num + 1}...")

            try:
                response = model.generate_content([prompt, page_text])
                out_file.write(response.text + "\n\n")
                print(f"✔ Page {page_num + 1} processed successfully.\n")

                time.sleep(30)  # Sleep for 30 seconds to prevent rate limits

            except Exception as e:
                print(f"❌ Error processing page {page_num + 1}: {e}")

    print(f"✅ All pages processed. Output saved to {output_file}")


# Example usage
if __name__ == "__main__":
    api_key = "AIzaSyBTh1RmO86Gr7IY79WN3CeU8VXWegYVK7A"
    pdf_path = "Concall_PDF/Concall GHCL Textiles Nov 2024.pdf"
    output_file = "output.txt"
    prompt = """You are an information extraction system. You will be given text from PDF documents such as concall transcripts and annual reports. Your goal is to build an intelligent knowledge graph for an investor to analyze the overall story outlined in these texts. The knowledge graph will be represented as a Python list of 6-element tuples, each of the form:

python
Copy
Edit
[
  ('h', 'type', 'r', 'o', 'type', 'source'), 
  ...
]
where:

'h' is the simplified subject entity (fewer than four words).
'type' is the subject entity's type (e.g., 'COMP', 'SECTOR', 'FIN_INSTRUMENT', 'RAW_MATERIAL', 'CAPEX', 'MANAGEMENT', etc.).
'r' is the relationship verb (must be taken from a set of common verbs like 'Introduce', 'Operate_In', 'Invest_In', 'Positive_Impact_On', 'Acquired', etc.).
'o' is the simplified object entity (fewer than four words).
'type' is the object entity's type.
'source' is the reference to the original PDF chunk, typically in the format of the file name or page (e.g., 'page_3.txt').
#### Important Instructions:
Entity Disambiguation:

If the text uses different names or acronyms for the same entity (e.g., "UK Central Bank", "BOE", "Bank of England"), unify them into one consistent name (e.g., "Bank of England").
Do this for management references, CAPEX references, raw materials, etc., so that the same underlying concept has a single name.
Simplify Entities:

Each entity (in both 'h' and 'o') must be fewer than four words.
For example, "Board of Directors" or "Management Team" could be unified simply as "Management" if appropriate.
Node Properties and Master Chunk References:

The final output must strictly follow the 6-element tuple format.
The last element 'source' should explicitly include the name of the PDF chunk (e.g., file name or page) that the information was extracted from.
This provides direct traceability, allowing each node to be linked back to its original source.
Output Format:

Only output the Python list of tuples.
No additional text, commentary, or JSON structure is allowed—just a Python list of the form:
python
Copy
Edit
[
  ('Entity1', 'Entity1Type', 'Relationship', 'Entity2', 'Entity2Type', 'source'),
  ...
]
Each element in each tuple must be a string.
Relationships:

Use relationship verbs relevant to the scenario, e.g.,
"Invest_In" (for CAPEX or expansions),
"Operate_In" (for sectors or regions),
"Acquire" (for acquisitions),
"Manage" (for management connections),
"Positive_Impact_On" (for stock or performance outcomes),
"Negative_Impact_On",
"Produce" (for raw materials or products),
etc.
Examples:

If the text says:
"Apple Inc. is set to introduce the new iPhone 14 in the technology sector this month. The product's release is likely to positively impact Apple's stock value."

The correct output is:

python
Copy
Edit
[
  ('Apple Inc.', 'COMP', 'Introduce', 'iPhone 14', 'PRODUCT', 'page_1.txt'),
  ('Apple Inc.', 'COMP', 'Operate_In', 'Technology Sector', 'SECTOR', 'page_1.txt'),
  ('iPhone 14', 'PRODUCT', 'Positive_Impact_On', "Apple's Stock Value", 'FIN_INSTRUMENT', 'page_1.txt')
]
Do not include any text or formatting beyond this Python list.
Your Task:
Read the provided PDF text (or textual input).
Identify important entities (including CAPEX, management, raw materials, etc.), unify references, and condense them to fewer than four words if necessary.
Link these entities with appropriate relationship verbs.
Produce only a Python list of tuples of the form:
python
Copy
Edit
[('h', 'type', 'r', 'o', 'type', 'source'), ...]
Include the Source Reference:

Ensure the 'source' field accurately reflects the name of the input file or page.
This reference is crucial for maintaining the connection back to the original document.
No Extra Commentary:

Only return the list of tuples—no additional explanation or formatting is needed."""

    process_pdf_with_gemini(api_key, pdf_path, output_file, prompt)
