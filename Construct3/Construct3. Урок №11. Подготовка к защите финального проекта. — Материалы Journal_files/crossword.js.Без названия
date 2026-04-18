///////////////////////////////////////////////////////////////////////////////////
var currentCrossword = null;
///////////////////////////////////////////////////////////////////////////////////
function checkCrosswordFilled(){
 for(var z=0; z < currentCrossword.items.length; z++){
  var item = currentCrossword.items[z];
  for(var i=0; i < item.word.length; i++){
   var charOk = true;
   var d = null;
   if(item.direction == "-"){
    d = document.getElementById('grid_'+(item.x+i)+'_'+item.y);
	if(d && trim(d.innerHTML) == "") charOk = false;
   }
   if(item.direction == "|"){
    d = document.getElementById('grid_'+item.x+'_'+(item.y+i));
	if(d && trim(d.innerHTML) == "") charOk = false;
   }
   if(item.direction == "\\"){
    d = document.getElementById('grid_'+(item.x+i)+'_'+(item.y+i));
	if(d && trim(d.innerHTML) == "") charOk = false;
   }
   if(item.direction == "/"){
    d = document.getElementById('grid_'+(item.x+i)+'_'+(item.y-i));
	if(d && trim(d.innerHTML) == "") charOk = false;
   }
   if(!charOk) return false;
  }
 }
 return true;
}
///////////////////////////////////////////////////////////////////////////////////
function checkSolution(){
 var done = true;

 for(var z=0; z < currentCrossword.items.length; z++){
  var item = currentCrossword.items[z];
  var wrongWord = false;
  for(var i=0; i < item.word.length; i++){
   var charOk = true;
   var d = null;
   if(item.direction == "-"){
    d = document.getElementById('grid_'+(item.x+i)+'_'+item.y);
	if(d && d.innerHTML != item.word.substr(i,1)) charOk = false;
   }
   if(item.direction == "|"){
    d = document.getElementById('grid_'+item.x+'_'+(item.y+i));
	if(d && d.innerHTML != item.word.substr(i,1)) charOk = false;
   }
   if(item.direction == "\\"){
    d = document.getElementById('grid_'+(item.x+i)+'_'+(item.y+i));
	if(d && d.innerHTML != item.word.substr(i,1)) charOk = false;
   }
   if(item.direction == "/"){
    d = document.getElementById('grid_'+(item.x+i)+'_'+(item.y-i));
	if(d && d.innerHTML != item.word.substr(i,1)) charOk = false;
   }
   if(d && d.innerHTML == " "){
    d.style.background = '#FFEEEE';
   }else{
    d.style.background = '#FFFFFF';
   }
   if(charOk){
    if(d) {
      d.style.color = "green"; 
      d.style.backgroundImage = ""; 
    }
   }else{
    if(d) {
      d.style.color = "red"; 
      d.style.backgroundImage = "linear-gradient(135deg, #fff2f2 25%, #ffffff 25%, #ffffff 50%, #fff2f2 50%, #fff2f2 75%, #ffffff 75%, #ffffff 100%)"; 
 	  d.style.backgroundSize = "24px 24px"; 

    }
    wrongWord = true;
   }
  }
  if(wrongWord) done = false;
 } 

  // alles gefüllt
 if(done){
  if(window.onCrosswordSolved) window.onCrosswordSolved();
 }
}
///////////////////////////////////////////////////////////////////////////////////
var lastClickItemIndex = 0;
var currentCharacterInput = 0;
var currentItemInput = null;
var lastClickedXY = "";
///////////////////////////////////////////////////////////////////////////////////
function selectCrosswordField(x,y){
 var direction = "";
 var d = document.getElementById('grid_'+x+'_'+y);
 // get item under cell
 var item;
 if(lastClickedXY != x+" "+y) lastClickItemIndex = 0;
 lastClickedXY = x+" "+y; 
 // check if this is the beginning of an item, if so, use this first
 
 var match = -1;
 var matchCount = 0;
 for(var i=0; i < currentCrossword.grid[y][x].items.length; i++){
   if(currentCrossword.grid[y][x].items[i].x == x && 
      currentCrossword.grid[y][x].items[i].y == y){
     // matches
     match = i;
     matchCount++;
   }  
 } 
  if(matchCount == 1){
    lastClickItemIndex = match;
  }
 item = currentCrossword.grid[y][x].items[lastClickItemIndex % ( currentCrossword.grid[y][x].items.length)];
 lastClickItemIndex++;

 // clear highlight
 for(var dy = currentCrossword.minY-1; dy < currentCrossword.maxY+2; dy++){
  for(var dx = currentCrossword.minX-1; dx < currentCrossword.maxX+2; dx++){
   if(currentCrossword.grid[dy][dx]){
    var d = document.getElementById('grid_'+dx+'_'+dy);
	if(d) d.className = "field filled";  
   }
  }
 }
 
 // highlight selected fields 
 if(item.direction == "-"){
  var run = true;
  var dx = 0;
  while(run){
   var d = document.getElementById('grid_'+(x+dx)+'_'+(y));
   run = (d && d.innerHTML != "");
   if(run){ d.className = "field filled highlight";}   
   dx++;
  }
  var run = true;
  var dx = 0;
  while(run){
   var d = document.getElementById('grid_'+(x+dx)+'_'+(y));
   run = (d && d.innerHTML != "");
   if(run){ d.className = "field filled highlight";}   
   dx--;
  }
 }
 
 if(item.direction == "|"){
  var run = true;
  var dy = 0;
  while(run){
   var d = document.getElementById('grid_'+(x)+'_'+(y+dy));
   run = (d && d.innerHTML != "");
   if(run){ d.className = "field filled highlight";}   
   dy++;
  }
  var run = true;
  var dy = 0;
  while(run){
   var d = document.getElementById('grid_'+(x)+'_'+(y+dy));
   run = (d && d.innerHTML != "");
   if(run){ d.className = "field filled highlight";}   
   dy--;
  }
 } 

 var d = document.getElementById("questionDisplay");
 var html = "";
 
 if(item.direction == "-") html += '<b>'+AppClient.getTranslation("Frage")+" "+item.id+' ('+AppClient.getTranslation("waagerecht")+'):</b><br><br>';
 if(item.direction == "|") html += '<b>'+AppClient.getTranslation("Frage")+" "+item.id+' ('+AppClient.getTranslation("senkrecht")+'):</b><br><br>';
 html += (window.onGetContent ? window.onGetContent(item.id) : '')+'<br>';
 html += '<b>'+AppClient.getTranslation("Lösung")+':</b></br>';
 var elements = "";
 currentCharacterInput = 0;
 for(var i=0; i < item.word.length; i++){
  if(item.direction == "|"){
   if(item.x == x && item.y+i == y) currentCharacterInput = i;
   var w = document.getElementById('grid_'+item.x+'_'+(item.y+i));
   var v = (w ? w.innerHTML : "");
   elements += '<div class="field filled" onclick="currentCharacterInput='+i+';highlightInputField();" style="float:left;margin-bottom:3px;" id="i_'+i+'">'+v+'</div>';
  }
  if(item.direction == "-"){
   if(item.x+i == x && item.y == y) currentCharacterInput = i;
   var w = document.getElementById('grid_'+(item.x+i)+'_'+item.y);
   var v = (w ? w.innerHTML : "");
   elements += '<div class="field filled" onclick="currentCharacterInput='+i+';highlightInputField();" style="float:left;margin-bottom:3px;" id="i_'+i+'">'+v+'</div>';
  }
 }
 if(currentItemInput != item) currentCharacterInput = 0;
 var sp = document.getElementById("questionSidePanel");
 sp.style.display = "block";
 sp.style.top = ((item.y-currentCrossword.minY)*1.5)+"em";
 sp.style.top = "1em";
 html += '<div style="position:relative"><div style="position:absolute;width:100%;height:100%">'+
         '<input id="eingabe" onclick="inputClicked(event)" autocomplete="off" onkeyup="characterInput(event,this);" value="" class="inputElement filled" style="width:100%;height:100%;background:transparent;border:0px;color:white;opacity:0.01;font-size:16px" type="text" />';
  html += '</div>'+elements+' <button class="field filled" style="box-shadow:none;margin-left:10px;float:left;position:relative;z-index:10;background: #f3f3f3;border: 1px solid #ddd;" onclick="closeQuestionSidePanel()">⏎</button><div style="clear:both"></div></div>';
 d.innerHTML = html;
 currentItemInput = item;

 highlightInputField();
 document.getElementById("eingabe").focus();
}

function inputClicked(event){
  var d = document.getElementById("questionDisplay");
  var e = document.elementsFromPoint(event.clientX,event.clientY,d);
  for(var i=0; i < e.length; i++){
    if(e[i].id == "eingabe") continue;
    if(e[i].click) e[i].click();
  }
}

document.elementsFromPoint = function(clientX,clientY,root) {
	// root defaults to document.body
	if (root == undefined)
		root = document.body;
		
	var elements = [];
	var elm;
	
	while (elm = document.elementFromPoint(clientX,clientY)) {
		if (elm == root) break;
		elements.push(elm);
		elm.oldDisplay = elm.style.display;
		elm.style.display = 'none';
        if(elm.className.indexOf("field") >= 0) break;
        if(elements.length > 3) break;
	}
	
	// restore the original display values
	for (var i = 0; i < elements.length; i++) {
		elements[i].style.display = elements[i].oldDisplay;
		delete elements[i].oldDisplay;	
	}

	return elements;
};
///////////////////////////////////////////////////////////////////////////////////
function highlightInputField(){
 if(currentCharacterInput >= currentItemInput.word.length) currentCharacterInput = 0;
 if(currentCharacterInput < 0) currentCharacterInput = currentItemInput.word.length-1;
 for(var i=0; i < currentItemInput.word.length; i++){
  var d = document.getElementById("i_"+i);
  if(currentCharacterInput == i){
   if(d && d.className.indexOf(" blink") == -1) d.className += ' blink';  
  }else{
   if(d && d.className.indexOf(" blink") > -1) d.className = d.className.replace(" blink","");  
  } 
 }
}
///////////////////////////////////////////////////////////////////////////////////
function updateGridInput(){
 var d = document.getElementById("i_"+currentCharacterInput);
 var input = (d ? d.innerHTML : " ");
 var w = null;

 if(currentItemInput.direction == "|")
  w = document.getElementById('grid_'+currentItemInput.x+'_'+(currentItemInput.y+currentCharacterInput));
 
 if(currentItemInput.direction == "-")
  w = document.getElementById('grid_'+(currentItemInput.x+currentCharacterInput)+'_'+currentItemInput.y); 

 if(w){
  w.innerHTML = input;
  w.style.color = "black";
  w.style.background = "#FFFFFF";
 }
}
///////////////////////////////////////////////////////////////////////////////////
function characterInput(event,e){
 setTimeout(function(){
   var input = (e.value);
   if(input.length > 1) {
    input = input.substr(0,1);
    e.value = e.value.substr(1);
   }else e.value = "";

   input = input.toUpperCase(); 
   var char = event.which || event.keyCode;
   var keyEvent = false;
   if(char == 13){
    closeQuestionSidePanel();  
    return;
   }
   if(trim(input) == "") keyEvent = true;
   if(char == 38 || char == 40) keyEvent = true;
   if(char == 8 || char == 37){
    // backspace || left key
    var d = document.getElementById("i_"+currentCharacterInput);

    if(char != 8 || (!currentCharacterInput == input.length-1 || (d && d.innerHTML == ""))){
      currentCharacterInput--;
      highlightInputField();
      d = document.getElementById("i_"+currentCharacterInput);
    }
    if(char == 8){
     if(d) d.innerHTML = "";  
     updateGridInput();
    }
    keyEvent = true;
   }
   if(char == 39){
    // right key
    currentCharacterInput++;
    highlightInputField();
    keyEvent = true;
   }
   if(!keyEvent){
    var d = document.getElementById("i_"+currentCharacterInput);
    if(d) d.innerHTML = input;
    updateGridInput();
    if(currentCharacterInput < currentItemInput.word.length-1) currentCharacterInput++;
    highlightInputField();
   }
 },1);
}
///////////////////////////////////////////////////////////////////////////////////
function updateSolutionTerm(places){
 // 
 var solution = document.getElementById('solutionword');
 if(!solution){
  var s = "";
  for(var p = 0; p < places.length; p++){
   s += '<div class="" style="float:left;position:relative">'+
        '<div class="field solution" style="cursor:default;z-Index:2;position:absolute;"></div>'+
	'<div style="cursor:default;z-Index:3;position:absolute;font-size:5pt;margin:2px;margin-top:2.6em">'+numToRoman(places[p].index+1)+'</div>'+ 
        '<div class="field filled" style="cursor:default;position:relative" id="solutionword'+p+'"></div></div>';
  }
  document.getElementById('innerCrossword').innerHTML += '<div id="solutionword" style="padding-left:1em;margin:10px;max-width:90%;width:'+((places.length+1)*2)+'em">'+s+'<div style="clear:both"></div></div>';
 }
 for(var p = 0; p < places.length; p++){
  var s = "";
  if(!places[p].fixed){
   var d = document.getElementById('grid_'+places[p].x+'_'+places[p].y);
   s = trim(d.innerHTML);
  }else{
   s = places[p].fixed;
  }
  var c = document.getElementById('solutionword'+places[p].index);
  c.innerHTML = s;
 }
}
///////////////////////////////////////////////////////////////////////////////////
function numToRoman(i){
 var r = "";
 while(i > 10){
  r += "X";
  i = i - 10;
 }
 if (i == 1) r += "I";
 if (i == 2) r += "II";
 if (i == 3) r += "III";
 if (i == 4) r += "IV";
 if (i == 5) r += "V";
 if (i == 6) r += "VI";
 if (i == 7) r += "VII";
 if (i == 8) r += "VIII";
 if (i == 9) r += "IX";
 if (i ==10) r += "X";
 return r;
}

///////////////////////////////////////////////////////////////////////////////////
function buildSolutionWord(cross,term){
 term = term.replace(/ /g,"").toUpperCase();
 if(term == "") return;
 if(cross.grid.length == 0) return;
 var Randomizer = new Rc4Random("seed");
 var places = new Array();
 if(cross.grid.fixedSolution){
  for(var i = 0; i < term.length; i++){
   var dx = cross.grid.firstSolutionX;
   var dy = cross.grid.firstSolutionY;
   places.push({x:dx, y:dy+i, index:i, fixed:null});
  }
 }else{
  for(var i = 0; i < term.length; i++){
   var possible = new Array();
   for(var y = cross.minY-1; y < cross.maxY+2; y++){
    for(var x = cross.minX-1; x < cross.maxX+2; x++){
     var d = document.getElementById('grid_'+x+'_'+y+'_number');
     if(cross.grid[y][x] && !d && cross.grid[y][x].character.toUpperCase() == term[i]){ 
	  possible.push({x:x, y:y, fixed:null});
     }  
    }
   }
   if(possible.length == 0){
    for(var y = cross.minY-1; y < cross.maxY+2; y++){
     for(var x = cross.minX-1; x < cross.maxX+2; x++){
      if(cross.grid[y][x] && cross.grid[y][x].character.toUpperCase() == term[i]){ 
	  possible.push({x:x, y:y, fixed:null});
      }  
     }
    }
   }
   if(possible.length == 0){
    possible.push({x:-1, y:-1, fixed:term[i]});
   }

   var z = 0;
   while(true){
    z++;
    var n = Math.floor(Randomizer.random()*possible.length);
    var isOk = true;
    for(var p = 0; p < places.length; p++){
     var dx = Math.abs(places[p].x - possible[n].x);
     var dy = Math.abs(places[p].y - possible[n].y);
 	 if(dx < 1 && dy < 1) isOk = false;
    }   
    if(!isOk && z < 50) continue;
    places.push({x:possible[n].x, y:possible[n].y, index:i, fixed: possible[n].fixed});
    break;
   }
  }
 }  
 // all characters placed somewhere in grid
 for(var p = 0; p < places.length; p++){
  if(places[p].fixed)continue;
  var d = document.getElementById('grid_'+places[p].x+'_'+places[p].y);
  var div = document.createElement("div");
  div.style.position = "absolute";
  div.style.zIndex = "2";
  var code = '<div style="cursor:pointer;position:absolute;" onclick="selectCrosswordField('+places[p].x+','+places[p].y+')">'+
             '<div class="field solution" style="position:absolute"></div>'+ 
             (!cross.grid.fixedSolution ? '<div style="font-size:5pt;margin:2px;margin-top:2.6em">'+numToRoman(places[p].index+1)+'</div>':'')+'</div>';
  div.innerHTML = code;
  d.parentNode.insertBefore(div,d);
 }
 if(!cross.grid.fixedSolution)
 setInterval(function(){updateSolutionTerm(places);},1000);
}
///////////////////////////////////////////////////////////////////////////////////
function displayCrosswordGrid(cross){
 currentCrossword = cross;
 var html = "";
 function joinIndex(startIndex){
   var s = "";
   for(var i = 0; i < startIndex.length; i++)
     s += (s == "" ? '':',')+startIndex[i].id;
   return s;
   
 } 
 html += '<table id="crossword" style="width:100%;" cellpadding="0" cellspacing="0"><tr><td id="innerCrossword" align="center"><table cellspacing="0" cellpadding="0">';
 if(cross.grid.length > 0)
 for(var y = cross.minY-1; y < cross.maxY+2; y++){
  html += '<tr>';
  for(var x = cross.minX-1; x < cross.maxX+2; x++){
   if(cross.grid[y][x]){
    startIndex = [];
    for(var it = 0; it < cross.grid[y][x].items.length; it++){
	 if(cross.grid[y][x].items[it].x == x && cross.grid[y][x].items[it].y == y) startIndex.push(cross.grid[y][x].items[it]);
	}
    html += '<td>'+(startIndex.length > 0 ? '<div id="grid_'+x+'_'+y+'_number" onclick="selectCrosswordField('+x+','+y+')" style="z-Index:3;cursor:pointer;position:absolute;font-size:6pt;margin:2px">'+joinIndex(startIndex)+'</div>' : '')+
	        '<div id="grid_'+x+'_'+y+'" style="position:relative;z-Index:1;" onclick="selectCrosswordField('+x+','+y+')" class="field filled"> </div></td>'; 
   } else
    html += '<td><div id="grid_'+x+'_'+y+'" class="field"></div></td>';  
  }
  html += '</tr>';
 }
 html += '</table>';

 html += '</td></tr></table>';
 html += '</td></tr></table>';
 return html;
}
///////////////////////////////////////////////////////////////////////////////////
function closeQuestionSidePanel(){
 document.getElementById("questionSidePanel").style.display = "none";
 document.getElementById("questionDisplay").innerHTML = "";
}
///////////////////////////////////////////////////////////////////////////////////
function createCrosswordGrid(items,directions,solutionTerm){
 if(!solutionTerm) solutionTerm = "";
 solutionTerm = solutionTerm.replace(/ /g,"").toUpperCase();
 var Randomizer = new Rc4Random("seed");

 if(!directions) directions = new Array("-","|","\\","/");
 var maxlen = 0;
 for(var i=0; i < items.length; i++) {
  maxlen += items[i].word.length*2; 
 }

 // create 2d grid			
 var grid = new Array(maxlen);
 for (var i=0; i < maxlen; i++) grid[i] = new Array(maxlen);
 var done = new Array();

 // fill grid
 if(solutionTerm != ""){
  if(solutionTerm.length != items.length){
   //alert("Solution word must have exactly "+items.length+" characters to be aligned.");
   return createCrosswordGrid(items,directions,"");
  }
  for(var i=0; i < items.length; i++) {
   var placed = false;
   for(var z=0; z < items[i].word.length; z++){
    var dx = Math.floor(items[i].word.length/2);
  	var dx1 = Math.max(0,dx-z); 
	var dx2 = Math.min(items[i].word.length,dx+z);
	var x = -1000;
    if(items[i].word[dx1] && items[i].word[dx1].toUpperCase() == solutionTerm[i]) {dx = dx1; x = maxlen/2-dx;}
    if(items[i].word[dx2] && items[i].word[dx2].toUpperCase() == solutionTerm[i]) {dx = dx2; x = maxlen/2-dx;}
	if(x == -1000) continue;
		
	placed = true;
 	items[i].direction = "-";
	items[i].x = x;
    items[i].y = i+1;
    if(i == 0) {
     grid.firstSolutionX = items[i].x+dx;
     grid.firstSolutionY = items[i].y;
    }

	for(var ic = 0; ic < items[i].word.length; ic++){
	 grid[i+1][x+ic] = {character:items[i].word.substr(ic,1),items: [items[i]]};
	}
	done.push(items[i]);
	break;
   }
   if(!placed){
    alert("The "+(i+1) +". character ("+solutionTerm[i]+") of "+solutionTerm+" is not part of the "+(i+1) +". question solution word. Crossword cannot be aligned.");
    return createCrosswordGrid(items,directions,"");
   }
  }
  
  grid.fixedSolution = true;
  savegrid = grid; lastfails = 0;
 }else{ 
  grid.fixedSolution = false;

  var impossible = new Array();
  var retry = 0;
  var lastfails = 0;

  while (retry < 100){
  var fails = 0;
  while (done.length < items.length) {
   find = true; 
   while (find) {
    r = Math.floor(Randomizer.random() * items.length);
    find = false;
    for(var i=0; i < done.length; i++){
     if(done[i].id == items[r].id) find = true;
    }
    for(var i=0; i < impossible.length; i++){
     if(impossible[i].id == items[r].id) find = true;
    }
   }
   
   var item = items[r];
   item.x = -1;
   item.y = -1;  

   if(done.length > 0){
    for(var i=0; i < done.length; i++){
     if(item.x >= 0 && item.y >= 0) break;
	
 	 var characters = new Array();
     for(var c=0; c < item.word.length;c++) characters.push(false);
	
     for(var c=0; c < item.word.length;c++){
      if(item.x >= 0 && item.y >= 0) break;
      var find = true;
      while(find){ 
	   var r = Math.floor(Randomizer.random() * item.word.length);
       find = characters[r];	  
      }	  
	  characters[r] = true; 
	  var chr = item.word.substr(r, 1);
      if (done[i].word.indexOf(chr) >= 0) {
  	   for(var z=0; z < done[i].word.length; z++){
        if(item.x >= 0 && item.y >= 0) break;
	    if(done[i].word.substr(z,1) == chr){
	     var x,y;
		
	     if(done[i].direction == "-"){
		  x = done[i].x + z;
		  y = done[i].y;
		 }
	     if(done[i].direction == "|"){
		  x = done[i].x;
		  y = done[i].y+z;
		 }
	     if(done[i].direction == "\\"){
		  x = done[i].x+z;
		  y = done[i].y+z;
		 }
	     if(done[i].direction == "/"){
		  x = done[i].x+z;
		  y = done[i].y-z;
		 }
		 var possibledirections = new Array();
		 for(var d=0; d < directions.length; d++)
		  if(directions[d] != done[i].direction) possibledirections.push(directions[d]);
		 
	 	 possibledirections.sort(function(a,b){return Randomizer.random()-0.5;});
		
		 while(possibledirections.length > 0){
		  var fail = false;

		  item.direction = possibledirections.pop();
		  if(item.direction == "|"){
		   y = y - r;
		   if (grid[y-1][x] || grid[y + item.word.length][x]) fail = true;
		  }
		  if(item.direction == "-"){
		   x = x - r;
		   if (grid[y][x - 1] || grid[y][x + item.word.length]) fail = true;
		  }
		  if(item.direction == "\\"){
		   x = x - r;
		   y = y - r;
           if (grid[y - 1][x - 1] || grid[y + item.word.length][x + item.word.length]) fail = true;
		  }
		  if(item.direction == "/"){
		   x = x - r;
		   y = y + r;
           if (grid[y + 1][x - 1] || grid[y - item.word.length][x + item.word.length]) fail = true;
		  }		

		  for(var w=0; w < item.word.length; w++){
		   if(item.direction == "-"){
		    if(grid[y][x+w] && grid[y][x+w].character != item.word.substr(w,1)) fail = true;
		    if(grid[y-1][x+w] && w != r) fail = true;
		    if(grid[y+1][x+w] && w != r) fail = true;
		   }
		   if(item.direction == "|"){
		    if(grid[y+w][x] && grid[y+w][x].character != item.word.substr(w,1)) fail = true;
		    if(grid[y+w][x-1] && w != r) fail = true;
		    if(grid[y+w][x+1] && w != r) fail = true;
		   }
		   if(item.direction == "\\"){
		    if(grid[y+w][x+w] && grid[y+w][x+w].character != item.word.substr(w,1)) fail = true;
		   }
		   if(item.direction == "/"){
		    if(grid[y-w][x+w] && grid[y-w][x+w].character != item.word.substr(w,1)) fail = true;
		   }		  
		  }	
	      if(!fail){
		   item.x = x;
		   item.y = y;
		   impossible = new Array();
		   break;		  
 		  }
		 }
	    }
	   }
	  }
     }
    }
    if(item.x == -1 && item.y == -1){
     impossible.push(item);
 	 if(impossible.length == items.length - done.length){ 
	  fails++;
	  var c = 0;
	  while(c < 100){
       if(item.x >= 0 && item.y >= 0) break;

 	   var r = Math.floor(Randomizer.random() * 2);
	   item.direction = (r == 0 ? "-" : "|");
       var fail = false;

	  
	   if(item.direction == "-"){
        var x = Math.floor(grid.length / 2) - Math.floor(item.word.length / 2);
        var y = Math.floor(grid[0].length / 2);

        x += (Randomizer.random() > 0.5 ? -1 : 1 ) * Math.floor(Randomizer.random()*c);
        y += (Randomizer.random() > 0.5 ? -1 : 1 ) * Math.floor(Randomizer.random()*c);

	    for(var z=0; z < item.word.length; z++){
	     if(grid[y][x+z] && grid[y][x+z].character != item.word.substr(z,1)) fail = true;
	     if(grid[y-1][x+z]) fail = true;
	     if(grid[y+1][x+z]) fail = true;
	    }
	    if(grid[y][x-1] || grid[y][x+item.word.length]) fail = true; 
	   }
	   if(item.direction == "|"){
        var x = Math.floor(grid[0].length / 2);
        var y = Math.floor(grid.length / 2) - Math.floor(item.word.length / 2);

        x += (Randomizer.random() > 0.5 ? -1 : 1 ) * Math.floor(Randomizer.random()*c);
        y += (Randomizer.random() > 0.5 ? -1 : 1 ) * Math.floor(Randomizer.random()*c);
	   
	    for(var z=0; z < item.word.length; z++){
	     if(grid[y+z][x] && grid[y+z][x].character != item.word.substr(z,1)) fail = true;
	     if(grid[y+z][x-1]) fail = true;
	     if(grid[y+z][x+1]) fail = true;
	    }
	    if(grid[y-1][x] || grid[y+item.word.length][x]) fail = true; 
	   }
	   if(!fail){
	    item.x = x;
	    item.y = y;
       }
	   c += 0.1;
	  }
	 
	  impossible = new Array();
	 }
    }
   }
   if(done.length == 0){
    item.direction = "|";
    item.x = Math.floor(grid[0].length / 2);
    item.y = Math.floor(grid.length / 2) - Math.floor(item.word.length / 2);
   }
  
   if(item.x >= 0 && item.y >= 0){
    done.push(item);
    function combineField(is,add){
     if(!is) return add;
 	 is.items.push(add.items[0]); 
	 return is;
    }
    for(var w=0; w < item.word.length; w++){
     if(item.direction == "-") grid[item.y][item.x+w] = combineField(grid[item.y][item.x+w] , {items:[item],character:item.word.substr(w,1)});
     if(item.direction == "|") grid[item.y+w][item.x] = combineField(grid[item.y+w][item.x] , {items:[item],character:item.word.substr(w,1)});
     if(item.direction == "\\")grid[item.y+w][item.x+w] = combineField(grid[item.y+w][item.x+w] , {items:[item],character:item.word.substr(w,1)});
     if(item.direction == "/") grid[item.y-w][item.x+w] = combineField(grid[item.y-w][item.x+w] , {items:[item],character:item.word.substr(w,1)});
    }
   }
  }
  if(retry == 0){
   savegrid = grid; lastfails = fails;
  } else if(lastfails > fails){
   savegrid = grid; lastfails = fails;
  }
  if(lastfails == 0) break;
  retry++;
 }
 }
 // cut out
 var minX = grid.length;
 var minY = grid.length;
 var maxX = 0;
 var maxY = 0;
 for(var y = 0; y < savegrid.length; y++){
  for(var x = 0; x < savegrid[y].length; x++){
   if(savegrid[y][x] && y < minY) minY = y;
   if(savegrid[y][x] && x < minX) minX = x;
   if(savegrid[y][x] && y > maxY) maxY = y;
   if(savegrid[y][x] && x > maxX) maxX = x;
  }
 }
 // new grid
 var o = new Object();
 o.minX = minX;
 o.minY = minY;
 o.maxX = maxX;
 o.maxY = maxY;
 o.grid = savegrid;
 o.items = done;
 return o;
}
///////////////////////////////////////////////////////////////////////////////////
function Rc4Random(seed){
	var keySchedule = [];
	var keySchedule_i = 0;
	var keySchedule_j = 0;
	
	function init(seed) {
		for (var i = 0; i < 256; i++)
			keySchedule[i] = i;
		
		var j = 0;
		for (var i = 0; i < 256; i++)
		{
			j = (j + keySchedule[i] + seed.charCodeAt(i % seed.length)) % 256;
			
			var t = keySchedule[i];
			keySchedule[i] = keySchedule[j];
			keySchedule[j] = t;
		}
	}
	init(seed);
	
	function getRandomByte() {
		keySchedule_i = (keySchedule_i + 1) % 256;
		keySchedule_j = (keySchedule_j + keySchedule[keySchedule_i]) % 256;
		
		var t = keySchedule[keySchedule_i];
		keySchedule[keySchedule_i] = keySchedule[keySchedule_j];
		keySchedule[keySchedule_j] = t;
		
		return keySchedule[(keySchedule[keySchedule_i] + keySchedule[keySchedule_j]) % 256];
	}
	
	this.random = function() {
		var number = 0;
		var multiplier = 1;
		for (var i = 0; i < 8; i++) {
			number += getRandomByte() * multiplier;
			multiplier *= 256;
		}
		return number / 18446744073709551616;
	}
}

