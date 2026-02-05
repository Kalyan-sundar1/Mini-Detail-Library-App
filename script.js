const API_URL = "http://localhost:8000";


// Load Details (FULL DATA)
async function loadDetails() {
    const res = await fetch(`${API_URL}/details`);
    const data = await res.json();

    let html = "";

    data.forEach(d => {
        html += `
        <div class="result-box">
            <strong>${d.title}</strong><br>

            <b>Category:</b> ${d.category}<br>
            <b>Tags:</b> ${d.tags}<br>
            <b>Description:</b> ${d.description}
        </div>`;
    });

    document.getElementById("detailsList").innerHTML = html;
}


// Search
async function searchDetails() {
    const q = document.getElementById("searchInput").value;

    const res = await fetch(`${API_URL}/details/search?q=${q}`);
    const data = await res.json();

    let html = "";
    data.forEach(d => {
        html += `
        <div class="result-box">
            <strong>${d.title}</strong><br>
            ${d.description}<br>
            Tags: ${d.tags}
        </div>`;
    });

    document.getElementById("searchResults").innerHTML = html;
}

// Suggest
async function suggestDetail() {
    const res = await fetch(`${API_URL}/suggest-detail`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            host_element: document.getElementById("host").value,
            adjacent_element: document.getElementById("adjacent").value,
            exposure: document.getElementById("exposure").value
        })
    });

    const data = await res.json();

    if (!data.detail) {
        document.getElementById("suggestResult").innerHTML =
            `<div class="alert alert-danger">${data.explanation}</div>`;
    } else {
        document.getElementById("suggestResult").innerHTML = `
            <div class="alert alert-info">
                <strong>${data.detail.title}</strong><br>
                ${data.detail.description}<br><br>
                <i>${data.explanation}</i>
            </div>`;
    }
}
