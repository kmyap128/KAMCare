const fs = require('fs');

const index = fs.readFileSync(`${__dirname}/../index.html`);
const css = fs.readFileSync(`${__dirname}/../css/style.css`);
const logo = fs.readFileSync(`${__dirname}/../media/kam_care-02.png`);

const getIndex = (request, response) => {
  response.writeHead(200, { 'Content-Type': 'text/html' });
  response.write(index);
  response.end();
};

const getCSS = (request, response) => {
  response.writeHead(200, { 'Content-Type': 'text/css' });
  response.write(css);
  response.end();
};

const getLogo = (request, response) => {
    response.writeHead(200, { 'Content-Type': 'image/png' });
    response.write(logo);
    response.end();
}

module.exports = {
  getIndex,
  getCSS,
  getLogo,
};
