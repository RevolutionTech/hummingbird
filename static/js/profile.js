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
		$('.editSongSelect > p').html(songHelpText);
		var dropdown_menu_songs = "";
		$.each(songs, function(key, val){
			if (key != walkin_song){
				dropdown_menu_songs += "<li value=\"" + key + "\"><a href=\"#\">" + val["title"] + "</a></li>";
			}
		});
		$('.dropdown-menu').html(dropdown_menu_songs);
		$('#profileWalkinSong').val(walkin_song);
	};
	function toggleProfileElements(){
		$('.btn').toggle();
		$('.btnFeedback').show();
		$('.txt').toggle();
		$('.edit').toggle();
	};
	function editProfile(){
		// write values from vars to page
		$('.editFirstName').val(firstName);
		$('.editLastName').val(lastName);
		$('.editEmail').val(email);
		$('.editMAC').val(MAC);
		$('.editUsername').val(username);
		$('.editDelay').val(delay);

		toggleProfileElements();

		// hide song upload
		$('.editSongBtnSelect').addClass('active');
		$('.editSongBtnUpload').removeClass('active');
		$('.editSongUpload').hide();
		$('#profileWalkinSongChoice').val('select');
	};
	function showProfile(save){
		// save values
		if (save){
			firstName = $('.editFirstName').val();
			lastName = $('.editLastName').val();
			email = $('.editEmail').val();
			MAC = $('.editMAC').val();
			username = $('.editUsername').val();
			password = $('.editPassword').val();
			passwordConfirm = $('.editPasswordConfirm').val();
			walkin_song = $('.dropdown-toggle:first-child').val();
			delay = $('.editDelay').val();
		}

		// write values from vars to page
		$('.txtName > p').html(firstName + " " + lastName);
		$('.txtEmail').html(email);
		$('.txtMAC').html(MAC);
		$('.txtUsername').html(username);
		var song = songs[walkin_song];
		var songHelpText = song["title"];
		if (song["artist"] && song["artist"] != "n/a"){
			songHelpText += " by " + song["artist"];
		}
		if (song["album"] && song["album"] != "n/a"){
			songHelpText += " from " + song["album"];
		}
		if (song["length"]){
			songHelpText += " (" + song["length"] + "s)";
		}
		$('.txtSong').html(songHelpText);
		$('.txtDelay').html(delay);

		toggleProfileElements();

		// hide song select and upload
		$('.editSongSelect').hide();
		$('.editSongUpload').hide();
	};
	var profileForm = $('#profile-form').validate({
		rules: {
			profileEmail: {
				email: true
			},
			profileMAC: {
				MAC: true
			},
			profilePassword: {
				minlength: 5
			},
			profilePasswordConfirm: {
				minlength: 5,
				equalTo: "#profilePassword"
			}
		},
		messages: {
			profileEmail: "Please enter a valid email address",
			profileMAC: "Please enter a valid MAC address",
			profilePassword: {
				minlength: "Your password must be at least 5 characters long"
			},
			profilePasswordConfirm: {
				minlength: "Your password must be at least 5 characters long",
				equalTo: "Your passwords must match"
			}
		}
	});
	$('.btnEdit').click(function(){
		editProfile();
	});
	$('.btnCancel').click(function(){
		profileForm.resetForm();
		updateDropdownSongs(walkin_song);
		showProfile(false);
	});
	$('.btnDone').click(function(){
		if ($('#profile-form').valid()){
			$('#profile-form').submit();
			showProfile(true);
		}
	});
	$('.editSongBtnSelect').click(function(){
		$('.editSongBtnSelect').addClass('active');
		$('.editSongBtnUpload').removeClass('active');
		$('.editSongSelect').show();
		$('.editSongUpload').hide();
		$('#profileWalkinSongChoice').val('select');
	});
	$('.editSongBtnUpload').click(function(){
		$('.editSongBtnSelect').removeClass('active');
		$('.editSongBtnUpload').addClass('active');
		$('.editSongSelect').hide();
		$('.editSongUpload').show();
		$('#profileWalkinSongChoice').val('upload');
	});
	$('.dropdown-menu').on('click', 'li', function(){
		updateDropdownSongs($(this).val());
	});

	// add items to dropdown menu
	updateDropdownSongs(walkin_song);

	// show profile elements
	showProfile(false);
	$('.btnEdit').show();
	$('.txt').show();
});
