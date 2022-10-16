const SERVER_URL = 'https://epli.herokuapp.com';

// Listener that fires whenever we change to a
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


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'getSummary') {
    console.log('Getting summary...', message.url)
    // sendResponse({ 'summary': 'This is a very simple summary of a paper abstract. Here is a second sentence to elaborate a bit more on the summary.' })
    fetch(`${SERVER_URL}/main_paper_information`, { paper_url: message.url })
      .then((response) => response.json())
      .then((data) => {
        console.log('Got summary', data)
        sendResponse(data);
      })
      .catch((e) => console.error(`ERROR: ${e}`))
  }
});

