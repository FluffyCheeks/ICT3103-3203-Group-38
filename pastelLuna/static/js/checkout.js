
window.onload = function() {
        document.getElementById('creditinfo').style.display = 'none';
    };
function showhidecredit(){
    if (document.getElementById('checked').checked){
        document.getElementById('creditinfo').style.display="block";
        document.getElementById('CODBTN').style.display="none";
    
    }
    else{
        document.getElementById('creditinfo').style.display="none";
        document.getElementById('CODBTN').style.display="block";
    }
}
function creditCardValidation(creditCradNum)
{
  var masregEx = /^5[1-5][0-9]{14}?$/;
  var visregex = /^4[0-9]{15}?$/;
    if(creditCradNum.value.match(masregEx | visregex))
    {
        return true;
    }
    else
    {
        alert("Please enter a valid Master/Visa credit card number.");
        return false;
    }
} 

