import os
from tika import parser

# Input directory with job role subfolders
root_directory = r"C:\Users\abdir\ResumeScreeningSystem\ResumeScreeningSystem\data\data"
# Output directory for organized extracted resumes
output_directory = r"C:\Users\abdir\ResumeScreeningSystem\ResumeScreeningSystem\Extracted_Resumes"

# Ensure main output directory exists
os.makedirs(output_directory, exist_ok=True)

# Loop through job role folders
for subdir, _, files in os.walk(root_directory):
    for file in files:
        if file.endswith(".pdf"):
            file_path = os.path.join(subdir, file)

            # Get the job role from the subfolder name
            job_role = os.path.basename(subdir)
            job_output_folder = os.path.join(output_directory, job_role)
            os.makedirs(job_output_folder, exist_ok=True)

            output_file = os.path.join(job_output_folder, f"{file}.txt")

            # Avoid reprocessing already extracted files
            if os.path.exists(output_file):
                print(f"⚠️ Skipping (already exists): {output_file}")
                continue

            try:
                print(f"📄 Extracting: {file_path}")
                parsed_data = parser.from_file(file_path)
                resume_text = parsed_data.get('content', '')

                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(resume_text if resume_text else "")

                print(f"✅ Saved to: {output_file}")
            except Exception as e:
                print(f"❌ Error processing {file}: {e}")
