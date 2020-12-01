var bookID = window.location.href.split('/')[4]
console.log(bookID)
let url = "http://3.139.54.214:8000/get_book/"+bookID
let bookEmotionData = {}
let bookEmotionNew = []
getBook(url)
console.log(getBook(url))
console.log(document.getElementById('chart'))
var ctx = document.getElementById('chart').getContext('2d');

async function upvote(){
    endpoint = "http://3.139.54.214:8000/rank/"
    const formData = new FormData();
    const rank_type = "upvote"
    const book_id = bookID
    formData.append("rank_type",rank_type)
    formData.append("book_id", book_id)
    let csrftoken = getCookie('csrftoken');
    const resp = await fetch(endpoint, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": csrftoken },
    });
    response = await resp.json();
    response = response.form_error
    if(response == "failed"){
        alert("You can only vote once!")
    }
    console.log("Response: "+response)
    window.location.reload();
}

async function createPlaylist(){
    endpoint = "http://3.139.54.214:8000/create_playlist/"
    const formData = new FormData();
    const book_id = bookID
    console.log(book_id)
    formData.append("book_id", book_id)
    let csrftoken = getCookie('csrftoken');
    button = document.getElementById('playlist')
    button.innerHTML = "Creating playlist...."
    const resp = await fetch(endpoint, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": csrftoken },
    });
    response = await resp.json();
    response = response.form_error
    if(response == "failed"){
        alert("You can only create one playlist per book!")
    }
    else if(response == "failed no history"){
        alert("Not enough listening history.")
    }
    else{
        var btnDiv = document.getElementById('buttons')
        var newButton = document.createElement('button');
        newButton.onclick = window.open(response)
        // newButton.setAttribute('href', response);
        newButton.setAttribute('class',"btn btn-lg");
        newButton.innerHTML = "Go to playlist here"
        document.getElementById('buttons').appendChild(newButton)
    }
    button.innerHTML = "Playlist created!"
    console.log("Response: "+response)
}

async function downvote(){
    endpoint = "http://3.139.54.214:8000/rank/"
    const formData = new FormData();
    const rank_type = "downvote"
    const book_id = bookID
    formData.append("rank_type",rank_type)
    formData.append("book_id", book_id)
    let csrftoken = getCookie('csrftoken');
    const resp = await fetch(endpoint, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": csrftoken },
    });
    response = await resp.json();
    response = response.form_error
    if(response == "failed"){
        alert("You can only vote once!")
    }
    console.log("Response: "+response)
    window.location.reload();
}

async function getBook(url){
    let book;
    const resp =  await fetch(url);
    respBook = await resp.json() ;
    bookEmotion = respBook['emotionDict']
    // console.log(bookEmotion)
    
    for (var emo in bookEmotion){
        // console.log(bookEmotion[emo])
        bookEmotionNew.push(bookEmotion[emo])
    }
    console.log(bookEmotionNew)
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['anticipation', 'fear', 'anger', 'trust', 'surprise', 'positive', 'negative', 'sadness', 'disgust', 'joy'],
            datasets: [{
                label: 'Emotion Scores for Current Book',
                data: bookEmotionNew,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

// The following function are copying from 
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
