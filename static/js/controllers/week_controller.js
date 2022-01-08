import { Controller } from "stimulus"
import Noty from 'noty';
import { Tooltip } from '@coreui/coreui'
import ApexCharts from "apexcharts"


Noty.overrideDefaults({
  theme    : 'sunset',
  progressBar: true,
  timeout: 3500,
});


export default class extends Controller {
  static targets = [ "upTimeContainer", "ghPrContainer", "gCalendarContainer", "weekendDays", "plot" ]

  connect(){
    this.addCharts()
  }

  _setApexChartOptions(name, data, categories){
    return {
      chart: {
        type: 'line',
        sparkline: {
          enabled: true,
        },
        stroke: {
          curve: 'smooth',
        }
      },
      stroke: {
        curve: 'smooth',
      },
      series: [{
        name: name,
        data: data,
      }],
      xaxis: {
        categories: categories
      }
    }
  }

  _plotApexChart(elm, options){
    var chart = new ApexCharts(elm, options);
    return chart.render();
  }

  _formatDataArray(arr){
    var res = arr.split(",")
    res.splice(-1,1)
    return res
  }

  addCharts(){
    this.plotTargets.forEach(plot => {
     console.log(plot.id)
     var opts = this._setApexChartOptions(plot.dataset.weekLegend, this._formatDataArray(plot.dataset.weekSeries), this._formatDataArray(plot.dataset.weekCategories))
     console.log(opts)
     this._plotApexChart(plot, opts)
    });
  }

  toggleWeekends(){
    this.weekendDaysTargets.forEach( day => {    
        day.classList.toggle('hidden')
    } )
  }
}