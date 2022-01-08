import { Controller } from "stimulus"
import Noty from 'noty';


Noty.overrideDefaults({
  theme    : 'sunset',
  progressBar: true,
  timeout: 3500,
});

export default class extends Controller {
  static targets = [ "upTimeContainer", "ghPrContainer", "gCalendarContainer" ]

  connect() {
   this.uptimeMonitors()
   this.PrList()
   this.GoogleCalendar()
  }

  _getCookie(name) {
    if (!document.cookie) {
      return null;
    }
  
    const xsrfCookies = document.cookie.split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));
  
    if (xsrfCookies.length === 0) {
      return null;
    }
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
  }

  uptimeMonitors(){
    fetch('/sync/uptimerobot/monitors')
        .then(response => response.text())
        .then(data => {
            this.upTimeContainerTarget.innerHTML = data
        })
        .catch( error => {
            new Noty ({ text: 'There was an error trying to fetch Uptime Robot', type: "warning" }).show()
            this.upTimeContainerTarget.textContent = error
        })
    }

    forcePRList(){
      this.PrList(true)
    }

    PrList(force=false) {
        var url = 'backups/prs/'
        if (force) url += "?force_sync=true"
        fetch(url)
          .then(response => response.text())
          .then(data => {
            this.ghPrContainerTarget.innerHTML = data
          })
          .catch( error => {
            new Noty ({ text: 'There was an error trying to fetching pending PRs', type: "warning" }).show()
            this.ghPrContainerTarget.textContent = error
          })
    }

    GoogleCalendar(force) {
        var url = 'prod/events/import'
        if (force) url += "?force_sync=true"
        fetch(url)
            .then(response => response.text())
            .then(data => {
              this.gCalendarContainerTarget.innerHTML = data
            })
            .catch( error => {
              new Noty ({ text: 'There was an error trying to fetching coming calendar events', type: "warning" }).show()
              this.gCalendarContainerTarget.textContent = error
            })
    }
}