const SERVER_URL = 'https://epli.herokuapp.com';
// const SERVER_URL = 'http://127.0.0.1:8000'

// Listener that fires whenever we change to a new tab
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  console.log(tabId, changeInfo, tab);
  if (changeInfo.status === 'complete' && tab.url.includes('https://www.arxiv-vanity.com')) {
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      files: ["./foreground.js"]
    })
    .then(() => {
        console.log("INJECTED FOREGROUND SCRIPT.");
    })
    .catch(err => console.log(err));
  }
});


// Listen for the foreground script wanting to send requests to the backend server
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'getSummary') {
    fetch_response = fetch(`${SERVER_URL}/main_paper_information`, {
      method: "POST",
      body: JSON.stringify({
        paper_url: message.url
      })
    })
      .then((response) => {
        console.log("Insideo of successful response I think?");        
        return response.json()
      })
      .then((data) => {
        console.log('Got summary', data)
        console.log(data);
        sendResponse(data);
      })
      .catch((e) => {
        console.error(`ERROR: ${e}`);
      })
    return true;
  }
});

