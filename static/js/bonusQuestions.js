// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    if (sortField === 'Description' || sortField === 'Title') {
        if (sortDirection === "asc") {
            items.sort((a, b) => {
                let ta = a[sortField],
                    tb = b[sortField];
                if (ta < tb) {
                    return -1;
                }
                if (ta > tb) {
                    return 1;
                }
                return 0;
            });
        } else {
            items.sort((a, b) => {
                let ta = a[sortField],
                    tb = b[sortField];
                if (ta < tb) {
                    return 1;
                }
                if (ta > tb) {
                    return -1;
                }
                return 0;
            });
        }
    } else {
        if (sortDirection === "asc") {
            items.sort((a, b) => {
                return a[sortField] - b[sortField];
            });
        } else {
            items.sort((a, b) => {
                return b[sortField] - a[sortField];
            });
        }
    }
    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    const newItems = []
    for (let i = 0; i < items.length; i++) {
        if (filterValue.slice(0, 13) === "!Description:" && items[i]['Description'].indexOf(filterValue.slice(13)) === -1) {
            newItems.push(items[i]);
        } else if (filterValue.slice(0, 12) === "Description:" && items[i]['Description'].indexOf(filterValue.slice(12)) !== -1) {
            newItems.push(items[i]);
        } else if (items[i]['Title'].indexOf(filterValue) !== -1) {
            newItems.push(items[i]);
        } else if (filterValue[0] === "!" && items[i]['Title'].includes(filterValue.slice(1)) === false && filterValue.slice(0, 13) !== "!Description:") {
            newItems.push(items[i]);
        }
    }
    return newItems
}

function toggleTheme() {
    console.log("toggle theme")
}

let tableHeader = 14,
    tableBody = 14,
    buttonAndSearch = 13.3333,
    counter = 3,
    changeFontSize = 4;

function increaseFont() {
    console.log("increaseFont");
    if (counter < 6) {
        counter++;
        buttonAndSearch += changeFontSize;
        tableHeader += changeFontSize;
        tableBody += changeFontSize;
        document.getElementById('doNotModifyThisId_QuestionsTableHeader').style.fontSize = `${tableHeader}px`;
        document.getElementById('doNotModifyThisId_QuestionsTableBody').style.fontSize = `${tableBody}px`;
        document.getElementById('increase-font-button').style.fontSize = `${buttonAndSearch}px`;
        document.getElementById('decrease-font-button').style.fontSize = `${buttonAndSearch}px`;
        document.getElementById('doNotModifyThisId_QuestionsFilter').style.fontSize = `${buttonAndSearch}px`;
    }
}

function decreaseFont() {
    console.log("decreaseFont");
    if (counter > 1) {
        counter--;
        buttonAndSearch -= changeFontSize;
        tableHeader -= changeFontSize;
        tableBody -= changeFontSize;
        document.getElementById('doNotModifyThisId_QuestionsTableHeader').style.fontSize = `${tableHeader}px`;
        document.getElementById('doNotModifyThisId_QuestionsTableBody').style.fontSize = `${tableBody}px`;
        document.getElementById('increase-font-button').style.fontSize = `${buttonAndSearch}px`;
        document.getElementById('decrease-font-button').style.fontSize = `${buttonAndSearch}px`;
        document.getElementById('doNotModifyThisId_QuestionsFilter').style.fontSize = `${buttonAndSearch}px`;
    }
}