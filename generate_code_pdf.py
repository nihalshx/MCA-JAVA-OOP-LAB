import os
from fpdf import FPDF

# Configuration
OUTPUT_PDF = "All_Code.pdf"
CODE_EXTENSIONS = [".java", ".py", ".c", ".cpp", ".js", ".ts", ".cs", ".rb", ".go", ".php", ".swift", ".kt", ".scala"]

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font("Courier", size=10)

    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, "All Code Files", ln=True, align="C")
        self.ln(5)
        self.set_font("Courier", size=10)

    def chapter_title(self, title):
        self.set_font("Arial", 'B', 12)
        self.set_fill_color(220, 220, 220)
        self.cell(0, 8, title, ln=True, fill=True)
        self.ln(2)
        self.set_font("Courier", size=10)

    def code_block(self, code):
        self.set_font("Courier", size=10)
        for line in code.splitlines():
            self.multi_cell(0, 5, line)
        self.ln(2)

def collect_code_files(root_dir):
    code_files = []
    for folder, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in CODE_EXTENSIONS):
                rel_dir = os.path.relpath(folder, root_dir)
                rel_file = os.path.join(rel_dir, file) if rel_dir != '.' else file
                code_files.append((rel_dir, file, os.path.join(folder, file)))
    return code_files

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    code_files = collect_code_files(root_dir)
    code_files.sort()  # Sort for consistent order

    pdf = PDF()
    current_folder = None
    for rel_dir, file, path in code_files:
        if rel_dir != current_folder:
            pdf.chapter_title(f"Folder: {rel_dir}")
            current_folder = rel_dir
        pdf.chapter_title(f"File: {file}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            code = f"[Could not read file: {e}]"
        pdf.code_block(code)

    pdf.output(OUTPUT_PDF)
    print(f"PDF generated: {OUTPUT_PDF}")

if __name__ == "__main__":
    main() 