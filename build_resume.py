import yaml
import argparse
import os
from jinja2 import Environment, FileSystemLoader
import subprocess
from time import sleep
import shutil

def escape_latex(text):
    """Escapes special LaTeX characters in a given string."""
    if not isinstance(text, str):
        return text
    return text.replace('&', r'\&').replace('%', r'\%').replace('$', r'\$') \
               .replace('#', r'\#').replace('_', r'\_').replace('{', r'\{') \
               .replace('}', r'\}').replace('~', r'\textasciitilde{}') \
               .replace('^', r'\textasciicircum{}')

def get_lang_specific_data(data, lang):
    """
    Recursively processes a data structure to extract strings
    for the specified language, defaulting to English if a translation is missing.
    """
    if isinstance(data, dict):
        if 'en' in data: # Check if this dictionary is a translatable item
            return data.get(lang, data['en'])
        # Otherwise, process the dictionary's values
        return {k: get_lang_specific_data(v, lang) for k, v in data.items()}
    if isinstance(data, list):
        return [get_lang_specific_data(i, lang) for i in data]
    return data

def generate_resume(data, profile_key):
    """
    Generates a resume in LaTeX format for a specific job profile.
    The resume is tailored based on the job profile and includes translations for English and German.
    """
    os.makedirs(profile_key, exist_ok=True)

    if profile_key not in data['job_profiles']:
        print(f"Error: Job profile '{profile_key}' not found in resume_data.yml.")
        print(f"Available profiles are: {', '.join(data['job_profiles'].keys())}")
        return

    for lang in ['en', 'de']:
        print(f"--- Generating {lang.upper()} version for {profile_key} in folder '{profile_key}' ---")

        # Create a full, translated copy of the data for the current language
        lang_data = get_lang_specific_data(data, lang)
        # Filter skills, learning, and projects based on the language-independent tags from the original data
        filtered_tech_skills = []
        for group in data['tech_skills']:
            filtered_skills_for_group = [s for s in group['skills'] if profile_key in s.get('tags', [])]
            if filtered_skills_for_group:
                # Add the translated version of the filtered group
                filtered_tech_skills.append({
                    'group_name': get_lang_specific_data(group['group_name'], lang),
                    'skills': get_lang_specific_data(filtered_skills_for_group, lang)
                })
                
        
        filtered_soft_skills = [s for s in data['soft_skills'] if profile_key in s.get('tags', [])]
        filtered_soft_skills = get_lang_specific_data(filtered_soft_skills, lang)

        filtered_learning = [s for s in data['learning'] if profile_key in s.get('tags', [])]
        filtered_learning = get_lang_specific_data(filtered_learning, lang)
        filtered_projects = [p for p in data['projects'] if profile_key in p.get('tags', [])]

        # Construct the dynamic tagline for the header
        profile_display_name = lang_data['job_profiles'][profile_key]
        tagline = f"{profile_display_name}"

        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
        env.filters['escape_latex'] = escape_latex
        template = env.get_template('resume.tex.j2')

        # Prepare the final context for rendering this language's template
        render_context = {
            'personal_info': lang_data['personal_info'],
            'ui': lang_data['ui_text'],
            'summary': lang_data['summaries'][profile_key],
            'experience': lang_data['experience'],
            'education': lang_data['education'],
            'languages': lang_data['languages'],
            'tech_skills': filtered_tech_skills,
            'soft_skills': filtered_soft_skills,
            'learning': get_lang_specific_data(filtered_learning, lang),
            'projects': get_lang_specific_data(filtered_projects, lang),
            'profile_tagline': tagline,
        }

        output_content = template.render(render_context)

        # Write the final .tex file
        name = lang_data['personal_info']['name'].strip().replace(' ', '_')
        if lang == 'de':
            output_filename = f'{name}_Lebenslauf.tex'
        else:
            output_filename = f'{name}_Resume.tex'
        output_path = os.path.join(profile_key, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)

        if os.path.isfile('altacv.cls'):
            shutil.copy('altacv.cls', profile_key)
        else:
            raise FileNotFoundError("altacv.cls file not found. Please ensure it is in the current directory.")
        subprocess.run(["pdflatex", output_filename], cwd=profile_key, check=True)
        sleep(1)
        intermediate_extensions = ['.aux', '.log', '.out', '.fdb_latexmk', '.fls', '.synctex.gz', '.xmpi']
        for ext in intermediate_extensions:
            try:
                path = os.path.join(profile_key, f"{output_filename[:-4]}{ext}")
                print(f"Removing intermediate file: {path}")
                os.remove(path)
            except FileNotFoundError:
                pass

        os.remove(os.path.join(profile_key, 'pdfa.xmpi'))
        print(f"Successfully generated resume: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate multilingual LaTeX resumes for a specific job application.")
    parser.add_argument("job_profile", default="DataScientist", help="The job profile to tailor the resume for (e.g., DataScientist).")
    args = parser.parse_args()
    profile_key = args.job_profile

    with open('resume_data.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if profile_key == 'all':
        for key in data['job_profiles']:
            generate_resume(data, key)
    else:
        generate_resume(data, profile_key)

    
if __name__ == "__main__":
    main()