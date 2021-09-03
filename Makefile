COMMIT_HASH = $(GITHUB_SHA)
package:
	@python3.9 -m pip install -r requirements.txt
	@zip -r whois_otterbot_$(COMMIT_HASH).zip . -x '*.git*' -x '*.zip' -x 'Makefile' -x 'sample.py' -x 'venv/'
	@cd venv/lib/python3.9/site-packages
	@zip -g whois_otterbot_$(COMMIT_HASH).zip .