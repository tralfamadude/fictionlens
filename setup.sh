#  source this
conda create --name fictionlens python=3.11a
conda activate fictionlens
pip install ebooklib beautifulsoup4
pip install openai
pip install -r ./frontend/requirements.txt
pip install -r ./backend/requirements.txt
