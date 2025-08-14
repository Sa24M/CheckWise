document.getElementById("uploadForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const resultsDiv = document.getElementById("results");
    const resultsSection = document.getElementById("resultsSection");

    resultsDiv.innerHTML = "<p class='loading'>⏳ Grading in progress...</p>";
    resultsSection.classList.remove("hidden");

    try {
        const response = await fetch("/upload_zip", { method: "POST", body: formData });
        const text = await response.text();
        let data;

        try {
            data = JSON.parse(text);
        } catch {
            resultsDiv.innerHTML = `<p style="color:red">Invalid JSON from server:<br>${text}</p>`;
            return;
        }

        if (data.error) {
            resultsDiv.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
            return;
        }

        if (data.length === 0) {
            resultsDiv.innerHTML = "<p>No results found in the ZIP.</p>";
            return;
        }

        let table = `<table class="results-table">
            <tr><th>Question</th><th>Answer File</th><th>Reference File</th><th>Marks</th></tr>`;

        data.forEach(row => {
            let markClass = row.marks >= (formData.get("max_marks") * 0.75) ? "mark-high" : "mark-low";
            table += `<tr>
                <td>${row.question}</td>
                <td>${row.answer_file}</td>
                <td>${row.reference_file}</td>
                <td class="${markClass}">${row.marks}</td>
            </tr>`;
        });
        table += "</table>";

        resultsDiv.innerHTML = table;

        // Store results for download
        window.latestResults = data;

    } catch (error) {
        resultsDiv.innerHTML = `<p style="color:red;">Error grading answers: ${error}</p>`;
    }
});

// Download as CSV
document.getElementById("downloadBtn").addEventListener("click", function() {
    if (!window.latestResults) {
        alert("No results to download!");
        return;
    }

    let csv = "Question,Answer File,Reference File,Marks\n";
    window.latestResults.forEach(row => {
        csv += `${row.question},${row.answer_file},${row.reference_file},${row.marks}\n`;
    });

    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "grading_results.csv";
    a.click();
    URL.revokeObjectURL(url);
});
