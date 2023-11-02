cd documentation

rmdir /s /Q _build

copy index.rst index.rst.temp
del /f *.rst
copy index.rst.temp index.rst

sphinx-apidoc -o . ..\cmsis2
make html
sphinx-serve
pause
