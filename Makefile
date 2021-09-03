COMMIT_HASH = $(GITHUB_SHA)
package:
	@zip -r whois_otterbot_$(COMMIT_HASH).zip ./* -x '*.git*' -x '*.zip'