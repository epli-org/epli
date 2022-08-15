chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  console.log(tabId, changeInfo, tab);
  if (changeInfo.status === 'complete' && tab.url.includes('https://www.arxiv-vanity.com')) {
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      files: ["./foreground.js"]
    })
    .then(() => {
        console.log("INJECTED THE FOREGROUND SCRIPT.");
    })
    .catch(err => console.log(err));
  }
});


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message === 'url') {
    fetch(sender)
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        sendResponse(data);
      });
  }
});

