const summaryId = 'epli-paper-summary';
const loadingId = 'epli-loading';
let timeoutId;

const mutationObserver = new MutationObserver(function(mutations_list) {
  mutations_list.forEach(function(mutation) {
		mutation.addedNodes.forEach(function(node) {
      console.log('DOM CHANGE');
      // className that the pop-up belongs to
      if (node.className === 'tippy-popper') {
        console.log('POPUP SHOWS UP', node.innerHTML);
        const url = getUrl(node.innerHTML);
        if (url && !document.getElementById(summaryId)) {
          const summaryEl = document.createElement("div");
          summaryEl.id = summaryId;
          summaryEl.innerText = 'Summary';
          // startLoading(summaryEl);

          chrome.runtime.sendMessage(
            chrome.runtime.id,
            { type: 'getSummary', url: getUrl(node.innerHTML) }, 
            (data) => {
              console.log('SUMMARY', data);

              // Create summary element to append to popup
              const summaryContentEl = document.createElement("div");
              summaryContentEl.innerText = data.summary;
              summaryEl.appendChild(summaryContentEl);
              node.children[0].appendChild(summaryEl);
            })
        }
      }
		});
	});
});

const startLoadingIcon = (el) => {
  const loading = document.createElement('div');
  loading.id = loadingId;
  el.appendChild(loading);
  let dots = '.';
  timeoutId = setTimeout(() => {
    if (dots.length <= 5) dots += '.';
    else dots = '.';
    loading.innerText = dots;
  }, 1000);
};

const stopLoadingIcon = () => {
  const loading = document.getElementById(loadingId)
  if (loading) {
    loadingImg.remove();
    clearTimeout(timeoutId);
  };
};

const getUrl = (html) => {
  const i = html.indexOf('/papers/');
  if (i === -1) return null;
  let j = i;
  while (html[j] != '"') {
    j++;
  }
  const url = html.substring(i, j);
  console.log('URL', url);
  return 'https://arxiv-vanity.com' + url;

};

mutationObserver.observe(document.documentElement, {
  attributes: true,
  characterData: true,
  childList: true,
  subtree: true,
  attributeOldValue: true,
  characterDataOldValue: true
});