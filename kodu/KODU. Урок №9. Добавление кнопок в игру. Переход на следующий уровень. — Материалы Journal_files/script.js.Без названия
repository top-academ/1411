///////////////////////////////////////////////////////////////////////////////
// get card data from user form input 
var ClusterItemLists = [
  AppClient.getParameters("clusteritems1"),
  AppClient.getParameters("clusteritems2"),
  AppClient.getParameters("clusteritems3"),
  AppClient.getParameters("clusteritems4"),
  AppClient.getParameters("clusteritems5"),
  AppClient.getParameters("clusteritems6"),
  AppClient.getParameters("clusteritems7"),
  AppClient.getParameters("clusteritems8")
]; 
var Clusters = [
  AppClient.getParameters().find("cluster1"),
  AppClient.getParameters().find("cluster2"),
  AppClient.getParameters().find("cluster3"),
  AppClient.getParameters().find("cluster4"),
  AppClient.getParameters().find("cluster5"),
  AppClient.getParameters().find("cluster6"),
  AppClient.getParameters().find("cluster7"),
  AppClient.getParameters().find("cluster8")
];
for(var i = 0; i < Clusters.length; i++){
  if(Clusters[i].value === "") {
    Clusters.splice(i,1); 
    ClusterItemLists.splice(i,1); 
    i--;
  }
}
var allCards = new Array();
var totalClusters = 0;
///////////////////////////////////////////////////////////////////////////////
// Some counters for Media elements
///////////////////////////////////////////////////////////////////////////////
var videoCardLetters = new Array();
var audioCardLetters = new Array();
///////////////////////////////////////////////////////////////////////////////
function getLetterForNumber(i){
 var s = "";
 while(i > 0){ s += String.fromCharCode(64+i%26); i = i - 26; } 
 return s;
}
///////////////////////////////////////////////////////////////////////////////
// on app init - after connection to learningapps.org server established
///////////////////////////////////////////////////////////////////////////////
AppClient.onInit = function(){
  
  $("#cardsOverlay").append('<div id="checksolutionBtnPanel"><div id="checkSolutionBtn" onclick="AppClient.checkSolution()">'+
                     '<i class="glyphicon glyphicon-check"></i></div></div><div id="fadeblack"></div>'); 

  var i;
 
  var audioCardCounter = 1;
  var videoCardCounter = 1;

  function addCardLetters(cluster,clusteritems){
   // count media cards for random letters (Audio A, Audio B, Audio C)
   // we want to shuffel them in order to make it not so easy
   // we have to count all parameters before creating cards
   // we can random choose from LetterArray for each card later
   for(var i = 0; i < clusteritems.length; i++){
    if(clusteritems[i].value !== "") {
       if(clusteritems[i].media == "speech" || 
          clusteritems[i].media == "audio") audioCardLetters.push(getLetterForNumber(audioCardCounter++));
       if(clusteritems[i].media == "video") videoCardLetters.push(getLetterForNumber(videoCardCounter++));
    }
   }
  }  
  for(var i = 0; i < Clusters.length; i++)
   if(Clusters[i].value !== "") addCardLetters(Clusters[i],ClusterItemLists[i]);

  for(var i = 0; i < Clusters.length; i++)
   if(Clusters[i].value !== "") addCluster(Clusters[i],ClusterItemLists[i]);

  function findMatchingCards(clusteritems,clusters){
   for(var i = 0; i < clusteritems.length; i++){
    clusteritems[i].card.matchingCards = new Array();
    for(var z = 0; z < clusters.length; z++){
     for(var t = 0; t < clusters[z].length; t++){
      if(clusteritems[i] == clusters[z][t]) continue; 
      // add all cards from other clusters which are equal to the card from first cluster
      if(clusteritems[i].isEqual(clusters[z][t]))
         clusteritems[i].card.matchingCards.push(clusters[z][t].card);
     }
    }
   }
  }
  // find all matching cards - special case: there might be equal cards in other clusters
  for(var i = 0; i < Clusters.length; i++)
   if(Clusters[i].value !== "") findMatchingCards(ClusterItemLists[i],ClusterItemLists);  
  
  $("#clusters").addClass("totalClusters"+totalClusters);
  
  // resize cards to match screen size, trigger twice because of font resize effects
  resizeWindow();
  setTimeout(function(){
    resizeWindow();
    if(AppClient.getParameters("cardtype").isEqual(AppClient.getTranslation("allcards")))
    showAllCards(); else nextCard();
    setTimeout(resizeWindow,100);
  },100);
  $(window).on('resize', resizeWindow);
    
  $('#fadeblack').on("click touchstart mousedown",function(){$(this).fadeOut("fast");});
};
///////////////////////////////////////////////////////////////////////////////
var newCard = null;
///////////////////////////////////////////////////////////////////////////////
function showAllCards(){
  for(var i=0; i < allCards.length; i++){
    var card = allCards[i]; 
    card.hidden = false;
    card.htmlElement.show();
  }     
  AppClient.forceSpreadElements($(".card"),document.getElementById("cardsOverlay"),
                                function(card){dedectCurrentCardCluster($(card).data("card"));});
  $("#usabilityHint").delay(1000).fadeIn();
}
///////////////////////////////////////////////////////////////////////////////
function nextCard(){
  if(newCard && newCard.currentCluster == null) return; // there is still a card

  var csw = $("#cardsOverlay").outerWidth(); 
  var csh = $("#cardsOverlay").outerHeight(); 
  var randomCards = new Array();
  for(var i=0; i < allCards.length; i++){
    var card = allCards[i]; 
    if(card.hidden)
      randomCards.push(card);
  }    
  if(randomCards.length == 0) {
    // no cards left make a check
    //checkSolution(); 
    return;
  }

  var card = null;
  if(AppClient.getParameters("ordertype") &&
     AppClient.getParameters("ordertype").isEqual && 
     AppClient.getParameters("ordertype").isEqual(AppClient.getTranslation("elementorder"))){
    // always use the lowest index cards first and random from this group
    var smallestCardIndex = 99999;
	for(var i=0; i < randomCards.length; i++){
      if(smallestCardIndex > randomCards[i].index) smallestCardIndex = randomCards[i].index;
    }
	for(var i=0; i < randomCards.length; i++){
      if(randomCards[i].index > smallestCardIndex) {
		randomCards.splice(i,1); 
        i--;
      }
    }
  }
  var r = Math.floor(Math.random() * randomCards.length);
  card = randomCards[r];

  var cw = card.htmlElement.outerWidth(); 
  var ch = card.htmlElement.outerHeight(); 
  card.hidden = false;
  var top = (csh/2-ch/2);
  if(totalClusters < 4) top = Math.max(60,(csh/3-ch/2));
  card.htmlElement.css({"left":(csw/2-cw/2)+"px","top":top+"px"}); 
  card.htmlElement.delay(100).fadeIn();
  card.htmlElement.addClass("newcard");
  Draggable.bringToFront([$('#fadeblack'),card.htmlElement]);

  $('#fadeblack').stop().fadeIn('fast');  
  if(newCard == null){
    // first card
    $("#usabilityHint").delay(1000).fadeIn();
  }
  newCard = card;
  setTimeout(function(){ doResizeText(card); }, 250);
}
///////////////////////////////////////////////////////////////////////////////
function getRandomLetterFromList(type){
  var r = 0;
  if(type == "audio") {
    r = AppClient.random(audioCardLetters.length);
    return audioCardLetters.splice(r,1);
  }
  if(type == "video") {
    r = AppClient.random(videoCardLetters.length);
    return videoCardLetters.splice(r,1);
  }
}
///////////////////////////////////////////////////////////////////////////////
// add a new cluster to table
///////////////////////////////////////////////////////////////////////////////
function addCluster(parameter,clusteritems){ 
 totalClusters++;
 parameter.clusterID = totalClusters; 
 
 // add cards
 for(i = 0; i < clusteritems.length; i++){
  if(clusteritems[i].value !== "") {
   clusteritems[i].card = addCard(clusteritems[i]);
   clusteritems[i].card.index = i; 
   clusteritems[i].card.cluster = parameter; 
   allCards.push(clusteritems[i].card);
  }else{  
   clusteritems.remove(i);
   i--;
  }
 }

 // build the cluster html element 
 var useColors = AppClient.getParameter("backgroundColors") !== "false";
 
 var html = $('<div class="cluster"><div class="colorOverlay'+(useColors ? ' pinColor'+totalClusters : ' noColor')+'"></div>'+
              (parameter.media == "text" ? '<table style="height:100%;width:100%"><tr><td align="center"><div style="font-size:200%;width:80%;text-align:center;position:relative;z-index:2;pointer-events:none">'+parameter.value+'</div></td></tr></table>' : '')+
              (parameter.media == "image" ? '<div style="display:flex;height:100%;width:100%;pointer-events:none;justify-content:center;align-items:center"><img src="'+parameter.value+'" alt="" style="max-width:90%;max-height:90%"/></div>' : '')+
              (parameter.hint !== "" ?
                '<div class="clusterHint">'+AppClient.linkifyText(parameter.hintTTS == '2' ? '' : parameter.hint)+'</div>'
               : '')+'</div>');
 
 parameter.htmlElement = html;     // this is the html Element for this cluster
 html.data("cluster",parameter);   // we also add the card object to the html Element, 
                                   // so we can use it in event handlers later
 if(parameter.hintTTS == '1' || parameter.hintTTS == '2')
   $('.clusterHint',html).css('cursor','pointer').on('click',function(){ 
     AppClient.textToSpeech(parameter.hint); 
   });

 $("#clusters").append(parameter.htmlElement); // add the cluster html Element to the #cardsOverlay container
}  
///////////////////////////////////////////////////////////////////////////////
// add a new card to table
///////////////////////////////////////////////////////////////////////////////
function addCard(parameter){ 
 // each card has a card object containing some properties
 var card = new Object(); 
 card.currentCluster = null;
 card.parameter = parameter;
 card.hidden = true; // cards start hidden
  
 // build some inner html content for each card based on its type 
 if(parameter.media == "text"){
  card.innerHTML = '<span unselectable="on" class="resizeText">'+AppClient.linkifyText(parameter.value)+'</span>';
 }
 if(parameter.media == "image"){
  card.innerHTML = '<img src="'+parameter.value+'" alt=""/>';
 } 
 if(parameter.media == "speech"){
  card.innerHTML = '<div class="playMediaBtn"><span class="glyphicon glyphicon-headphones"></span> '+
                   'Audio '+ getRandomLetterFromList("audio")+'</div>';
 } 
 if(parameter.media == "audio"){
  card.innerHTML = '<div class="playMediaBtn"><span class="glyphicon glyphicon-headphones"></span> '+
                   'Audio '+ getRandomLetterFromList("audio")+'</div>'; 
 }
 if(parameter.media == "video"){
  card.innerHTML = '<div class="playMediaBtn"><span class="glyphicon glyphicon-film"></span> '+
                   'Video '+ getRandomLetterFromList("video")+'</div><img class="videoThumb" src="'+parameter.thumbURL+'" alt=""/>';
 }
 
 // build the card html element with pin and hint if available
 var html = $('<div class="card" style="display:none"><div class="pin unset"></div>'+
              (card.parameter.hint !== "" ?
                '<span class="hintbtn hintbtn_'+card.parameter.media+' popovers"'+ 
                ' data-container="#cardsOverlay" data-toggle="popover" data-placement="auto"'+
               ' data-content="'+AppClient.linkifyText(card.parameter.hintTTS == '2' ? '' : card.parameter.hint).replace(/"/g,'&quot;')+'">'+
                '<span class="glyphicon glyphicon-info-sign infoicon"></span></span>'
               : '')+
              card.innerHTML+'</div>');
 
 card.htmlElement = html; // this is the html Element for this card
 html.data("card",card);  // we also add the card object to the html Element, 
                          // so we can use it in event handlers later

 if(card.parameter.hintTTS == '1' || card.parameter.hintTTS == '2')
   $('.hintbtn',html).on('click mouseover touchend',function(){ 
     AppClient.textToSpeech(card.parameter.hint); 
   });

 $("#cardsOverlay").append(card.htmlElement); // add the card html Element to the #cardsOverlay container
 
 // make card draggable
 Draggable.create(card.htmlElement,{ type:"top,left", bounds:"#cardsOverlay", 
  onClick:     onCardClick,
  onDragStart: onCardDragStart,
  onDrag:      onCardDrag,
  onDragEnd:   onCardDragEnd
 });

 // make hint popover hoverable and touchable
 $('.popovers',card.htmlElement).popover({trigger:"hover"})
  .on('touchstart mousedown', function(e) {
     stopEvent(e);
     $(this).popover('toggle');
  });

 return card;
}
///////////////////////////////////////////////////////////////////////////////
// card was clicked / touched
///////////////////////////////////////////////////////////////////////////////
function onCardClick(e){
 $("#usabilityHint").fadeOut();
 stopEvent(e);
 // card clicked, show lightbox if necessary 
 var card = $(this.target).data("card");

 // card is not clickable at the moment because tape between cards was clicked  
 if(card.htmlElement.hasClass("noclick")) return;

 if(card.parameter.media == "text"){
    // text has no lightbox, do nothing
 }
     
 if(card.parameter.media == "image"){
  // only open lightbox, if image is twice as large as the card
  var img = new Image();
  img.src = card.parameter.value;
    
  if(img.width > card.htmlElement.width()*2 || img.height > card.htmlElement.height()*2){
   createModalDialogFrame('<div id="modalContentInner"></div>',
    function() {
     // on show
     $('#modalContentInner').html('<img data-dismiss="modal" class="img-responsive" '+
                                  'style="margin: 0 auto;" src="'+card.parameter.value+'" alt=""/>');
    }
   ).modal("show");
  }
 }  

 if(card.parameter.media == "speech"){
  createModalDialogFrame(card.innerHTML+'<div id="modalContentInner"></div>',
   function(){ 
    card.parameter.loadPlayer("modalContentInner",true); 
    $("#modalContentInner a").addClass("speechPlayBtn");
   }, function(){ AppClient.textToSpeechStop();}
  ).modal("show");
 }

 if(card.parameter.media == "audio"){
  createModalDialogFrame(card.innerHTML+'<div id="modalContentInner"></div>',
   function(){ card.parameter.loadPlayer("modalContentInner",true); }
  ).modal("show");
 }

 if(card.parameter.media == "video"){
  createModalDialogFrame(card.innerHTML+'<div id="modalContentInner"></div>',
   function(){
    $("#modalContentInner").height(
      Math.min($("#modalContentInner").width() / 4 * 3 +30,$(window).height()*0.8));
    card.parameter.loadPlayer("modalContentInner",true);
   }
  ).modal("show");
 }     
}
///////////////////////////////////////////////////////////////////////////////
// start card dragging
///////////////////////////////////////////////////////////////////////////////
function onCardDragStart(e){
 $("#usabilityHint").fadeOut();
 $('#fadeblack').fadeOut();
 var card = $(this.target).data("card");
 // make other cards a bit transparent
 $(".card").addClass("transparent");
 card.htmlElement.removeClass("newcard transparent wrong correct");
 card.htmlElement.addClass("dragging");

 // hide hint popups if open 
 $('.popovers',card.htmlElement).popover("hide");
 $('.pin',card.htmlElement).hide();
}
///////////////////////////////////////////////////////////////////////////////
function dedectCurrentCardCluster(card){
 var pos = card.htmlElement.position();
 var w =  card.htmlElement.outerWidth();
 var h =  card.htmlElement.outerHeight();
 var cx = pos.left + w / 2; 
 var cy = pos.top; 
  
 card.currentCluster = null;
 for(var i = 0; i < Clusters.length; i++){
  if(!Clusters[i].htmlElement) continue; 
  var cp = Clusters[i].htmlElement.position();
  var cw = Clusters[i].htmlElement.width(); 
  var ch = Clusters[i].htmlElement.height();
  if(cx >= cp.left && cx <= cp.left+cw && cy >= cp.top && cy <= cp.top+ch) {
   card.clusterX = (pos.left - cp.left) / cw; 
   card.clusterY = (pos.top - cp.top) / ch; 
   card.currentCluster = Clusters[i];
   break;
  }
 }
 
 // set pin color to cluster color 
 var useColors = AppClient.getParameter("backgroundColors") !== "false";
 if(useColors)
   $(".pin",card.htmlElement).attr('class', 'pin pin'+(card.currentCluster ? ' pinColor'+card.currentCluster.clusterID:'')); else 
   $(".pin",card.htmlElement).attr('class', 'pin noColorPin'); 
  
}
///////////////////////////////////////////////////////////////////////////////
// moving card around the table
///////////////////////////////////////////////////////////////////////////////
function onCardDrag(e){
 var card = $(this.target).data("card");
 // find cluster under card based on position
 dedectCurrentCardCluster(card);  
 // highlight current cluster 
 for (var i=0; i < Clusters.length; i++)
   if(Clusters[i].htmlElement)
     if(card.currentCluster == Clusters[i])
       $(".colorOverlay",Clusters[i].htmlElement).css("opacity",0.6); else 
       $(".colorOverlay",Clusters[i].htmlElement).css("opacity",0.2);
}
///////////////////////////////////////////////////////////////////////////////
// card drag ended, attach cards if possible
///////////////////////////////////////////////////////////////////////////////
function onCardDragEnd(e){
 stopEvent(e);
 var card = $(this.target).data("card");

 // unhighlight clusters
 $(".colorOverlay").css("opacity",0.2);
  
 $(".card").removeClass("transparent dragging");

 if(!AppClient.getParameters("cardtype").isEqual(AppClient.getTranslation("allcards"))) nextCard(); 
 $('.pin',card.htmlElement).show();
  
  checkAppCompleted();
}
///////////////////////////////////////////////////////////////////////////////
// check if all elements are connected and inform upper frames via postmessage
///////////////////////////////////////////////////////////////////////////////
function checkAppCompleted () {
 var completed = true;
 for(i = 0; i < allCards.length; i++){
   if(allCards[i].currentCluster === null) {
    completed = false;
    break;
   }
 }
 AppClient.setCompleted(completed);
}
///////////////////////////////////////////////////////////////////////////////
var lastWindowSizeW = -1;
var lastWindowSizeH = -1;
///////////////////////////////////////////////////////////////////////////////
// scale cards and position of cards when window size is changing
///////////////////////////////////////////////////////////////////////////////
function resizeWindow() {
 var w = $(window).width();
 var h = $(window).height();
 var m = Math.max(h,w);


 // resize clusters
 if(h > w){
  // portrait mode
  var cols = totalClusters < 4 ? 1 : 2;
  for(var i = 0; i < totalClusters; i++)
    Clusters[i].htmlElement.css({"left":(100/cols*(i % cols))+"%","top":(100/(Math.ceil(totalClusters/cols))*(Math.floor(i/cols)))+"%",
                                 "height":(100/(Math.ceil(totalClusters/cols)))+"%","width":(100 / cols)+"%"});  
  if(totalClusters % 2 == 1) Clusters[totalClusters-1].htmlElement.css("width","100%");
 }else{
  // landscape mode
  var rows = totalClusters < 4 ? 1 : 2;
  for(var i = 0; i < totalClusters; i++)
   if((totalClusters % 2 == 1) && (i > totalClusters / rows))
    Clusters[i].htmlElement.css({"top":(100/rows*Math.floor(i / Math.ceil(totalClusters / rows)))+"%",
                                 "left":(100/(Math.floor(totalClusters/rows))*(Math.ceil(i % Math.ceil(totalClusters / rows))))+"%",
                                 "width":(100/(Math.floor(totalClusters/rows)))+"%","height":(100 / rows)+"%"});  
   else
    Clusters[i].htmlElement.css({"top":(100/rows*Math.floor(i / Math.ceil(totalClusters / rows)))+"%",
                                 "left":(100/(Math.ceil(totalClusters/rows))*(Math.floor(i % Math.ceil(totalClusters / rows))))+"%",
                                 "width":(100/(Math.ceil(totalClusters/rows)))+"%","height":(100 / rows)+"%"});  
 }

 // font size of everything based on window size
 $("body").css({"font-size":Math.round(m/60)+"px"}); 
  
 $(".card").css({"width":Math.round(m*0.2)+"px", "padding":Math.round(m*0.01)+"px"}); 
 $(".pin").css({"border-radius":Math.round(m/50)+"px",
                "width":Math.round(m/50)+"px",
                "height":Math.round(m/50)+"px",
                "top":-Math.round(m/50/1.5)+"px",
                "margin-left":-Math.round(m/50/2)+"px"});
  
 $(".card").each(function(){
  var card = $(this).data("card");
  var p = card.htmlElement.position();
  var x = p.left;
  var y = p.top;
  var cw = card.htmlElement.outerWidth();
  var ch = card.htmlElement.outerHeight();
  if(lastWindowSizeW != -1 && lastWindowSizeH != -1){
   // make sure any card keeps in its cluster
   if(card.currentCluster){     
    var cp = card.currentCluster.htmlElement.position();
    var clw = card.currentCluster.htmlElement.width();
    var clh = card.currentCluster.htmlElement.height();
    x = cp.left + clw*card.clusterX;
    y = cp.top + clh*card.clusterY;
    card.htmlElement.css("left",Math.round(Math.max(5,Math.min(w-cw-5,x)))+"px");
    card.htmlElement.css("top" ,Math.round(Math.max(5,Math.min(h-ch-5,y)))+"px");
   } else {   
    card.htmlElement.css("left",Math.round(Math.max(5,Math.min(w-cw-5,((w * x / lastWindowSizeW)))))+"px");
    card.htmlElement.css("top" ,Math.round(Math.max(5,Math.min(h-ch-5,((h * y / lastWindowSizeH)))))+"px");
   }
  }
  // images have to fit inside a cluster
  var maxHeight = m / (totalClusters < 4 ? totalClusters : 2);
  if(h > w && totalClusters > 4 ) maxHeight = m/3;
  if(h > w && totalClusters > 6 ) maxHeight = m/4;
   
  $("img",card.htmlElement).css("max-height",Math.round(Math.min(cw*2, Math.min(maxHeight,h/2)-(m*0.02 + m/50*2)))+"px");

  doResizeText(card);
 });
 

 // remember current window size for next change
 lastWindowSizeW = w;
 lastWindowSizeH = h;
}

function doResizeText(card){
  // resize card font size: 
  var resizeText = $('.resizeText', card.htmlElement);
  if(resizeText.length > 0){
    var fontSize = 1.2;
    resizeText.css('font-size', fontSize+"em");
    resizeText.css('line-height', "normal");
    var maxWidth = card.htmlElement.width()*1.1;
    var maxHeight = card.htmlElement.height()*1;
    var textWidth;
    var textHeight;
    fontSize = 1.0;
    do {
       resizeText.css('font-size', fontSize+"em");
       textHeight = resizeText.height();
       textWidth = resizeText.width();
       fontSize = fontSize - 0.1;
    } while ((textHeight > maxHeight || textWidth > maxWidth) && fontSize > 0.3);
  }
}
///////////////////////////////////////////////////////////////////////////////
function checkSolution(){
  var i,card;
  var wrong = 0;
  // remove card colors for new check
  for(i = 0; i < allCards.length; i++){
    allCards[i].htmlElement.removeClass("wrong correct");
  }

  // test if pairs are matching 
  var solutionOk = true;
  var checkResults = [];
  
  for(i = 0; i < allCards.length; i++){
    card = allCards[i]; 
    // find other matching and unchecked card if this one is not where it should be
    if(card.currentCluster != card.cluster)
     for(var z = 0; z < card.matchingCards.length; z++){
      if(card.matchingCards[z].htmlElement.hasClass("correct") == false && 
         card.matchingCards[z].cluster == card.currentCluster){
        // exchange cards target cluster
        var t = card.cluster;
        card.cluster = card.matchingCards[z].cluster;
        card.matchingCards[z].cluster = t;
        break;
      }  
     }
    
    if(card.currentCluster == card.cluster){
     checkResults.push(1);
     card.htmlElement.addClass("correct");
    }else{  
     checkResults.push(0);
     if(card.currentCluster !== null)
        card.htmlElement.addClass("wrong");
     solutionOk = false;
     Draggable.bringToFront([card.htmlElement]);
     wrong++;
    }  
  }

  AppClient.setChecked(checkResults);
  // tell LearningApps this app was solved
  if(solutionOk) AppClient.setSolved();
  
  // user found the correct solution? if feedback is not already displayed show it
  if(solutionOk)
    AppClient.showFeedbackPanel("feedback");  
  
  if(newCard !== null) Draggable.bringToFront([newCard.htmlElement]);
}

