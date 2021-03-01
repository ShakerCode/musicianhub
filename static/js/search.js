$(document).ready(function () {
    $("#instrument").autocomplete({
      source: function(request, response) {
        $.ajax({
          url: $("#autocomplete_url").attr("data-url"),
          dataType: 'json',
          data: {
            'term': request.term,
            'searchType': 'userSearch'
          },
          success: function(data) { 
            response(data)
          }
        });
      },
      minLength: 2,
      open: function () {
        setTimeout(function () {
          $('.ui-autocomplete').css('z-index', 99);
        }, 0);
      }
    });
    // $('#searchForm').submit(function (event) {
    //     var token = '{{csrf_token}}';
    // })
});

function validateForm() {
  var proximity = document.getElementById("proximity").value.trim();
  if(isNaN(proximity) || /^ *$/.test(proximity)) {
      console.log('');
      alert("Enter data correctly");
      return false
  }
}