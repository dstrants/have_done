import { Controller } from "stimulus"
import Noty from 'noty';

var octicons = require("@primer/octicons")


Noty.overrideDefaults({
  theme    : 'sunset',
  progressBar: true,
  timeout: 3500,
});

export default class extends Controller {
    static targets = ["repoIcon", "repoSearch", "repo", "repoList"]

    connect(){
        this._set_repo_icons()
    }

    _set_repo_icons(){
        const iconSpans = this.repoIconTargets
        iconSpans.forEach( icon => {
            const iconName = icon.classList.contains("private") ? "lock" : "repo"
            icon.innerHTML = octicons[iconName].toSVG({ "width": 24 })
        });   
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
    
   getRepoList(){
    fetch("/sync/github/list")
        .then(response => response.text())
        .then( data => this.repoListTarget.innerHTML = data)
        .finally(() => this._set_repo_icons())
   } 

    searchRepos(){
        const term = this.repoSearch
        if (term == ""){
            this.repoTargets.forEach(repo => repo.classList.remove("hidden"))
            return 
        }
        this.repoTargets.forEach( (repo) => {
            if (repo.dataset.name.indexOf(term) > -1){
                repo.classList.remove("hidden")
            }
            else{
                repo.classList.add("hidden")
            }
        })
    }

    toggleRepoStatus(event) {
        const btn = event.target
        fetch(`/sync/github/watch/${btn.dataset.repo}`, {method: 'POST', headers: {"X-CSRFToken": this._getCookie('csrftoken')}})
        .then(response => response.json())
        .then( data => {
            setTimeout( ()  =>{
              new Noty ({ text: data.message, type: "success" }).show()
            }, 250)
          })
        .finally( () => this.getRepoList())
    }

    get repoSearch(){
        return this.repoSearchTarget.value
    }
}