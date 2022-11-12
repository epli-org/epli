# EPLI - Explain Paper Like I'm (5) / Sciren

TL;DR: Chrome extension that improves the UX of reading a paper, using language models to generate summaries and definitions + wikipedia-style popups for easy access.

 <!-- that makes papers easier to understand by surfacing relevant information to you as you read a paper, instead of forcing you to open many separate tabs. Uses Language Models to summarize relevant content for you, and provides relevant context. -->

Science has produced incredible innovations, yet there is incredible amounts of progress to be made on the scientific process itself. Specifically, scientific knowledge is still spread via academic papers, and people still read them as if they are textual documents that live in your computer, as opposed to interactive elements for querying and collaboration. We hope to change that with Epli, our Chrome extension that uses large language models to make it easier to access the relevant information from a paper.

When looking at papers, researchers often find themselves needing to manually look up the referenced papers in separate tabs and search for the relevant section within them, as the links directly to the papers aren’t usually provided by default. This causes a lot of context switching, and generally increases friction to learn new concepts. To alleviate this, our Chrome extension allows a user to hover over a reference within a paper, and presents a pop-up containing:

- The direct link to the paper
- The abstract of the paper
- A context-sensitive GPT-3 generated summary of the referenced paper

This allows the reader to quickly understand the relevant concepts within the cited resource, so that they can immediately resume their processing of the current paper.  This also reduces the number of clicks steps they will need to go through in order to access that paper if they so desire.

Scientific papers also contain "jargon", and this often forces readers to spend more time than necessary getting up to speed with the language of a paper before they can actually understand the concepts presented within. When our users hover over scientific jargon within a paper, a pop-up will be presented that shows the definition of the piece of jargon, along with links to locations where it’s defined previously. This is similar to jump-to-definition in IDEs, except applied for concepts in a paper.

In the long term, we plan on enabling a commenting system on top of papers, so that users can ask and answer questions on top of papers, while earning reputation for doing so. The features outlined above will be useful for getting initial interest in the extension.

## Demo

Quick demo of the extension can be found here: https://www.loom.com/share/808cb0f99691438eb661db56984f0c27

## Frontend
Beautifies scientific papers, starting with arxiv-vanity urls.
- Displays the abstracts + summaries of references

Future work:
- Displays a pop-up on top of jargon, containing the definition for that piece of jargon
  - If definition is within another paper, could potentially do a jump-to-definition of some sort

## Backend
Key endpoints:
- Return an abstract, introduction, etc. + a summary for each of these sections and the entire paper
- Return profile / bio info for a given author + email
- Recommend next papers for a given paper




## Notes

### Features to add
- Add context menu, which will let people add new words to jargon list (potentially?)
- 


### Resources for us
- https://explainjargon.com/ 
- 