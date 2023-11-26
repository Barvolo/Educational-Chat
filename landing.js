// Handle form submission
document.getElementById("userPreferences").addEventListener("submit", function(event){
    event.preventDefault();  // Prevent the form from submitting in the traditional manner

    // Get the user's data
    let name = document.getElementById("name").value;
    let age = document.getElementById("age").value;
    let interests = document.getElementById("interests").value;
    let currentTopic = document.getElementById("currentTopic").value;

    // Save the data to local storage
    localStorage.setItem("name", name);
    localStorage.setItem("userAge", age);
    localStorage.setItem("userInterests", interests);
    localStorage.setItem("userCurrentTopic", currentTopic);

    // Redirect to the chat page
    window.location.href = "/chat";
});
