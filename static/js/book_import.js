console.log("hello")
async function importBook(){
    alert("book sending")
    const file = document.getElementById("file")
    const title = document.getElementById("title").value
    const author = document.getElementById("author").value
    // console.log(file)
    const endpoint = "http://127.0.0.1:8000/book_import_upload/";
    const formData = new FormData();
    formData.append("title", title)
    formData.append("author", author)
    formData.append("text", file.files[0]);
    console.log(file.files[0])
    let csrftoken = getCookie('csrftoken');
    const resp = await fetch(endpoint, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": csrftoken },
    });
    response = await resp.json();
    response = response.form_error
    console.log("Response: "+response)
    if(response == "Submission successful"){
      console.log("reached")
    }else {
        console.log("failed")
    }
    alert("Book added!");
    
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