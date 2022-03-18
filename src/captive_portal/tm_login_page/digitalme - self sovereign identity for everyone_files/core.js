$(document).ready(function() {
  // -- form name
  if ($('#form-name').length) {
    $('#name').focus();
    $('#form-name').submit(function(e) {
      var name = $('#name').val();
      if (name.length < 3) {
        $('#name').addClass('alert-danger');
        $('#err_name')
          .removeClass('mx-hide')
          .html('Please enter full name');
        $('#name').focus();
        e.preventDefault();
      }
    });
  }

  // -- form email
  var on_submit_email = function(e) {
    var email = $('#email').val();
    if (email.length < 3) {
      $('#email').addClass('alert-danger');
      $('#err_email')
        .removeClass('mx-hide')
        .html('Please enter valid email');
      $('#email').focus();
      e.preventDefault();
    }
  };

  if ($('#form-email').length) {
    $('#email').focus();
    $('#form-email').on('submit', on_submit_email);
  }

  // -- sms tac validation
  $('#tac_1').keypress(function(e) {
    if (parseInt(String.fromCharCode(e.which)) >= 0) {
      $('#tac_2').focus();
      $('#tac_2').val(' ');
      $('#tac_1').val(String.fromCharCode(e.which));
    } else {
      $('#tac_1').val(' ');
    }
  });
  $('#tac_2').keypress(function(e) {
    if (parseInt(String.fromCharCode(e.which)) >= 0) {
      $('#tac_3').focus();
      $('#tac_3').val(' ');
      $('#tac_2').val(String.fromCharCode(e.which));
    } else {
      $('#tac_2').val(' ');
    }
  });
  $('#tac_3').keypress(function(e) {
    if (parseInt(String.fromCharCode(e.which)) >= 0) {
      $('#tac_4').focus();
      $('#tac_4').val(' ');
      $('#tac_3').val(String.fromCharCode(e.which));
    } else {
      $('#tac_3').val(' ');
    }
  });
  $('#tac_4').keypress(function(e) {
    if (parseInt(String.fromCharCode(e.which)) >= 0) {
      $('#tac_5').focus();
      $('#tac_5').val(' ');
      $('#tac_4').val(String.fromCharCode(e.which));
    } else {
      $('#tac_4').val(' ');
    }
  });
  $('#tac_5').keypress(function(e) {
    if (parseInt(String.fromCharCode(e.which)) >= 0) {
      $('#tac_6').focus();
      $('#tac_6').val(' ');
      $('#tac_5').val(String.fromCharCode(e.which));
    } else {
      $('#tac_5').val(' ');
    }
  });
  $('#tac_6').keypress(function(e) {
    if (parseInt(String.fromCharCode(e.which)) >= 0) {
      $('#tac_6').val(String.fromCharCode(e.which));
    } else {
      $('#tac_6').val(' ');
    }
  });

  $('.toggle-password').click(function() {
    $(this).toggleClass('fa-eye fa-eye-slash');
    var input = $($(this).attr('toggle'));
    if (input.attr('type') == 'password') {
      input.attr('type', 'text');
    } else {
      input.attr('type', 'password');
    }
  });

  // -- password
  $('#password').keyup(function() {
    $('#strength .message').html(checkStrength($('#password').val()));
  });
  function clearClass() {
    $('#strength .level-1').removeClass('short weak good strong');
    $('#strength .level-2').removeClass('short weak good strong');
    $('#strength .level-3').removeClass('short weak good strong');
    $('#strength .level-4').removeClass('short weak good strong');
    $('#strength .message').removeClass('short weak good strong');
    $('#strength .col').removeClass('short weak good strong');
  }
  function checkStrength(password) {
    var strength = 0;
    if (password.length == 0) {
      clearClass();
      return '';
    }
    if (password.length < 8) {
      clearClass();
      $('#strength .level-1').addClass('short');
      $('#strength .message').addClass('short');
      return 'Come on, this is too short';
    }
    if (password.length > 7) strength += 1;
    // If password contains both lower and uppercase characters, increase strength value.
    // if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 1;
    // if (password.match(/([a-z].*[A-Z])/)) strength += 1;
    // If it has numbers and characters, increase strength value.
    if (password.match(/([a-zA-Z])/) || password.match(/([0-9])/)) strength += 1;
    // If it has one special character, increase strength value.
    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~,.])/)) strength += 1;
    // If it has two special characters, increase strength value.
    if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~,.].*[!,%,&,@,#,$,^,*,?,_,~,.])/)) strength += 1;
    // Calculated strength value, we can return messages
    // If value is less than 2
    if (strength < 3) {
      clearClass();
      $('#strength .level-1').addClass('weak');
      $('#strength .level-2').addClass('weak');
      $('#strength .message').addClass('weak');
      return 'Nope, too weak, you need a symbol';
    } else if (strength == 3) {
      clearClass();
      $('#strength .level-1').addClass('good');
      $('#strength .level-2').addClass('good');
      $('#strength .level-3').addClass('good');
      $('#strength .message').addClass('good');
      return 'Great, this is good enough';
    } else {
      clearClass();
      $('#strength .level-1').addClass('strong');
      $('#strength .level-2').addClass('strong');
      $('#strength .level-3').addClass('strong');
      $('#strength .level-4').addClass('strong');
      $('#strength .message').addClass('strong');
      return 'Awesome! You have a super secure password!';
    }
  }

  // -- organisation
  $('#form-input-organisation').on('input', function(evt) {
    $(this).val(function(_, val) {
      return val.toUpperCase();
    });
  });

  // -- disable dbl click submit
  $('.no-dbl-submit').on('submit', function() {
    $('button[type="submit"], input[type="submit"]').removeAttr('type');
  });

  // -- on submit national id
  $('#form-identification').on('submit', function(e) {
    var select = $('#form-identification #inputGroupSelect01');
    if (select.val() == 'SELECT') {
      select.addClass('mx-opt-error');
      $('#js-message').html("Don't forget to select ID Type");
      $('#go-message').html('');
      return false;
    }
  });

  $('#form-identification #inputGroupSelect01').on('change', function(e) {
    var select = $(this);
    if (select.val() != '') {
      select.removeClass('mx-opt-error');
      $('#js-message').html('');

      var idType = select.val();
      switch (idType) {
        case 'MY_NRIC':
          $('input[name="number"]').attr('placeholder', 'ID Number (e.g: 902020012121)');
          $('input[name="number"]').val('');
          $('input[name="number"]').removeAttr('disabled');
          break;
        case 'MY_PR':
          $('input[name="number"]').attr('placeholder', 'ID Number (e.g: 902020012121)');
          $('input[name="number"]').val('');
          $('input[name="number"]').removeAttr('disabled');
          break;
        case 'MY_POLIS':
          $('input[name="number"]').attr('placeholder', 'ID Number (e.g: RF/T7890)');
          $('input[name="number"]').val('');
          $('input[name="number"]').removeAttr('disabled');
          break;
        case 'MY_TENTERA':
          $('input[name="number"]').attr('placeholder', 'ID Number (e.g: JMF12345)');
          $('input[name="number"]').val('');
          $('input[name="number"]').removeAttr('disabled');
          break;
        case 'MY_KAS':
          $('input[name="number"]').attr('placeholder', 'ID Number (e.g: 902020012121)');
          $('input[name="number"]').val('');
          $('input[name="number"]').removeAttr('disabled');
          break;
        default:
          $('input[name="number"]').attr('placeholder', 'Select ID Type');
          $('input[name="number"]').val('');
          $('input[name="number"]').attr({ disabled: 'disabled' });
      }
    }
  });

  $('#form-organisation #inputGroupSelect01')
    .on('change', function(e) {
      var input = $('#form-organisation #form-input-organisation');
      $(this).val() === '' ? input.attr('disabled', true) : input.removeAttr('disabled');
    })
    .trigger('change');
  
  $('#form-organisation #inputGroupSelect01').on('change', function() {
	    var select = $(this);
	    if (select.val() != '') {
	      select.removeClass('mx-opt-error');
	      $('#js-message').html('');

	      var organisationRegType = select.val();
	      switch (organisationRegType) {
	        case 'BUSINESS':
	          $('input[name="organisationRegNumber"]').attr('placeholder', 'Organisation Number');
	          $('input[name="organisationRegNumber"]').val('');
	          $('input[name="organisationRegNumber"]').removeAttr('disabled');
	          break;
	        case 'OTHERS':
	          $('input[name="organisationRegNumber"]').attr('placeholder', 'Organisation Number');
	          $('input[name="organisationRegNumber"]').val('');
	          $('input[name="organisationRegNumber"]').removeAttr('disabled');
	          break;
	        default:
	          $('input[name="organisationRegNumber"]').attr('placeholder', 'Select Organisation Type');
	          $('input[name="organisationRegNumber"]').val('');
	          $('input[name="organisationRegNumber"]').attr({ disabled: 'disabled' });
	      }
	    }
	  });


  $('#phone_number').on('focusout', function() {
    var mobile_number = $('#phone_number').val();
    if (!mobile_number.startsWith('60')) {
      if (mobile_number.startsWith('0')) {
        $('#phone_number').val('6' + mobile_number);
      }
    }
    console.log($('#phone_number').val());
    $('#phone_number').val(
      $('#phone_number')
        .val()
        .trim()
    );
  });

  $('#number').on('keyup', function(e) {
    var select_type = $('#inputGroupSelect01').val();

    if (select_type == 'MY_NRIC' || select_type == 'MY_PR' || select_type == 'MY_KAS') {
      var id_number = $(this);
      var id_number_length = id_number.val().length;
      var id_number_value = id_number.val();

      var dashCounts = 0;

      if (id_number_value.match(/-/g) != null) {
        dashCounts = id_number_value.match(/-/g).length;
      }

      if (id_number_length > 6 && dashCounts == 0) {
        if (id_number_value.indexOf('-') != 6) id_number.val(id_number_value.splice(6, 0, '-'));
      }
      if (id_number_length > 9 && dashCounts == 1) {
        if (id_number_value.lastIndexOf('-') != 9) id_number.val(id_number_value.splice(9, 0, '-'));
      }
    }
  });

// update password
$('.mx-show-hide').click(function(e){
  e.preventDefault();
  var fieldID = $(this).data('for');
  if($('#'+fieldID).attr('type') == 'password') {
    $('#'+fieldID).attr('type', 'text');
    $(this).html('HIDE')
  } else {
    $('#'+fieldID).attr('type', 'password');
    $(this).html('SHOW')
  }
});

if ($('#national-id-type').html() == 'MYPR' || $('#national-id-type').html() == 'MYKAD' || $('#national-id-type').html() =='MYKAS') {
	 if ($('#national-id-preview').length > 0) {	
	      var nationalIdPreview = $('#national-id-preview').html();	
	      nationalIdPreview = nationalIdPreview.splice(6, 0, '-');	
	      nationalIdPreview = nationalIdPreview.splice(9, 0, '-');	
	      $('#national-id-preview').html(nationalIdPreview);	
	    }	
}

});

String.prototype.splice = function(idx, rem, str) {
  return this.slice(0, idx) + str + this.slice(idx + Math.abs(rem));
};
