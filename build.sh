pyinstaller --clean -y -F -n "$1" \
	--icon="GramUp Icon.ico" \
	--paths="gramup" gramup/main.py

rm -rf build "${1}.spec" && echo "Removed unwanted files"
