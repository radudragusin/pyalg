function highlightFlow(btn, strnumber, flowarray) {
	var intnumber = parseInt(strnumber);
	
	//remove current highlightning
	if(strnumber != '-1'  && intnumber < flowarray.length && intnumber > -1) {
		$('#t'+flowarray[intnumber].toString()).removeClass('highlight');
	}
	$('#nextbt').removeClass(strnumber);
	$('#prevbt').removeClass(strnumber);

	//add current highlightning
	if(btn.toString() == "nextbt") {
		//verify if in range
		if(intnumber+1 < flowarray.length) {
			pbt = document.getElementById("prevbt");
			pbt.disabled = false;
			$('#t'+flowarray[intnumber+1].toString()).addClass('highlight');
			$('#nextbt').addClass((intnumber+1).toString());
			$('#prevbt').addClass((intnumber+1).toString());
		}
		else {
			nbt = document.getElementById("nextbt");
			nbt.disabled = true;
			$('#nextbt').addClass((intnumber+1).toString());
			$('#prevbt').addClass((intnumber+1).toString());
		}
	}
	else {
		//verify if in range
		if(intnumber-1 > -1) {
			nbt = document.getElementById("nextbt");
			nbt.disabled = false;
			$('#t'+flowarray[intnumber-1].toString()).addClass('highlight');
			$('#nextbt').addClass((intnumber-1).toString());
			$('#prevbt').addClass((intnumber-1).toString());
		}
		else {
			pbt = document.getElementById("prevbt");
			pbt.disabled = true;		
			$('#nextbt').addClass((intnumber-1).toString());
			$('#prevbt').addClass((intnumber-1).toString());
		}
	}
}

function highlightFlowNext(btn, strnumber, flowarray) {
	var btn = $(btn);
	var intnumber = parseInt(strnumber);
	
	if(intnumber != 0){
		var prev = flowarray[intnumber-1].toString()
		$('#t'+prev).removeClass('highlight');
	}
	btn.removeClass(strnumber);
	
	var newo = flowarray[intnumber].toString()
	$('#t'+newo).addClass('highlight');
	
	if(intnumber+1 < flowarray.length) {	
		btn.addClass((intnumber+1).toString());
	}
	else {
		btn.addClass("0");
		nbtn = document.getElementById("nextbt");
		nbtn.disabled = true;
		nbtn.value = "Finished";
	}
}

function highlightFlowPrev(btn, strnumber, flowarray) {
	var btn = $(btn);
	var intnumber = parseInt(strnumber);
	
	btn.removeClass(strnumber);
	if(intnumber == -1) {
		intnumber = flowarray.length-1;
		strnumber = intnumber.toString();
	}
	
	if(intnumber != flowarray.length-1){
		var prev = flowarray[intnumber+1].toString()
		$('#t'+prev).removeClass('highlight');
	}
	
	var newo = flowarray[intnumber].toString()
	$('#t'+newo).addClass('highlight');
	
	if(intnumber-1 >= 0) {	
		btn.addClass((intnumber-1).toString());
	}
	else {
		btn.addClass((flowarray.length-1).toString());
		nbtn = document.getElementById("prevbt");
		nbtn.disabled = true;
		nbtn.value = "Finished";
	}
}
