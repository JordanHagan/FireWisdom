let data

function updateEvents() {
  const communities = getActive()
    .map(entry => ({name: entry[0], events: entry[1].event_info[3] + entry[1].event_info[4]}))
    .sort((commA, commB) => commB.events - commA.events)
    .slice(0, 10)
    .map(comm => `<tr><td>${comm.name}</td><td>${comm.events}</td></tr>`)
    .join('')
  document.querySelector('#events').innerHTML = communities;
}

function updateInvestment() {
  const communities = getActive()
    .map(entry => ({name: entry[0], investment: (entry[1].lifetime_investment / entry[1].residentcount)}))
    .sort((commA, commB) => commB.investment - commA.investment)
    .slice(0, 10)
    .map(comm => `<tr><td>${comm.name}</td><td>$${Math.round(comm.investment).toLocaleString()}</td></tr>`)
    .join('')
  document.querySelector('#investment').innerHTML = communities
}

function updateInfoBox() {
  [0,1,2,3,4,5].forEach(index => {
    const total = Object.values(data)
      .map(comm => comm.event_info[index])
      .reduce((a, x) => x += a, 0)
    document.querySelector(`#event${index}`).innerHTML = total
  })
}

function getActive() {
  return Object.entries(data)
    .filter(entry => entry[1].community_status != 'Inactive')
}

function updateLeaderboard() {
  updateInfoBox()
  updateEvents()
  updateInvestment()
}

fetch('/data')
  .then(response => response.json())
  .then(parsed => {
    data = parsed
    updateLeaderboard()
  })
