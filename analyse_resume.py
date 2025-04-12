import os
import spacy
import pandas as pd
import re

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Paths
root_directory = r"C:\Users\abdir\ResumeScreeningSystem\ResumeScreeningSystem\Extracted_Resumes"
analysis_directory = r"C:\Users\abdir\ResumeScreeningSystem\ResumeScreeningSystem\Analysed_Resumes"
os.makedirs(analysis_directory, exist_ok=True)

# Job categories and keywords
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

# Clean text
def clean_text(text):
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return re.sub(r"\s+", " ", text).strip()

# Analyze single resume
def analyze_resume(file_path, resume_text, category_keywords):
    doc = nlp(resume_text)

    entities = {"PER": [], "ORG": [], "LOC": []}
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["PER"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["ORG"].append(ent.text)
        elif ent.label_ == "GPE":
            entities["LOC"].append(ent.text)

    name = clean_text(entities["PER"][0]) if entities["PER"] else "Not Found"
    organization = clean_text(entities["ORG"][0]) if entities["ORG"] else "Not Found"
    location = clean_text(entities["LOC"][0]) if entities["LOC"] else "Not Found"

    skill_score = sum([1 for keyword in category_keywords if keyword.lower() in resume_text.lower()])
    collaboration_score = 2 if "team" in resume_text.lower() else 0
    adaptability_score = 2 if "adaptable" in resume_text.lower() else 0
    overall_score = skill_score + collaboration_score + adaptability_score

    return {
        "File Name": os.path.basename(file_path),
        "Name": name,
        "Organization": organization,
        "Location": location,
        "Skill Score": skill_score,
        "Collaboration Score": collaboration_score,
        "Adaptability Score": adaptability_score,
        "Overall Score": overall_score
    }

# Process all resumes
def process_all_resumes():
    all_results = []

    for category, keywords in job_categories.items():
        category_path = os.path.join(root_directory, category)
        if not os.path.exists(category_path):
            continue

        results = []
        for file in os.listdir(category_path):
            if file.endswith(".txt"):
                file_path = os.path.join(category_path, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    resume_text = f.read()
                    if resume_text.strip():
                        result = analyze_resume(file_path, resume_text, keywords)
                        result["Category"] = category
                        results.append(result)
                        all_results.append(result)

        # Save per-job-role analysis
        if results:
            df = pd.DataFrame(results).sort_values(by="Overall Score", ascending=False).head(5)
            output_folder = os.path.join(analysis_directory, category)
            os.makedirs(output_folder, exist_ok=True)
            df.to_csv(os.path.join(output_folder, f"{category}_results.csv"), index=False)

    # Save full analysis
    if all_results:
        full_df = pd.DataFrame(all_results)
        full_df.to_csv(os.path.join(analysis_directory, "resume_analysis.csv"), index=False)
        print("✅ Master resume_analysis.csv saved with all roles.")
    else:
        print("⚠ No resumes analyzed.")

# Run
if __name__ == "__main__":
    process_all_resumes()
