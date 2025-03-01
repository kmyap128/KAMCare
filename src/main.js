let searchTerm = '';
let obj = []; 

function fetchJSONData() {
    fetch('../drugs.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();  
        })
        .then(data => {
            obj = data.medicines; 
        })
        .catch(error => console.error('Failed to fetch data:', error)); 
}

window.onload = fetchJSONData;

const processTerm = () => {
    searchTerm = document.querySelector('#drug-term').value.trim(); 
    if (!searchTerm) {
        document.querySelector("#content").innerHTML =
            '<p>Please enter a term to search.</p>';
        return;
    }

    let info = findDefinition(searchTerm);
    
    if (info) {
        document.querySelector('#content').innerHTML =
            `<h3>${info.name}</h3>
            <p>Summary: ${info.summary}</p>
            <p>Common Uses: ${info.use}</p>`;     
    } else {
        document.querySelector('#content').innerHTML =
            '<p>No matching drug found.</p>';
    }
};

const findDefinition = (term) => {
    let info = obj.find(drug => drug.name.toLowerCase() === term.toLowerCase()); 
    return info || null;
};

document.querySelector("#submit").addEventListener('click', processTerm);
