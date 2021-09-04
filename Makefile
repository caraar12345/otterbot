whois: COMMIT_HASH=$(GITHUB_SHA)
router: COMMIT_HASH=$(GITHUB_SHA)

whois:
	@python3.9 -m venv venv
	@. venv/bin/activate
	@python3.9 -m pip install -r whois_requirements.txt
	@zip -r whois_otterbot_$(COMMIT_HASH).zip . -x '*.git*' -x '*.zip' -x 'Makefile' -x 'sample.py' -x 'venv/*' -x 'router.py' -x '*requirements.txt'
	@CDPATH=. cd venv/lib/python3.9/site-packages; zip -r -g ../../../../whois_otterbot_$(COMMIT_HASH).zip */*

router:
	@python3.9 -m venv venv
	@. venv/bin/activate
	@python3.9 -m pip install -r router_requirements.txt
	@zip -r otterbot_router_$(COMMIT_HASH).zip . -x '*.git*' -x '*.zip' -x 'Makefile' -x 'sample.py' -x 'venv/*' -x 'whois.py' -x '*requirements.txt' -x 'python_whois'
	@CDPATH=. cd venv/lib/python3.9/site-packages; zip -r -g ../../../../otterbot_router_$(COMMIT_HASH).zip */*
