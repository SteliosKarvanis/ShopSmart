const http = require('http');

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World\n');
});

// run in either "globally exposed" mode (for docker) or locally:

const port = 3000;

if(process.env.DEPLOY_MODE == "docker") {
  const hostname = '0.0.0.0';
  server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
  });
}
else {
  const hostname = '127.0.0.1';
  server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
  });
}