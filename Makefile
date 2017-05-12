.PHONY: build
build:
	docker build -t nodejs-require-test -f Dockerfile.test .

.PHONY: test
test: build
	docker run --rm nodejs-require-test

.PHONY: test-i
test-i: build
	docker run -it --rm -v $(PWD)/app nodejs-require-test bash
