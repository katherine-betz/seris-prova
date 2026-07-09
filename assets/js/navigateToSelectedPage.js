function navigateToSelectedPage(dropdown) {
    const targetUrl = dropdown.value;
    window.location.href = targetUrl;
}

// takes a list of items and populates a html dropdown with them
async function populateDropdown(dropdownName){
    const dropdown = document.getElementById(dropdownName);
    console.log("Inside populateDropdown");

    itemList = await fetchFiles();

    for (i = 0; i < itemList.length; i++){
        // create a new <option> element for each list element
        let option = document.createElement("option");

        option.textContent = itemList[i].name;
        option.value = itemList[i].name.toLowerCase();
        dropdown.appendChild(option);
    }
}

async function fetchFiles(dropdownName){
    const url = 'https://api.github.com/repos/katherine-betz/seris-prova/contents/Data/Channel_1';
    console.log("Inside fetchFiles");
    try {
        const response = await fetch(url);
        const data = await response.json();
        console.log("Data is", data);
        
        if (data.content){
            const decodedContent = atob(data.content.replace(/\n/g, ''));
            console.log("File Contents:", decodedContent);
        } else {
            console.log("Directory Structure:", data);
        }
        return data;
    } catch (error) {
        console.error("Error fetching repository data:", error);
    }
    return "data";
}