import os
from django.db import models

# Job Categories for dropdown selection
JOB_CATEGORIES = [
    ("ACCOUNTANT", "Accountant"),
    ("ADVOCATE", "Advocate"),
    ("AGRICULTURE", "Agriculture"),
    ("APPAREL", "Apparel"),
    ("ARTS", "Arts"),
    ("AUTOMOBILE", "Automobile"),
    ("AVIATION", "Aviation"),
    ("BANKING", "Banking"),
    ("BPO", "BPO"),
    ("BUSINESS-DEVELOPMENT", "Business Development"),
    ("CHEF", "Chef"),
    ("CONSTRUCTION", "Construction"),
    ("CONSULTANT", "Consultant"),
    ("DESIGNER", "Designer"),
    ("DIGITAL-MEDIA", "Digital Media"),
    ("ENGINEERING", "Engineering"),
    ("FINANCE", "Finance"),
    ("FITNESS", "Fitness"),
    ("HEALTHCARE", "Healthcare"),
    ("HR", "HR"),
    ("INFORMATION-TECHNOLOGY", "Information Technology"),
    ("PUBLIC-RELATIONS", "Public Relations"),
    ("SALES", "Sales"),
    ("TEACHER", "Teacher"),
]

class Resume(models.Model):
    full_name = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to="resumes/")
    job_category = models.CharField(max_length=50, choices=JOB_CATEGORIES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Return just the file name for display.
        return self.full_name or self.file.name

    @property
    def base_file_name(self):
        # Extracts and returns the file name from the full file path.
        return os.path.basename(self.file.name)

class ScreeningResult(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    organization = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    skill_score = models.IntegerField(default=0)
    collaboration_score = models.IntegerField(default=0)
    adaptability_score = models.IntegerField(default=0)
    overall_score = models.IntegerField(default=0)

    def __str__(self):
        return f"Result for {self.resume.base_file_name}"
