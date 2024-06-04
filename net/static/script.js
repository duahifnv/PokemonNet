const form = document.getElementById('upload-form')
const input = document.getElementById('upload-input')

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = new URL(e.currentTarget.action)
    const formData = new FormData();

    formData.append('file', input.files[0]);

    cacheImage(input.files[0]);
    const post = await fetch(url, {
        method: 'POST',
        body: formData
    }).then((response) => {
        if (!response.ok) {
            console.error('Ошибка POST');
        }
    }).catch(error => {
        throw error;
    });
    window.location.href = '/upload';
    /*const get = await fetch('/upload')
        .then((response) => {
        if (response.ok) {
            window.location.href = '/upload';
        }
        else {
            console.error('Ошибка GET');
        }
        })
        .catch(error => {
            throw error;
        });*/
});

function cacheImage(file) {
    const reader = new FileReader();
    reader.addEventListener("load", () => {
        localStorage.setItem('image', reader.result);
    }, false);
    if (file) {
        reader.readAsDataURL(file);
    }
}