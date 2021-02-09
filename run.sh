cd $(dirname "$0")

if [ ! -f "./.flag" ]; then
	echo "Installing dependencies..."
	pip install -r requirements.txt
	touch "./.flag"
fi

python3 main.py || python main.py
