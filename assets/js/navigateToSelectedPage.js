function navigateToSelectedPage(dropdown) {
    const targetUrl = dropdown.value;
    window.location.href = targetUrl;
}

// takes a list of items and populates a html dropdown with them
function populateDropdown(itemList, dropdownName){
    const dropdown = document.getElementById(dropdownName);
    dropdown.innerHTML = ""; // clearing any existing options

    frameworks.forEach(item => {
        // create a new <option> element for each list element
        let option = document.createElement("option");

        option.textContent = item;
        option.value = item.toLowerCase();

        dropdown.appendChild(option);
    });
}

// returns a list of file names from csv files uploaded to specific folder
function fetchFileNames(owner, repo, folderPath = ""){
    const url = `https://api/github.com/repos/${owner}/${repo}/contents/${folderPath}`;
    
    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('GitHub API error: ${response.status} ${response.statusText}');
        }

        const data = await response.json();

        // return only files (ignore sub-folders)
        const files = data.filter(item => item.type === "file");
        
        if (files.length === 0) {
            return ["first if"];
        }
        
        files.forEach(file => {
            const li = document.createElement('li')
            
            li.innerHTML = `<a href="${file.download_url}" target="_blank">${file.name}</a>`;
            filelist.append[file.name]
        });

    } catch (e) {
        console.error("Failed to fetch folder contents:", e);
        return [];
    }
    return filelist;
}