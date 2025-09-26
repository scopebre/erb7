SHELL := /bin/zsh
.SHELLFLAGS := -C
up:
# 	workon erb7
	source~/.zshrc && workon erb7 && python manage.py runserver

static:
	python manage.py collectstatic