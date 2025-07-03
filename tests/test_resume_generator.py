import os
import subprocess
import pytest

JOB_PROFILES = ["DataScientist", "MachineLearningEngineer", "DataAnalyst", "BIAnalyst", "AIEngineer"]

@pytest.mark.parametrize("profile", JOB_PROFILES)
def test_resume_generation(profile):
    """
    Tests that the resume generation script runs successfully for each job profile
    and that the expected PDF and TeX files are created.
    """
    result = subprocess.run(
        ["python", "build_resume.py", profile],
        capture_output=True
    )
    
    stdout = result.stdout.decode('utf-8', errors='ignore')
    stderr = result.stderr.decode('utf-8', errors='ignore')

    assert result.returncode == 0, f"Script failed for profile {profile}: {stderr}"

    assert os.path.isdir(profile), f"Output directory for {profile} was not created."

    base_name_en = "John_Doe_Resume"
    base_name_de = "John_Doe_Lebenslauf"
    
    assert os.path.isfile(os.path.join(profile, f"{base_name_en}.pdf")), f"English PDF not found for {profile}"
    assert os.path.isfile(os.path.join(profile, f"{base_name_en}.tex")), f"English TeX file not found for {profile}"
    assert os.path.isfile(os.path.join(profile, f"{base_name_de}.pdf")), f"German PDF not found for {profile}"
    assert os.path.isfile(os.path.join(profile, f"{base_name_de}.tex")), f"German TeX file not found for {profile}"