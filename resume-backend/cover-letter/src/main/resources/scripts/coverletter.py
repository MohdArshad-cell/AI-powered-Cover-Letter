import sys
import os
import json
import re
import google.generativeai as genai
import contextlib

# --- CONFIGURATION ---
API_KEY = os.getenv("GEMINI_API_KEY", "API key") # <--- ADD YOUR API KEY
MODEL_NAME = "gemini-2.5-flash-lite"

# --- HELPER FUNCTIONS ---

def load_file(file_path: str) -> str:
    """Reads and returns the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}", file=sys.stderr)
        raise

@contextlib.contextmanager
def suppress_stderr():
    """A context manager to temporarily suppress stderr."""
    original_stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w', encoding='utf-8')
    try:
        yield
    finally:
        sys.stderr.close()
        sys.stderr = original_stderr

def call_gemini_api(prompt: str) -> str:
    """Calls the Gemini API and returns the text response."""
    with suppress_stderr():
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt)
    return response.text

def clean_json_string(json_string: str) -> str:
    """Extracts the first valid JSON object or array from a string."""
    match = re.search(r'\{[\s\S]*\}|\[[\s\S]*\]', json_string)
    if match:
        return match.group(0)
    else:
        raise ValueError(f"No valid JSON found in AI response: {json_string}")

def main():
    """Main execution function for the cover letter generation."""
    # *** CRITICAL CHANGE: Now expects 3 arguments: script_name, resume_filepath, jd_filepath ***
    if len(sys.argv) != 3:
        print(f"Error: Invalid arguments. Expected 2 file paths, but got {len(sys.argv) - 1}.", file=sys.stderr)
        sys.exit(1)

    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print("Error: Gemini API key is not configured.", file=sys.stderr)
        sys.exit(1)

    try:
        # *** CRITICAL CHANGE: Read content from the provided file paths ***
        resume_filepath = sys.argv[1]
        jd_filepath = sys.argv[2]
        
        resume_content = load_file(resume_filepath)
        job_description = load_file(jd_filepath)
    except Exception as e:
        print(f"Error reading input files: {e}", file=sys.stderr)
        sys.exit(1)

    script_dir = os.path.dirname(__file__)

    try:
        # Step 1: Analysis
        prompt1_template = load_file(os.path.join(script_dir, 'cl_prompt_step1_analysis.txt'))
        prompt1 = prompt1_template.format(job_description=job_description, resume_content=resume_content)
        analysis_str = call_gemini_api(prompt1)
        analysis_json = json.loads(clean_json_string(analysis_str))
        
        # Step 2: Outlining
        prompt2_template = load_file(os.path.join(script_dir, 'cl_prompt_step2_outline.txt'))
        prompt2 = prompt2_template.format(analysis_json=json.dumps(analysis_json, indent=2))
        outline_str = call_gemini_api(prompt2)
        outline_json = json.loads(clean_json_string(outline_str))

        # Step 3: Drafting
        prompt3_template = load_file(os.path.join(script_dir, 'cl_prompt_step3_draft.txt'))
        prompt3 = prompt3_template.format(outline_json=json.dumps(outline_json, indent=2), resume_content=resume_content, job_description=job_description)
        cover_letter_draft = call_gemini_api(prompt3)

        # Step 4: Reviewing
        prompt4_template = load_file(os.path.join(script_dir, 'cl_prompt_step4_review.txt'))
        prompt4 = prompt4_template.format(cover_letter_draft=cover_letter_draft, analysis_json=json.dumps(analysis_json, indent=2))
        final_cover_letter = call_gemini_api(prompt4)
        
        print(final_cover_letter) # Send the final result to stdout

    except Exception as e:
        print(f"A critical error occurred during the AI generation process: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()