// گۆڕینی هەموو داواکارییەکان بەم شێوەیە:
fetch('http://localhost:5000/upload', {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
    },
    body: formData
})
.then(response => {
    if (!response.ok) {
        return response.text().then(text => { throw new Error(text) })
    }
    return response.json()
})
.then(data => {
    console.log(data)
    alert(data.message || 'سەرکەوتووبوو!')
})
.catch(error => {
    console.error('هەڵە:', error)
    alert('هەڵە: ' + error.message)
})
