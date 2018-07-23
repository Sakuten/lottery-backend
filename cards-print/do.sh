#!/usr/bin/env bash
#
# this script outputs PDF file of QR cards list.
#
# copyright (c) 2018 Sakutendev

trap 'rm src/qr/*.png src/*.html' 2
echo "Generating html..."
echo "Done.\nGenerating PDF..."
echo "Done.\nAll processes are done properly.exit."
  pipenv run python mkhtml.py
wkhtmltopdf --encoding 'utf-8' --lowquality cards.html cards.pdf
