const form = document.getElementById('upload-form')
const input = document.getElementById('upload-input')

function loadAsset(name) {
    const url = '/get_asset';
    const get = fetch(url, {
        method: 'POST',
        body: name,
        headers: {
            'content-type': 'text/plain'
        }
    }).then((response) => {
        return response.blob();
    }).then((blob) => {
        let objectURL = URL.createObjectURL(blob);
        let element = document.getElementById(name);
        element.src = objectURL;
        console.log('Успешно принят файл: ' + objectURL);
    }).catch(error => {
            throw error;
    });
}
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

loadAsset('github')
loadAsset('kaggle')