// گۆڕینی ئەمە
const response = await fetch('/upload', {
    method: 'POST',
    body: formData
});

// بۆ ئەمە (بە ناونیشانی تەواوی سێرڤەرەکەت)
const response = await fetch('http://localhost:5000/upload', {
    method: 'POST',
    body: formData
});
