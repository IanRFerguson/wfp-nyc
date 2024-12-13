function loadMap() {
    console.log("Map finished loading...")

    // Hide loading text + spinner
    var loadText = document.getElementById("loadingText")
    loadText.style.display = 'none'

    var load = document.getElementById("loadingElement")
    load.style.display = 'none'

    // Display map
    var wfp = document.getElementById("wfp-map")
    wfp.style.display = 'inline'

    console.log("Displays rotated...")
}