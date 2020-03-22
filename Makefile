test:
	python3 -m pytest

launch:
	python3 covid19/app.py

dbuild:
	docker build -t covid19 .

drun:
	docker run --rm -tp 8000:8000 covid19 make launch

dkill:
	docker kill `docker ps -q`

.PHONY: test launch dbuild drun dkill
