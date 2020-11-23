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
        bookDiv.setAttribute('class', "col-sm-4 book");
        bookDiv.setAttribute('id', 'book'+book);
        bookDiv.setAttribute('name', books[book].id + '')
        bookDiv.style.border = "2px solid black"
        // bookDiv.style.margin = "10px"
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
        img.style.height = "100px"
        img.style.width = "100px"
        document.getElementById('book'+book).appendChild(img);

        

        // document.getElementById("book"+book).innerHTML = contacts[cardInd].firstName + " " + contacts[cardInd].lastName;
    }
}

function bookLink(bookID){
    let bookUrl = "http://gutendex.com/books/"+bookID
    console.log(bookUrl)
    getBook(bookUrl)
}

function getBook(url){
    fetch(url)
        .then((reponse) => {
            if(reponse.ok){
                books = response.results
                return reponse.json();
            }else{
                return Promise.reject('something went wrong!');
            }
        })
        .then((myJson) => {
            
            console.log(myJson);
        })
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