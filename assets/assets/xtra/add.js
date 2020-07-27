
$("#addform").submit(function(event) {
    event.preventDefault(); //prevent default action 
    let post_url = $(this).attr("action"); //get form action url
    let request_method = $(this).attr("method"); //get form GET/POST method
    let form_data = new FormData($('#addform').get(0)); //Encode form elements for submission	
    
    $.ajax({
        url: post_url,
        type: request_method,
        data: form_data,
        contentType: 'multipart/form-data',
        processData: false,
        contentType: false,
    }).done(function(resp) { //
       // $("#server-results").html(response);
       if(resp.sent == 'username_taken'){
           alert('Username already taken');
       }else if(resp.sent == 'email_taken') {
            $("#delete_patient").modal('show');
       }else if(resp.sent == 'pass_not_matched') {
            alert('Password not matched');
       }else if(resp.sent == 'no_valid_pass') {
            alert('No valid password entered');
       }else if(resp.sent == 'data_not_valid') {
            alert('Data not valid');
       }else if(resp.sent == 'saved') {
            window.location.href = "/patientview";
       }
    });
     $("#button_1").click(function(event) {
          event.preventDefault();
          $("#delete_patient").modal('hide');
          $.ajax({
               type: request_method,
               url: '/add_patient_merge',
               data: form_data,
               contentType: 'multipart/form-data',
               processData: false,
               contentType: false,
          }).done(function(result) {
               if(result.sent == 'saved') {
                    
                    window.location.href = "/patientview";
                    alert('Accounts merged');
               }else if(result.sent == 'data_not_valid') {
                    alert('No valid data Entered')
               }
          });                
     });
});
$(document).on({
     ajaxStart: function(){
         $("body").addClass("loading"); 
     },
     ajaxStop: function(){ 
         $("body").removeClass("loading"); 
     }    
 }); 

