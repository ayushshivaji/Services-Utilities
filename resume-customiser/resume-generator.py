import json
import requests
from bs4 import BeautifulSoup
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from markdown_pdf import MarkdownPdf

nltk.download("punkt")
nltk.download("stopwords")


def load_resume(json_path):
    with open(json_path, "r") as f:
        return json.load(f)


def get_job_description(source):
    """Takes URL or raw job description string."""
    if source.startswith("http"):
        response = requests.get(source)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    return source


def extract_keywords(text):
    text = re.sub(r"[^a-zA-Z0-9\- ]", " ", text)
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    filtered = [t for t in tokens if t not in stop_words and len(t) > 2]
    freq = nltk.FreqDist(filtered)
    return {word for word, count in freq.items() if count > 1}


def filter_resume_sections(resume, keywords):
    filtered = {
        "name": resume["name"],
        "contact": resume["contact"],
        "sections": []
    }

    for section in resume["sections"]:
        matches = [item for item in section["content"]
                   if any(k in item.lower() for k in keywords)]
        if matches:
            filtered["sections"].append({
                "title": section["title"],
                "content": matches
            })

    return filtered


def resume_to_markdown(resume):
    lines = [f"# {resume['name']}", f"**{resume['contact']}**", ""]
    for section in resume["sections"]:
        lines.append(f"## {section['title']}")
        for item in section["content"]:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines)


def save_markdown_file(text, path="custom_resume.md"):
    with open(path, "w") as f:
        f.write(text)
    return path


def convert_markdown_to_pdf(md_file, pdf_file="custom_resume.pdf"):
    MarkdownPdf().from_path(md_file).write(pdf_file)
    return pdf_file


# Main Execution
def generate_custom_resume(json_path, job_input, output_pdf="custom_resume.pdf"):
    base = load_resume(json_path)
    job_text = get_job_description(job_input)
    keywords = extract_keywords(job_text)
    tailored_resume = filter_resume_sections(base, keywords)
    markdown_text = resume_to_markdown(tailored_resume)
    md_file = save_markdown_file(markdown_text)
    pdf_path = convert_markdown_to_pdf(md_file, output_pdf)
    print(f"✅ Resume generated: {pdf_path}")


# Example usage
if __name__ == "__main__":
    generate_custom_resume("base_resume.json", "https://www.hashicorp.com/en/career/7004503")
