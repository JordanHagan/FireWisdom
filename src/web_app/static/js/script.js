const cats = ['Education Events', 'Distribution Events', 'Home Assessments',
  'Community Preparedness', 'Mitigation Events', 'Others']
let community
let data = {}

function updateDropdown() {
  let html = ''
  const communities = Object.keys(data)
  community = communities[0]
  communities.forEach(community => {
    html += `<option value="${community}">${community}</option>`
  })
  document.querySelector('#communities').innerHTML = html
}

function updateInfoBox() {
  const communityData = data[community]
  document.querySelector('#resident-count').innerHTML = communityData.residentcount
  document.querySelector('#percent-growth').innerHTML =
    `${(communityData.pop_percent_change * 100).toFixed(2)}%`
  document.querySelector('#total-investment').innerHTML = `$${communityData.lifetime_investment}`
}

function updateEventChart() {
  const eventData = ['No. of Events'].concat(data[community].event_info)
  c3.generate({
    bindto: '#event-chart',
    data: {
        columns: [eventData],
        type: 'bar'
    },
    legend: {hide: true},
    axis: {
      y: {
        tick: {
          format: x => { if(x%1 == 0) return x }
        }
      },
      x: {
        tick: {
          format: x => cats[x]
        }
      }
    }
  });
}

function updateInvestmentChart() {
  const yearlyData = data[community].yearly_investments
  const investmentData = ['Yearly Investment'].concat(yearlyData)
  const totalInvestment = ['Total Investment']
  let total = 0
  yearlyData.forEach(value => {
    total = Number((total + value).toFixed(2))
    totalInvestment.push(total)
  })

  c3.generate({
    bindto: '#investment-chart',
    data: {
      columns: [investmentData, totalInvestment]
    },
    axis: {
      y: {
        tick: {
          format: x => `$${x}`
        }
      },
      x: {
        tick: {
          format: x => x + 2003
        }
      }
    }
  })
}

function communityChanged() {
  community = document.querySelector('#communities').value
  updateDashboard()
}

function updateDashboard() {
  updateInfoBox()
  updateEventChart()
  updateInvestmentChart()
}

fetch('/data')
  .then(response => response.json())
  .then(parsed => {
    data = parsed
    updateDropdown()
    updateDashboard()
  })
