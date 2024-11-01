document.addEventListener('DOMContentLoaded', () => {

    // Обработчик для формы отзывов
    const reviewForm = document.getElementById('review-form');
    const reviewList = document.getElementById('review-list');

    reviewForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const reviewText = document.getElementById('review-text').value;
        if (reviewText.trim()) {
            const reviewItem = document.createElement('div');
            reviewItem.classList.add('card');
            reviewItem.textContent = reviewText;
            reviewList.appendChild(reviewItem);
            document.getElementById('review-text').value = '';
        }
    });

    // Обработчик для экстренной кнопки
    const emergencyButton = document.getElementById('emergency-button');
    emergencyButton.addEventListener('click', () => {
        alert('Вызов экстренных служб инициирован!');
    });
});