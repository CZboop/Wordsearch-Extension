(function (){
 'use strict';
 var path, slash;
 path = location.href;
	if(getOS() == "MAC") {
		slash = "/";
		path = path.substring(0, path.length - 11);
	}
	if(getOS() == "WIN") {
		slash = "/";
		path = path.substring(8, path.length - 11);
	}
	
	init();
 }());

var csInterface = new CSInterface();

function init(){
	var terminal;

	var instructions = document.createElement("P");
	instructions.id = "instructions-words";
	instructions.innerHTML = "Enter the words for the wordsearch below (separated by semicolons)"

	var widthDiv = document.createElement("DIV");
	widthDiv.id = 'widthDiv';
	document.getElementById("container").append(widthDiv);

	widthDiv.append(instructions);

	var inputWords = document.createElement("TEXTAREA");
	inputWords.id = "inputText";
	inputWords.type = "text";

	var submitButton = document.createElement("BUTTON");
	submitButton.id = "submitButton";
	submitButton.innerHTML = "Submit";

	widthDiv.append(inputWords);
	widthDiv.append(submitButton);
	
	submitButton.addEventListener("click", ()=> {
		submit(inputWords.value);
	});
}

function submit(words){
	var wordsArray = words.split(";");
	var cmdArgString = wordsArray.join(" ")
	var gridArray = [];
	var solutionInfo;

	if (getOS() == "WIN") {
		terminal = require("child_process").spawn("cmd");
	}
	else {
		terminal = require("child_process").spawn("bash");
	}

	terminal.stdout.on("data", function (data) {
		// csInterface.evalScript('alertJSX('+JSON.stringify(data.toString())+')');
		// TODO: take CLI outputs and do something with it
		if (data.toString().startsWith("wordsearch_output")) {
			var stringData = data.toString().trim().replace("wordsearch_output", "").split("****")[0].trim();
			gridSplit = stringData.split("\r");
			gridArray.push(...gridSplit);
			// TODO: need to make into array or into something that can be split into array in the next lower level part of the script
			var solutionData = data.toString().trim().split("****")[1];
			solutionInfo = solutionData;
			alert(solutionInfo);
			csInterface.evalScript('drawSolution('+JSON.stringify(solutionInfo)+')');
		}
	});

	terminal.stderr.on("data", function (data) {
		csInterface.evalScript('alertJSX('+JSON.stringify(data.toString())+')');
	});

	terminal.on("exit", function () {
		makeGrid(gridArray);
		makeWordList(wordsArray);
	});

	setTimeout(function() {
		// NOTE: __dirname gets current path but needs quotes and replacing. dependant on OS too..?
		let t = `"${__dirname.replaceAll('\\', '/')}/py/exe/dist/wordsearch.exe" ${cmdArgString}`;
		terminal.stdin.write(t + ' \n');
		// NOTE: can chain and add multiple commands with other stdin write statements as above
		terminal.stdin.end();
	}, 1000)

}

function makeGrid(gridArray) {
	var csInterface = new CSInterface();
	var gridString = gridArray.join(",");
	csInterface.evalScript('createGrid('+JSON.stringify(gridString)+')');
}

function makeWordList(wordArray) {
	csInterface.evalScript('createWordList('+JSON.stringify(wordArray)+')');
}

function getOS() {
 		var userAgent = window.navigator.userAgent,
 		platform = window.navigator.platform,
 		macosPlatforms = ['Macintosh', 'MacIntel', 'MacPPC', 'Mac68K'],
 		windowsPlatforms = ['Win32', 'Win64', 'Windows', 'WinCE'],
 		os = null;

 		if(macosPlatforms.indexOf(platform) != -1) {
 			os = "MAC";
 		} else if(windowsPlatforms.indexOf(platform) != -1) {
 			os = "WIN";
 		}
 		return os;
 	}