let messageHistory = [];  
let testMode = false;  // Set this to true when you want to enable testing
let refreshButtonClicked = false;
let previousSuggestions = [];

function sendMessage() {
    let message = document.getElementById("userInput").value;

    if (refreshButtonClicked) {
        fetchSuggestions();
        refreshButtonClicked = false;  // Reset the flag after handling
        
    }

    if (message) {
        messageHistory.push(message);
        let chatWindow = document.getElementById("chatWindow");
        let userName = document.getElementById("userName").textContent;
        chatWindow.innerHTML += `<p><strong>${userName}:</strong> ${message}</p>`;
        document.getElementById("userInput").value = '';

        // Only the main API call for the main response
        fetch('http://192.168.40.100:5001/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: messageHistory,
                test_mode: testMode
            }), 
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            chatWindow.innerHTML += `<p><strong>ChatGPT:</strong> ${data.response}</p>`;
            fetchSuggestions();  // Fetch the suggestions after getting the main response
        })
        .catch(error => {
            console.error('There was a problem:', error);
            chatWindow.innerHTML += `<p><strong>Error:</strong> ${error.message}</p>`;
        });
    }
}

function fetchSuggestions() {
    fetch('http://192.168.40.100:5001/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ get_suggestions: true, test_mode: testMode,refresh_clicked: refreshButtonClicked }),
    })
    .then(response => response.json())
    .then(data => {
        let suggestions = data.suggestions || [];
        previousSuggestions = suggestions;
        let suggestionButtons = document.getElementById("suggestionButtons");
        let refreshButton = document.getElementById("refreshButton");
        suggestionButtons.innerHTML = '';

        suggestions.forEach(suggestion => {
            suggestionButtons.innerHTML += `<button onclick="useSuggestion('${suggestion}')">${suggestion}</button>`;
        });

        if (suggestions.length > 0) {
            refreshButton.style.display = "inline-block";
        } else {
            refreshButton.style.display = "none";
        }
    })
    .catch(error => {
        console.error('There was a problem fetching suggestions:', error);
    });
}
function useSuggestion(suggestion) {
    document.getElementById("userInput").value = suggestion;
    sendMessage();
}

function handleRefreshClick() {
    refreshButtonClicked = true;
    sendMessage();
}
