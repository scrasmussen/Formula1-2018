PC=python3
FILE=analyze_2022.py
NEWFILE=new_analyze.py

all: run

run:
	$(PC) $(FILE)

new:
	$(PC) $(NEWFILE)
