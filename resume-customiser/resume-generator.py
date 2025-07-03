import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# Convert markdown to HTML
with open('base_resume.md', 'r') as f:
    md_content = f.read()

html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

# Add basic styling
css_content = """
body { font-family: Arial, sans-serif; margin: 40px; }
h1, h2, h3 { color: #333; }
code { background-color: #f4f4f4; padding: 2px 4px; }
pre { background-color: #f4f4f4; padding: 10px; }
"""

# Generate PDF
HTML(string=html).write_pdf('output.pdf', stylesheets=[CSS(string=css_content)])
