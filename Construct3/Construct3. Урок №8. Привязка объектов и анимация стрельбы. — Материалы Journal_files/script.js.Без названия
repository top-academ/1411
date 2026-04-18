///////////////////////////////////////////////////////////////////////////////
var playMode = "";
// get card data from user form input 
var Pair1List = AppClient.getParameters("v1_#");
var Pair2List = AppClient.getParameters("v2_#");
var WrongList = AppClient.getParameters("u#");
var direction = AppClient.getParameter("direction");
if(AppClient.isTranslationOf("horizontal",direction)) direction = "horizontal"; else direction = "vertical";
var colorCards = AppClient.getParameter("color");

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
  
  playMode = "normal";
  // Fade mode = cards fade out when connected correctly, no check solution button required
  if(AppClient.getParameters("fade").value == "true") playMode = "fade";

  // add check solution button in normal play
  if(playMode == "normal")
    $("#cards").append('<div id="checksolutionBtnPanel"><div id="checkSolutionBtn" onclick="AppClient.checkSolution()">'+
                       '<i class="glyphicon glyphicon-check"></i></div></div>'); 
    
  var i;
 
  // count media cards for random letters (Audio A, Audio B, Audio C)
  // we want to shuffel them in order to make it not so easy
  // we have to count all parameters before creating cards
  // we can random choose from LetterArray for each card later
  var audioCardCounter = 1;
  var videoCardCounter = 1;
  for(i = 0; i < Pair1List.length; i++){
    if(Pair1List[i].value !== "" && Pair2List[i].value !== "") {
       // both pairs have some user input
       if(Pair1List[i].media == "speech" || 
          Pair1List[i].media == "audio") audioCardLetters.push(getLetterForNumber(audioCardCounter++));
       if(Pair1List[i].media == "video") videoCardLetters.push(getLetterForNumber(videoCardCounter++));
       if(Pair2List[i].media == "speech" || 
          Pair2List[i].media == "audio") audioCardLetters.push(getLetterForNumber(audioCardCounter++));
       if(Pair2List[i].media == "video") videoCardLetters.push(getLetterForNumber(videoCardCounter++));
    }
  }
  for(i = 0; i < WrongList.length; i++){
    if(WrongList[i].value !== ""){
      if(WrongList[i].media == "speech" || 
         WrongList[i].media == "audio") audioCardLetters.push(getLetterForNumber(audioCardCounter++));
      if(WrongList[i].media == "video") videoCardLetters.push(getLetterForNumber(videoCardCounter++));
    }
  }

  // read additional wrong elements from user form input and add cards
  for(i = 0; i < WrongList.length; i++){
    if(WrongList[i].value !== ""){
       WrongList[i].card = addCard(WrongList[i]); 
    } else { 
       WrongList.remove(i);
       i--;
    }  
  }
  
  // read pairs from user form input and add cards 
  for(i = 0; i < Pair1List.length; i++){
    if(Pair1List[i].value !== "" && Pair2List[i].value !== "") {
       // both pairs have some user input
       // create cards and attach card objects to there parameter for later use
       Pair1List[i].card = addCard(Pair1List[i],1);
       Pair2List[i].card = addCard(Pair2List[i]);
    } else {
       // this pair is incomplete or unused delete it 
       Pair1List.remove(i);
       Pair2List.remove(i);
       i--;
    }
  }
 
  // find all matching cards - special case: there might be equal cards in other pairs
  for(i = 0; i < Pair1List.length; i++){
    Pair1List[i].card.matchingCards = new Array();
    for(var z = 0; z < Pair1List.length; z++){
      // add all cards from Pair2List which are equal to the card from index i 
      if(Pair2List[i].isEqual(Pair2List[z]))
         Pair1List[i].card.matchingCards.push(Pair2List[z].card);

      if(Pair1List[i].isEqual(Pair1List[z]))
         Pair1List[i].card.matchingCards.push(Pair2List[z].card);
    }
  }
  
  
  // set initial position of cards not too random, spread them out
  AppClient.forceSpreadElements($(".card"),document.getElementById("cards"));
  // resize cards to match screen size, trigger twice because of font resize effects
  resizeWindow();
  setTimeout(resizeWindow,100);
  $(window).on('resize', resizeWindow);
  $("#usabilityHint").delay(1000).fadeIn();
};
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
// add a new card to table
///////////////////////////////////////////////////////////////////////////////
function addCard(parameter,firstSet){ 
 // each card has a card object containing some properties
 var card = new Object(); 
 card.attached = null;
 card.attachedTo = null;
 card.parameter = parameter;

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
 
 // build the card html element with pin, tape and hint if available
  // && WrongList.length == 0 
  var html = $('<div class="card '+(direction)+(colorCards == "true" ? ( firstSet ? ' cc1':' cc2'):"")+'"><div class="pin'+( firstSet ? ' orange':'')+'"></div><div class="tape"></div>'+
              (card.parameter.hint !== "" ?
                '<span class="hintbtn hintbtn_'+card.parameter.media+' popovers"'+ 
                ' data-container="#cards" data-toggle="popover" data-placement="auto"'+
               ' data-content="'+AppClient.linkifyText(card.parameter.hintTTS == '2' ? '' : card.parameter.hint).replace(/"/g,'&quot;')+'">'+
                '<span class="glyphicon glyphicon-info-sign infoicon"></span></span>'
               : '')+
              card.innerHTML+'</div>');
 
 card.htmlElement = html; // this is the html Element for this card
 html.data("card",card);  // we also add the card object to the html Element, 
                          // so we can use it in event handlers later
 if(card.parameter.hintTTS == '1' || card.parameter.hintTTS == '2')
   $('.hintbtn',html).on('click',function(){ 
     AppClient.textToSpeech(card.parameter.hint); 
   });

 $("#cards").append(card.htmlElement); // add the card html Element to the #cards container
 
 // make card draggable
 Draggable.create(card.htmlElement,{ type:"top,left", bounds:"#cards", 
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
 // card clicked, show lightbox if necessary 
 stopEvent(e);
  
 var card = $(this.target).data("card");

 // card is not clickable at the moment because tape between cards was clicked  
 if(card.htmlElement.hasClass("noclick")) return;

 // if the card has another card attached, bring it to front as well
 if(card.attached !== null) 
   Draggable.bringToFront([card.htmlElement,card.attached.htmlElement]);
 if(card.attachedTo !== null) 
   Draggable.bringToFront([card.attachedTo.htmlElement,card.htmlElement]);

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
  
 var card = $(this.target).data("card");
 // make dragging card a bit transparent
 card.htmlElement.addClass("dragging");
 // hide hint popups if open 
 $('.popovers',card.htmlElement).popover("hide");

 if(card.attachedTo){ 
   card.attachedTo.htmlElement.addClass("dragging");
   $('.pin',card.attachedTo.htmlElement).hide(); 
 }
 if(card.attached){ 
   card.attached.htmlElement.addClass("dragging");
   $('.pin',card.attached.htmlElement).hide(); 
 }
 $('.pin',card.htmlElement).hide(); 
 
}
///////////////////////////////////////////////////////////////////////////////
// moving card around the table
///////////////////////////////////////////////////////////////////////////////
function onCardDrag(e){
 var card1 = $(this.target).data("card");
 card1.htmlElement.removeClass("drophighlight");

 // card is not attached to another card or has another card attached
 if(card1.attached === null && card1.attachedTo === null){
  // iterate over all cards
  var foundHoveringCard = false;
  $(".card").each(function(){
   var card2 = $(this).data("card");
   if(card2 == card1) return; // this is the same card skip it
   // check if this card has already something attached to
   if(card2.attached !== null || card2.attachedTo !== null) return; 
   
   // we found no other card yet to highlight
   // check if the parameter names missmatch - never attach v1_# with v1_# and v2_# with v2_# 
   // if this card overlaps 20% highlight it and bring it to front
   if (!foundHoveringCard && 
       card1.parameter.xmlName != card2.parameter.xmlName &&
       Draggable.hitTest(card1.htmlElement,card2.htmlElement,"25%")) {

        foundHoveringCard = true;
        card2.htmlElement.addClass("drophighlight"); 
        Draggable.bringToFront([card1.htmlElement,card2.htmlElement]);
     
   } else { 
    // unhighlight all cards we hovered earlier
    card2.htmlElement.removeClass("drophighlight");
   } 
  });
  if(!foundHoveringCard){
    var x1 = parseInt(card1.htmlElement.css("left"));
    var y1 = parseInt(card1.htmlElement.css("top"));
    $(".card").each(function(){
     var card2 = $(this).data("card");
     if(card2.invisible) return;
     if(card2.attached !== null || card2.attachedTo !== null) return; 
     if(card2 == card1) return; // this is the same card skip it
     if(!foundHoveringCard && card1.parameter.xmlName != card2.parameter.xmlName){
       var x2 = parseInt(card2.htmlElement.css("left"));
       var y2 = parseInt(card2.htmlElement.css("top"));
       var w = parseInt(card2.htmlElement.css("width"));
       var h = parseInt(card2.htmlElement.css("height"));
       if(x1 > x2-w/4 && x1 < x2+w-w/4 && y1 > y2+h-10 && y1 < y2+h+10){
         foundHoveringCard = true;
         card2.htmlElement.addClass("drophighlight"); 
         Draggable.bringToFront([card1.htmlElement,card2.htmlElement]);
       }
     }
    });
  }
 } else {
  // card is attached to another card or has another card attached, just reposition both
  repositionCardPair(card1);
 } 
}
///////////////////////////////////////////////////////////////////////////////
// card drag ended, attach cards if possible
///////////////////////////////////////////////////////////////////////////////
function onCardDragEnd(e){
 stopEvent(e);
  
 var card1 = $(this.target).data("card");
 $('.card').removeClass("dragging");

 var over = $(".card.drophighlight");
 if(over.length == 1){
  var card2 = over.data("card");
  // dragged over another card - dock to it
  card2.htmlElement.removeClass("drophighlight");
  
  card1.attachedTo = card2;
  card2.attached = card1;

  repositionCardPair(card2);
  repositionCardPair(card1);

  Draggable.bringToFront([card2.htmlElement, card1.htmlElement]);

  $(".pin",card1.htmlElement).hide();

  // tape between cards 
  var k = $(".tape",card1.htmlElement);
  
  k.animate({width: [ "show", "swing" ]});
  k.off().
   // click on tape => detach cards
   on("mousedown touchstart MSPointerDown pointerdown", function(e){
    stopEvent(e);
    // disable click on card (popup) by adding noclick class
    card1.htmlElement.addClass("noclick");
    
    k.animate({width: [ "hide", "swing" ]});
    // move upper card a bit up
    $('.pin',card1.htmlElement).hide(); 
    if(card1.attachedTo)
      $('.pin',card1.attachedTo.htmlElement).hide(); 
    var c2 = card1.attachedTo;
    card1.htmlElement.addClass("dragging");
    if(card1.attachedTo)
      card1.attachedTo.htmlElement.addClass("dragging");
    var changePos1 = null;
    var changePos2 = null;
    if(direction == "horizontal") {
      changePos1 = {"left":"-=8"};
      changePos2 = {"left":"+=8"};
    }
    if(direction == "vertical") {
      changePos1 = {"top":"-=8"};
      changePos2 = {"top":"+=8"};
    }
    if(card1.attachedTo)
      card1.attachedTo.htmlElement.animate(changePos1,500,function(){
        $('.pin',card1.htmlElement).show(); 
        $('.pin',c2.htmlElement).show(); 
        $('.card').removeClass("dragging");
      }).removeClass("wrong correct");
    // move lower card a bit down
    card1.htmlElement.animate(changePos2).removeClass("wrong correct");

    card1.attachedTo = null;
    card2.attached = null;
    checkAppCompleted();
   }).
   on("touchend mouseup MSPointerUp pointerup", function(e){
    card1.htmlElement.removeClass("noclick");
   });

  // automatically check for correct solution in fade play
  if(playMode == "fade")
    checkSolution();
 }

 if(direction == "vertical"){
  if(card1.attachedTo) 
   $('.pin',card1.attachedTo.htmlElement).show(); else
   $('.pin',card1.htmlElement).show(); 
 }else{
  if(card1.attachedTo) 
   $('.pin',card1.attachedTo.htmlElement).show(); 
  if(card1.attached) 
   $('.pin',card1.attached.htmlElement).show(); 
  $('.pin',card1.htmlElement).show(); 
 }
  
  checkAppCompleted();
     
}
///////////////////////////////////////////////////////////////////////////////
// check if all elements are connected and inform upper frames via postmessage
///////////////////////////////////////////////////////////////////////////////
function checkAppCompleted () {
 var completed = true;
 for(i = 0; i < Pair1List.length; i++){
   if(Pair1List[i].card.attached === null && Pair1List[i].card.attachedTo === null) {
     completed = false;
     break;
   }
 }
 AppClient.setCompleted(completed);
}

///////////////////////////////////////////////////////////////////////////////
// make card pairs move always together while dragging around
///////////////////////////////////////////////////////////////////////////////
function repositionCardPair(card){
 var h = $("#cards").height(); 
 var w = $("#cards").width(); 
 var dx, dy;
 // this card has another on attached to it 
 if(direction == "horizontal") {
   if(card.attached !== null) {
    Draggable.bringToFront([card.htmlElement, card.attached.htmlElement]);

    card.attached.htmlElement.css({"top":card.htmlElement.css("top"),
                                   "left" :(parseInt(card.htmlElement.css("left"))+
                                           card.htmlElement.outerWidth()+
                                           card.htmlElement.outerHeight()*0.04)+"px"});

    dx = w - (card.attached.htmlElement.position().left+
              card.attached.htmlElement.outerWidth());

    if (dx < 0) card.htmlElement.css("left",parseInt(card.htmlElement.css("left"))+dx-5+"px");

    card.attached.htmlElement.css("left",(parseInt(card.htmlElement.css("left"))+
                                         card.htmlElement.outerWidth()+
                                         card.htmlElement.outerHeight()*0.04)+"px");
   }

   // this card is attached to another card
   if(card.attachedTo !== null) {
    Draggable.bringToFront([card.attachedTo.htmlElement, card.htmlElement]);
    card.attachedTo.htmlElement.css({"top":card.htmlElement.css("top"),
                                     "left" :(parseInt(card.htmlElement.css("left"))-
                                            (card.attachedTo.htmlElement.outerWidth()+
                                             card.htmlElement.outerHeight()*0.04))+"px"});

    dx = card.attachedTo.htmlElement.position().left;
    if (dx < 0) card.htmlElement.css("left",parseInt(card.htmlElement.css("left"))-dx+5+"px");

    card.attachedTo.htmlElement.css("left",(parseInt(card.htmlElement.css("left"))-
                                      (card.attachedTo.htmlElement.outerWidth()+
                                       card.htmlElement.outerHeight()*0.04))+"px");
   }
 }
 if(direction == "vertical") {
   if(card.attached !== null) {
    Draggable.bringToFront([card.htmlElement, card.attached.htmlElement]);

    card.attached.htmlElement.css({"left":card.htmlElement.css("left"),
                                   "top" :(parseInt(card.htmlElement.css("top"))+
                                           card.htmlElement.outerHeight()+
                                           card.htmlElement.outerWidth()*0.04)+"px"});

    dy = h - (card.attached.htmlElement.position().top+
              card.attached.htmlElement.outerHeight());

    if (dy < 0) card.htmlElement.css("top",parseInt(card.htmlElement.css("top"))+dy-5+"px");

    card.attached.htmlElement.css("top",(parseInt(card.htmlElement.css("top"))+
                                         card.htmlElement.outerHeight()+
                                         card.htmlElement.outerWidth()*0.04)+"px");
   }

   // this card is attached to another card
   if(card.attachedTo !== null) {
    Draggable.bringToFront([card.attachedTo.htmlElement, card.htmlElement]);
    card.attachedTo.htmlElement.css({"left":card.htmlElement.css("left"),
                                     "top" :(parseInt(card.htmlElement.css("top"))-
                                            (card.attachedTo.htmlElement.outerHeight()+
                                             card.htmlElement.outerWidth()*0.04))+"px"});

    dy = card.attachedTo.htmlElement.position().top;
    if (dy < 0) card.htmlElement.css("top",parseInt(card.htmlElement.css("top"))-dy+5+"px");

    card.attachedTo.htmlElement.css("top",(parseInt(card.htmlElement.css("top"))-
                                      (card.attachedTo.htmlElement.outerHeight()+
                                       card.htmlElement.outerWidth()*0.04))+"px");
   }
 }
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
 // font size of everything based on window size
 $("body").css({"font-size":Math.round(m/60)+"px"}); 
  
 $(".card").css({"width":Math.round(m*0.175)+"px", "padding":Math.round(m*0.01)+"px"}); 
 $(".pin").css({"border-radius":Math.round(m/50)+"px",
                "width":Math.round(m/50)+"px",
                "height":Math.round(m/50)+"px",
                "top":-Math.round(m/50/1.5)+"px",
                "margin-left":-Math.round(m/50/2)+"px"});
 
 $(".card").each(function(){
  var card = $(this).data("card");
  var x = card.htmlElement.position().left;
  var y = card.htmlElement.position().top;
  if(lastWindowSizeW != -1 && lastWindowSizeH != -1){
   var cw = card.htmlElement.outerWidth();
   var ch = card.htmlElement.outerHeight();
   card.htmlElement.css("left",Math.round(Math.min(w-cw-5,(Math.round(w * x / lastWindowSizeW))))+"px");
   card.htmlElement.css("top" ,Math.round(Math.min(h-ch-5,(Math.round(h * y / lastWindowSizeH))))+"px");
  }
  var ow = card.htmlElement.outerWidth();
  var oh = card.htmlElement.outerHeight();
  $("img",card.htmlElement).css("max-height",Math.min(Math.round(h/2-m*0.03), Math.round(Math.min(ow*2, h/2-20)))+"px");

  if(direction == "horizontal")
    $(".tape",card.htmlElement).css({"height":Math.round(ow*0.25)+"px",
                              "width":Math.round(ow*0.8 / 2)+"px",
                              "margin-left":-1*Math.round(ow / 4)+"px",
                              "top":"0px",
                              "left":Math.round(ow*0.8 / 32)+"px",
                              "background-size":Math.round(ow*0.35)+"px"});
  if(direction == "vertical")
    $(".tape",card.htmlElement).css({"width":Math.round(ow*0.8)+"px",
                              "height":Math.round(ow*0.8 / 4)+"px",
                              "top":-Math.round(ow/6)+"px",
                              "margin-left":-Math.round(ow*0.8 / 2)+"px", 
                              "background-size":Math.round(ow*0.8)+"px"});
 });

 // after resize refit attached cards again 
 $(".card").each(function(){
   var card = $(this).data("card");
   if(card.attached) repositionCardPair(card);
   doResizeText(card);
 });

 // remember current window size for next change
 lastWindowSizeW = w;
 lastWindowSizeH = h;
}
///////////////////////////////////////////////////////////////////////////////
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
  var cardsattached = 0;
  // remove card colors for new check
  for(i = 0; i < Pair1List.length; i++){
    Pair1List[i].card.htmlElement.removeClass("wrong correct");
    Pair2List[i].card.htmlElement.removeClass("wrong correct");
  }
  for(i = 0; i < WrongList.length; i++){
    WrongList[i].card.htmlElement.removeClass("wrong correct");
  }  
  
  // test if pairs are matching 
  var solutionOk = true;
  var checkResults = [];
  
  for(i = 0; i < Pair1List.length; i++){
    card = Pair1List[i].card; 
    // card has another card attached 
    if(card.attached !== null){
      // does other card  match pair 1? 
      cardsattached++;
      if($.inArray(card.attached, card.matchingCards) >= 0) {
       checkResults.push(1);
       card.htmlElement.addClass("correct");
       card.attached.htmlElement.addClass("correct");
       if(playMode == "fade"){
         card.htmlElement.css("pointer-events","none");
         card.attached.htmlElement.css("pointer-events","none");
         card.htmlElement.fadeOut();
         card.attached.htmlElement.fadeOut();
         card.invisible = true; 
         card.attached.invisible = true; 
       }else
         Draggable.sendToBack([card.attached.htmlElement,card.htmlElement]);
      }else{
       checkResults.push(0);
       card.htmlElement.addClass("wrong");
       card.attached.htmlElement.addClass("wrong");
       Draggable.bringToFront([card.htmlElement,card.attached.htmlElement]);
       solutionOk = false;
       wrong++;
      }
    }
    else
    // card is attached to another card  
    if(card.attachedTo !== null){
      // does other card  match pair 1? 
      if($.inArray(card.attachedTo, card.matchingCards) >= 0) {
       checkResults.push(1);
       card.htmlElement.addClass("correct");
       card.attachedTo.htmlElement.addClass("correct");
       if(playMode == "fade"){
         card.htmlElement.fadeOut();
         card.attachedTo.htmlElement.fadeOut();
         card.invisible = true; 
         card.attachedTo.invisible = true; 
       }else
         Draggable.sendToBack([card.htmlElement,card.attachedTo.htmlElement]);
      }else{
       checkResults.push(0);
       card.htmlElement.addClass("wrong");
       card.attachedTo.htmlElement.addClass("wrong");
       Draggable.bringToFront([card.attachedTo.htmlElement,card.htmlElement]);
       solutionOk = false;
       wrong++;
      }
    }    
    else{
     // check if this card is attached anywhere, solution cannot be right yet
     solutionOk = false;
     checkResults.push(0);
    }
  } 
  
  // check wrong cards (not part of the solution), 
  // if there is a card attached to them, solution cannot be right yet
  for(i = 0; i < WrongList.length; i++){
    card = WrongList[i].card; 

    if(card.attachedTo !== null){
       checkResults.push(0);
       card.htmlElement.addClass("wrong");
       card.attachedTo.htmlElement.addClass("wrong");
       Draggable.bringToFront([card.attachedTo.htmlElement,card.htmlElement]);
       solutionOk = false;
       wrong++;
    }else
    if(card.attached !== null){
       checkResults.push(0);
       card.htmlElement.addClass("wrong");
       card.attached.htmlElement.addClass("wrong");
       Draggable.bringToFront([card.htmlElement,card.attached.htmlElement]);
       solutionOk = false;
       wrong++;
    }else
       checkResults.push(1);
  }

  if(playMode == "fade"){
    if(cardsattached == Pair1List.length || wrong > 0) AppClient.setChecked(checkResults); 
  }else
    AppClient.setChecked(checkResults);

  // tell LearningApps this app was solved
  if(solutionOk) AppClient.setSolved();

  if(solutionOk && playMode == "fade"){
    for(i = 0; i < WrongList.length; i++){
      card = WrongList[i].card; 
      card.htmlElement.fadeOut();
    }
  }
  
  // user found the correct solution? if feedback is not already displayed show it
  if(solutionOk)
    AppClient.showFeedbackPanel("feedback");
}

