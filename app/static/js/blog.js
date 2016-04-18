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
	$(".category").each(function(){
		if ($(this).attr('href') == full_url) { 
			$(this).addClass("active_cat");
		}
	});
});
