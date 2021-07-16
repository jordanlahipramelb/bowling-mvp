console.log('is this thing on?');

const clearScoresBtn = document.querySelector('#clear');
const scorecardForm = document.querySelector('#scorecard');
const maxScore = document.querySelector('#max-score');
let balls = document.querySelectorAll('.ball');
let scores = document.querySelectorAll('.score');

clearScoresBtn.addEventListener('click', clearScores);

balls.forEach((ball) => {
  ball.addEventListener('change', calculateScores);
});

// Clear input value fields
function clearScores() {
  for (let i = 0; i <= 20; i++) {
    balls[i].value = '';
  }
  for (let i = 0; i < 10; i++) {
    scores[i].value = '';
  }
  maxScore.value = '300';
}

// Calculates the frames if the fields are changed
function calculateScores() {
  let nextBall = '';
  let followingNextBall = '';
  let totalScore = 0;

  // Clear the scores before calculating
  for (let i = 0; i < 10; i++) {
    scores[i].value = '';
  }

  // Validates the fields of the first 19 balls
  for (let i = 0; i <= 18; i++) {
    // Convert dashes to zeroes
    if (balls[i].value == '-') {
      balls[i].value = '0';
    }

    // Validates 1st ball of each frame
    // Can't be '/' which are spares
    ballValues = balls[i].value;
    if (
      i % 2 == 0 &&
      ballValues != '0' &&
      ballValues != '1' &&
      ballValues != '2' &&
      ballValues != '3' &&
      ballValues != '4' &&
      ballValues != '5' &&
      ballValues != '6' &&
      ballValues != '7' &&
      ballValues != '8' &&
      ballValues != '9' &&
      ballValues.toLowerCase() != 'x'
    ) {
      balls[i].value = '';
    }

    // Validates 2nd ball of each frame except 10th frame
    if (
      i % 2 != 0 &&
      ballValues != '0' &&
      ballValues != '1' &&
      ballValues != '2' &&
      ballValues != '3' &&
      ballValues != '4' &&
      ballValues != '5' &&
      ballValues != '6' &&
      ballValues != '7' &&
      ballValues != '8' &&
      ballValues != '9' &&
      ballValues != '/'
    ) {
      balls[i].value = '';
    }
  }

  // Validates ball 19 and 20 (extra frames)
  for (let i = 19; i <= 20; i++) {
    // Convert dashes to 0 pins
    if (balls[i].value == '-') {
      balls[i].value = '0';
    }

    ballValues = balls[i].value;
    if (
      ballValues != '0' &&
      ballValues != '1' &&
      ballValues != '2' &&
      ballValues != '3' &&
      ballValues != '4' &&
      ballValues != '5' &&
      ballValues != '6' &&
      ballValues != '7' &&
      ballValues != '8' &&
      ballValues != '9' &&
      ballValues != '/' &&
      ballValues.toLowerCase() != 'x'
    ) {
      balls[i].value = '';
    }
  }
  // End input validation
  ///////////////////////////////
  // Main loop for calculating

  // Calculate 1st ball of each frame
  for (let j = 0; j <= 18; j += 2) {
    // Start frame score at 0
    let frameScore = 0;
    let showScore = false;

    // Strike Validation
    // Only allowed on 1st ball of each frame except 10th
    if (balls[j].value.toLowerCase() == 'x') {
      frameScore += 10;

      // Frames 1-8
      if (j < 16) {
        // Remove value if value entered in 2nd ball of strike frame
        if (balls[j + 1].value != '') {
          balls[j + 1].value = '';
        }

        // Next ball becomes 1st ball in next frame
        nextBall = balls[j + 2].value;

        // If the next ball is a strike, then we take the next ball of the next frame as first ball in the following frame
        if (nextBall.toLowerCase() == 'x') {
          followingNextBall = balls[j + 4].value;
        }

        // Otherwise, it's the second ball in the next frame
        else {
          followingNextBall = balls[j + 3].value;
        }
      }

      // Frame 9
      if (j == 16) {
        // Next ball is the 1st ball in the next frame
        nextBall = balls[j + 2].value;

        // following next ball is the 2nd ball in the next frame
        followingNextBall = balls[j + 3].value;
      }

      // 10th frame
      if (j == 18) {
        // Next ball is the next ball
        nextBall = balls[j + 1].value;

        // actually follows the next ball
        followingNextBall = balls[j + 2].value;
      }

      // Check if they actually have a value/aren't empty
      if (nextBall != '' && followingNextBall != '') {
        //Add score if the next ball is a strike
        if (nextBall.toLowerCase() == 'x') {
          frameScore += 10;

          // Add score agai if the followingNext is a strike
          if (followingNextBall.toLowerCase() == 'x') {
            frameScore += 10;
          }
          // if it's not, then take its value instead
          else {
            frameScore += parseInt(followingNextBall);
          }
        } else {
          // if the ball after the next ball is a spare
          if (followingNextBall == '/') {
            frameScore += 10;
          }

          // if it's an open frame
          else {
            frameScore += parseInt(nextBall);
            frameScore += parseInt(followingNextBall);
          }
        }
        showScore = true;
      }
    }

    // If it's not a strike, it's a spare or open frame
    else if (balls[j].value != '' && balls[j + 1].value != '') {
      // If it's a spare, add to score
      if (balls[j + 1].value == '/') {
        frameScore += 10;

        // Next ball needs to be checked
        if (balls[j + 2].value != '') {
          // If the next ball is a strike
          if (balls[j + 2].value.toLowerCase() == 'x') {
            frameScore += 10;
            showScore = true;
          }

          // If the next ball isn't a strike, take its value
          else {
            frameScore += parseInt(balls[j + 2].value);
            showScore = true;
          }
        }
      }

      // If it's an open frame
      else {
        frameScore += parseInt(balls[j].value);
        frameScore += parseInt(balls[j + 1].value);
        showScore = true;
      }
    }

    // Keep running total of the score
    totalScore += frameScore;
    if (showScore) {
      k = j / 2; // Convert to correct score location
      scores[k].value = totalScore;
      maxScore.value = (9 - k) * 30 + totalScore;
    }
  }
}
