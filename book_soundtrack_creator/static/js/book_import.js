console.log("hello")
async function importBook(){
    alert("book sending")
    const myForm = document.getElementById("form")
    const file = document.getElementById("file")

    const endpoint = "http://127.0.0.1/book_upload";
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