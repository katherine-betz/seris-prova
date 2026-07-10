function displayFileData(channel, file){
    // Path to your CSV file relative to index.html
    const csvPath = "Data/" + channel + "/" + file; 

    d3.csv(csvPath).then(function(data) {
        if (data.length === 0) return;
        console.log("display file data:", data);

        // Create table elements
        const container = d3.select("#
                                    table-container");
        const table = container.append("table");
        const thead = table.append("thead");
        const tbody = table.append("tbody");

        console.log("Container created");

        // Extract headers from the first data object
        const headers = Object.keys(data[0]);

        // Append headers row
        thead.append("tr")
            .selectAll("th")
            .data(headers)
            .enter()
            .append("th")
            .text(d => d);

        // Append data rows
        const rows = tbody.selectAll("tr")
            .data(data)
            .enter()
            .append("tr");

        // Populate cells for each row
        rows.selectAll("td")
            .data(row => headers.map(header => row[header]))
            .enter()
            .append("td")
            .text(d => d);

        console.log("Data added");
    }).catch(function(error) {
        console.error("Error loading the CSV file:", error);
    });
}
