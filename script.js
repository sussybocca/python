function saveFile() {
    const filename = document.getElementById("filename").value;
    const code = document.getElementById("code").value;
    fetch("/save", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: `filename=${filename}&code=${encodeURIComponent(code)}`
    }).then(res => res.json()).then(data => alert(data.status));
}

function openFile() {
    const filename = document.getElementById("filename").value;
    fetch(`/open?filename=${filename}`)
        .then(res => res.json())
        .then(data => {
            if (data.code) document.getElementById("code").value = data.code;
            else alert(data.error);
        });
}

function runFile() {
    const filename = document.getElementById("filename").value;
    fetch("/run", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: `filename=${filename}`
    })
    .then(res => res.json())
    .then(data => document.getElementById("output").textContent = data.output);
}
