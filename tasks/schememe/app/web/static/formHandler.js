function handleUpload() {
    var e = document.getElementById("caption");
    if(e!==null) e.remove();
    const fileInput = document.getElementById('image');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const contents = event.target.result;
            const customXML = createCustomXML(contents);
            sendRequest(customXML);
        };
        reader.readAsText(file);
    }
}

function createCustomXML(svgXML) {
    var upperText = document.getElementById('upper').value;
    var bottomText = document.getElementById('bottom').value;
    var xmlData = '<?xml version="1.0" encoding="UTF-8"?>\n<meme>\n'
    svgXML = svgXML.replace(/\<\?xml.+\?\>|\<\!DOCTYPE.+\>/g, '');
    xmlData += svgXML;
    xmlData += `\n<upper>${upperText}</upper>\n`
    xmlData += `<bottom>${bottomText}</bottom>\n</meme>`
    return xmlData;
}

function sendRequest(xmlPayload) {
    var token = document.URL.split('/')[3] 
    const url = `/${token}/process`;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/xml'
        },
        body: xmlPayload})
    .then(response => {
        if (response.ok) {
            console.log('Request successful');
            return response.text();
        } else {
            console.error('Request failed');
        }
    })
    .then( svg => {
        const text_node = document.createElement("p")
        text_node.setAttribute("id", "caption")
        const text = document.createTextNode("Ваш мем:")
        text_node.appendChild(text)
        document.getElementById('memebox').prepend(text_node)
        document.getElementById('meme').innerHTML = svg
        document.getElementById('meme').scrollIntoView({ behavior: "smooth"})
    })
    .catch(error => {
        console.error('An error occurred:', error);
    });
}