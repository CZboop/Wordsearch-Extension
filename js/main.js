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

	widthDiv.append(wordsTitle);
	widthDiv.append(instructions);

	var inputWords = document.createElement("INPUT");
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
	// TODO: take the input, process and pass to cli
	var wordsArray = words.split(";");
	var cmdArgString = wordsArray.join(" ")
	alert("COMMAND LINE STRING: "+ cmdArgString)
	var gridArray = [];

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
			alert("STARTS WITH EXPECTED!!")
			alert("RETURNED DATA: " + data.toString());
			var stringData = data.toString().trim().replace("wordsearch_output", "").split("****")[0].trim();
			gridSplit = stringData.split("\r");
			alert("GRID SPLIT" + gridSplit);
			gridArray.push(...gridSplit);
		}
	});

	terminal.stderr.on("data", function (data) {
		csInterface.evalScript('alertJSX('+JSON.stringify(data.toString())+')');
	});

	terminal.on("exit", function () {
		// TODO: main functionality
		alert("EXITED TERMINAL PROCESS");
		makeGrid(gridArray);
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
	alert("gridArray");
	alert(gridArray);
	var csInterface = new CSInterface();
	var gridString = gridArray.join(",");
	alert("GRID STRING: "+gridString);
	csInterface.evalScript('createGrid('+JSON.stringify(gridString)+')');
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