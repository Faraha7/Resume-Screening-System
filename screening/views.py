import os
import re
import spacy
import fitz  # PyMuPDF for PDFs
import docx  # python-docx for DOCX files
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ResumeUploadForm
from .models import Resume, ScreeningResult

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Collaboration and adaptability keywords
COMMON_COLLAB_KEYWORDS = [
    "team", "collaborate", "leadership", "communication", "interpersonal",
    "coordination", "cooperation", "synergy", "support", "network", "liaison"
]
COMMON_ADAPT_KEYWORDS = [
    "flexible", "adapt", "fast learner", "problem-solving", "change",
    "resilient", "innovative", "resourceful", "quick learner", "versatile", "adjustable"
]

def clean_text(text):
    return " ".join(text.split())

def extract_text_from_file(path):
    ext = os.path.splitext(path)[-1].lower()
    text = ""

    try:
        if ext == ".pdf":
            with fitz.open(path) as doc:
                for page in doc:
                    text += page.get_text()
        elif ext == ".docx":
            doc = docx.Document(path)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif ext == ".txt":
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        else:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
    except Exception as e:
        print(f"Could not extract text from {path}: {e}")
        text = ""

    return text

@login_required
def upload_resume(request):
    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            Resume.objects.all().delete()
            ScreeningResult.objects.all().delete()

            job_category = form.cleaned_data["job_category"]
            files = request.FILES.getlist("files")
            print("Number of files uploaded:", len(files))
            for file in files:
                resume = Resume.objects.create(
                    full_name=file.name,
                    file=file,
                    job_category=job_category
                )
                screen_resume(resume)
            messages.success(request, f"{len(files)} resume(s) uploaded successfully!")
            return redirect("upload_success")
        else:
            error_messages = []
            for field, errors in form.errors.items():
                error_messages.append(f"{field}: {errors.as_text()}")
            messages.error(request, " ".join(error_messages))
    else:
        form = ResumeUploadForm()
    return render(request, "screening/upload_resume.html", {"form": form})

@login_required
def upload_success(request):
    return render(request, "screening/upload_success.html")

@login_required
def top_candidates(request):
    selected_category = request.GET.get("category", "")
    selected_count = request.GET.get("count", "5")
    try:
        per_page = int(selected_count)
    except ValueError:
        per_page = 5
    results = ScreeningResult.objects.all().order_by("-overall_score")
    if selected_category:
        results = results.filter(resume__job_category=selected_category)
    paginator = Paginator(results, per_page)
    page_number = request.GET.get("page")
    try:
        results_page = paginator.page(page_number)
    except PageNotAnInteger:
        results_page = paginator.page(1)
    except EmptyPage:
        results_page = paginator.page(paginator.num_pages)
    job_categories = ResumeUploadForm.JOB_CATEGORIES
    return render(request, "screening/results.html", {
        "results": results_page,
        "job_categories": job_categories,
        "selected_category": selected_category,
        "selected_count": per_page,
    })

@login_required
def tutorial(request):
    return render(request, "screening/tutorial.html")

def screen_resume(resume_obj):
    path = os.path.join(settings.MEDIA_ROOT, resume_obj.file.name)
    text = extract_text_from_file(path)
    if not text:
        print(f"No text extracted from {resume_obj.file.name}. Skipping...")
        return

    text_clean = clean_text(text)
    lower_text = text_clean.lower()

    if "experience" in lower_text:
        experience_section = lower_text.split("experience", 1)[-1]
    else:
        experience_section = lower_text

    experience_score = experience_section.count("company name")
    tokens = set(re.findall(r'\w+', lower_text))
    matched_collab = {kw for kw in COMMON_COLLAB_KEYWORDS if kw in tokens}
    matched_adapt = {kw for kw in COMMON_ADAPT_KEYWORDS if kw in tokens}
    collab_score = len(matched_collab)
    adapt_score = len(matched_adapt)
    overall = experience_score + collab_score + adapt_score

    result, created = ScreeningResult.objects.get_or_create(resume=resume_obj)
    result.skill_score = experience_score
    result.collaboration_score = collab_score
    result.adaptability_score = adapt_score
    result.overall_score = overall
    result.save()
