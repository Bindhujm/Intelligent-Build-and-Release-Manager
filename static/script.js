function buildProject() {
    fetch("/build", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        alert(JSON.stringify(data));
    })
    .catch(error => {
        alert("Error: " + error);
    });
}

function deployProject() {
    fetch("/deploy", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        alert(JSON.stringify(data));

        if (data.status === "success") {
            window.open(data.url, "_blank");
        }
    })
    .catch(error => {
        alert("Error: " + error);
    });
}