document.addEventListener('DOMContentLoaded', function () {
  const gameContainer = document.getElementById('game-container');
  const lights = document.querySelectorAll('.light');
  const startButton = document.getElementById('start-button');
  let lightsClicked = 0;
  let startTime, endTime, lastResponseTime, gameRunning = false;

  function startGame() {
    resetLights();

    lightsClicked = 0;
    updateLights();

    lights.forEach((light, index) => {
      light.style.backgroundColor = '#d1d1d1';

      setTimeout(() => {
        if (lightsClicked < lights.length) {
          light.style.backgroundColor = 'red';
          lightsClicked++;
          updateLights();
        }

        if (lightsClicked === lights.length) {
          startRace();
        }
      }, index * 1000);
    });
  }

  function startRace() {
    startTime = new Date();
    gameRunning = true;

    enableClicks();

    lights.forEach((light) => {
      light.style.backgroundColor = '#00ff00';
    });
  }

  function enableClicks() {
    gameContainer.onclick = function (event) {
      if (gameRunning) {
        const clickedLight = event.target;
        if (clickedLight.classList.contains('light')) {
          if (clickedLight.style.backgroundColor === 'rgb(0, 255, 0)') {
            endTime = new Date();
            const responseTime = endTime - startTime;
            lastResponseTime = responseTime;
            var prevResult = document.getElementById('blinkResult');

            sendForm(responseTime);
            alert('Your response time: ' + responseTime + ' milliseconds');
            gameRunning = false;
            gameContainer.onclick = null;
            updateLastResponseTime();
          } else {
            resetGame();
          }
        }
      }
    };
  }

  function resetGame() {
    resetLights();
    gameContainer.onclick = null; // Disable further clicks
    startButton.style.display = 'block';
  }

  function resetLights() {
    // Set all lights to grey and make them visible
    lights.forEach((light, index) => {
      light.style.backgroundColor = '#d1d1d1';
      light.style.display = 'block';
    });
    gameRunning = false;
  }

  function updateLights() {
    document.getElementById('lights-clicked').textContent = 'Lights Turned: ' + lightsClicked;
  }

  function updateLastResponseTime() {
    document.getElementById('last-response-time').textContent = 'Last Response Time: ' + lastResponseTime + ' milliseconds';
    document.getElementById('last-response-time').style.display = 'block'; // Show the last response time
    startButton.style.display = 'block'; // Show the start button after the response time is displayed
  }

  startButton.addEventListener('click', function () {
    startButton.style.display = 'none'; // Hide the start button when the game starts
    document.getElementById('last-response-time').style.display = 'none'; // Hide the last response time when starting a new game
    startGame();
  });

  // Initially, show the start button
  startButton.style.display = 'block';
});

function sendForm(blinkScore) {
  var form = document.createElement('form');

  form.method = 'post';
  form.action = '/gameBlink';

  var resultInput = document.createElement('input');
  resultInput.type = 'hidden';
  resultInput.name = 'blinkResult';
  resultInput.value = blinkScore;

  form.appendChild(resultInput);

  document.body.appendChild(form);

  form.submit();
}