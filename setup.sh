#  source this
eval "$(command conda 'shell.bash' 'hook' 2> /dev/null)"
conda create --name fictionlens python=3.11
conda activate fictionlens
pip install ebooklib beautifulsoup4
pip install openai
pip install poetry
cd backend   # important
poetry init
poetry install
poetry shell

export OPENAI_API_KEY=....

python app/engine/generate.py    # temporary until we have out data loaded
# no # pip install -r requirements.txt



