const fs = require('fs');

const drugs = JSON.parse(fs.readFileSync(`${__dirname}/../data/drug.json`, 'utf-8'));

const getJSON = (request, response) => {
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.write(JSON.stringify(drugs)); 
    response.end();
};

module.exports = {
    getJSON,
};
