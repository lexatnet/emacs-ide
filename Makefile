
build-appimage-builder:
	./scripts/build-appimage-builder-docker.sh

build-gulp-appimage-builder:
	./scripts/build-gulp-appimage-builder-docker.sh

docker-push:
	./scripts/docker-push.sh

build-appimage:
	./scripts/build-appimage.sh

gulp-builder-build-appimage:
	./scripts/gulp-builder-build-appimage.sh

gulp-builder-bash:
	./scripts/gulp-builder-bash.sh

build-appimage-with-log:
	./scripts/build-appimage.sh |& tee build.log

appimage-builder-bash:
	./scripts/appimage-builder-bash.sh

appimage-builder-bash-root:
	./scripts/appimage-builder-bash-root.sh

build-appimage-test:
	./scripts/build-appimage-test.sh

clean:
	./scripts/clean.sh

test-alpine:
	./scripts/test-alpine.sh

test-centos:
	./scripts/test-centos.sh

test-ubuntu-bionic:
	./scripts/test-ubuntu-bionic.sh
