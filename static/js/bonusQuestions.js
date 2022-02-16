// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    // for (let i=0; i<filterValue.length; i++) {
    //     items.pop()
    // }
    const newItems = []
    for (let i=0; i<items.length; i++) {
        console.log(items[i])

        if (  filterValue.slice(0,13) === "!Description:"  &&  items[i]['Description'].indexOf(filterValue.slice(13)) !== -1) {
            newItems.push(items[i])
            console.log(newItems)
        }
        else if (  filterValue.slice(0,12) === "Description:" &&  items[i]['Description'].indexOf(filterValue.slice(12)) !== -1) {
            newItems.push(items[i])
        }
        else if (items[i]['Title'].indexOf(filterValue) !== -1 || items[i]['Description'].indexOf(filterValue) !== -1) {
            newItems.push(items[i])
        }
        else if (filterValue[0] === "!" && (items[i]['Title'].includes(filterValue.slice(1)) === false && items[i]['Description'].includes(filterValue.slice(1)) === false)){
            newItems.push(items[i])
        }

    }
// ha ! és benne van, akkor ne mutassa, minden mást igen
    return newItems
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    console.log("increaseFont")
}

function decreaseFont() {
    console.log("decreaseFont")
}