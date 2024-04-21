# Wordsearcher-Extension-Illustrator📝🔍
CEP extension for Adobe Illustrator, creates editable wordsearches :)

## Summary
This project is an easy way to create wordsearches within Adobe Illustrator, with a simple graphical UI within the program. Once words are entered, two grids will be drawn - one with boxes around the words to act as a solution, and one without - as well as a list of the words you're looking for.

### Built With
The extension uses JavaScript/Node, ExtendScript (Adobe's JS derived scripting language) as well as Python.

Python is used to calculate word positions, and the Python executable script is called from the terminal via Node, which then uses CSInterface to pass the result to ExtendScript functions that draw the wordsearch in the active Illustrator document. Some HTML and CSS is used to create the UI, and XML is used within the manifest.

## Setup
To set up this extension, follow these steps:
* Clone this repository locally
* Find your CEP extension folder for your installation of Adobe programs. For Windows, this should be in: C:\Program Files (x86)\Common Files\Adobe\CEP\extensions
* Move the cloned repository to this extensions folder
* You should then see the extension as "Wordsearcher" under Window > Extensions in the top ribbon menu

## How to Use
Once the extension in set up locally, to use it:
* Create or open an Illustrator document. Note: the wordsearch will be approximately 50px per letter, so a size of around 1000x1000px or more is likely needed
* Open the extension from Window > Extensions in the top ribbon menu
* Enter the list of words separated by semicolons in the text area
* Click the 'Submit' button
* Wait a few seconds for the wordsearch to be drawn
* Adjust the output to your taste. Note: the solution and non-solved grids will be exactly on top of each other initially, so you will likely want to move/rescale one of them

## Acknowledgements
Huge thanks to [NT Productions](https://github.com/NTProductions) for the extension testing starter code which was used as a base in this project, and his excellent tutorials on Adobe scripting, including how to incorporate terminal scripts and their outputs!
