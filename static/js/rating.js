var reviewBtn = document.getElementById("write_review")
var overlay = document.querySelector('.overlay')
var reviewPostContainer = document.querySelector('.review-post-container')
var RatingStar = document.querySelectorAll('.rating-star')
var review_form = document.getElementById('review_form')



var header = document.getElementById('exampleInputHeader')
var message = document.getElementById('exampleFormControlTextarea')

var reviewcloseBtn = document.querySelector('.revie-section-close-btn')

var savedHomeIcon = document.querySelector('.fa-heart')

console.log(savedHomeIcon.classList)


console.log("heart")

console.log(savedHomeIcon)

let rating_value = '5'
let header_value = ''
let message_value = ''

var currentUrl = window.location.href
var strs = currentUrl.split()






// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// const csrftoken = getCookie('csrftoken');




reviewBtn.addEventListener('click', () =>{
    if(user == 'AnonymousUser'){
        displayLoginContainer()
    }else{
        overlay.style = "display: block"
        reviewPostContainer.style = "display: block"
    }
   
})




reviewcloseBtn.addEventListener('click', () =>{
    console.log("hello")
    overlay.style = "display: none"
    reviewPostContainer.style = "display: none"
})




RatingStar.forEach((btn, i) =>{
    btn.addEventListener('click', () =>{

        updateStarButtons(i)
        rating_value = btn.dataset.number
    })
})



function updateStarButtons(i){
    RatingStar.forEach((btn) =>{
        btn.classList.contains('selected') &&
        btn.classList.remove('selected')
    })

    RatingStar[i].classList.add('selected')
}



var review_section = document.querySelector('.review-section')







for(var i = 0; i< rating.length; i++){

    var reviewBody = document.createElement('div')
    var stars = document.createElement('div')
    var date = document.createElement('div')
    var headline = document.createElement('div')
    var reviewMssg = document.createElement('div')
    var readMore  = document.createElement('div')


    reviewBody.classList.add('review-body')
    stars.classList.add('stars')
    date.classList.add('date')
    headline.classList.add('headline')
    reviewMssg.classList.add('review-mssg')
    readMore.classList.add('read-more')

    getRatingStar(rating[i]['fields']['rating'])
    // stars.innerHTML =(getRatingStar(rating[i]['fields']['rating']))
    date.innerHTML = <p>${rating[i]['fields']['created_date']}</p>
    headline.innerHTML = <h2>${rating[i]['fields']['title']}</h2>
    reviewMssg.innerHTML = <p>${getRatingMssg(rating[i]['fields']['message'])}</p>
    readMore.innerHTML = <p>Read More</p>


    reviewBody.appendChild(stars)
    reviewBody.appendChild(date)
    reviewBody.appendChild(headline)
    reviewBody.appendChild(reviewMssg)
    reviewBody.appendChild(readMore)

    review_section.appendChild(reviewBody)

}





function getRatingMssg(e){

    if(e.length > 250){
        e = e.substring(0, 250)
    }

    return e

}





function getRatingStar(e){

    e = parseInt(e)

    console.log("e", e)

    var i = 0

    
    for(i; i< 5; i++){
        console.log(i)
        for(i; i < e; i++){
            stars.innerHTML += <i class="fa-solid fa-star"></i>
        
        }
        stars.innerHTML += ` <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"  class="bi bi-star" viewBox="0 0 16 16">
                            <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"/>
                            </svg>`

    }

}


// savedHomeIcon.addEventListener('click', (btn) =>{
//     console.log("hello")
//     console.log(savedHomeIcon.classList)
//     console.log(btn.classList)
//     savedHomeIcon.classList.toggle('saved-room-icon')


// })




function savedHomesFunction(id){
    
    if(user == 'AnonymousUser'){
        displayLoginContainer()
    }else{
        savedHomeIcon.classList.toggle('saved-room-icon')
        data = new FormData()
        data.append('id', id)
        
        console.log('abcd')

        var url = '/saved_Homes/'


        fetch(url, {

            method: 'POST',
            headers : {
                'Content-Type': 'application/json',        
                'X-CSRFToken': csrftoken},

            body: JSON.stringify({'id': id})
        })

        .then((response) =>{
            return response.json()
        })

        .then((data) =>{
            console.log(data)

        
        })

    }
    
  
}

// var navbar = document.querySelector('.navbar')
console.log(navbar)



window.addEventListener('scroll', ()=>{

    var message_section = document.querySelector('.message-section')
    let body = document.querySelector("body");
    let first_column = document.querySelector('.first-column')
    message_section = document.querySelector('.message-section')


    if(window.scrollY > 560){
        navbar.classList.add('sticky')
        console.log(message_section)
        // message_section.classList.add('sticky')

        // body.style.overflow = "hidden"
        // first_column.style = "overflow-y = scroll"
    }else{
        navbar.classList.remove('sticky')
        // message_section.classList.remove('sticky')

    }

    // navbar.classList.toggle('sticky', window.scrollY > 560)
    // if(window.scrollY > 565){
    //    navbar.classList.toggle('sticky')

    // }
})





review_form.addEventListener('submit', (e) =>{
    
    e.preventDefault()

    console.log("{{request.user}}")

    header_value = header.value
    message_value = message.value


    if(header_value == '' && message_value == ''){
        console.log('empty')
        if(header_value == ''){
            header.style = "border: 1px solid red"
        }

        if(message_value == ''){
            message.style = "border: 1px solid red"
        }  
    }else{

        let url = "/postReview/"

        var data = new FormData()


        data.append('rating', rating_value)
        data.append('header', header_value)
        data.append('message', message_value)
        data.append('id', id)
    


        fetch(url, {
            method: 'POST',
            headers : {'X-CSRFToken': csrftoken},

            body: data
        })
        .then((response) =>{
            return response.json()
        })

        .then((data) =>{
            console.log(data)

            window.location.href = /room_detail/${data['id']}/
        
        })
    }

})


$("#success-alert").fadeTo(2000, 500).slideUp(500, function(){
    $("#success-alert").slideUp(500);
});


// $(document).ready(function() {
//     $("#success-alert").hide()

// });