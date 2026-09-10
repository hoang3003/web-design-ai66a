const form = document.querySelector('#house-form');
const resultBox = document.querySelector('#result');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const params = new URLSearchParams({
        area: document.querySelector('#area').value,
        bedrooms: document.querySelector('#bedrooms').value,
        location: document.querySelector('#location').value || 'other',
    });

    resultBox.textContent = 'Đang gửi dữ liệu...';

    try {
        const response = await fetch(`http://127.0.0.1:8000/predict?${params}`);

        if (!response.ok) {
            throw new Error('Không thể gửi dữ liệu đến server.');
        }

        const result = await response.json();
        resultBox.innerHTML = `
            <h2>Kết quả</h2>
            <p>Diện tích: ${result.area} m2</p>
            <p>Khu vực: ${result.location}</p>
            <p>Số phòng ngủ: ${result.bedrooms}</p>
            <p>Giá dự đoán: ${result.predicted_price.toLocaleString('vi-VN')} VND</p>
        `;
    } catch (error) {
        resultBox.textContent = error.message;
    }
});
