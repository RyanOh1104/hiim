function randomPlaceholder() {
    var questions = [
      '[기억 낚아올리기] 오늘 먹었던 음식 중 뭐가 제일 기억에 남아요?',
      '[기억 낚아올리기] 오늘 하루 아쉬웠던 점이 있다면?',
      '[기억 낚아올리기] 오늘 하루 소소한 행복을 어디서 찾았어요?',
      '[기억 낚아올리기] 오늘이 어제와 달랐던 점은 뭔가요?',
      '[기억 낚아올리기] 오늘 시간이 가장 빨리 간 때는 언제인가요?',
      '[기억 낚아올리기] 오늘을 하나의 단어로 표현한다면?',
      '[기억 낚아올리기] 오늘이 어제와 달랐던 점 한가지를 꼽으라면?',
      '[기억 낚아올리기] 오늘 있었던 장면 중 하나를 최대한 구체적으로 묘사해보세요!',
      '[기억 낚아올리기] 오늘 날씨는 어땠어요? 날씨가 오늘 하루에 영향을 미쳤나요?',
    ];
    const randomQuestion = questions[Math.floor(Math.random() * questions.length)];
    console.log('random question is :', randomQuestion);
    document.getElementById('id_what').setAttribute('placeholder', randomQuestion);
  }

function init() {
    randomPlaceholder();
}
init();