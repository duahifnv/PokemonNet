const form = document.getElementById('upload-form')
const input = document.getElementById('upload-input')

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = new URL(e.currentTarget.action)
    const formData = new FormData();

    formData.append('file', input.files[0]);

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        }).then((response) => {
            if (response.ok) {
                console.log('Изображение успешно загружено на сервер');
            }
            else {
                console.error('Произошла ошибка при загрузке изображения');
            }
        }).then(window.location.href = '/upload');
    }
    catch (err) {
        console.error(err);
    }
});