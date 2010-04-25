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

function changeColor(nr) {
	if($('#'+nr).hasClass('highlightLineNo')){
		$('#'+nr).removeClass('highlightLineNo');
	}
	else {
		$('#'+nr).addClass('highlightLineNo');
	}
}
