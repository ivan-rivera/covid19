appname=covid-monitor
pname=covid19
duser=n3v3r

test:
	python3 -m pytest

launch:
	gunicorn app:server

devlaunch:
	python app.py

dbuild:
	docker build -t $(duser)/$(pname) .

drun:
	docker run --rm -tp 8000:8000 $(duser)/$(pname) make launch

dkill:
	docker kill `docker ps -q`

dpush:
	docker push $(duser)/$(pname):latest

hpr:
	heroku container:push web -a $(appname); \
	heroku container:release web -a $(appname)


.PHONY: test launch dbuild drun dpush dkill hpr
