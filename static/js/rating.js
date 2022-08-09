console.log('Hello asc asdcasdc cd');

const one = document.getElementById('first');
const two = document.getElementById('second');
const three = document.getElementById('third');
const four = document.getElementById('fourth');
const five = document.getElementById('fifth');

const form = document.querySelector('.rate-form');
const confirmBox = document.getElementById('confirm-box');
const csrf = document.getElementsByName('csrfmiddlewaretoken'); 

const handleStarSelect = (size) =>{
    const children = form.button
    for (let i=0; i < children.length; i++){
        if(i <= size){
            children[i].classList.add('checked')
        }
        else{
            children[i].classList.remove('checked')
        }
    }
};



//longer version - to be optimized
const handleSelect = (selection) => {
    switch(selection){
        case 'first':{
            // one.classList.add('checked')
            // two.classList.remove('checked')
            // three.classList.remove('checked')
            // four.classList.remove('checked')
            // five.classList.remove('checked')
            handleStarSelect(1)
            return
        }
        case 'second':{
            handleStarSelect(2)
            return
        }
        case 'third':{
            handleStarSelect(3)
            return
        }
        case 'fourth':{
            handleStarSelect(4)
            return
        }
        case 'fifth':{
           handleStarSelect(5)
            return
        }
    }
};

const getNumericValue = (stringValue) =>{
    let numericValue;
    if (stringValue === 'first') {
        numericValue = 1
    } 
    else if (stringValue === 'second') {
        numericValue = 2
    }
    else if (stringValue === 'third') {
        numericValue = 3
    }
    else if (stringValue === 'fourth') {
        numericValue = 4
    }
    else if (stringValue === 'fifth') {
        numericValue = 5
    }
    else {
        numericValue = 0
    }
    return numericValue
};


    const arr = [one, two, three, four, five];

    arr.forEach(item=>item.addEventListener('mouseover', (event)=>{
        handleSelect(event.target.id)
    }));

    arr.forEach(item=> item.addEventListener('click', (event)=>{
        const val = event.target.id

        let isSubmit = false

        form.addEventListener('submit', e=>{
            e.preventDefault()

            if (isSubmit) {
                return
            }
            isSubmit = true

            //user id
            const id = e.target.id
            
            //value of rating into number
            const val_num = getNumericValue(val)
            
            $.ajax({
                type: 'POST',
                url: 'rating/<int:pk>/worker-rating',
                data: {
                    'csrfmiddlewaretoken': csrf[0].value,
                    'u_id': id,
                    'rate': val_num,
                },
                success: function(response){
                    console.log(response)
                    confirmBox.innerHTML = `<h1>Successfully rated with ${response.rate}</h1>`
                },
                error: function(error){
                    console.log(error)
                    confirmBox.innerHTML = '<h1>Ups... something went wrong</h1>'
                }
            })
        })
    }))