
let mutationObserver = new MutationObserver(function(mutations_list) {
  mutations_list.forEach(function(mutation) {
		mutation.addedNodes.forEach(function(node) {
      if (node.class === 'tippy-popper') {
        chrome.runtime.sendMessage('url', (data) => {
          console.log(data);
        })
        console.log(node);
      }
		});
	});
});
mutationObserver.observe(document.documentElement, {
  attributes: true,
  characterData: true,
  childList: true,
  subtree: true,
  attributeOldValue: true,
  characterDataOldValue: true
});