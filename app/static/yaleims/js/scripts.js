/* Adds specific sport selector admin page */
$("#action").change(function() {
	$action = $(this).val();
	if ($action == "edit" || $action == "delete") {
		$("#select_sport").removeClass("hidden");	
		// Prepopulate with info- see function below
	} else {
		$("#select_sport").addClass("hidden");
		// Clear info
		$("#sport").val("");
	}
});

/* Prepopulate with info */
$("#select_sport").change(function() {
	// Name
	$sport = $(this).val();
	$("#sport").val($sport);

	// Scores
	$.post("/yaleims/db_sport/" + $sport, function(data) {
		$("#bk").val(data["Berkeley"]);
		$("#br").val(data["Branford"]);
		$("#cc").val(data["Calhoun"]);
		$("#dc").val(data["Davenport"]);
		$("#es").val(data["Ezra Stiles"]);
		$("#je").val(data["Jonathan Edwards"]);
		$("#mc").val(data["Morse"]);
		$("#pc").val(data["Pierson"]);
		$("#sm").val(data["Silliman"]);
		$("#sy").val(data["Saybrook"]);
		$("#td").val(data["Timothy Dwight"]);
		$("#tc").val(data["Trumbull"]);
	});
});