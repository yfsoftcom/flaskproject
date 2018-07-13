@echo off
echo ###################################################
echo              Ready to make test
echo ###################################################
echo Run Script: python -m unittest discover -s %1\test -v -p *%2.py
echo ---------------------------------------------------
python -m unittest discover -s %1\test -v -p *%2.py