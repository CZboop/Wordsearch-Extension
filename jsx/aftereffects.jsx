"object"!=typeof JSON&&(JSON={}),function(){"use strict";var rx_one=/^[\],:{}\s]*$/,rx_two=/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,rx_three=/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,rx_four=/(?:^|:|,)(?:\s*\[)+/g,rx_escapable=/[\\"\u0000-\u001f\u007f-\u009f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,rx_dangerous=/[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,gap,indent,meta,rep;function f(t){return t<10?"0"+t:t}function this_value(){return this.valueOf()}function quote(t){return rx_escapable.lastIndex=0,rx_escapable.test(t)?'"'+t.replace(rx_escapable,function(t){var e=meta[t];return"string"==typeof e?e:"\\u"+("0000"+t.charCodeAt(0).toString(16)).slice(-4)})+'"':'"'+t+'"'}function str(t,e){var r,n,o,u,f,a=gap,i=e[t];switch(i&&"object"==typeof i&&"function"==typeof i.toJSON&&(i=i.toJSON(t)),"function"==typeof rep&&(i=rep.call(e,t,i)),typeof i){case"string":return quote(i);case"number":return isFinite(i)?String(i):"null";case"boolean":case"null":return String(i);case"object":if(!i)return"null";if(gap+=indent,f=[],"[object Array]"===Object.prototype.toString.apply(i)){for(u=i.length,r=0;r<u;r+=1)f[r]=str(r,i)||"null";return o=0===f.length?"[]":gap?"[\n"+gap+f.join(",\n"+gap)+"\n"+a+"]":"["+f.join(",")+"]",gap=a,o}if(rep&&"object"==typeof rep)for(u=rep.length,r=0;r<u;r+=1)"string"==typeof rep[r]&&(o=str(n=rep[r],i))&&f.push(quote(n)+(gap?": ":":")+o);else for(n in i)Object.prototype.hasOwnProperty.call(i,n)&&(o=str(n,i))&&f.push(quote(n)+(gap?": ":":")+o);return o=0===f.length?"{}":gap?"{\n"+gap+f.join(",\n"+gap)+"\n"+a+"}":"{"+f.join(",")+"}",gap=a,o}}"function"!=typeof Date.prototype.toJSON&&(Date.prototype.toJSON=function(){return isFinite(this.valueOf())?this.getUTCFullYear()+"-"+f(this.getUTCMonth()+1)+"-"+f(this.getUTCDate())+"T"+f(this.getUTCHours())+":"+f(this.getUTCMinutes())+":"+f(this.getUTCSeconds())+"Z":null},Boolean.prototype.toJSON=this_value,Number.prototype.toJSON=this_value,String.prototype.toJSON=this_value),"function"!=typeof JSON.stringify&&(meta={"\b":"\\b","\t":"\\t","\n":"\\n","\f":"\\f","\r":"\\r",'"':'\\"',"\\":"\\\\"},JSON.stringify=function(t,e,r){var n;if(indent=gap="","number"==typeof r)for(n=0;n<r;n+=1)indent+=" ";else"string"==typeof r&&(indent=r);if((rep=e)&&"function"!=typeof e&&("object"!=typeof e||"number"!=typeof e.length))throw new Error("JSON.stringify");return str("",{"":t})}),"function"!=typeof JSON.parse&&(JSON.parse=function(text,reviver){var j;function walk(t,e){var r,n,o=t[e];if(o&&"object"==typeof o)for(r in o)Object.prototype.hasOwnProperty.call(o,r)&&(void 0!==(n=walk(o,r))?o[r]=n:delete o[r]);return reviver.call(t,e,o)}if(text=String(text),rx_dangerous.lastIndex=0,rx_dangerous.test(text)&&(text=text.replace(rx_dangerous,function(t){return"\\u"+("0000"+t.charCodeAt(0).toString(16)).slice(-4)})),rx_one.test(text.replace(rx_two,"@").replace(rx_three,"]").replace(rx_four,"")))return j=eval("("+text+")"),"function"==typeof reviver?walk({"":j},""):j;throw new SyntaxError("JSON.parse")})}();

function getLayerNames(arg) {
    var layerNames = [];
    var comp = app.project.activeItem;
    for(var i = 1; i <= comp.numLayers; i++) {
        layerNames.push(comp.layer(i).name);
        }

    return JSON.stringify(layerNames);
    }

function createGrid(data) {
    var splitData = data.split(",");

    var myDocument = app.activeDocument;
    var artLayer = myDocument.layers.add();
    artLayer.name = "Wordsearch";

    var wsearchGroup = artLayer.groupItems.add();
    wsearchGroup.name = "Wordsearch Group";
    wsearchGroup.move(artLayer, ElementPlacement.PLACEATEND);

    // NOTE: measure starts from bottom left of page - bottom, left, width, length

    for (var i = 0; i < splitData.length; i++){
        // removing line feeds
        var currentRow = splitData[i].replace(/[\r\n]+/, "");
        currentRowReplaced = "";
        // removing pipes between letters (remove this from py?)
        // TODO: this is missingt he final 2 columns?
        for (var k = 0; k < currentRow.length; k++) {
            if (currentRow[k] !== "|") {
                currentRowReplaced = currentRowReplaced + currentRow[k];
            }
        }
        for (var j = 0; j < currentRowReplaced.length; j++){
            var currentChar = currentRowReplaced[j];
            currentChar = currentChar.toUpperCase()

            var textRect;
            textRect = artLayer.pathItems.rectangle( -70 - 50*i - 50/10, 50 + 50*j + 5, 50 - 50/10, 50 - 50/10);
            var areaTextRef = myDocument.textFrames.areaText(textRect);
            var textRange = areaTextRef.textRange;
            var textAreaCharAttrs = textRange.characterAttributes;
            textAreaCharAttrs.size = 20;
            areaTextRef.contents = currentChar;
            areaTextRef.move(wsearchGroup, ElementPlacement.PLACEATEND);
            
        }
    }
}

function createWordList(wordArray) {
    var wordString = wordArray.join("\n").toUpperCase();

    var myDocument = app.activeDocument;
    var artLayer = myDocument.layers.add();
    artLayer.name = "Wordsearch Words";
    // TODO: take from wordsearch output in case not all words placed?
    var textRect = artLayer.pathItems.rectangle(- myDocument.height / 4 * 3 - 50, 50, myDocument.width / 2 - 25, myDocument.height /4 - 50);
    var areaTextRef = myDocument.textFrames.areaText(textRect);
    var textRange = areaTextRef.textRange;
    var textAreaCharAttrs = textRange.characterAttributes;
    textAreaCharAttrs.size = 24;
    areaTextRef.contents = wordString;
    areaTextRef.move(artLayer, ElementPlacement.PLACEATEND);

}

function drawSolution(solutionInfo) {
    alert(solutionInfo);
    var solutionJSON = solutionInfo.split("|");
    // alert(solutionJSON);
    var myDocument = app.activeDocument;
    var artLayer = myDocument.layers.add();
    artLayer.name = "Solution";

    var wsearchGroup = artLayer.groupItems.add();
    wsearchGroup.name = "Solution Group";
    wsearchGroup.move(artLayer, ElementPlacement.PLACEATEND);
    for (var i = 0; i < solutionJSON.length; i++){
        // TODO: centre the rectangles nicely
        // TODO: round the edges?
        alert(solutionJSON[i]);
        var solutionSplit = solutionJSON[i].split("-");
        // alert("solution split 0: " + solutionSplit[0]);
        var wordLen = solutionSplit[0].replace(/^\s+|\s+$/gm,'').length;
        // alert(wordLen);
        var direction = solutionSplit[1];
        var coords = solutionSplit[2];
        // alert(coords);
        var coord1 = coords.split(", ")[0].slice(1);
        // alert(coord1)
        var coord2 = coords.split(", ")[1].slice(0, coords.split(", ")[1].length - 1);
        // alert(coord2)
        // word-direction-(coord1,coord2)
        var textRect;
        if (direction == "across") {
            textRect = artLayer.pathItems.rectangle( -70 - 50*coord1 - 8, 50 + 50*coord2 -8, wordLen*50, 50);
        }
        if (direction == "down") {
            textRect = artLayer.pathItems.rectangle( -70 - 50*coord1 -8, 50 + 50*coord2 -8, 50, wordLen*50);
        }
        if (direction == "diag_up") {
            textRect = artLayer.pathItems.rectangle( -70 - 50*coord1 -8, 50 + 50*coord2 -8, wordLen*50, 50);
            textRect.rotate(45);
        }
        if (direction == "diag_down") {
            textRect = artLayer.pathItems.rectangle( -70 - 50*coord1 - 8, 50 + 50*coord2 - 8, wordLen*50, 50);
            textRect.rotate(315);
        }

        textRect.move(wsearchGroup, ElementPlacement.PLACEATEND);
            
        }
    }

function osCheck() {
        var os = $.os;
        var match = os.indexOf("Windows");
        if(match != (-1)) {
                var userOS = "PC";
            } else {
                 var userOS = "MAC";
                }
            return userOS;
    }

function alertJSX(string){
    alert(JSON.stringify(string), "");
    }