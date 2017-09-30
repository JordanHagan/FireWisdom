const cats = ['Education Events', 'Distribution Events', 'Home Assessments',
  'Community Events', 'Mitigation Events', 'Others']
let community = '555 Freeman Road'
let data = {}

function updateDropdown() {
  let html = ''
  const communities = Object.keys(data)
  communities.forEach(community => {
    html += `<option value="${community}">${community}</option>`
  })
  document.querySelector('#communities').innerHTML = html
}

function showEventChart() {
  const eventData = data[community].event_info
  eventData.unshift('No. of Events')
  var chart = c3.generate({
    bindto: '#chart',
    data: {
        columns: [
            eventData
        ],
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
          format: (x) => cats[x]
        }
      }
    }
  });
}

function communityChanged() {
  community = document.querySelector('#communities').value
  showEventChart()
}

fetch('/data')
  .then(response => response.json())
  .then(parsed => {
    data = parsed
    updateDropdown()
    showEventChart()
  })
