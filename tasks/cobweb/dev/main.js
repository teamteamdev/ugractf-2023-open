const cursor = require('ani-cursor');

let pollingInterval = window.setInterval(() => {
    fetch("cursor.ani")
        .then(response => {
            if (response.status === 201) {
                return; // Wait!
            } else if (response.status === 200) {
                window.clearInterval(pollingInterval);
                document.querySelector(".loading").style.display = "none";
                response.arrayBuffer().then(data => {
                    const uarr = new Uint8Array(data);
                    const style = document.createElement("style");
                    style.innerText = cursor.convertAniBinaryToCSS("main", uarr);
                    document.head.appendChild(style);
                })
            } else {
                alert(`Ошибка ${response.status}, попробуйте позже`);
                window.clearInterval(pollingInterval);
            }
        })
}, 900);
