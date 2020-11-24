let books = []
let response = []
let url = "http://gutendex.com/books/" 

async function loadBooks(url){
    console.log(url)
    const resp =  await fetch(url);
    response = await resp.json() ;
    books = response.results;
    console.log(books)
    loadPage()
}
loadBooks(url)

function loadPage(){
    document.getElementById("row").innerHTML = ""
    for (var book in books){
        console.log("works")
        var bookDiv = document.createElement('div');
        bookDiv.setAttribute('class', "col-md-3 book");
        bookDiv.setAttribute('id', 'book'+book);
        bookDiv.setAttribute('name', books[book].id + '')
        bookDiv.style.border = "2px solid #44bcc9"
        bookDiv.style.margin = "10px"
        bookDiv.style.padding = "10px"
        bookDiv.style.borderRadius = "5px"
        
        bookDiv.style.cursor = "pointer"
        bookDiv.setAttribute('onclick', 'bookLink('+books[book].id+')')
        document.getElementById("row").appendChild(bookDiv);
        
        var title = document.createElement('p');
        title.setAttribute('class', 'title');
        title.setAttribute('id', 'name'+book);
        title.innerHTML = books[book].title
        title.style.fontWeight = "bold"
        document.getElementById('book'+book).appendChild(title);
        
        var author = document.createElement('p');
        author.setAttribute('class', 'author');
        author.setAttribute('id', 'author'+book);
        if(books[book].authors != ""){
            author.innerHTML = books[book].authors[0].name
        }else{
            author.innerHTML = "No Known Author"
        }
        
        document.getElementById('book'+book).appendChild(author);

        var img = document.createElement('img');
        img.setAttribute('src', books[book].formats["image/jpeg"]);
        img.setAttribute('alt','Book Cover');
        img.style.height = "200px"
        img.style.width = "125px"
        document.getElementById('book'+book).appendChild(img);

        

        // document.getElementById("book"+book).innerHTML = contacts[cardInd].firstName + " " + contacts[cardInd].lastName;
    }
}

function bookLink(bookID){
    let bookUrl = "http://gutendex.com/books/"+bookID
    console.log(bookUrl)
    getBook(bookUrl, bookID)
}

function getBookTopic(){
    url = "http://gutendex.com/books?topic="
    bookSearch = document.getElementById("bookTopic").value
    if(bookSearch == ""){
        alert("Please enter something into the search bar")
    }else{
        // console.log(bookSearch)
        book_tokens = bookSearch.split(" ")
        for (var tok in book_tokens){
            if(tok == 0){
                url += book_tokens[tok]
            }else{
                url += "%20"+book_tokens[tok]
            }
            
        }
        loadBooks(url)
    }

}

async function getBook(url){
    let book;
    console.log(url)
    const resp =  await fetch(url);
    respBook = await resp.json() ;
    book = respBook
    console.log(book)
    importBook(book)
}

function nextPage(){
    url = response.next
    console.log(url)
    loadBooks(url)
}

function getSearchBook(){
    url = "http://gutendex.com/books?search="
    bookSearch = document.getElementById("bookSearch").value
    if(bookSearch == ""){
        alert("Please enter something into the search bar")
    }else{
        // console.log(bookSearch)
        book_tokens = bookSearch.split(" ")
        for (var tok in book_tokens){
            if(tok == 0){
                url += book_tokens[tok]
            }else{
                url += "%20"+book_tokens[tok]
            }
            
        }
        loadBooks(url)
    }
    
}

async function importBook(book){
    console.log(book)
    var title = book.title
    var id = book.id
    var author = ""
    if(book.authors != ""){
        author = book.authors[0].name
    }
    var textUrl= book.formats['text/plain; charset=utf-8']
    console.log(textUrl)
    var cover = book.formats['image/jpeg']
    console.log(cover)
    const endpoint = "http://127.0.0.1:8000/book_upload/";
    let csrftoken = getCookie('csrftoken');

    var formData = new FormData();
    formData.append('title',title)
    formData.append('id',id)
    formData.append('author',author)
    formData.append('text',textUrl)
    formData.append('cover',cover)

    const resp = await fetch(endpoint, {
        method: "POST",
        body: formData,
        headers:{ "X-CSRFToken": csrftoken },
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

async function importBooks(){
    alert("book sending")
    const myForm = document.getElementById("form")
    const file = document.getElementById("file")

    const endpoint = "http://127.0.0.1/gutenberg_book_upload";
    const formData = new FormData();

    formData.append("book_multiFile", file.files[0]);
    console.log(file.files[0])
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