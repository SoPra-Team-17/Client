.PHONY: build
build:
	docker build -t soprateam17/client .

.PHONY: run
run:
	xhost local:docker
	docker run --rm --volume="${HOME}/.Xauthority:/root/.Xauthority:rw" --env="DISPLAY" --net=host soprateam17/client
