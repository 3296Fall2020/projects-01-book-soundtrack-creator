function importBook(){

    const myForm = document.getElementById("form")
    const file = document.getElementById("file")

    myForm.addEventListener("submit", e =>{
        e.preventDefault();
        const endpoint = "http://127.0.0.1/book_upload";
        const formData = new FormData();

        formData.append("book_multiFile", file.files[0]);
        console.log(file.files[0])
        fetch(endpoint, {
            method: "post",
            body: formData
        }).catch(console.error);
        alert("Book added!");
    });
}