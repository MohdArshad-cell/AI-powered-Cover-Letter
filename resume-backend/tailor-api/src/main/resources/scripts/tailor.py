import sys
import os
import json
import re
import google.generativeai as genai
import contextlib

# --- CONFIGURATION ---
API_KEY = os.getenv("GEMINI_API_KEY", "API KEY")
MODEL_NAME = "gemini-2.5-flash-lite"

# --- HELPER FUNCTIONS ---

def load_file(file_path: str) -> str:
    """Reads and returns the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Required file not found at {file_path}")

@contextlib.contextmanager
def suppress_stderr():
    """A context manager to temporarily suppress stderr to hide library warnings."""
    original_stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w', encoding='utf-8')
    try:
        yield
    finally:
        sys.stderr.close()
        sys.stderr = original_stderr

def call_gemini_api(prompt: str) -> str:
    """Calls the Gemini API with a given prompt and returns the text response."""
    with suppress_stderr():
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt)
    return response.text

def clean_json_string(json_string: str) -> str:
    """Finds and extracts the first valid JSON object or array from a string."""
    match = re.search(r'\{[\s\S]*\}|\[[\s\S]*\]', json_string)
    if match:
        return match.group(0)
    else:
        raise ValueError(f"No valid JSON object or array found in the AI's response: {json_string}")

# --- UPGRADED, MORE ROBUST CLEANING FUNCTION ---

import re

def clean_final_latex(text: str) -> str:
    """
    Performs a final, safer cleaning of the LaTeX code to fix common AI errors
    without breaking tabular environments.
    """
    start_index = text.find(r'\documentclass')
    if start_index == -1:
        raise ValueError("Could not find \\documentclass in the final output.")
    clean_text = text[start_index:]

    # Fix curly apostrophes, dashes, invalid unicode
    replacements = {
        "’": "'",
        "–": "--",
        "—": "--",
        "\uFFFD": "--",
    }
    for old, new in replacements.items():
        clean_text = clean_text.replace(old, new)

    # Escape % in numbers
    clean_text = re.sub(r'(\d)\%', r'\1\\%', clean_text)

    # Escape bare & only if not already escaped (safer than global " & ")
    # Escape ampersands only when surrounded by text, not when starting a brace
    clean_text = re.sub(r'(?<=\w)&(?=\w)', r'\\&', clean_text)


    # Fix double braces
    clean_text = clean_text.replace('{{', '{').replace('}}', '}')

    return clean_text.strip()


def main():
    """Main execution function to run the 4-step prompt chain."""
    if len(sys.argv) != 3:
        print("Error: Invalid arguments. Script requires a resume and a job description.", flush=True)
        sys.exit(1)

    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        raise ValueError("Gemini API key is not configured. Please replace 'YOUR_API_KEY_HERE' in the script.")

    resume_content = sys.argv[1]
    job_description = sys.argv[2]
    
    script_dir = os.path.dirname(__file__)

    try:
        prompt1_template = load_file(os.path.join(script_dir, 'prompt_step1_jd_analysis.txt'))
        prompt1 = prompt1_template.format(job_description=job_description)
        jd_analysis_str = call_gemini_api(prompt1)
        jd_analysis_json = json.loads(clean_json_string(jd_analysis_str))
    except Exception as e:
        print(f"A critical error occurred during STEP 1 (JD Analysis): {e}", flush=True)
        sys.exit(1)
    
    try:
        prompt2_template = load_file(os.path.join(script_dir, 'prompt_step2_planning.txt'))
        prompt2 = prompt2_template.format(jd_analysis_json=json.dumps(jd_analysis_json, indent=2), resume_content=resume_content)
        strategic_plan_str = call_gemini_api(prompt2)
        strategic_plan_json = json.loads(clean_json_string(strategic_plan_str))
    except Exception as e:
        print(f"A critical error occurred during STEP 2 (Strategic Planning): {e}", flush=True)
        sys.exit(1)
    
    try:
        latex_template = load_file(os.path.join(script_dir, 'template.tex'))
        prompt3_template = load_file(os.path.join(script_dir, 'prompt_step3_drafting.txt'))
        prompt3 = prompt3_template.format(strategic_plan_json=json.dumps(strategic_plan_json, indent=2), resume_content=resume_content, DEFAULT_LATEX_TEMPLATE=latex_template)
        latex_draft = call_gemini_api(prompt3)
    except Exception as e:
        print(f"A critical error occurred during STEP 3 (Draft Generation): {e}", flush=True)
        sys.exit(1)

    try:
        prompt4_template = load_file(os.path.join(script_dir, 'prompt_step4_review.txt'))
        prompt4 = prompt4_template.format(jd_analysis_json=json.dumps(jd_analysis_json, indent=2), strategic_plan_json=json.dumps(strategic_plan_json, indent=2), latex_draft=latex_draft)
        final_latex_with_critique = call_gemini_api(prompt4)
        
        final_latex = clean_final_latex(final_latex_with_critique)
        print(final_latex)
    except Exception as e:
        print(f"A critical error occurred during STEP 4 (Critique and Refine): {e}", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()