let searchTerm = '';
let obj = []; 

function fetchJSONData() {
    fetch('../data/drug.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();  
        })
        .then(data => {
            obj = data.drugs; 
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
            `<h3>${info.medicinal_name} (Generic Name: ${info.generic_name})</h3>
            <p>Purpose: ${info.purpose}</p>
            <p>Usage: ${info.usage}</p>
            <p>Warnings: ${info.warning}</p>`;     
    } else {
        document.querySelector('#content').innerHTML =
            '<p>No matching drug found.</p>';
    }
};

const findDefinition = (term) => {
    console.log(obj);
    let info = obj.find(drug => drug.medicinal_name.toLowerCase() === term.toLowerCase()); 
    return info || null;
};

const runPy = () => {
    var output = $.ajax ({
        type: "POST",
        url: "/video.py",
        async: false,
    })
    console.log(output);
    console.log(output.responseText);
    return output.responseText;
}


document.querySelector("#video").addEventListener('click', runPy)
document.querySelector("#submit").addEventListener('click', processTerm);
