function starry(id_info){
	let match_id = id_info.getAttribute("data-value") 
	let icon_prefix = document.querySelector('#star > SVG').getAttribute('data-prefix')

	if ( icon_prefix == 'far'){
		$('#star_icon').toggleClass('fas')
	} else{
		$('#star_icon').toggleClass('far')
	}	
	$.ajax({
		url: 'http://127.0.0.1:8000/starred',
		type: 'GET',
		data: {'match_id' : match_id },
		success: function(){
		}
	})
}

function open_club(club_id){
	let id = club_id.getAttribute("data-value")
	let previous_page = document.documentElement.outerHTML
	$.ajax({
		url: `http://127.0.0.1:8000/club/${id}`,
		type: "GET",
		data: {'id' : id},
		success: function(htmlre){
			document.open();
			document.write(htmlre)
			document.close()
			window.history.pushState({"html":htmlre},"", `http://127.0.0.1:8000/club/${id}`);
			window.onpopstate = function(event) {
				document.open()
				document.write(previous_page)
				document.close()
    		}
		}
	})
}

function weekControl(id){
    var value = id.value;
    $.ajax({
        url: '', // The url suffix that leads to your home function, example: '/home/'
        type: "GET", // Http method
        data: {'dir': value}, // The data to be sent to the server.
        success: function (htmlres) { // What to do on success and response reaching back
            $("#matchweek").html(htmlres);
        }
    });
}

function open_match(info){
	let id = info.getAttribute("data-value")
	console.log(id)
	let home_page = document.documentElement.outerHTML
	$.ajax({
		url: `http://127.0.0.1:8000/match/${id}`,
		type: "GET",
		data: {'id' : id},
		success: function(htmlre){
			document.open();
			document.write(htmlre)
			document.close()
			window.history.pushState({"html":htmlre},"", `http://127.0.0.1:8000/match/${id}`);
			window.onpopstate = function(event) {
				document.open()
				document.write(home_page)
				document.close()
    		}
		}
	})
}

function change_section(link){
	unselect_section('stats_box')
	unselect_section('standings')
	unselect_section('match_events')

	let value = link.getAttribute("data-value")
	document.querySelector(`#${value}_link`).style.color = 'black'
	document.querySelector(`#${value}_link`).style.borderBottom = '2px solid red'

	document.querySelector('#standings').style.display = 'none'
	document.querySelector('#stats_box').style.display = 'none'
	document.querySelector('#match_events').style.display = 'none'

	document.querySelector(`#${value}`).style.display = 'block'

}

function unselect_section(value){
	document.querySelector(`#${value}_link`).style.setProperty('color', 'grey', 'important')
	document.querySelector(`#${value}_link`).style.borderBottom = '0px solid red'
}