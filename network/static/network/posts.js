document.addEventListener('DOMContentLoaded', () =>{
	all_posts()
	let current_user = document.querySelector('#current').value
	document.querySelector('#edit_form').style.display = 'none'
	document.querySelector("#following_page").addEventListener('click', following_page)
	document.querySelector('#user_title').addEventListener('click', () => user_page(current_user))
})

var start = 0;
var number = 10;

function all_posts(){
	let user = document.querySelector('#current').value
	fetch('/all_posts')
	.then(response => response.json())
	.then(posts => {
		display_posts(user, posts)
	})
}

function following_page(){
	document.querySelector('#all_posts').style.display = 'none'
	let user = document.querySelector('#current').value
	document.querySelector('h2').innerHTML = 'Your Followings'
	document.querySelector('#user_page').innerHTML = ''
	document.querySelector('#user_info').innerHTML = ''
	fetch(`/following_page/${user}`)
	.then(response => response.json())
	.then(posts => {
		start = 0
		display_posts(user, posts)
	})

}

function user_page(userr){
	document.querySelector('#user_page').innerHTML = ''
	document.querySelector('#user_info').innerHTML = ''
	document.querySelector('#all_posts').style.display = 'none'
	document.querySelector('h2').innerHTML = `${userr}'s profile`
	fetch(`/page/${userr}`)
	.then(response => response.json())
	.then(postss => {
		start = 0
		user_info(userr)
		display_posts(userr, postss)
	})
}

function display_posts(userr, postss){
	document.querySelector('#user_page').innerHTML = ''
	let posts = postss.slice(start, start+number);
	for (post in posts){
		let id = posts[post].pk
		let container = document.createElement('div')
		let username = document.createElement('div')
		let time = document.createElement('div')
		let content = document.createElement('div')
		let likes = document.createElement('div')
		let like = document.createElement('button')	
		let current_user = document.querySelector('#current').value
		let post_user = posts[post].fields.user
		container.className = 'container'
		username.className = 'user'
		time.className = 'time'
		

		fetch(`/date/${posts[post].fields.timestamp}`)
		.then(response => response.json())
		.then(date => {
			time.innerHTML = date.date
		})
		
		username.innerHTML = posts[post].fields.user
		content.innerHTML = posts[post].fields.content

		fetch(`likes/${current_user}/${id}`)
		.then(response => response.json())
		.then(data => {
			if (data.liked == false){
				like.innerHTML = `Like ${data.number}`
				like.className = 'btn btn-outline-danger'
			}
			else {
				like.innerHTML = `Liked ${data.number}`
				like.className = 'btn btn-danger'
			}
		})

		like.addEventListener('click', () => {
            fetch(`likes/${current_user}/${id}`, {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                if (data.liked == false){
                    like.innerHTML = `Like ${data.number}`
                    like.className = 'btn btn-outline-danger'
                }
                else{
                    like.innerHTML = `Liked ${data.number}`
                    like.className = 'btn btn-danger'
                }
            })
        })

		document.querySelector('#user_page').append(container)

		if (current_user == posts[post].fields.user){
			let edit = document.createElement('button')
			edit.className = "btn btn-sm btn-outline-primary"
			edit.style.display = "inline"
			edit.style.float = 'right'
			edit.innerHTML = "Edit"

			likes.append(like, edit)
			container.append(time, username, content, likes)

			let e_post = posts[post]
			
			edit.addEventListener('click', () => {
				let formm = document.querySelector('#edit_form')
				let edit_box = document.querySelector('#edit_box')
				let save = document.querySelector('#save')

				formm.style.display = "block"
				edit_box.value = e_post.fields.content

				container.innerHTML = ''
				likes.innerHTML = ''

				likes.append(like)
				container.append(time, username, formm, likes)

				save.addEventListener('click', () => {
					fetch(`/edit_post/${id}`, {
						method: "PUT",
						body: JSON.stringify({
							new_content: edit_box.value
						})
					})
				})

			})
		}
		else{
			likes.append(like)
			container.append(time, username, content, likes)
		}
		
		username.addEventListener('click', () => user_page(post_user))
	}

	let pagination = document.createElement('div')
	let previous = document.createElement('button')
	let next = document.createElement('button')

	pagination.className = "pagination"
	previous.className = "btn btn-outline-info"
	next.className = "btn btn-outline-info"

	previous.innerHTML = 'Previous'
	next.innerHTML = 'Next'

	if(start < number){
		previous.disabled = true
	}
	if(start + number >= postss.length){
		next.disabled = true
	}

	pagination.append(previous, next)
	document.querySelector('#user_page').append(pagination)

	previous.addEventListener('click', () =>{
		start = start - number;
    	display_posts(userr, postss);
	})

	next.addEventListener('click', () =>{
		start = start + number;
    	display_posts(userr, postss);
	})
}

function user_info(userr) {
	let user_info = document.createElement('div')
	let username = document.createElement('div')
	let followers = document.createElement('div')
	let following = document.createElement('div')
	
	user_info.className = 'container'
	username.className = 'user'
	username.style.cssText = 'font-size: 30px;'

	username.innerHTML = `${userr}`
	followers_no(userr, followers, following)

	document.querySelector('#user_info').append(user_info)
	user_info.append(username, followers, following)


	let current_user = document.querySelector('#current').value
	let match = `${current_user}`.localeCompare(`${userr}`)

	if (match != 0){
		buttons = document.createElement('div')
		follow = document.createElement('button')
		follow.className = "btn btn-sm btn-outline-primary";

		fetch(`/check/${userr}`)
		.then(response => response.json())
		.then(result => {
			if (result.message === "you follow this user"){
				follow.innerHTML = "Unfollow"
				
			}
			else{
				follow.innerHTML = "Follow"
			}
		})
		

		follow.addEventListener("click", () => {

			if (follow.innerHTML === "Follow"){
				follow.innerHTML = "Unfollow"
				fetch(`/follow/follow`,{
					method: 'POST',
					body: JSON.stringify({
						user: userr
					})
				})
				.then(response => response.json())
				.then(result => {
				    followers_no(userr, followers, following)
				})
			}
			else{
				follow.innerHTML = "Follow"
				fetch(`/follow/unfollow`,{
					method: 'POST',
					body: JSON.stringify({
						user: userr
					})
				})
				.then(response => response.json())
				.then(result => {
				    followers_no(userr, followers, following)
				})
			}
		})
		user_info.append(buttons)
		buttons.append(follow)
	}

}

function followers_no(user, followers, following){
	fetch(`/followers_number/${user}`)
	.then(response => response.json())
	.then(data => {
		followers.innerHTML = `Followers: ${data[0]}`
		following.innerHTML = `Following: ${data[1]}`
	})
}