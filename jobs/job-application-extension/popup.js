document.getElementById("autofill-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const data = {
        firstName: document.getElementById("first-name").value,
        lastName: document.getElementById("last-name").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value
    };

    // Save the data
    chrome.storage.sync.set({ autofillData: data }, () => {
        // Get the active tab
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs.length === 0) {
                console.error("No active tab found.");
                return;
            }

            const activeTabId = tabs[0].id;

            // Execute content script on the active tab
            chrome.scripting.executeScript({
                target: { tabId: activeTabId },
                files: ["content.js"]
            });
        });
    });
});
