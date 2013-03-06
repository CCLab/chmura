function context_popup (speech_id, lemma_id) {

  var xmlhttp;
  var url;

  if (window.XMLHttpRequest)
  { // code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
  } else { // code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }

  url = '/word/context/' + speech_id + '/' + lemma_id + '/';

  xmlhttp.onreadystatechange=function() {
    var popup = document.getElementById("popup")
    if (xmlhttp.readyState==4 && xmlhttp.status==200) {
      popup.innerHTML=xmlhttp.responseText;
      popup.style.display = 'block';
      document.getElementById("metainfo").style.visibility = 'hidden';
    }
  }
  
  xmlhttp.open('GET', url, true);
  xmlhttp.send();
}

function hide_popup () {
  document.getElementById("metainfo").style.visibility = 'visible';
  document.getElementById("popup").style.display = 'none' 
}