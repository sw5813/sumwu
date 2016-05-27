// Show subscribe modal
$(function() {
	if (window.location.hash == "#subscribe") {
		$('#subscribe').modal('show');
	}
});

// Select current category
$(window).load(function(){
	var pathvalue = window.location.pathname;
	var qvalue = window.location.search;
	var full_url = pathvalue + qvalue;

	// Handle pagination by removing page numbers and article limits from path before checking
	var patharray = pathvalue.split('\/');
	for (var i = 0; i < patharray.length; i++) {
		if (!isNaN(parseFloat(patharray[i]))) {
			patharray.splice(i, 1);
		}
	}
	var newpath = patharray.join('\/');

	$(".category").each(function(){
		if ($(this).attr('href') == newpath) { 
			$(this).addClass("active_cat");
		}
	});
});
