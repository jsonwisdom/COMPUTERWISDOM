
fetch('deck.json')
  .then(response => response.json())
  .then(data => {
    const container = document.getElementById('deck-container');
    data.cards.forEach((card, index) => {
      const cardEl = document.createElement('div');
      cardEl.className = 'card';
      cardEl.setAttribute('data-card-id', card.card_id);  // Lock to card ID
      cardEl.innerHTML = `
        <h2>${card.title}</h2>
        <p>${card.caption}</p>
        <pre>${JSON.stringify(card, null, 2)}</pre>
      `;
      container.appendChild(cardEl);
    });
  });
