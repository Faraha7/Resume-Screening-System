import os
import pandas as pd
import spacy

# Load the English NLP model in spaCy
nlp = spacy.load("en_core_web_sm")

# Define Paths
root_directory = r"C:\Users\abdir\ResumeScreeningSystem\ResumeScreeningSystem\Extracted_Resumes"
analysis_directory = r"C:\Users\abdir\ResumeScreeningSystem\ResumeScreeningSystem\Analysis_Results"

# Ensure output directory exists
os.makedirs(analysis_directory, exist_ok=True)

# Define Job Categories & Keywords
job_categories = {
    "ACCOUNTANT": ["finance", "accounting", "audit", "tax"],
    "ADVOCATE": ["law", "legal", "court", "attorney"],
    "AGRICULTURE": ["farming", "crops", "agriculture", "harvest"],
    "APPAREL": ["fashion", "clothing", "design", "merchandising"],
    "ARTS": ["painting", "sculpting", "illustration", "photography"],
    "AUTOMOBILE": ["car", "automobile", "mechanic", "vehicle"],
    "AVIATION": ["pilot", "aircraft", "flight", "aviation"],
    "BANKING": ["bank", "finance", "investment", "loans"],
    "BPO": ["customer service", "call center", "outsourcing"],
    "BUSINESS-DEVELOPMENT": ["sales", "strategy", "partnerships"],
    "CHEF": ["cooking", "culinary", "restaurant", "chef"],
    "CONSTRUCTION": ["building", "construction", "architecture"],
    "CONSULTANT": ["advisory", "consulting", "strategy"],
    "DESIGNER": ["graphics", "design", "UI/UX", "fashion"],
    "DIGITAL-MEDIA": ["social media", "marketing", "content"],
    "ENGINEERING": ["mechanical", "electrical", "civil", "software"],
    "FINANCE": ["investment", "finance", "wealth management"],
    "FITNESS": ["gym", "trainer", "workout", "nutrition"],
    "HEALTHCARE": ["doctor", "nurse", "hospital", "medical"],
    "HR": ["recruitment", "human resources", "hiring"],
    "INFORMATION-TECHNOLOGY": ["software", "coding", "AI", "machine learning"],
    "PUBLIC-RELATIONS": ["communications", "PR", "media"],
    "SALES": ["retail", "selling", "customer service"],
    "TEACHER": ["education", "teaching", "students", "classroom"]
}

# Extract & Process Resumes
def extract_resume_text(file_path):
    """Extracts text from a resume TXT file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""

def analyze_resume(file_path, category_keywords):
    """Processes a single resume and extracts relevant entities."""
    resume_text = extract_resume_text(file_path)
    if not resume_text:
        return None  # Skip empty resumes

    # Process text with spaCy NLP
    doc = nlp(resume_text)

    # Extract Named Entities
    extracted_entities = {"PER": [], "ORG": [], "LOC": []}
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            extracted_entities["PER"].append(ent.text)
        elif ent.label_ == "ORG":
            extracted_entities["ORG"].append(ent.text)
        elif ent.label_ == "GPE":
            extracted_entities["LOC"].append(ent.text)

    # Get the first organization and location found (avoid duplicates)
    organization = extracted_entities["ORG"][0] if extracted_entities["ORG"] else "Not Found"
    location = extracted_entities["LOC"][0] if extracted_entities["LOC"] else "Not Found"

    # Assign scores based on presence of keywords
    skill_score = sum([1 for keyword in category_keywords if keyword in resume_text.lower()])
    collaboration_score = 2 if "team" in resume_text.lower() else 0
    adaptability_score = 2 if "adaptable" in resume_text.lower() else 0

    overall_score = skill_score + collaboration_score + adaptability_score

    return {
        "File Name": os.path.basename(file_path),
        "Organization": organization,
        "Location": location,
        "Skill Score": skill_score,
        "Collaboration Score": collaboration_score,
        "Adaptability Score": adaptability_score,
        "Overall Score": overall_score
    }

def process_resumes_for_category(category, keywords):
    """Processes all resumes for a given job category."""
    category_path = os.path.join(root_directory, category)
    output_folder = os.path.join(analysis_directory, category)
    os.makedirs(output_folder, exist_ok=True)

    results = []
    if not os.path.exists(category_path):
        print(f"⚠️ No resumes found for category: {category}")
        return

    print(f"🔍 Processing category: {category}")

    for file in os.listdir(category_path):
        if file.endswith(".txt"):  
            file_path = os.path.join(category_path, file)
            print(f"📄 Processing: {file}")
            result = analyze_resume(file_path, keywords)
            if result:
                results.append(result)

    if results:
        df = pd.DataFrame(results).sort_values(by="Overall Score", ascending=False).head(5)
        df.index = [f"Candidate {i+1}" for i in range(len(df))]
        
        output_csv = os.path.join(output_folder, f"{category}_results.csv")
        df.to_csv(output_csv, index=False)
        print(f"✅ Results saved: {output_csv}")

        print(f"🏆 Top 5 Candidates for {category}:")
        print(df)
    else:
        print(f"⚠️ No valid resumes found for {category}")

def process_job_categories():
    """Processes resumes for all job categories."""
    for category, keywords in job_categories.items():
        process_resumes_for_category(category, keywords)

# 🚀 Run Screening
if __name__ == "__main__":
    process_job_categories()

