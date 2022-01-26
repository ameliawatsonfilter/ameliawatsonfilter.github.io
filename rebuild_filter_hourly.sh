cd /home/amefilter/ameliawatsonfilter.github.io
python3 filter_builder.py
git add filter.txt
if git commit -m "update filter.txt"; then
	git push -u $(cat upstream)
fi
