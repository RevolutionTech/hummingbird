$(document).ready(function(){
	// define functions
	function addNewMessage(message){
		// first element goes after the header (assumes header is there)
		if ($('.table tr').length == 1){
			$('.table tr').after("<tr value=\"" + message["id"] + "\"><td>" + message["date"] + "</td><td>" + message["message"] + "</td></tr>");
		}
		// all following elements come before the last-added element
		else {
			$('.table tr:nth-child(2)').before("<tr value=\"" + message["id"] + "\"><td>" + message["date"] + "</td><td>" + message["message"] + "</td></tr>");
		}
	};

	// get messages
	$.each(message_list, function(i, val){
		addNewMessage(val);
	});
});
