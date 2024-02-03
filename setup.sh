#  source this
#conda create --name fictionlens python=3.11
#conda activate fictionlens
pip install ebooklib beautifulsoup4
pip install openai
poetry install
poetry shell
pip install -r ./backend/requirements.txt
python ./backend/app/engine/generate.py    # temporary
(cd backend ; python main.py  >main.py.out 2>main.py.err & )
