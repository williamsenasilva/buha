$(document).ready(function() {
  $("#insert-server").on('click', insertServer);
});

function insertStudent() {
  var student = {};
  student["name"] = $("#input-name").val();  
  student["university"] = $("#input-university").val();  
  student["academicID"] = $("#input-academic-id").val();  
  $.ajax({
    type: "POST",
    url: "/api/insert-student",
    data: JSON.stringify(student, null, '\t'),
    contentType: 'application/json;charset=UTF-8',
    timeout: 10000,
    success: function(data){
      window.location.reload();
    },
    error: function(error){
      alert("Erro. Por favor tente novamente.\nErro:" + error);
    }
  }); 
}

function insertServer() {
  $.ajax({
    type: "POST",
    url: "/api/insert-server",
    contentType: 'application/json;charset=UTF-8',
    timeout: 10000,
    success: function(){
      window.location.reload();
    },
    error: function(error){
      alert("Erro. Por favor tente novamente.\nErro:" + error);
    }
  }); 
}