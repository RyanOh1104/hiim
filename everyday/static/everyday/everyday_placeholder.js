function randomPlaceholder() {
    console.log('function called');
    var questions = [
      '기억 낚아올리기 : 오늘 먹었던 음식 중 뭐가 제일 기억에 남아요?',
      '기억 낚아올리기 : 오늘 하루 아쉬웠던 점이 있다면?',
      '기억 낚아올리기 : aaa',
      '기억 낚아올리기 : bbb',
      '기억 낚아올리기 : ccc',
    ];
    const randomQuestion = questions[Math.floor(Math.random() * questions.length)];
    console.log('random is: ', randomQuestion);
    document.getElementById('what')[0].setAttribute('placeholder', randomQuestion);
  }

function init() {
    randomPlaceholder();
}
init();