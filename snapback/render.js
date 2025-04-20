
fetch('deck.json')
  .then(response => response.json())
  .then(data => {
    const container = document.getElementById('deck-container');
    data.cards.forEach(card => {
      const cardEl = document.createElement('div');
      cardEl.className = 'card';
      cardEl.innerHTML = `
        <h2>${card.title}</h2>
        <p>${card.caption}</p>
        <pre>${JSON.stringify(card, null, 2)}</pre>
      `;
      container.appendChild(cardEl);
    });
  });
