
cd documentation

rm -r _build

cp index.rst index.rst.temp
rm -f *.rst
cp index.rst.temp index.rst

sphinx-apidoc -o . ../cmsis2

make html

sphinx-serve

read -p "Presiona Enter para salir..."
