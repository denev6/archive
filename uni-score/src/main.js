/*
document.addEventListener("DOMContentLoaded", function (event) {
  document.getElementById("info-text").innerHTML =
    "\
    대학별 점수 환산법(1000점)을 기반으로<br /> \
    가중치를 부여해 점수를 계산합니다. <br /> \
    실제 대학 입시 점수와는 다르므로 <br /> \
    참고 자료로만 활용하세요.<br /><br /> \
    + 밑줄로 표시된 내용은 클릭을 통해 확인해 볼 수 있습니다.";
});
*/

function closeInfoBox() {
  document.getElementById("info-bg").style.display = "none";
  document.getElementById("info-box").style.display = "none";
}

const dt_uniName =
  "<b>대학명 최저</b> <br><br> \
    0합 0 이내 <br> \
    - 국어 <br> \
    - 수학 <br> \
    - 영어";

// 생략

const dt_score =
  "<b>점수 계산 방법</b> <br><br> \
    - (중요) 2023학년도 모집요강을 기준으로 환산하였기 때문에,\
     이전 연도 등급과 비교 시 일치하지 않을 수 있습니다. <br> \
    - 각 학교별 내 점수를 비교해 나에게 유리한 학교를 찾을 수 있습니다.";

const details = [
  dt_score,
  dt_uniName,
  // 생략 
];

function showDetail(id) {
  // 1: 대학명, 2: ... 
  // 0: 점수 보는 법
  document.getElementById("info-text").innerHTML = details[id];
  document.getElementById("info-bg").style.display = "block";
  document.getElementById("info-box").style.display = "block";
}
