
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


