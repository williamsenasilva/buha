$(document).ready(function() {
});

function insertStudent() {
  var student = {};
  student["name"] = $("#input-name").val();  
  student["university"] = $("#input-university").val();  
  student["academicID"] = $("#input-academic-id").val();  
  //alert("Inserindo estudante "+student["name"]+" "+student["university"]+" "+student["academicID"])
  $.ajax({
    type: "post",
    url: "/api/insert-student",
    data: JSON.stringify(student, null, '\t'),
    contentType: 'application/json;charset=UTF-8',
    timeout: 30000,
    success: function(data){
      window.location.reload();
    },
    error: function(error){
      console.log("Erro.")
      console.log(error)
      alert("Erro. Por favor tente novamente.\nErro:" + error);

    }
    
  });
  return false
}