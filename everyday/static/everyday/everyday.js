var today = new Date();//오늘 날짜. 내 컴퓨터 로컬을 기준으로 today에 Date 객체를 넣어줌
var date = new Date();//today의 Date를 세어주는 역할

function range(start, end) {  /// range()함수 생성
    var arr = [];
    var length = end - start;
    for (var i=0; i<=length; i++) {
        arr[i] = start;
        start++;
    }
    return arr;
}

function prevCalendar() {//이전 달
// 이전 달을 today에 값을 저장하고 달력에 today를 넣어줌
//today.getFullYear() 현재 년도//today.getMonth() 월  //today.getDate() 일 
//getMonth()는 현재 달을 받아 오므로 이전달을 출력하려면 -1을 해줘야함
 today = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
 buildCalendar(); //달력 cell 만들어 출력 
}

function nextCalendar() {//다음 달
    // 다음 달을 today에 값을 저장하고 달력에 today 넣어줌
    //today.getFullYear() 현재 년도//today.getMonth() 월  //today.getDate() 일 
    //getMonth()는 현재 달을 받아 오므로 다음달을 출력하려면 +1을 해줘야함
     today = new Date(today.getFullYear(), today.getMonth() + 1, today.getDate());
     buildCalendar();//달력 cell 만들어 출력
}

function progressBar() {
  var lastDate = new Date(today.getFullYear(),today.getMonth()+1, 0);
  var datesThisMonth = lastDate.getDate();
  
  var howManyThisMonth = parseInt(thisMonth); // 원래 string인 thisMonth를 integer로 바꿔줌
  var progress = Math.ceil((howManyThisMonth / datesThisMonth)*100); // 소숫점 올림
  document.getElementsByClassName('progress-bar')[0].setAttribute('aria-valuenow', progress);
  document.getElementsByClassName('progress-bar')[0].setAttribute('style', `width: ${progress}%;`);
  console.log('percentage is', progress);
}

function buildCalendar(){//현재 달 달력 만들기
    var doMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    //이번 달의 첫째 날,
    //new를 쓰는 이유 : new를 쓰면 이번달의 로컬 월을 정확하게 받아온다.     
    //new를 쓰지 않았을때 이번달을 받아오려면 +1을 해줘야한다. 
    //왜냐면 getMonth()는 0~11을 반환하기 때문
    var lastDate = new Date(today.getFullYear(),today.getMonth()+1, 0);
    //이번 달의 마지막 날
    //new를 써주면 정확한 월을 가져옴, getMonth()+1을 해주면 다음달로 넘어가는데
    //day를 1부터 시작하는게 아니라 0부터 시작하기 때문에 
    //대로 된 다음달 시작일(1일)은 못가져오고 1 전인 0, 즉 전달 마지막일 을 가져오게 된다
    var tbCalendar = document.getElementById("mycalendar");
    //날짜를 찍을 테이블 변수 만듬, 일 까지 다 찍힘
    var yearMonth = document.getElementById("yearMonth");
    //테이블에 정확한 날짜 찍는 변수
    //innerHTML : js 언어를 HTML의 권장 표준 언어로 바꾼다
    //new를 찍지 않아서 month는 +1을 더해줘야 한다. 
     yearMonth.innerHTML = today.getFullYear() + "년 " + (today.getMonth() + 1) + "월"; 

     /*while은 이번달이 끝나면 다음달로 넘겨주는 역할*/
    while (tbCalendar.rows.length > 2) {
    //열을 지워줌
    //기본 열 크기는 body 부분에서 2로 고정되어 있다.
          tbCalendar.deleteRow(tbCalendar.rows.length-1);
          //테이블의 tr 갯수 만큼의 열 묶음은 -1칸 해줘야지 
        //30일 이후로 담을달에 순서대로 열이 계속 이어진다.
     }
     var row = null;
     row = tbCalendar.insertRow();
     //테이블에 새로운 열 삽입//즉, 초기화
     var cnt = 0;// count, 셀의 갯수를 세어주는 역할
    // 1일이 시작되는 칸을 맞추어 줌
     for (i=0; i<doMonth.getDay(); i++) {
     /*이번달의 day만큼 돌림*/
          cell = row.insertCell();//열 한칸한칸 계속 만들어주는 역할
          cnt = cnt + 1;//열의 갯수를 계속 다음으로 위치하게 해주는 역할
     }
    /*달력 출력*/
     for (i=1; i<=lastDate.getDate(); i++) { 
     //1일부터 마지막 일까지 돌림
          cell = row.insertCell();//열 한칸한칸 계속 만들어주는 역할
          row.classList.add("eachRow");
          var dateString = `${today.getFullYear()}년 ${today.getMonth()+1}월 ${i}일`;
          cell.innerHTML = `<div class="eachDate">${i}</div>`
          + `<a href='/everyday/everydaycreate'>
          <div class='empty'>it's<br>empty<br>here</div></a>`;
          var dateStringyfied = `${today.getFullYear()}-${today.getMonth() < 10 ? `0${today.getMonth()+1}` : today.getMonth()+1}-${i < 10 ? `0${i}` : i}`
          cell.setAttribute('date', dateStringyfied);

          var eventsLength = Object.keys(events).length; // events 오브젝트의 길이
          
          for (j in range(0,eventsLength-1)) {
            if (events[j].dates === dateStringyfied) {
                var thisCell = document.querySelector(`[date='${dateStringyfied}']`);
                if (events[j].emoji === "") {
                  thisCell.innerHTML = `<div class = eachDate>${i}</div>` +
                  `<a href='/everyday/everydaydetail/${userId}/${events[j].slug}'>
                  <div class='keywords pc-only'>${events[j].keywords}</div>
                  <div class='empty mobile-only'>its'<br>empty<br>here</div></a>`;
                } else {
                thisCell.innerHTML = `<div class = eachDate>${i}</div>` +
                `<a href='/everyday/everydaydetail/${userId}/${events[j].slug}'>
                <div class='keywords pc-only'>${events[j].keywords}</div>
                <div class='main-emoji mobile-only'>${events[j].emoji}</div></a>`;
                } 
                }
             }
          
          
          cnt = cnt + 1;//열의 갯수를 계속 다음으로 위치하게 해주는 역할
      if (cnt % 7 == 1) {/*일요일 계산*/
          //1주일이 7일 이므로 일요일 구하기
          //월화수목금토일을 7로 나눴을때 나머지가 1이면 cnt가 1번째에 위치함을 의미한다
        //+`<div class="content">${events[i].keywords}</div>`;

        //1번째의 cell에만 색칠
    }    
    if (cnt%7 == 0){/* 1주일이 7일 이므로 토요일 구하기*/
          //월화수목금토일을 7로 나눴을때 나머지가 0이면 cnt가 7번째에 위치함을 의미한다

          //+`<div class="content">${events[i].keywords}</div>`;          //7번째의 cell에만 색칠
           row = mycalendar.insertRow();
           //토요일 다음에 올 셀을 추가
    }
      /*  오늘  */
    if (today.getFullYear() == date.getFullYear()
         && today.getMonth() == date.getMonth()
         && i == date.getDate()) {
          //달력에 있는 년,달과 내 컴퓨터의 로컬 년,달이 같고, 일이 오늘의 일과 같으면
        cell.classList.add("todayCell")

        for (k in range(0, eventsLength-1)) { // 오늘 event가 등록되어 있으면 키워드를, 없으면 Add
          if (events[k].dates === dateStringyfied) {
            cell.innerHTML = `<div class = eachDate>${i}</div>` +
                `<a href='/everyday/everydaydetail/${userId}/${events[k].slug}'>
                <div class='keywords pc-only'>${events[k].keywords}</div>
                <div class='main-emoji mobile-only'>${events[k].emoji}</div></a>`;
          } else {
            // cell.innerHTML = `<div class="eachDate">${i}</div>`+
            // `<a href='/everyday/everydaycreate'><div class='empty'>It's<br>empty<br>here</div></a>`
          }
        }      
       }
     }
}

function init() {
    progressBar();
    buildCalendar();
}
init();