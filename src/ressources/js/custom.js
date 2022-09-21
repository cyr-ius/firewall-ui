function checkMessage(jsonMsg) {
  if (jsonMsg.meta.type == 'form') {
    $("#form_add").removeClass("was-validated")
    for (var i = 0; i < jsonMsg.errors.length; i++) {
      var error = jsonMsg.errors[i]
      for (var k in error) {
        $('#'+k).addClass('is-invalid')
        $('#'+k).siblings('.valid-feedback').addClass('invalid-feedback').removeClass('valid-feedback').html(error[k][0])
      }
    }
  } else {
    for (var i = 0; i < jsonMsg.errors.length; i++) {
      if (jsonMsg.errors[i].message) {
        alertForm(jsonMsg.errors[i].title+": "+jsonMsg.errors[i].message, "danger", "form_add");
      } else {
        alertForm(jsonMsg.errors[i], "danger", "form_add");
      }
    }
  }
}

// Alert
function alert(message, type, elementId) {
    var wrapper = document.createElement('div')
    wrapper.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible fade show" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
    var liveAlert = document.getElementById(elementId)
    liveAlert.append(wrapper)
  }

  // Alert Form
function alertForm(message, type, elementId) {
  var wrapper = document.createElement('div')
  wrapper.innerHTML = '<div class="row py-1"><span class="badge bg-' + type +'" role="alert">' + message + '</span></div>'
  var liveAlert = document.getElementById(elementId)
  liveAlert.prepend(wrapper)
}

// Observer catch toast added
function eventToast(element){
    // Select the node that will be observed for mutations
    const targetNode = document.getElementById(element);

    // Options for the observer (which mutations to observe)
    const config = { attributes: true, childList: true, subtree: true };

    // Callback function to execute when mutations are observed
    const callback = function(mutationsList, observer) {
        for(const mutation of mutationsList) {
            if (mutation.type === 'childList') {
                $.each($('.toast'), function(e) { 
                    $(this).toast("show");
                    $(this).on('hidden.bs.toast', function () {
                        $(this).remove();
                    });
                })
            }
    }
};

// Create an observer instance linked to the callback function
const observer = new MutationObserver(callback);

// Start observing the target node for configured mutations
observer.observe(targetNode, config);

return observer
}

// Create Toast
function flashMessage(message, type="success", time="", img="", title="Firewall UI"){
    var toast  = $('.toast_template').clone()
    $(toast).removeClass('toast_template').addClass('toast')
    $(toast).removeAttr('style')
    var role = "status";
    var arialive = "polite";
    var color = "green";    
    if (type == "alert") {
      var role = "alert";
      var arialive = "assertive";
      var color = "red";
    }
    $(toast).attr("role",role);
    $(toast).attr("aria-live",arialive);
    $(toast).find('.toast-color').attr("fill", color);
    $(toast).find('.toast-title').text(title);
    $(toast).find('.toast-body').text(message);
    $('.toast-container').append(toast);
}

// JSONify Form
(function ($) {
    $.fn.serializeFormJSON = function () {

        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name]) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };
})(jQuery);

// Check Validity form
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })
  })()


// Sidebar button
$("#sidebarCollapse").unbind()
$('#sidebarCollapse').on('click', function () {
  $('#sidebar').toggleClass('active');
  document.cookie = "sidebar-collapsed="+$('#sidebar').hasClass('active')+";path=/;samesite=strict;"; 
});

// Modal New section
function section_create(form) {
    section = $(form).attr("data-attr");
    data = $(form).serializeFormJSON();
    $.ajax({
      cache: false,
      method: "POST",
      url: $(form).attr('action'),
      dataType: "json",
      data: JSON.stringify(data),
      contentType: "application/json",
      success: function (responseJson) {
        location.replace('/fw/'+section+'/'+ data.name);
      },
      error: function (jqXHR, exception) {  
        checkMessage(jqXHR.responseJSON.error);
      },
    });
}


$("#section_edit").unbind()
$("#section_edit").click(function (event) {
  form = $('#modal_form_section')
  url = $(this).attr("data-uri");
  data = $(form).serializeFormJSON();
  $.ajax({
    cache: false,
    method: "PUT",
    url: url,
    dataType: "json",
    data: JSON.stringify(data),
    contentType: "application/json",
    success: function () { 
      location.reload();
    },
    error: function (jqXHR, exception) {
      checkMessage(jqXHR.responseJSON.error);
    },
  });    
});

$("#section_delete").unbind()
$("#section_delete").click(function (event) {
  var recipient = this.getAttribute('data-message');
  var url = this.getAttribute('data-uri');
  var yesno = document.getElementById('yesno');
  var modalBody = yesno.querySelector('#yesno .modal-body');
  modalBody.textContent=recipient;  

  var yesno_modal = new bootstrap.Modal(yesno);
  yesno_modal.show()

  $('#yesno .modal-footer button').unbind()
  $('#yesno .modal-footer button').on('click', function(event) {
    var button = $(event.target); // The clicked button
    $(this).closest('.modal').one('hidden.bs.modal', function() {
      if (button.val() == 'True') {
        $.ajax({
          method: "DELETE",
          url: url,
          success: function () {
            location.replace('/');
          },
          error: function (jqXHR) {
            checkMessage(jqXHR.responseJSON.error);
          },
        }); 
      };
    });
  });
});



$("#section_reset").unbind()
$("#section_reset").click(function (event) {
  var recipient = this.getAttribute('data-message');
  var url = this.getAttribute('data-uri');
  var yesno = document.getElementById('yesno');
  var modalBody = yesno.querySelector('#yesno .modal-body');
  modalBody.textContent=recipient;  

  var yesno_modal = new bootstrap.Modal(yesno);
  yesno_modal.show()

  $('#yesno .modal-footer button').unbind()
  $('#yesno .modal-footer button').on('click', function(event) {
    var button = $(event.target); // The clicked button
    $(this).closest('.modal').one('hidden.bs.modal', function() {
      if (button.val() == 'True') {
        $.ajax({
          method: "POST",
          url: url,
          success: function () {
            location.reload();
          },
          error: function (jqXHR) {
            checkMessage(jqXHR.responseJSON.error);
          },
        }); 
      };
    });
  });
});


$(document).ready(function () {
  // Run observer to toast
  eventToast('toast')

  // Catch flash message from Flask
  var toastLiveBox = document.getElementById('toastBox')
  if (toastLiveBox) {

    toastLiveBox.addEventListener('hidden.bs.toast', function () {
      $(this).remove();
    });

    var toast = new bootstrap.Toast(toastLiveBox)
    toast.show()

  }
});