# Back-end ShopSmart

## Executing locally with a host installation of Node.js
Inside this directory, run `node server.js`

## Executing with Docker
First, we recommend installing the official Node.js docker image (`docker install node`) so Docker can
reuse it to build the application Docker image faster even if you removed the last image (if you always 
re-build the image with the same tag, docker will already be smart enough to reuse the `FROM node` line
in `Dockerfile` as a chached layer).
Then:
* To build the application image: `docker build . -t back_shopsmart`
* To run the application: `docker run --rm --env DEPLOY_MODE=docker -p 3000:3000 --name test_shopsmart back_shopsmart` \
The `--rm` means that stopping the container will also remove it (see comments below on how to stop it), the
`--env DEPLOY_MODE=docker` is used by the JavaScript code to expose the application "globally" when we run it wit
Docker, `-p 3000:3000` allows us to associate the docker container's 3000 port with host's 3000 port.
* To stop the application, if CTRL+C does not work, open the terminal elsewhere and run `docker stop test_shopsmart`