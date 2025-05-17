chrome.storage.sync.get("autofillData", ({ autofillData }) => {
    if (!autofillData) return;


    function fillInput(selectorName, value) {
    // Try selecting by ID, Name, Placeholder, Aria-Label, or Label For
    const field = document.querySelector(
        `[id='${selectorName}'], 
         [name='${CSS.escape(selectorName)}'], 
         [placeholder='${selectorName}'], 
         [aria-label='${selectorName}'], 
         label[for='${selectorName}']`
    );
    console.log(field)

    if (field) {
        if (field.tagName === "SELECT") {
            field.value = value;
            field.dispatchEvent(new Event("change", { bubbles: true }));
        } else if (field.tagName === "TEXTAREA" || field.tagName === "INPUT") {
            field.value = value;
            field.dispatchEvent(new Event("input", { bubbles: true }));
            field.dispatchEvent(new Event("change", { bubbles: true }));
        }
    } else {
        console.warn(`⚠️ Field not found for selector: ${selectorName}`);
    }
}


    fillInput("name", "Ayush Srivastava");

    fillInput("first_name", autofillData.firstName);
    fillInput("first-name", autofillData.firstName);

    fillInput("last_name", autofillData.lastName);
    fillInput("last-name", autofillData.lastName);

    fillInput("email", autofillData.email);

    fillInput("phone", autofillData.phone);
    fillInput("job_application[first_name]", "John"); // Handles bracketed names
    
    fillInput("location-input", "Bengaluru")

    fillInput("org", "Vimaan Robotics")

    fillInput("urls[LinkedIn]", "https://www.linkedin.com/in/ayush-shivaji/")
    fillInput("urls[GitHub]", "https://github.com/ayushshivaji")

});

