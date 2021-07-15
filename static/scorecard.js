const clearScoresBtn = document.querySelector('#clear');
const scorecardForm = document.querySelector('.scorecard');
const maxScore = document.querySelector('#max-score');
let balls = document.querySelectorAll('.ball');
let scores = document.querySelectorAll('.score');

function clearScores() {
  for (
    let i = 0;
    i <= 20;
    i++ // Clear ball entries
  ) {
    balls[i].value = '';
  }
  for (let i = 0; i < 10; i++) {
    // Clear score fields
    scores[i].value = '';
  }
  // Clear Max Score field
  maxScore.value = '300';
}

clearScoresBtn.addEventListener('click', clearScores);
