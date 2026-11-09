// Browser demo. SYNTHETIC rolls only; same rejection@252 rule as src/dice.js.
(function () {
  'use strict';
  var FACES = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685'];
  var ROLES = ['Mayor', 'Council', 'Resident', 'Reporter', 'Auditor', 'Youth delegate'];
  var ACTIONS = ['propose', 'question', 'amend', 'fact-check', 'summarize', 'vote on'];
  var ANGLES = ['cost', 'fairness', 'evidence', 'timeline', 'who is left out', 'trade-offs'];
  function byte() { var a = new Uint8Array(1); crypto.getRandomValues(a); return a[0]; }
  function die() { for (;;) { var b = byte(); if (b < 252) return 1 + (b % 6); } }
  document.getElementById('roll').addEventListener('click', function () {
    var d = [die(), die(), die()];
    var idx = (d[0] - 1) * 36 + (d[1] - 1) * 6 + (d[2] - 1);
    var topic = document.getElementById('topic');
    var text = 'SYNTHETIC roll ' + d.join(', ') + ' (outcome ' + (idx + 1) + ' of 216): As ' +
      ROLES[d[0] - 1] + ', ' + ACTIONS[d[1] - 1] + ' the ' + topic.options[topic.selectedIndex].text +
      ' plan, focusing on ' + ANGLES[d[2] - 1] + '.';
    document.getElementById('result').textContent = text;
    document.getElementById('dice').textContent = d.map(function (x) { return FACES[x - 1]; }).join(' ');
    var li = document.createElement('li'); li.textContent = text;
    document.getElementById('history').prepend(li);
  });
})();
