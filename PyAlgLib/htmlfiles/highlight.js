/*
 * Authors: Radu Dragusin and Paula Petcu
 * Insitute of Computer Science, Copenhagen University, Denmark
 * 
 * Script for highlighting the flow of the algorithm shown in the html file */

function highlightFlow(btn, strnumber, flowarray) {
	var intnumber = parseInt(strnumber);
	
	//remove previous highlighting
	if(strnumber != '-1'  && intnumber < flowarray.length && intnumber > -1) {
		$('#t'+flowarray[intnumber].toString()).removeClass('highlight');
	}
	$('#nextbt').removeClass(strnumber);
	$('#prevbt').removeClass(strnumber);

	//add current highlighting
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
