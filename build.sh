pip install -r requirements.txt

pyinstaller --clean -y -F -n "$1" \
	--add-data="lib/libtdjson.so:telegram/lib/linux" \
	--add-data="lib/libtdjson.dylib:telegram/lib/darwin" \
	--icon="GramUp Icon.ico" \
	--paths="gramup" gramup/__main__.py 

rm -rf build "${1}.spec"	
