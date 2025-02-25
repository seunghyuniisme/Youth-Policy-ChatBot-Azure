function toggleGuide() {
  const moreText = document.getElementById("more-text");
  const toggleButton = document.querySelector(".toggle-guide");
  const userGuide = document.querySelector('.user-guide');

  if (moreText.style.display === "none" || moreText.style.display === "") {
      moreText.style.display = "inline";
      userGuide.style.maxHeight = "1000px"; // 충분히 큰 값으로 박스 크기 확대
      toggleButton.textContent = "접기";
  } else {
      moreText.style.display = "none";
      userGuide.style.maxHeight = "200px"; // 원래 높이로 돌아가도록 설정
      toggleButton.textContent = "펼치기";
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const characterButtons = document.querySelectorAll('.character-button');

  characterButtons.forEach(button => {
      button.addEventListener('click', function() {
          const selectedCharacter = this.getAttribute('data-character');
          localStorage.setItem('selectedCharacter', selectedCharacter);
          window.location.href = 'index.html'; // 채팅 페이지로 이동
      });
  });
});
