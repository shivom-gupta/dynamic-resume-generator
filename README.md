# Dynamic LaTeX Resume Generator

This project is a dynamic LaTeX resume generator that creates tailored resumes for various job profiles. It uses a Python script to populate a LaTeX template with data from a YAML file, generating professional-looking resumes in both English and German.

## Features

  * **Multiple Job Profiles**: Generate resumes for different job roles such as Machine Learning Engineer, Data Scientist, Data Analyst, BI Analyst, and AI Engineer.
  * **Multilingual Support**: Creates resumes in both English and German.
  * **Dynamic Content**: The content of the resume, including personal information, experience, skills, and projects, is managed through a single `resume_data.yml` file.
  * **LaTeX Quality**: Utilizes LaTeX to produce high-quality, professional-looking PDF resumes.
  * **Automated Build Process**: A Python script automates the generation of resumes, making it easy to create multiple versions.

## Prerequisites

Before you begin, ensure you have the following installed:

  * **Python 3.13+**
  * **Pip or uv**: For installing Python packages.
  * **Tex Live**: A comprehensive TeX system.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/shivom-gupta/dynamic-resume-generator.git
    cd dynamic-resume-generator
    ```

2.  **Create a virtual environment and install dependencies:**

    Using `uv`:

    ```bash
    uv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

    or using `pip`:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Install Tex Live:**

      * **macOS (via Homebrew):**
        ```bash
        brew install --cask mactex
        ```
      * **Linux (Debian/Ubuntu):**
        ```bash
        sudo apt-get install texlive-full
        ```
      * **Windows:**
        Download and install from the [Tex Live website](https://www.tug.org/texlive/).

## Usage

1.  **Update your information:**
    Open the `resume_data.yml` file and fill in your personal information, work experience, education, skills, and projects.

2.  **Replace the placeholder photo:**
    Replace the `me.png` file in the root directory with your own photo.

3.  **Generate your resume:**
    Run the `build_resume.py` script with the desired job profile as an argument.

      * **For a specific job profile:**

        ```bash
        python build_resume.py DataScientist
        ```

        You can replace `DataScientist` with any of the job profiles defined in `resume_data.yml` under the `job_profiles` section.

      * **For all job profiles:**

        ```bash
        python build_resume.py all
        ```

4.  **Find your resume:**
    The generated resume will be saved in a directory named after the job profile (e.g., `DataScientist/`). This directory will contain the `.tex` file and the compiled PDF.

## Customization

### Content

All the content of the resume can be customized by editing the `resume_data.yml` file. This file is structured to be easily understandable and editable.

### Appearance

The appearance of the resume is controlled by the `altacv.cls` file and the `resume.tex.j2` template. You can modify these files to change the layout, colors, and fonts of your resume.

  * `altacv.cls`: This is the LaTeX class file that defines the structure and style of the resume.
  * `resume.tex.j2`: This is the Jinja2 template file that the Python script uses to generate the final `.tex` file.

## Contributing

Contributions are welcome\! If you have any suggestions or find any bugs, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

The `altacv.cls` file is used under the LaTeX Project Public License (LPPL), v1.3c or later. See the `LICENSE` file for more information.