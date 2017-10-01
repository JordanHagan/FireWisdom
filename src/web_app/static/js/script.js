const cats = ['Education Events', 'Distribution Events', 'Home Assessments',
  'Community Events', 'Mitigation Events', 'Others']
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

function updateEventChart() {
  const eventData = ['No. of Events'].concat(data[community].event_info)
  c3.generate({
    bindto: '#event-chart',
    data: {
        columns: [eventData],
        type: 'bar'
    },
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
    total += Math.round(value*100) / 100
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
