# GitHub AntiPlagiarism

#### Find similar files in specified repositories

# Setup

1. Clone project
2. `cd gh-ap`
3. `pip install -r gh-ap/requirements.txt`
4. `cp .env-example .env`
5. Open `.env` and paste [GitHub Token](https://github.com/settings/tokens)

___

# Use

1. Fill repositories link in `repos.txt`
2. Fill GitHub file links, which need to check for plagiarism, in `url` variable in `main.py`
3. Additionally, you can change the max threads(`MAX_THREADS`) and the min match percentage for output (`MIN_DIFF`) in `config.py`.
4. If all is OK, you will see the result.
