$(document).ready(function(){
     
     $("#addform").submit(function(event) {
          
          event.preventDefault(); //prevent default action 
          let post_url = $(this).attr("action"); //get form action url
          let request_method = $(this).attr("method"); //get form GET/POST method
          let form_data = new FormData($('#addform').get(0)); //Encode form elements for submission	
          var dialog;
          
          $.ajax({
               url: post_url,
               type: request_method,
               data: form_data,
               contentType: 'multipart/form-data',
               processData: false,
               contentType: false,
               
         
          }).done(function(resp) { //
               // $("#server-results").html(response);
               // dialog.modal('hide');
               if(resp.sent == 'username_taken'){
                    bootbox.alert('Username already taken');
               }else if(resp.sent == 'email_taken') {
                    
                    bootbox.confirm({
                         message: "The provided email address is linked to a user but not to a patient. Would you like to merge the accounts?",
                         buttons: {
                              cancel: {
                                   label: '<i class="fa fa-times"></i> Cancel'
                              },
                              confirm: {
                                   label: '<i class="fa fa-check"></i> Confirm'
                              }
                         },
                         callback: function (result) {
                              if(result) {
                                        
                                   $.ajax({
                                        type: request_method,
                                        url: '/add_patient_merge',
                                        data: form_data,
                                        contentType: 'multipart/form-data',
                                        processData: false,
                                        contentType: false,
                                   }).done(function(resp) {
                                        if(resp.sent == 'saved') {
                                             
                                             window.location.href = "/patientview";
                                             
                                        }else if(resp.sent == 'data_not_valid') {
                                             bootbox.alert('No valid data Entered')
                                             
                                        }
                                   })
                                        
                              }else {
                                   setTimeout(function(){
                                        bootbox.alert('Please change your email address');
                                   }, 350);
                              }
                         }
                    });
               }else if(resp.sent == 'pass_not_matched') {
                    
                    bootbox.alert('Password not matched');
               }else if(resp.sent == 'no_valid_pass') {
                    bootbox.alert('No valid password entered');
               }else if(resp.sent == 'data_not_valid') {
                    bootbox.alert('Data not valid');
                    
               }else if(resp.sent == 'saved') {
                    
                    window.location.href = "/patientview";
               }
          })
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








