let books = []
let response = []
 /*An array containing all the country names in the world:*/




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
    if(books.length == 0){
        document.getElementById("emptySearch").innerHTML = "No Books Found."
        
    }
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
    getBook(bookUrl)
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

function lastPage(){
    url = response.previous
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
    console.log(book.formats)
    var textUrl;
    // checks for a url that is either 'text/plain; charset=utf-8' or is a txt file
    var finalForm = ""
    for(var form in book.formats){
        // console.log("form" + form)
        // textUrl = books.formats[form]
        if(form == 'text/plain; charset=us-ascii'){
            console.log("good")
            textUrl = book.formats['text/plain; charset=us-ascii']
            finalForm = form
            break;
        }else if(book.formats[form].includes('.txt') ){ //&& !form.includes('utf-8')
            textUrl = book.formats[form]
            finalForm = form
        }else if(form.includes('text/plain') && (book.formats[form].includes('.zip'))){
            textUrl = book.formats[form]
            finalForm = form
        }
    }
    console.log("Final file format: " + finalForm) // prints out the final chosen file format
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
    responseMsg = response.form_error
    console.log("Response: "+responseMsg)
    if(responseMsg == "Submission successful"){
      console.log("reached")
    }else {
        alert(responseMsg)
    }
    window.location.href = "http://127.0.0.1:8000/book_info/"+id
    console.log("didn't work?")
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


// testing auto complete form 
var bookshelves = ["Adventure","Africa","African American Writers","Ainslee's","American Revolutionary War","Anarchism","Animal","Animals-Domestic","Animals-Wild-Birds","Animals-Wild-Insects","Animals-Wild-Mammals","Animals-Wild-Reptiles and Amphibians","Animals-Wild-Trapping","Animals-Wild","Anthropology","Archaeology","Architecture","Argentina","Armour's Monthly Cook Book","Art","Arthurian Legends","Astounding Stories","Astronomy","Atheism","Australia","B","BahÃ¡'Ã­ Faith","Banned Books List from the American Library Association","Banned Books from Anne Haight's list","BarnavÃ¤nnen","Bestsellers, American, 1895-1923","Best Books Ever Listings","Bibliomania","Biographies","Biology","Bird-Lore","Birds, Illustrated by Color Photography","Blackwood's Edinburgh Magazine","Boer War","Botany","British Law","Buchanan's Journal of Man","Buddhism","Bulgaria","Bulletin de Lille","C","CIA World Factbooks","Camping","Canada","Canon Law","Celtic Magazine","Chambers's Edinburgh Journal","Chemistry","Child's Own Book of Great Musicians","Children's Anthologies","Children's Biography","Children's Book Series","Children's Fiction","Children's History","Children's Instructional Books","Children's Literature","Children's Myths, Fairy Tales, etc.","Children's Picture Books","Children's Religion","Children's Verse","Christianity","Christmas","Classical Antiquity","Contemporary Reviews","Continental Monthly","Cookbooks and Cooking","Crafts","Crime Fiction","Crime Nonfiction","Current History","Czech","D","DE Drama","DE Kinderbuch","DE Lyrik","DE Prosa","DE Sachbuch","Detective Fiction","Dew Drops","De Aarde en haar Volken","Donahoe's Magazine","E","Early English Text Society","Ecology","Education","Egypt","Engineering","English Civil War","Erotic Fiction","Esperanto","F","FR Beaux-Arts","FR Biographie, MÃ©moires, Journal intime, Correspondance","FR Chansons","FR Chroniques","FR Contes","FR Droit et Justice","FR Education et Enseignement","FR Femmes","FR Guerres","FR Histoire","FR Humour","FR Illustrateurs","FR Jeunesse","FR Langues","FR La PremiÃ¨re Guerre Mondiale, 1914-1918","FR LittÃ©rature","FR LittÃ©rature francophone","FR Livres, Collections et Bibliophilie","FR Musique","FR MÃ©tiers et Artisanat","FR NouveautÃ©s","FR Nouvelles","FR Occultisme","FR Peinture","FR Peuples et SociÃ©tÃ©s","FR Philosophie, Religion et Morale","FR Politique","FR PoÃ©sie","FR Presse","FR Prix Nobel","FR Sciences et Techniques","FR Science fiction","FR Services publics","FR Sports et loisirs","FR SÃ©duction et libertinage","FR ThÃ©Ã¢tre","FR Villes","FR Voyages et pays","Famous Scots Series","Fantasy","Folklore","Forestry","France","G","Garden and Forest","General Fiction","Geology","Germany","German Language Books","Godey's Lady's Book","Golden Days for Boys and Girls","Gothic Fiction","Graham's Magazine","Greece","H","Harper's New Monthly Magazine","Harper's Young People","Harvard Classics","Hinduism","Historical Fiction","Horror","Horticulture","Humor","I","IT Agraria","IT Archeologia e Storia dell'arte","IT Architettura","IT Arte varia","IT Biografie","IT Botanica","IT Cucina","IT Discorsi e Orazioni","IT Economia","IT Filosofia","IT Folklore","IT Geografia","IT Legge","IT Letteratura","IT Letteratura per ragazzi","IT Linguistica","IT Miscellanea","IT Musica","IT Narrativa varia","IT Numismatica","IT Poesia","IT Psicologia e Sociologia","IT Racconti","IT Religione e SpiritualitÃ ","IT Romanzi","IT Romanzi storici","IT Salute","IT Scienza","IT Scienze militari","IT Scienze politiche","IT Storia","IT Teatro dialettale","IT Teatro in prosa","IT Teatro in versi","IT Tecnologia","IT Umorismo","IT Viaggi","Illustrators","India","Islam","Italy","J","Judaism","Journal of Entomology and Zoology","L","L'Illustration","Language Education","Latter Day Saints","Lippincott's Magazine","Little Folks","London Medical Gazette","Love","M","Manufacturing","Maps and Cartography","Masterpieces in Colour","Mathematics","McClure's Magazine","Medicine","MediÃ¦val Town Series","Microbiology","Microscopy","Mother Earth","Movie Books","Mrs Whittelsey's Magazine for Mothers and Daughters","Music","Mycology","Mystery Fiction","Mythology","N","Napoleonic(Bookshelf)","Native America","Natural History","New Zealand","Northern Nut Growers Association","Norway","Notes and Queries","Noteworthy Trials(Bookshelf)","O","One Act Plays","Opera","Our Young Folks","P","PT Arte","PT Biografia","PT CiÃªncia e TÃ©cnica","PT Contos","PT HistÃ³ria","PT Infantil e Juvenil","PT LÃ­ngua Portuguesa","PT NavegaÃ§Ãµes e ExploraÃ§Ãµes","PT PeriÃ³dicos","PT Poesia","PT PolÃ­tica e Sociedade","PT Romance","PT Teatro","Paganism","Philosophy","Photography","Physics","Physiology","Pirates, Buccaneers, Corsairs, etc.","Plays","Poetry, A Magazine of Verse","Poetry","Politics","Popular Science Monthly","Prairie Farmer","Precursors of Science Fiction","Project Gutenberg","Psychology","Punch","Punchinello","R","Racism","Reference","Romantic Fiction","S","School Stories","Science","Science Fiction","Science Fiction by Women","Scientific American","Scouts","Scribner's Magazine","Short Stories","Slavery","Sociology","South Africa","South America","Spanish American War","St. Nicholas Magazine for Boys and Girls","Suffrage","T","Technology","The Aldine","The American Architect and Building News","The American Bee Journal","The American Journal of Archaeology","The American Missionary","The American Quarterly Review","The Arena","The Argosy","The Atlantic Monthly","The Baptist Magazine","The Bay State Monthly","The Botanical Magazine","The Brochure Series of Architectural Illustration","The Catholic World","The Christian Foundation","The Church of England Magazine","The Contemporary Review","The Economist","The Esperantist","The Galaxy","The Girls Own Paper","The Great Round World And What Is Going On In It","The Haslemere Museum Gazette","The Idler","The Illustrated War News","The International Magazine of Literature, Art, and Science","The Irish Ecclesiastical Record","The Irish Penny Journal","The Journal of Negro History","The Knickerbocker","The Mayflower","The Menorah Journal","The Mentor","The Mirror of Literature, Amusement, and Instruction","The Mirror of Taste, and Dramatic Censor","The National Preacher","The North American Medical and Surgical Journal","The Nursery","The Philatelic Digital Library Project","The Scrap Book","The Speaker","The Stars and Stripes","The Strand Magazine","The Unpopular Review","The Writer","The Yellow Book","Transportation","Travel","U","US Civil War","United Kingdom","United States","United States Law","W","Western","Witchcraft","Women's Travel Journals","Woodwork","World War I","World War II","Z","Zoology"]

function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
          /*check if the item starts with the same letters as the text field value:*/
          if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
            /*create a DIV element for each matching element:*/
            b = document.createElement("DIV");
            /*make the matching letters bold:*/
            b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
            b.innerHTML += arr[i].substr(val.length);
            /*insert a input field that will hold the current array item's value:*/
            b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
            /*execute a function when someone clicks on the item value (DIV element):*/
            b.addEventListener("click", function(e) {
                /*insert the value for the autocomplete text field:*/
                inp.value = this.getElementsByTagName("input")[0].value;
                /*close the list of autocompleted values,
                (or any other open lists of autocompleted values:*/
                closeAllLists();
            });
            a.appendChild(b);
          }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          /*If the arrow DOWN key is pressed,
          increase the currentFocus variable:*/
          currentFocus++;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 38) { //up
          /*If the arrow UP key is pressed,
          decrease the currentFocus variable:*/
          currentFocus--;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 13) {
          /*If the ENTER key is pressed, prevent the form from being submitted,*/
          e.preventDefault();
          if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (x) x[currentFocus].click();
          }
        }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
          x[i].parentNode.removeChild(x[i]);
        }
      }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
  }
  
 