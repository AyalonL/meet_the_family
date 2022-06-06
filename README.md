[![Build Status](https://app.travis-ci.com/AyalonL/meet_the_family.svg?branch=Dev)](https://app.travis-ci.com/AyalonL/meet_the_family)

# meet_the_family
Test Driven Development Tutorial - meet_the_family

# INSTRUCTIONS TO RUN:
- pip install -r requirements.txt
- python -m geektrust <absolute_path_to_filename>

# INSTRUCTIONS TO TEST:
Unit Test
- python -m unittest discover -s "./tests/unit/" -p "test_*.py" && flake8

Integration Test
- python -m unittest discover -s "./tests/integration/" -p "test_*.py" && flake8

System Test
- python -m unittest discover -s "./tests/system/" -p "test_*.py" && flake8
