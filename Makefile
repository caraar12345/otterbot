COMMIT_HASH = $(GITHUB_SHA)
package:
	@git submodule update
	@zip -r whois_otterbot_$(COMMIT_HASH).zip ./* -x '*.git*' -x '*.zip' -x 'Makefile' -x 'sample.py'