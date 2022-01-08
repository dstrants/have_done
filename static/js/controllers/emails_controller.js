import { Controller } from "stimulus"
import Noty from 'noty';

import 'noty/lib/noty.css'


Noty.overrideDefaults({
  theme    : 'sunset',
  progressBar: true,
  timeout: 3500,
});

export default class extends Controller {
    static targets = [ ]

    connect(){

    }

    fetchMails(){
        fetch('/prod/emails/import')
            .then(response => response.json())
            .then(data => {
                new Noty ({ text: data.result, type: 'info' }).show()
            })
            .catch(error => {
                new Noty ({ text: `An error occured: ${error}`, type: 'error'}).show()
            })
        }
}