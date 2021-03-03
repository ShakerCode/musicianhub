function validateForm() {
    var proximity = document.getElementById("proximity").value.trim();
    if(isNaN(proximity) || /^ *$/.test(proximity)) {
        console.log('');
        alert("Enter data correctly");
        return false
    }
}