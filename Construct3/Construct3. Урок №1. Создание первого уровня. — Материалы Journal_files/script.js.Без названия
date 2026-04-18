var MODEL = null;
var NUMBER_REPLACED_GAPS = 0;
/////////////////////////////////////////////////////////////////////////////
AppClient.onInit = function () {
 MODEL = createModel( AppClient.getParameters('cloze#') );
  
 cacheDomElements();
 bindOnCheckEvent();
  
 formatBackground( AppClient.getParameter('backgroundImage') );
 formatHeading( AppClient.getParameters('titel') );
 formatHeading( AppClient.getParameters('untertitel'), true );
 formatText( AppClient.getParameters('clozetext') );
};
/////////////////////////////////////////////////////////////////////////////
function cacheDomElements () {
 $content = $('#content');
 $checkSolutionBtn = $('#checkSolutionBtn');
}
/////////////////////////////////////////////////////////////////////////////
function formatBackground (background) {
 var backgroundImageURL = background;
 if (backgroundImageURL === "") backgroundImageURL = "back.jpg";
 var img = new Image() ;
 img.onload = function() {
  $('body').css('background-image','url('+backgroundImageURL+')');
 };
 img.src = backgroundImageURL; 
}
/////////////////////////////////////////////////////////////////////////////
function formatHeading (heading,tiny) {
 var id = Math.random();
 var $card = $('<div class="card '+(tiny ? 'small-card' : 'bold')+'"></div>');
 var $cardInner = $('<div id="'+id+'"></div>');
  
 $card.append($cardInner);
  
 if (heading.media === "text") {
  if (heading.value !== "") {
   $card.append(AppClient.linkifyText(heading.value));
   $content.append($card);
  }
 }
 
 if (heading.media === "image") {
  $img = $('<img src="'+heading.value+'" />');
  $card.append($img);
   
  $img.load(function () {
   $img.on('click', function () {
    var img = new Image();
    img.src = heading.value;
     
    if(img.width > $card.width()*2 || img.height > $card.height()*2){
     createModalDialogFrame(
      '<div id="modalContentInner"></div>',
       function() {
        // on show
        $('#modalContentInner').html(
         '<img data-dismiss="modal" class="img-responsive" style="margin: 0 auto;" src="'+heading.value+'" alt=""/>' +
          (heading.hint !== "" ? '<div class="modal-hint">' + AppClient.linkifyText(heading.hint).replace(/"/g,'&quot;') + '<div>' : '')
        );
       }  
      ).modal("show");
     }
    });
   });
   
  if (heading.value !== "") {
   $content.append($card);
   $content.addClass("sidebyside");
  }
 }
  
 if (heading.media === "speech") {
  if (heading.value !== "") {
   $content.append($card);
   heading.loadPlayer(id,false);
   $content.addClass("sidebyside");
  }
 }
  
 if (heading.media === "audio") {
  if (heading.value !== "") {
   $content.append($card);
   heading.loadPlayer(id,false);
   $content.addClass("sidebyside");
  }
 }
  
 if (heading.media === "video") {
  if (heading.value !== "") {
   $content.append($card);
   $cardInner.css('height','300px');
   heading.loadPlayer(id,false);
   $content.addClass("sidebyside");
  } 
 }
  
 // hint
 if (heading.hint !== "") {
  if (heading.media !== "image") {
   $card.append(
    '<span class="hintbtn hintbtn_'+heading.media+' popovers"'+ 
    ' data-container="#cards" data-toggle="popover" data-placement="auto"'+
    ' data-content="'+AppClient.linkifyText(heading.hint).replace(/"/g,'&quot;')+'">'+
    '<span class="glyphicon glyphicon-info-sign infoicon"></span></span>');
     
    $('.popovers',$card).popover({
     trigger:"hover",
     placement: "bottom",
     container:'body'
    }).on('touchstart mousedown', function(e) {
     stopEvent(e);
     $(this).popover('toggle');
    });
   } else {
     $card.append(
      '<div class="heading-hint">'+AppClient.linkifyText(heading.hint).replace(/"/g,'&quot;')+'</div>'
     );
   }
 }
  
}
/////////////////////////////////////////////////////////////////////////////
function replaceBetween (start, end, what, str) {
 return str.substring(0, start) + what + str.substring(end);
}
/////////////////////////////////////////////////////////////////////////////
function formatText (text) {
 var pattern = /-\d+-/g;
 var $text = $('<div class="gap-text"></div>');
  
 // make text more readable if a custom background is provided
 if (AppClient.getParameter('backgroundImage') !== "") {
  $text.css('background-color','rgba(255,255,255,.7)');
 }
  
 // if no title / subtitle --> make more top space (special case app matrix)
 if (AppClient.getParameter('titel') === "" && AppClient.getParameter('untertitel') === "") {
  $text.css('margin-top','50px');   
 }
  
 // make line breaks and paragraphs
 text.value = text.value.replace(/\r/g,"");
 text.value = text.value.replace(/\n/g,"<br>");
 
 var gapsReplaced = 0;
 var modelIndex = null;
  
 // preprocess white spaces around gaps
 while ( (result = pattern.exec(text.value)) ) {
   var searchBack = 1;
   var whiteSpacheBefore = 0;
   while(result.index-searchBack >= 0){
     if(text.value[result.index-searchBack] == " " || text.value[result.index-searchBack] == ">"){
       whiteSpacheBefore = searchBack;
       break;
     }
     searchBack++;
     if(result.index-searchBack < 0){
       whiteSpacheBefore = searchBack;
     }
   } 
   var searchAfter = 1;
   var whiteSpacheAfter = 1;
   while(result.index+result[0].length-1+searchAfter < text.value.length){
     if(text.value[result.index+result[0].length-1+searchAfter] == " " || text.value[result.index+result[0].length-1+searchAfter] == "<"){
       whiteSpacheAfter = searchAfter;
       break;
     }
     searchAfter++;
     if(result.index+result[0].length-1+searchAfter >= text.value.length){
       whiteSpacheAfter = searchAfter;
     }
   } 
    
   if(whiteSpacheBefore > 1 || whiteSpacheAfter > 1){
     var inner = text.value.substring(result.index-whiteSpacheBefore+1,result.index+result[0].length+whiteSpacheAfter-1);
     var innerNew = inner.replace(/-(\d+)-/g,"▂$1▂");
     text.value = replaceBetween(result.index-whiteSpacheBefore+1,result.index+result[0].length+whiteSpacheAfter-1,'<span style="white-space:nowrap">'+innerNew+'</span>',text.value);   
   }else{
     var inner = result[0];
     var innerNew = inner.replace(/-(\d+)-/g,"▂$1▂");
  	 text.value = replaceBetween(result.index,result.index+result[0].length,innerNew,text.value);   
   
   }
 }  
 var pattern = /▂\d+▂/g;
  
 // Dropdown MODE
 if (!AppClient.isTranslationOf('Einschreiben',AppClient.getParameter("type"))) { 
  while ( (result = pattern.exec(text.value)) ) {
   modelIndex = result[0].split('▂')[1]-1;
   text.value = replaceBetween(result.index,result.index+result[0].length,createDropDown(modelIndex),text.value);
   gapsReplaced++;
  }
  $content.append($text.append(text.value));
  $('.gap').on('click',onGapSelect);
  dynamicDropdownOrUp();
 }
  
 // Input MODE
 else {
  while ( (result = pattern.exec(text.value)) ) {
   modelIndex = result[0].split('▂')[1]-1;
   text.value = replaceBetween(result.index,result.index+result[0].length,createInput(modelIndex),text.value);
   gapsReplaced++;
  }
  $content.append($text.append(text.value));
  $('.input-field').on('input propertychange',onInput);
  $('.input-field').on('keypress',jumpOnEnterToTheNextField);
 }
  
 // make hint popover hoverable and touchable
 $('.popovers').popover({trigger:"hover"})
  .on('touchstart mousedown', function(e) {
     stopEvent(e);
     $(this).popover('toggle');
  });


 NUMBER_REPLACED_GAPS = gapsReplaced;
}
/////////////////////////////////////////////////////////////////////////////
function createModel (model) {
 var m = [];
 for (var i = 0,index=0; i < model.length; i++) {
  if (model[i].value !== "") {
   // clean out any -1- inside answers or we get infinite loop later
   model[i].value = model[i].value.replace(/-\d+-/g,"");
   var values = model[i].value.split(';');
   for (var j = 0; j < values.length; j++) {
     values[j] = $.trim(values[j]);
     values[j] = values[j].replace(/\n/g," ").replace(/ +(?= )/g,'');
     values[j] = values[j].replace(/ +(?= )/g,'');
     values[j] = values[j].replace(/\n/g,' ');
     values[j] = values[j].replace(/[\u00A0\u202F]/g," ");
     values[j] = values[j].replace(/[´’‘‘’]/g,"'"); 
     values[j] = values[j].replace(/[„“”]/g,'"');
     values[j] = values[j].replace(/ +(?= )/g,'');
     values[j] = values[j].replace(/[−˗➖﹣－\u2014\u2015\u203E\u2043\u23AF\u23E4\u2500\u2501]/g,'-');
   }
   m.push( {values:values,correctAnswer:values[0],index:index} );
   index++;
  }
 }
 return m; 
}
/////////////////////////////////////////////////////////////////////////////
function createInput (modelIndex) {
 var obj = MODEL[modelIndex];
 var size = 0;
 if (obj) {
  for (var i = 0; i < obj.values.length; i++) {
   if (obj.values[i].length > size) size = obj.values[i].length + 1;
  }
  return '<input class="form-control input-field" size="'+size+'" data-model-index="'+modelIndex+'"></input><span class="solvebtn popovers" data-model-index="'+modelIndex+'"'+ 
         ' data-toggle="popover" data-placement="auto"'+
         ' data-content="'+obj.values.join("; ").replace(/"/g,'&quot;')+'">'+
         '<span class="glyphicon glyphicon-question-sign solutionicon"></span></span>';
 } else return createMissingInputValue(modelIndex);
}
/////////////////////////////////////////////////////////////////////////////
function createMissingInputValue (modelIndex) {
 // if the user created a gap but doesn't fill in a solution, show him that it is missing
 return '<span>&ndash;'+(modelIndex+1)+'&ndash;</span>';
}
/////////////////////////////////////////////////////////////////////////////
function getDropdownlist (values) {
 $.unique(values);
 values.sort(function (a,b) { 
   if(a.value.toLowerCase() != b.value.toLowerCase())
     return a.value.toLowerCase().localeCompare(b.value.toLowerCase()); 
   return a.value.localeCompare(b.value); 
 });
  
 var l = "";
 var alreadyInList = [];
  
 for (var i = 0; i < values.length; i++) {
  if(alreadyInList.indexOf(values[i].value) != -1) continue; 
  var v = values[i].value.replace(/"/g, "&quot;");
  l += '<li>' +
   '<a role="button" class="gap" data-value="'+v+'" data-index="'+values[i].gap+'">'+values[i].value+'</a>' +
  '</li>';
  alreadyInList.push(values[i].value); 
 }
 return l;
}
/////////////////////////////////////////////////////////////////////////////
function createDropDown (index) {
  
 var obj = getObjectByIndex(index);
 var values = [];
 
 if (obj) {
  // if there are no multiple options, display all entries at the dropdown
  if (obj.values.length === 1) { 
   for (var i = 0; i < MODEL.length; i++) {
    for (var j = 0; j < MODEL[i].values.length; j++) {
      values.push({value:MODEL[i].values[j],gap:index});
    }
   }
  }
  // multiple entries, just use these, leave others
  if (obj.values.length > 1) {
   for (var a = 0; a < obj.values.length; a++) {
     values.push({value:obj.values[a],gap:index});
   }
  }
 }
  
 var s =
  '<div class="dropdown gap-dropdown" data-selected-value="" data-selected-model-index="-1">' +
   '<button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">' +
  '</button>' +
  '<ul class="dropdown-menu">'+
   getDropdownlist(values) +
  '</ul>' +
 '</div>';
  
 return s;
}
/////////////////////////////////////////////////////////////////////////////
function onGapSelect (e) {
 var data; 
 if($(e.target).hasClass("gap")){
   data = $(e.target).data();
 }else{
   data = $(e.target).parents('.gap').data(); 
 }
 
 var button = $('button', $(e.target).parents('.gap-dropdown'));
 button.html(data.value);
 button.removeClass('btn-danger btn-success').addClass('btn-default');
  
 $(e.target).parents('.gap-dropdown').data().selectedValue = data.value;
 $(e.target).parents('.gap-dropdown').data().selectedModelIndex = data.index;
 checkAppCompleted();
}
/////////////////////////////////////////////////////////////////////////////
function onInput (e) {      
 $(e.target).removeClass('btn-danger btn-success');
 $(e.target).next().hide(); // .solvebtn
 // how often this input was changed by the user
 if(!$(e.target).data().changes) $(e.target).data().changes = 0;
 if(!$(e.target).data().unchecked) $(e.target).data().changes++; 
 $(e.target).data().unchecked = true; // not count ahead until next check 
 checkAppCompleted();
}
/////////////////////////////////////////////////////////////////////////////
function jumpOnEnterToTheNextField (e) {
 if (e.which == 13) {
  // go to next element
  e.preventDefault();
  var $canfocus = $('input');
  var index = $canfocus.index(document.activeElement) + 1;
  if (index >= $canfocus.length) index = 0;
   $canfocus.eq(index).focus();
 } 
}
/////////////////////////////////////////////////////////////////////////////
function bindOnCheckEvent () {
 $checkSolutionBtn.on('click',checkSolution); 
}
/////////////////////////////////////////////////////////////////////////////
function checkSolution () {
  if (!AppClient.isTranslationOf('Einschreiben',AppClient.getParameter("type"))) {
   onCheck_select();
  } else {
   onCheck_input();
  } 
  checkAppCompleted();
}
///////////////////////////////////////////////////////////////////////////////
// check if all gaps are filled or selected (depends on mode) and inform upper frames via postmessage
///////////////////////////////////////////////////////////////////////////////
function checkAppCompleted () {
 var completed = true;
  if (!AppClient.isTranslationOf('Einschreiben',AppClient.getParameter("type"))) {
    $('.gap-dropdown').each(function (index,element) {
      var data = $(element).data();
      var selectedValue = $.isNumeric(data.selectedValue) ? data.selectedValue : (data.selectedValue+"").replace(/&quot;/g, '\\"'); 
      if (!selectedValue) {
       completed = false; 
      }
    });
  } else {
    
    // input mode, check all inputs if they have some input
    var elems = $('.input-field');
    for (var i = 0; i < elems.length; i++) {
      var input = elems[i].value;
      if (!input || input === "" || input === null) {
       completed = false;
        break;
      }
    }
 }
 AppClient.setCompleted(completed);
}
/////////////////////////////////////////////////////////////////////////////
function getCorrectAnswerFromIndex (index) {
 for (var i = 0; i < MODEL.length; i++) {
  if (MODEL[i].index === index) {
   return MODEL[i].correctAnswer; 
  }
 }
 return "";
}
/////////////////////////////////////////////////////////////////////////////
function getObjectByIndex (index) {
 for (var i = 0; i < MODEL.length; i++) {
  if (MODEL[i].index === index) {
   return MODEL[i]; 
  }
 }
 return null;
}
/////////////////////////////////////////////////////////////////////////////
function onCheck_select () {
 var countCorrectSelectedItems = 0; 
 var checkedResults = [];
  
 $('.gap-dropdown').each(function (index,element) {
  var data = $(element).data();
  var isCorrect = false;
  var selectedValue = $.isNumeric(data.selectedValue) ? data.selectedValue : (data.selectedValue+"").replace(/&quot;/g, '\\"'); 
   
  if (selectedValue !== "" && data.selectedModelIndex !== -1) {
   isCorrect = getCorrectAnswerFromIndex(data.selectedModelIndex) == selectedValue;
  }
 
  if (isCorrect) {
   $(element).find('button').removeClass('btn-default btn-danger').addClass('btn-success'); 
   countCorrectSelectedItems++;
   checkedResults.push(1);
  } else {
   $(element).find('button').removeClass('btn-default btn-success').addClass('btn-danger');
   checkedResults.push(0);
  }
 });
 
 AppClient.setChecked(checkedResults);
 if (countCorrectSelectedItems === NUMBER_REPLACED_GAPS) {
  quitApp(); 
 } 
}
/////////////////////////////////////////////////////////////////////////////
function onCheck_input () {
 var countCorrectSelectedItems = 0; 
 var checkedResults = [];
  
 $('.input-field').each(function (index,element) {
  var data = $(element).data();
  var isCorrect = false;
  var val = $.trim(element.value);
  val = val.replace(/\n/g," ").replace(/ +(?= )/g,'');
  val = val.replace(/ +(?= )/g,'');
  val = val.replace(/\n/g,' ');
  val = val.replace(/[\u00A0\u202F]/g," ");
  val = val.replace(/[´’‘‘’]/g,"'"); 
  val = val.replace(/[„“”]/g,'"');
  val = val.replace(/ +(?= )/g,'');
  val = val.replace(/[−˗➖﹣－\u2014\u2015\u203E\u2043\u23AF\u23E4\u2500\u2501]/g,'-');
  if(val.match(/^[0-9,\s]+$/)) val = val.replace(/,\s+/g,",");

  var isCaseSensitive = AppClient.getParameter('casesense') === "" || AppClient.getParameter('casesense') === "false";
   
  if (val !== '') {
    // if only 1 solution, check it
    if (MODEL[data.modelIndex].values.length === 1) {
     if (isCaseSensitive) isCorrect = val.toUpperCase() === MODEL[data.modelIndex].correctAnswer.toUpperCase();
     else isCorrect = val === MODEL[data.modelIndex].correctAnswer;
    }
    // multiple entries, all of them are correct, check all
    if (MODEL[data.modelIndex].values.length > 1) {
     for (var i = 0; i < MODEL[data.modelIndex].values.length; i++) {
      if (isCaseSensitive) {
       if (MODEL[data.modelIndex].values[i].toUpperCase() === val.toUpperCase()) {
        isCorrect = true;
        break;
       }
      } 
      else {
       if (MODEL[data.modelIndex].values[i] === val) {
        isCorrect = true;
        break;
       }
      }
     }
    }
  }
   
  if (isCorrect) {
   $(element).removeClass('btn-success btn-danger').addClass('btn-success');
   countCorrectSelectedItems++;
   checkedResults.push(1);
  } else {
   $(element).removeClass('btn-success btn-danger').addClass('btn-danger');
   if(AppClient.getParameter('useHelp') !== "false")
     if($(element).data().changes > 2) $(element).next().show(); // .solvebtn
   checkedResults.push(0);
  }
  $(element).data().unchecked = false; // we just checked, reset so we can count another change
 }); 
 AppClient.setChecked(checkedResults);
 if (countCorrectSelectedItems === NUMBER_REPLACED_GAPS) {
  quitApp(); 
 } 
}
/////////////////////////////////////////////////////////////////////////////
function quitApp () {
 AppClient.setSolved();   
 AppClient.showFeedbackPanel("feedback");  
}
/////////////////////////////////////////////////////////////////////////////
function dynamicDropdownOrUp () {
 $(document).on("shown.bs.dropdown", ".dropdown", function () {
  var $ul = $(this).children(".dropdown-menu");
  var $button = $(this).children(".dropdown-toggle");
  var ulOffset = $ul.offset();
  var spaceUp = (ulOffset.top - $button.height() - $ul.height()) - $(window).scrollTop();
  var spaceDown = $(window).scrollTop() + $(window).height() - (ulOffset.top + $ul.height());
  if (spaceDown < 0 && (spaceUp >= 0 || spaceUp > spaceDown))
   $(this).addClass("dropup");
  var wd = $(window).width() - (ulOffset.left + $ul.width())-24;
  if(wd < 0) $ul.css("margin-left",wd+"px");
  // check if list overflows the top, if so, make it temp scrollable
  var maxOnScreenHeight = isOffScreen($ul[0]);
  if (maxOnScreenHeight) {
   $ul.css({'max-height':maxOnScreenHeight+'px',"overflow":"auto"});
  }
 }).on("hidden.bs.dropdown", ".dropdown", function() {
  $(this).removeClass("dropup");
  var $ul = $(this).children(".dropdown-menu");
  $ul.removeAttr('style');
 });
}
/////////////////////////////////////////////////////////////////////////////
function isOffScreen (el) {
 var rect = el.getBoundingClientRect();
 // element is out of top bounds
 if (rect.top < 0 ) {
  var marginTop = 10;
  return rect.height + rect.top - marginTop;
 }
 // element is out of bottom bounds, make max-height 80% of window height
 if (rect.bottom >= $(window).height()) {
  var marginBottom = $(window).height() * 3 / 100;
  return ($(window).height() - rect.top) - marginBottom;
 }
 return null;
}








