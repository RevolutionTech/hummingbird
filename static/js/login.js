$(document).ready(function(){
	// define functions
	jQuery.validator.addMethod("MAC", function(value, element){
		var regex = /^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$/;
		return this.optional(element) || regex.test(value);
	}, "* Value is a valid MAC address");
	function updateDropdownSongs(walkin_song){
		var song = songs[walkin_song];
		$('.dropdown-toggle:first-child').html(song["title"] + "&nbsp;<span class=\"caret\"></span>");
		$('.dropdown-toggle:first-child').val(walkin_song);
		var songHelpText = "";
		if (song["artist"] && song["artist"] != "n/a"){
			songHelpText += " by " + song["artist"];
		}
		if (song["album"] && song["album"] != "n/a"){
			songHelpText += " from " + song["album"];
		}
		if (song["length"]){
			songHelpText += " (" + song["length"] + "s)";
		}
		$('.editSong > p').html(songHelpText);
		var dropdown_menu_songs = "";
		$.each(songs, function(key, val){
			if (key != walkin_song){
				dropdown_menu_songs += "<li value=\"" + key + "\"><a href=\"#\">" + val["title"] + "</a></li>";
			}
		});
		$('.dropdown-menu').html(dropdown_menu_songs);
		$('#createWalkinSong').val(walkin_song);
	};
	function toggleLoginElements(){
		$('.create').toggle();
		$('.login').toggle();
		createForm.resetForm();
		loginForm.resetForm();
	};
	$('.header-link a').click(function(){
		toggleLoginElements();
	});
	$('.dropdown-menu').on('click', 'li', function(){
		updateDropdownSongs($(this).val());
	});
	var createForm = $('#create-form').validate({
		rules: {
			createFirstName: "required",
			createEmail: {
				required: true,
				email: true
			},
			createMAC: {
				required: true,
				MAC: true
			},
			createPassword: {
				minlength: 5
			},
			createPasswordConfirm: {
				minlength: 5,
				equalTo: "#createPassword"
			},
		},
		messages: {
			createFirstName: "Please enter your first name",
			createEmail: "Please enter a valid email address",
			createMAC: "Please enter a valid MAC address",
			createPassword: {
				minlength: "Your password must be at least 5 characters long"
			},
			createPasswordConfirm: {
				minlength: "Your password must be at least 5 characters long",
				equalTo: "Your passwords must match"
			},
		}
	});
	var loginForm = $('#login-form').validate({
		rules: {
			loginEmail: "required",
			loginPassword: "required"
		},
		messages: {
			loginEmail: "Please enter a username or email address",
			loginPassword: "Please enter your password"
		}
	});
	$('#submit-create').click(function(){
		if ($('#create-form').valid()){
			$('#create-form').submit();
		}
	});
	$('.btn-reset').click(function(){
		$('.edit input').val(null);
		updateDropdownSongs(0);
		$('.editDelay').val(delay_default);
		createForm.resetForm();
	});
	$('#submit-login').click(function(){
		if ($('#login-form').valid()){
			$('#login-form').submit();
		}
	});

	// add items to dropdown menu
	updateDropdownSongs(walkin_song);

	// hide create elements
	$('.create').hide();
});
