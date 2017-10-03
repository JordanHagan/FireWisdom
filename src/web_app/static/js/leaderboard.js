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

function getActive() {
  return Object.entries(data)
    .filter(entry => entry[1].community_status != 'Inactive')
}

function updateLeaderboard() {
  updateEvents()
  updateInvestment()
}

fetch('/data')
  .then(response => response.json())
  .then(parsed => {
    data = parsed
    console.log(data)
    updateLeaderboard()
  })
